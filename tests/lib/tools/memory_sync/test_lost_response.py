"""An upload whose response never arrives.

The server can save a create or update and the response still be lost — a
timeout, a dropped connection. The sync then cannot tell whether the bytes
landed. If they did, the server's copy is the sync's own upload, not another
writer's edit, and a newer local edit must go out over it.
"""

from __future__ import annotations

from typing import Any
from pathlib import Path
from contextlib import contextmanager
from collections.abc import Iterator

import httpx2
import pytest

from anthropic import APIConnectionError
from anthropic.lib.tools._memories import SessionMemoryStores

from .conftest import run_sync
from ._fake_anthropic import MemoryServer, created, deleted, updated, fake_anthropic

LOGGER = "anthropic.lib.tools.agent_toolset"


async def _downloaded(tmp_path: Path, initial: dict[str, str]) -> tuple[Path, MemoryServer, SessionMemoryStores, Any]:
    """A `SessionMemoryStores` with one store already downloaded, plus the
    fake `client.beta.memory_stores.memories` resource it calls."""
    client, server = fake_anthropic(initial)
    stores = SessionMemoryStores(client, workdir=tmp_path)
    await stores.download(await client.beta.sessions.retrieve("s1"))
    return tmp_path / "memory" / "notes", server, stores, client.beta.memory_stores.memories


@contextmanager
def uploads_fail(memories: Any, *, after_saving: bool) -> Iterator[None]:
    """Every create and update raises a connection error — after the server
    has saved the write (the response was lost) or before it arrived at all."""
    real_create, real_update = memories.create, memories.update

    def failing(send: Any) -> Any:
        async def call(*args: Any, **kwargs: Any) -> Any:
            if after_saving:
                await send(*args, **kwargs)
            raise APIConnectionError(request=httpx2.Request("POST", "https://api.example/v1/memory"))

        return call

    memories.create, memories.update = failing(real_create), failing(real_update)
    try:
        yield
    finally:
        memories.create, memories.update = real_create, real_update


@pytest.mark.asyncio()
async def test_an_edit_made_after_a_lost_upload_response_still_reaches_the_server(tmp_path: Path) -> None:
    local, server, stores, memories = await _downloaded(tmp_path, {"note.md": "v0"})

    (local / "note.md").write_text("v1")
    (local / "new.md").write_text("v1")
    with uploads_fail(memories, after_saving=True):
        await run_sync(stores)
    # The server holds both writes; the sync never heard back.
    assert server.files == {"note.md": "v1", "new.md": "v1"}

    (local / "note.md").write_text("v2")
    (local / "new.md").write_text("v2")
    await run_sync(stores)

    # The server's v1 was this sync's own upload, so v2 goes out over it.
    assert server.files == {"note.md": "v2", "new.md": "v2"}
    assert (local / "note.md").read_text() == "v2"
    assert (local / "new.md").read_text() == "v2"
    assert server.received == [
        created("new.md", "v1"),
        updated("note.md", "v1", was="v0"),
        updated("new.md", "v2", was="v1"),
        updated("note.md", "v2", was="v1"),
    ]

    # Settled: nothing more to send.
    await run_sync(stores)
    assert len(server.received) == 4


@pytest.mark.asyncio()
async def test_a_retry_whose_response_is_lost_is_remembered_too(tmp_path: Path) -> None:
    local, server, stores, memories = await _downloaded(tmp_path, {"note.md": "v0"})

    (local / "note.md").write_text("v1")
    with uploads_fail(memories, after_saving=False):
        await run_sync(stores)
    # The retry sends the same bytes; this time they land and the response is lost.
    with uploads_fail(memories, after_saving=True):
        await run_sync(stores)
    assert server.files["note.md"] == "v1"

    (local / "note.md").write_text("v2")
    await run_sync(stores)

    assert server.files["note.md"] == "v2"
    assert (local / "note.md").read_text() == "v2"


@pytest.mark.asyncio()
async def test_a_client_retry_refused_because_the_first_attempt_landed_is_remembered(tmp_path: Path) -> None:
    """The client's own retry re-sends the update with the old precondition;
    the first attempt already moved the server, so the retry gets a 409."""
    local, server, stores, memories = await _downloaded(tmp_path, {"note.md": "v0"})
    real_update = memories.update

    async def sent_twice(memory_id: str, **kwargs: Any) -> Any:
        await real_update(memory_id, **kwargs)
        return await real_update(memory_id, **kwargs)

    (local / "note.md").write_text("v1")
    memories.update = sent_twice
    await run_sync(stores)
    memories.update = real_update
    assert server.files["note.md"] == "v1"
    assert server.received == [updated("note.md", "v1", was="v0")] * 2

    (local / "note.md").write_text("v2")
    await run_sync(stores)

    assert server.files["note.md"] == "v2"
    assert (local / "note.md").read_text() == "v2"


@pytest.mark.asyncio()
async def test_a_deletion_made_after_a_lost_upload_response_still_reaches_the_server(tmp_path: Path) -> None:
    local, server, stores, memories = await _downloaded(tmp_path, {"note.md": "v0", "keep.md": "v0"})

    (local / "note.md").write_text("v1")
    (local / "new.md").write_text("v1")
    with uploads_fail(memories, after_saving=True):
        await run_sync(stores)
    (local / "note.md").unlink()
    (local / "new.md").unlink()

    await stores.finish()

    # The server's copies are this sync's own uploads, so the deletions go
    # out, guarded by the content that was sent.
    assert server.files == {"keep.md": "v0"}
    assert server.received[-2:] == [deleted("new.md", was="v1"), deleted("note.md", was="v1")]


@pytest.mark.asyncio()
async def test_a_folder_wiped_after_a_lost_create_response_is_rebuilt_not_read_as_deletions(tmp_path: Path) -> None:
    local, server, stores, memories = await _downloaded(tmp_path, {"note.md": "v0"})

    (local / "new.md").write_text("v1")
    with uploads_fail(memories, after_saving=True):
        await run_sync(stores)
    # Both files vanish at once; the marker stays.
    (local / "note.md").unlink()
    (local / "new.md").unlink()

    # The final sync waives the delete window, so a misread wipe would delete at once.
    await stores.finish()

    # Two known files gone together is a wipe: re-downloaded, nothing deleted.
    assert server.files == {"note.md": "v0", "new.md": "v1"}
    assert (local / "note.md").read_text() == "v0"
    assert (local / "new.md").read_text() == "v1"
    assert server.received == [created("new.md", "v1")]


@pytest.mark.asyncio()
async def test_the_shutdown_flush_pushes_a_revert_made_after_a_lost_upload_response(tmp_path: Path) -> None:
    local, server, stores, memories = await _downloaded(tmp_path, {"note.md": "v0"})

    (local / "note.md").write_text("v1")
    with uploads_fail(memories, after_saving=True):
        await run_sync(stores)
    # Back to the last content the sync knows it saved — but the server moved on.
    (local / "note.md").write_text("v0")

    await stores.flush_writes()

    assert server.files["note.md"] == "v0"
    assert server.received[-1] == updated("note.md", "v0", was="v1")


@pytest.mark.asyncio()
async def test_the_shutdown_flush_sends_nothing_for_a_revert_whose_upload_never_landed(tmp_path: Path) -> None:
    local, server, stores, memories = await _downloaded(tmp_path, {"note.md": "v0", "keep.md": "v0"})

    (local / "note.md").write_text("v1")
    with uploads_fail(memories, after_saving=False):
        await run_sync(stores)
    (local / "note.md").write_text("v0")
    # Another writer deletes the memory; the file holds no edit to save.
    server.delete("note.md")

    await stores.flush_writes()

    assert server.files == {"keep.md": "v0"}
    assert server.received == []


@pytest.mark.asyncio()
async def test_the_shutdown_flush_pushes_an_edit_made_after_a_lost_upload_response(tmp_path: Path) -> None:
    local, server, stores, memories = await _downloaded(tmp_path, {"note.md": "v0"})

    (local / "note.md").write_text("v1")
    with uploads_fail(memories, after_saving=True):
        await run_sync(stores)
    (local / "note.md").write_text("v2")

    await stores.flush_writes()

    assert server.files["note.md"] == "v2"
    assert server.received[-1] == updated("note.md", "v2", was="v1")


@pytest.mark.asyncio()
async def test_another_writers_edit_after_a_lost_upload_response_still_wins(
    tmp_path: Path, caplog: pytest.LogCaptureFixture
) -> None:
    caplog.set_level("WARNING", logger=LOGGER)
    local, server, stores, memories = await _downloaded(tmp_path, {"note.md": "v0"})

    (local / "note.md").write_text("v1")
    with uploads_fail(memories, after_saving=True):
        await run_sync(stores)
    server.write("note.md", "theirs")
    (local / "note.md").write_text("v2")

    await run_sync(stores)

    # The server's copy is not what this sync sent, so the usual conflict rule holds.
    assert server.files["note.md"] == "theirs"
    assert (local / "note.md").read_text() == "theirs"
    assert "changed both locally and remotely" in caplog.text


@pytest.mark.asyncio()
async def test_a_send_is_forgotten_once_a_later_sync_has_seen_the_server(
    tmp_path: Path, caplog: pytest.LogCaptureFixture
) -> None:
    """A remembered send must not outlive the next completed sync: kept longer,
    it would mistake another writer's identical bytes for this sync's upload
    and overwrite them."""
    caplog.set_level("WARNING", logger=LOGGER)
    local, server, stores, memories = await _downloaded(tmp_path, {"note.md": "v0"})

    (local / "note.md").write_text("v1")
    with uploads_fail(memories, after_saving=False):
        await run_sync(stores)
    assert server.files["note.md"] == "v0"

    # The agent reverts, so the next sync has nothing to send — its listing
    # shows the v1 upload never landed.
    (local / "note.md").write_text("v0")
    await run_sync(stores)

    # Another writer now saves the very bytes that failed upload carried.
    server.write("note.md", "v1")
    (local / "note.md").write_text("v2")
    await run_sync(stores)

    assert server.files["note.md"] == "v1"
    assert (local / "note.md").read_text() == "v1"
    assert "changed both locally and remotely" in caplog.text
    assert server.received == []
