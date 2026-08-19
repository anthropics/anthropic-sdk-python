"""``flush_writes`` — the push-only shutdown pass.

A session that ends on an error or cancel gets no full reconcile, but the
writes already on disk are the only copy of the agent's edits.
``flush_writes`` pushes those and does nothing else: no remote deletes, no
local removals, no pulls.
"""

from __future__ import annotations

from typing import Any
from pathlib import Path

import anyio
import pytest

import anthropic.lib.tools._memories as memories_mod
from anthropic.lib.tools._memories import MARKER_PATH, SessionMemoryStores

from .conftest import run_sync
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
async def test_flush_pushes_new_and_changed_files_and_nothing_else(
    tmp_path: Path, caplog: pytest.LogCaptureFixture
) -> None:
    caplog.set_level("WARNING", logger=LOGGER)
    local, server, stores = await _downloaded(
        tmp_path,
        {
            "a-pull.md": "v1",
            "b-push.md": "v1",
            "d-local-gone.md": "v1",
            "e-remote-gone.md": "v1",
            "f-remote-gone-edited.md": "v1",
            "g-both.md": "v1",
        },
    )

    (local / "b-push.md").write_text("v2 from agent")
    (local / "c-new.md").write_text("new from agent")
    (local / "d-local-gone.md").unlink()
    (local / "f-remote-gone-edited.md").write_text("v2 from agent")
    (local / "g-both.md").write_text("v2 from agent")
    server.write("a-pull.md", "v2 from server")
    server.delete("e-remote-gone.md")
    server.delete("f-remote-gone-edited.md")
    server.write("g-both.md", "v2 from server")

    await stores.flush_writes()

    # Only additions went out: the update, the new file, and the re-created
    # edited file whose remote copy was deleted.
    sent = [
        updated("b-push.md", "v2 from agent", was="v1"),
        created("c-new.md", "new from agent"),
        created("f-remote-gone-edited.md", "v2 from agent"),
    ]
    assert sorted(server.received) == sorted(sent)
    # A locally missing file was not deleted remotely.
    assert server.files["d-local-gone.md"] == "v1"
    # A remotely deleted, locally unedited memory was not re-uploaded — and
    # its file was not removed from disk either.
    assert "e-remote-gone.md" not in server.files
    assert (local / "e-remote-gone.md").read_text() == "v1"
    # Remote changes were not pulled.
    assert (local / "a-pull.md").read_text() == "v1"
    # The conflict was left to the server, and logged.
    assert server.files["g-both.md"] == "v2 from server"
    assert (local / "g-both.md").read_text() == "v2 from agent"
    assert "changed both locally and remotely" in caplog.text

    # Settled: a second flush pushes nothing more.
    await stores.flush_writes()
    assert sorted(server.received) == sorted(sent)


@pytest.mark.asyncio()
async def test_flush_uploads_several_files_at_once_up_to_the_bound(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Two uploads are in flight together, and never more than the bound —
    a serial flush would time out waiting for the second to start."""
    monkeypatch.setattr(memories_mod, "_UPLOAD_CONCURRENCY", 2)
    local, server, stores = await _downloaded(tmp_path, {})
    for i in range(5):
        (local / f"f{i}.md").write_text(f"file {i}")

    in_flight = peak = 0
    release = anyio.Event()

    async def hook(_path: str) -> None:
        nonlocal in_flight, peak
        in_flight += 1
        peak = max(peak, in_flight)
        try:
            if in_flight == 2 and not release.is_set():
                # Hold both a little longer so a flush that ignored the bound
                # would have time to start a third upload before they leave.
                await anyio.sleep(0.1)
                release.set()
            with anyio.fail_after(5):
                await release.wait()
        finally:
            in_flight -= 1

    server.upload_hook = hook
    await stores.flush_writes()

    assert peak == 2
    assert server.files == {f"f{i}.md": f"file {i}" for i in range(5)}


@pytest.mark.asyncio()
async def test_a_flush_cut_off_part_way_logs_how_many_files_it_had_not_uploaded(
    tmp_path: Path, caplog: pytest.LogCaptureFixture
) -> None:
    caplog.set_level("WARNING", logger=LOGGER)
    local, server, stores = await _downloaded(tmp_path, {})
    for name in ("a.md", "b.md", "c.md", "y.md", "z.md"):
        (local / name).write_text(f"content of {name}")

    never = anyio.Event()
    fast_arrived = 0
    with anyio.CancelScope() as scope:

        async def hook(path: str) -> None:
            nonlocal fast_arrived
            if path in ("y.md", "z.md"):
                with anyio.fail_after(5):
                    await never.wait()
            else:
                fast_arrived += 1
                if fast_arrived == 3:
                    scope.cancel()

        server.upload_hook = hook
        await stores.flush_writes()

    def cut_off_lines() -> list[str]:
        return [r.getMessage() for r in caplog.records if "cut off" in r.getMessage()]

    assert scope.cancelled_caught
    assert cut_off_lines() == [
        "memory flush cut off part-way; 2 of 5 changed files had not finished uploading memory_store_id=memstore_notes"
    ]
    assert sorted(server.files) == ["a.md", "b.md", "c.md"]

    # The three that made it are not sent again; the two that did not are.
    # A flush that finishes in time adds no cut-off line.
    server.upload_hook = None
    await stores.flush_writes()
    assert sorted(server.files) == ["a.md", "b.md", "c.md", "y.md", "z.md"]
    assert sorted(r[1] for r in server.received) == ["a.md", "b.md", "c.md", "y.md", "z.md"]
    assert len(cut_off_lines()) == 1


@pytest.mark.asyncio()
async def test_flush_adopts_a_file_the_server_already_holds(tmp_path: Path, caplog: pytest.LogCaptureFixture) -> None:
    """A final sync cut off after uploading a file leaves the baseline stale;
    the flush sees the server already has those bytes and records that
    instead of reporting a conflict."""
    caplog.set_level("WARNING", logger=LOGGER)
    local, server, stores = await _downloaded(tmp_path, {"n.md": "v1"})
    (local / "n.md").write_text("v2")
    server.write("n.md", "v2")

    await stores.flush_writes()

    assert server.received == []
    assert "changed both locally and remotely" not in caplog.text

    (local / "n.md").write_text("v3")
    await stores.flush_writes()
    assert server.received == [updated("n.md", "v3", was="v2")]


@pytest.mark.asyncio()
async def test_flush_never_pushes_a_read_only_store(tmp_path: Path) -> None:
    local, server, stores = await _downloaded(tmp_path, {"edit.md": "v1"}, access="read_only")

    (local / "edit.md").write_text("v2 from agent")
    (local / "new.md").write_text("new from agent")

    await stores.flush_writes()

    assert server.received == []
    assert server.files == {"edit.md": "v1"}


@pytest.mark.asyncio()
async def test_flush_skips_files_the_server_already_refused(tmp_path: Path) -> None:
    local, server, stores = await _downloaded(tmp_path, {"note.md": "v1"})
    server.max_content_bytes = 64

    (local / "big.md").write_text("x" * 100)
    await run_sync(stores)
    assert sum(1 for r in server.received if r[0] == "create") == 1

    await stores.flush_writes()

    # The refused file was not retried; nothing else needed pushing.
    assert sum(1 for r in server.received if r[0] == "create") == 1
    assert "big.md" not in server.files


@pytest.mark.asyncio()
async def test_flush_pushes_nothing_when_the_marker_check_fails(
    tmp_path: Path, caplog: pytest.LogCaptureFixture
) -> None:
    caplog.set_level("WARNING", logger=LOGGER)
    local, server, stores = await _downloaded(tmp_path, {"a.md": "v1"})

    (local / MARKER_PATH).unlink()
    (local / "foreign.md").write_text("someone else's notes")

    await stores.flush_writes()

    assert server.received == []
    assert "foreign.md" not in server.files
    # Unlike sync's recovery, the flush does not re-download the folder.
    assert not (local / MARKER_PATH).exists()
    assert "not uploading anything from the memory store folder" in caplog.text


@pytest.mark.asyncio()
async def test_flush_never_raises(tmp_path: Path, caplog: pytest.LogCaptureFixture) -> None:
    caplog.set_level("WARNING", logger=LOGGER)
    local, server, stores = await _downloaded(tmp_path, {"a.md": "v1"})
    (local / "a.md").write_text("v2 from agent")

    def boom(*_a: Any, **_k: Any) -> Any:
        raise RuntimeError("listing exploded")

    stores._client.beta.memory_stores.memories.list = boom  # pyright: ignore[reportPrivateUsage]
    await stores.flush_writes()

    assert server.received == []
    assert "memory flush failed" in caplog.text
