"""Never destroy the only copy of a local edit: a memory deleted remotely
while its file holds an un-pushed edit keeps the file — a writable store
re-creates the memory from it, a read-only store keeps it on disk unsynced.
Only an unedited file follows the remote delete off the disk.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from anthropic.lib.tools._memories import SessionMemoryStores

from .conftest import run_sync, listing_interrupted_by
from ._fake_anthropic import MemoryServer, created, updated, fake_anthropic

LOGGER = "anthropic.lib.tools.agent_toolset"


async def _downloaded(
    tmp_path: Path, initial: dict[str, str], *, access: str | None = None
) -> tuple[Path, MemoryServer, SessionMemoryStores]:
    """A ``SessionMemoryStores`` with one store already downloaded to disk."""
    client, server = fake_anthropic(initial, access=access)
    stores = SessionMemoryStores(client, workdir=tmp_path)
    await stores.download(await client.beta.sessions.retrieve("s1"))
    return tmp_path / "memory" / "notes", server, stores


@pytest.mark.asyncio()
async def test_an_edited_file_survives_a_remote_delete_and_is_re_created(
    tmp_path: Path, caplog: pytest.LogCaptureFixture
) -> None:
    caplog.set_level("INFO", logger=LOGGER)
    local, server, stores = await _downloaded(tmp_path, {"edited.md": "v1", "plain.md": "v1"})
    (local / "edited.md").write_text("v2 from agent")
    server.delete("edited.md")
    server.delete("plain.md")

    await run_sync(stores)

    # The edit's only copy survives and the memory is re-created from it;
    # the unedited file follows the remote delete off the disk.
    assert (local / "edited.md").read_text() == "v2 from agent"
    assert server.files == {"edited.md": "v2 from agent"}
    assert server.received == [created("edited.md", "v2 from agent")]
    assert not (local / "plain.md").exists()
    assert "re-creating it from the file" in caplog.text

    # Settled: nothing more goes out.
    await run_sync(stores)
    assert server.received == [created("edited.md", "v2 from agent")]

    # The upload's sha became the baseline: the next edit is a guarded update.
    (local / "edited.md").write_text("v3")
    await run_sync(stores)
    assert server.received[-1] == updated("edited.md", "v3", was="v2 from agent")


@pytest.mark.asyncio()
async def test_a_read_only_store_keeps_the_edited_file_without_pushing(
    tmp_path: Path, caplog: pytest.LogCaptureFixture
) -> None:
    caplog.set_level("WARNING", logger=LOGGER)
    local, server, stores = await _downloaded(tmp_path, {"edited.md": "v1", "plain.md": "v1"}, access="read_only")
    (local / "edited.md").write_text("v2 from agent")
    server.delete("edited.md")
    server.delete("plain.md")

    await run_sync(stores)

    assert (local / "edited.md").read_text() == "v2 from agent"
    assert not (local / "plain.md").exists()
    assert server.received == []
    assert caplog.text.count("cannot push") == 1

    # Later passes see a local-only file in a read-only store: a quiet no-op.
    await run_sync(stores)
    await run_sync(stores)
    assert server.received == []
    assert (local / "edited.md").read_text() == "v2 from agent"
    assert caplog.text.count("cannot push") == 1


@pytest.mark.asyncio()
async def test_a_refused_edit_survives_a_remote_delete_without_a_retry(tmp_path: Path) -> None:
    """The server already refused this content, so the remote delete neither
    removes the file nor triggers a re-create the server would refuse again."""
    local, server, stores = await _downloaded(tmp_path, {"big.md": "v1"})
    server.max_content_bytes = 64

    (local / "big.md").write_text("x" * 100)
    await run_sync(stores)
    assert len(server.received) == 1  # the one refused update

    server.delete("big.md")
    await run_sync(stores)
    await run_sync(stores)

    assert (local / "big.md").read_text() == "x" * 100
    assert len(server.received) == 1
    assert "big.md" not in server.files


@pytest.mark.asyncio()
async def test_a_memory_deleted_between_the_listing_and_the_update_is_re_created(tmp_path: Path) -> None:
    """An update that meets a 404 re-creates the memory in the same pass."""
    local, server, stores = await _downloaded(tmp_path, {"note.md": "v1"})
    (local / "note.md").write_text("v2 from agent")

    async def deleted_meanwhile(path: str) -> None:
        server.files.pop(path, None)
        server.upload_hook = None

    server.upload_hook = deleted_meanwhile
    await run_sync(stores)

    assert server.files == {"note.md": "v2 from agent"}
    assert server.received == [updated("note.md", "v2 from agent", was="v1"), created("note.md", "v2 from agent")]

    # The create's sha is the new baseline.
    (local / "note.md").write_text("v3")
    await run_sync(stores)
    assert server.received[-1] == updated("note.md", "v3", was="v2 from agent")


@pytest.mark.asyncio()
async def test_an_edit_written_mid_sync_still_survives_a_remote_delete(tmp_path: Path) -> None:
    """The directory scan saw the file unedited; an edit is written while
    the server listing is in flight. The removal must re-read the file
    instead of destroying the edit based on the stale scan."""
    local, server, stores = await _downloaded(tmp_path, {"z.md": "v1", "keep.md": "v1"})
    server.delete("z.md")

    with listing_interrupted_by(stores, lambda: (local / "z.md").write_text("late edit")):
        await run_sync(stores)

    assert (local / "z.md").read_text() == "late edit"
    assert server.files["z.md"] == "late edit"


@pytest.mark.asyncio()
async def test_a_read_only_pull_over_a_local_edit_is_warned(tmp_path: Path, caplog: pytest.LogCaptureFixture) -> None:
    """Read-only stores always take the server version, but overwriting a
    local edit must leave a trace instead of happening silently."""
    caplog.set_level("WARNING", logger=LOGGER)
    local, server, stores = await _downloaded(tmp_path, {"pull.md": "v1"}, access="read_only")
    (local / "pull.md").write_text("local edit")
    server.write("pull.md", "v2 from server")

    await run_sync(stores)

    assert (local / "pull.md").read_text() == "v2 from server"
    assert server.received == []
    assert "changed both locally and remotely" in caplog.text


@pytest.mark.asyncio()
async def test_a_failed_re_read_does_not_resurrect_a_server_deleted_memory(tmp_path: Path) -> None:
    """The re-read before removal can fail (a transient I/O error). That must
    mean "retry next sync", not "file gone": dropping the entry would make
    the next sync upload the file as new, re-creating the memory the server
    just deleted."""
    from anthropic.lib.tools import _file_store

    local, server, stores = await _downloaded(tmp_path, {"z.md": "v1", "keep.md": "v1"})
    server.delete("z.md")

    real_hash_file = _file_store.LocalFileStore.hash_file

    async def flaky_hash_file(self: _file_store.LocalFileStore, rel_path: str) -> str | None:
        if rel_path == "z.md":
            raise OSError(5, "I/O error")
        return await real_hash_file(self, rel_path)

    with pytest.MonkeyPatch.context() as mp:
        mp.setattr(_file_store.LocalFileStore, "hash_file", flaky_hash_file)
        await run_sync(stores)

    # The error held everything: file still on disk, nothing pushed.
    assert (local / "z.md").read_text() == "v1"
    assert server.received == []

    # With the error gone, the next sync completes the server delete.
    await run_sync(stores)
    assert not (local / "z.md").exists()
    assert "z.md" not in server.files
    assert server.received == []
