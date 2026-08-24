"""The sync's two passes: a content-free listing, then targeted fetches.

A sync lists shas only (``basic`` view) and fetches a memory's body just
before writing it to disk; only the download takes ``full`` pages, since
it needs every memory anyway. These tests pin that fetch discipline: a
sync that writes nothing fetches nothing, a changed path fetches exactly
itself, fetches fan out rather than queue, and a fetch that fails — or
races a server-side delete — leaves the old state for the next sync.
"""

from __future__ import annotations

from typing import Any
from pathlib import Path

import pytest

from anthropic.lib.tools._memories import SessionMemoryStores

from .conftest import run_sync
from ._fake_anthropic import MemoryServer, updated, _status_error, fake_anthropic


async def _downloaded(tmp_path: Path, initial: dict[str, str]) -> tuple[Path, MemoryServer, SessionMemoryStores]:
    """A ``SessionMemoryStores`` with one store already downloaded to disk."""
    client, server = fake_anthropic(initial)
    stores = SessionMemoryStores(client, workdir=tmp_path)
    await stores.download(await client.beta.sessions.retrieve("s1"))
    return tmp_path / "memory" / "notes", server, stores


@pytest.mark.asyncio()
async def test_a_sync_that_pulls_nothing_fetches_no_content(tmp_path: Path) -> None:
    local, server, stores = await _downloaded(tmp_path, {"a.md": "v1", "b.md": "v1", "c.md": "v1"})
    # The download took full listing pages: no single-memory fetches at all.
    assert server.content_fetches == []

    (local / "a.md").write_text("v2 from agent")  # a push needs no remote content
    await run_sync(stores)

    assert server.content_fetches == []
    assert server.files["a.md"] == "v2 from agent"


@pytest.mark.asyncio()
async def test_only_the_changed_memory_is_fetched(tmp_path: Path) -> None:
    local, server, stores = await _downloaded(tmp_path, {"a.md": "v1", "b.md": "v1"})
    server.content_fetches.clear()

    server.write("a.md", "v2 from server")
    await run_sync(stores)

    assert server.content_fetches == ["a.md"]
    assert (local / "a.md").read_text() == "v2 from server"
    assert (local / "b.md").read_text() == "v1"


@pytest.mark.asyncio()
async def test_a_file_already_holding_the_remote_content_is_adopted_without_a_fetch(tmp_path: Path) -> None:
    local, server, stores = await _downloaded(tmp_path, {"a.md": "v1"})
    server.content_fetches.clear()

    # Both sides landed on the same bytes independently.
    (local / "a.md").write_text("v2 on both")
    server.write("a.md", "v2 on both")
    await run_sync(stores)

    assert server.content_fetches == []
    assert server.received == []

    # The baseline advanced to the adopted sha: the next edit pushes guarded by it.
    (local / "a.md").write_text("v3 from agent")
    await run_sync(stores)
    assert server.received == [updated("a.md", "v3 from agent", was="v2 on both")]


@pytest.mark.asyncio()
async def test_content_fetches_fan_out_within_a_store(tmp_path: Path) -> None:
    """The first memory's fetch completes only after the second's starts —
    only parallel fetches satisfy that; serial ones would time out."""
    import anyio

    client, server = fake_anthropic({"a.md": "v1", "b.md": "v1"})
    stores = SessionMemoryStores(client, workdir=tmp_path)
    await stores.download(await client.beta.sessions.retrieve("s1"))
    local = tmp_path / "memory" / "notes"
    server.write("a.md", "v2 from server")
    server.write("b.md", "v2 from server")

    memories = client.beta.memory_stores.memories
    real_retrieve = memories.retrieve
    second_started = anyio.Event()

    async def gated(memory_id: str, **kwargs: Any) -> Any:
        if memory_id == "mem:a.md":
            with anyio.fail_after(10):
                await second_started.wait()
        else:
            second_started.set()
        return await real_retrieve(memory_id, **kwargs)

    memories.retrieve = gated
    await run_sync(stores)

    assert (local / "a.md").read_text() == "v2 from server"
    assert (local / "b.md").read_text() == "v2 from server"


@pytest.mark.asyncio()
async def test_a_failed_fetch_keeps_the_old_state_and_the_next_sync_retries(tmp_path: Path) -> None:
    local, server, stores = await _downloaded(tmp_path, {"a.md": "v1"})
    server.write("a.md", "v2 from server")

    def boom(_path: str) -> None:
        raise _status_error(500)

    server.fetch_hook = boom
    await run_sync(stores)
    assert (local / "a.md").read_text() == "v1"

    server.fetch_hook = None
    await run_sync(stores)
    assert (local / "a.md").read_text() == "v2 from server"
    # The stale baseline drove no uploads or deletes along the way.
    assert server.received == []


@pytest.mark.asyncio()
async def test_a_memory_deleted_between_listing_and_fetch_waits_for_the_next_sync(tmp_path: Path) -> None:
    local, server, stores = await _downloaded(tmp_path, {"a.md": "v1", "keep.md": "v1"})
    server.write("a.md", "v2 from server")

    def vanish(path: str) -> None:
        server.files.pop(path, None)

    server.fetch_hook = vanish
    await run_sync(stores)
    # The fetch 404ed: disk and baseline keep the old version for now.
    assert (local / "a.md").read_text() == "v1"

    server.fetch_hook = None
    await run_sync(stores)
    # The next sync saw the server-side delete and took the local copy with it.
    assert not (local / "a.md").exists()
    assert server.received == []
