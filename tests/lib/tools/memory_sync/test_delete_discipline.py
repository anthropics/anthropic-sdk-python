"""Server-delete discipline: a locally deleted file is deleted on the server
only after a second sync confirms it, at a bounded rate per sync, and only
when server deletes are enabled at all.

The first sync that sees the file missing records it; a later sync — after
:data:`DELETE_CORROBORATION_SECONDS` (skipped on the session's final
``finish()``, the session's last sync) and a re-check that the file is still gone and the
marker still intact — sends the DELETE. Each sync sends a bounded number
of deletes; ``sync_deletions="log_only"`` only logs them, and
``"disabled"`` sends none, ever.
"""

from __future__ import annotations

import os
import shutil
from pathlib import Path

import pytest

import anthropic.lib.tools._memories as memories_mod
from anthropic.lib.tools._memories import MemoryDeleteMode, SessionMemoryStores

from .conftest import Clock, run_sync, listing_interrupted_by
from ._fake_anthropic import MemoryServer, deleted, updated, fake_anthropic

LOGGER = "anthropic.lib.tools.agent_toolset"

ELAPSED = memories_mod.DELETE_CORROBORATION_SECONDS + 1


async def _downloaded(
    tmp_path: Path, initial: dict[str, str], *, sync_deletions: MemoryDeleteMode = "enabled"
) -> tuple[Path, MemoryServer, SessionMemoryStores]:
    """A ``SessionMemoryStores`` with one store already downloaded to disk."""
    client, server = fake_anthropic(initial)
    stores = SessionMemoryStores(client, workdir=tmp_path, sync_deletions=sync_deletions)
    await stores.download(await client.beta.sessions.retrieve("s1"))
    return tmp_path / "memory" / "notes", server, stores


@pytest.mark.asyncio()
async def test_a_local_deletion_is_confirmed_before_it_reaches_the_server(tmp_path: Path, clock: Clock) -> None:
    local, server, stores = await _downloaded(tmp_path, {"a.md": "v1", "keep.md": "v1"})
    (local / "a.md").unlink()

    # The first pass only records the absence.
    await run_sync(stores)
    assert server.received == []
    assert server.files == {"a.md": "v1", "keep.md": "v1"}

    # Still inside the window: nothing goes out.
    clock.now = memories_mod.DELETE_CORROBORATION_SECONDS - 1
    await run_sync(stores)
    assert server.received == []

    # Window elapsed and the file is still gone: the guarded delete is sent.
    clock.now = ELAPSED
    await run_sync(stores)
    assert server.received == [deleted("a.md", was="v1")]
    assert server.files == {"keep.md": "v1"}


@pytest.mark.asyncio()
async def test_a_file_that_reappears_is_not_deleted_and_leaves_pending(tmp_path: Path, clock: Clock) -> None:
    local, server, stores = await _downloaded(tmp_path, {"a.md": "v1"})
    (local / "a.md").unlink()
    await run_sync(stores)

    (local / "a.md").write_text("v1")
    clock.now = ELAPSED
    await run_sync(stores)
    assert server.received == []
    assert server.files == {"a.md": "v1"}

    # The reappearance cleared the pending entry: deleting again starts a
    # fresh window instead of firing on the stale observation.
    (local / "a.md").unlink()
    await run_sync(stores)
    assert server.received == []
    clock.now = 2 * ELAPSED
    await run_sync(stores)
    assert server.received == [deleted("a.md", was="v1")]


@pytest.mark.asyncio()
async def test_disabled_mode_never_deletes_but_still_syncs(
    tmp_path: Path, clock: Clock, caplog: pytest.LogCaptureFixture
) -> None:
    caplog.set_level("DEBUG", logger=LOGGER)
    local, server, stores = await _downloaded(
        tmp_path, {"gone.md": "v1", "push.md": "v1", "pull.md": "v1"}, sync_deletions="disabled"
    )
    (local / "gone.md").unlink()
    (local / "push.md").write_text("v2 from agent")
    server.write("pull.md", "v2 from server")

    await run_sync(stores)
    clock.now = ELAPSED
    await run_sync(stores)
    clock.now = 2 * ELAPSED
    await run_sync(stores)

    # Uploads and pulls still flow; the deletion never does.
    assert server.received == [updated("push.md", "v2 from agent", was="v1")]
    assert server.files == {"gone.md": "v1", "push.md": "v2 from agent", "pull.md": "v2 from server"}
    assert (local / "pull.md").read_text() == "v2 from server"
    assert "server deletes are disabled" in caplog.text


@pytest.mark.asyncio()
async def test_the_per_pass_cap_spreads_deletes_over_passes(
    tmp_path: Path, clock: Clock, caplog: pytest.LogCaptureFixture
) -> None:
    caplog.set_level("WARNING", logger=LOGGER)
    files = {f"f{i:02d}.md": "v1" for i in range(14)}
    local, server, stores = await _downloaded(tmp_path, files)
    doomed = sorted(files)[:12]
    for name in doomed:
        (local / name).unlink()

    await run_sync(stores)
    assert server.received == []

    # cap = max(8, min(50, 14 // 4)) = 8: the first confirming sync stops there.
    clock.now = ELAPSED
    await run_sync(stores)
    assert server.received == [deleted(name, was="v1") for name in doomed[:8]]
    assert "delete cap reached: sent 8 deletes, held 4 for later syncs" in caplog.text

    # The held-back deletions confirm on the next pass.
    await run_sync(stores)
    assert server.received == [deleted(name, was="v1") for name in doomed]
    assert server.files == {name: "v1" for name in sorted(files)[12:]}


@pytest.mark.asyncio()
async def test_the_final_sync_waives_the_window_but_still_re_checks(tmp_path: Path) -> None:
    """A deletion made in a session shorter than the waiting window still
    goes through: the final sync skips the wait, and the re-check just
    before the delete stands in for the second observation."""
    local, server, stores = await _downloaded(tmp_path, {"a.md": "v1", "keep.md": "v1"})
    (local / "a.md").unlink()

    await stores.finish()

    assert server.received == [deleted("a.md", was="v1")]
    assert server.files == {"keep.md": "v1"}


@pytest.mark.asyncio()
async def test_a_folder_destroyed_mid_sync_sends_no_deletes(tmp_path: Path, clock: Clock) -> None:
    """The directory scan saw an intact folder, then the folder vanished
    while the server listing was in flight: the re-check just before the
    delete must notice the marker is gone and hold every delete."""
    local, server, stores = await _downloaded(tmp_path, {"a.md": "v1", "keep.md": "v1"})
    (local / "a.md").unlink()
    await run_sync(stores)
    clock.now = ELAPSED

    with listing_interrupted_by(stores, lambda: shutil.rmtree(local)):
        await run_sync(stores)

    assert server.received == []
    assert server.files == {"a.md": "v1", "keep.md": "v1"}


@pytest.mark.skipif(os.geteuid() == 0, reason="permission checks do not bind root")
@pytest.mark.asyncio()
async def test_an_unreadable_subdirectory_fails_the_pass_instead_of_reading_as_deletions(
    tmp_path: Path, clock: Clock, caplog: pytest.LogCaptureFixture
) -> None:
    """Files under a directory the scan cannot enter are not treated as deleted."""
    caplog.set_level("WARNING", logger=LOGGER)
    local, server, stores = await _downloaded(tmp_path, {"sub/a.md": "v1", "sub/b.md": "v1", "top.md": "v1"})
    (local / "top.md").write_text("v2")
    (local / "sub").chmod(0o000)
    try:
        await run_sync(stores)
        clock.now = ELAPSED
        await run_sync(stores)
    finally:
        (local / "sub").chmod(0o700)

    assert server.received == []
    assert caplog.text.count("memory sync failed") == 2

    # Readable again: the edit goes out and nothing is deleted.
    clock.now = 2 * ELAPSED
    await run_sync(stores)
    assert server.received == [updated("top.md", "v2", was="v1")]
    assert server.files == {"sub/a.md": "v1", "sub/b.md": "v1", "top.md": "v2"}


@pytest.mark.asyncio()
async def test_a_recovery_re_download_clears_pending_deletes(tmp_path: Path, clock: Clock) -> None:
    """The re-download rebuilt the disk, so an absence observed before it says
    nothing about the rebuilt folder."""
    local, server, stores = await _downloaded(tmp_path, {"a.md": "v1"})
    (local / "a.md").unlink()
    await run_sync(stores)

    clock.now = ELAPSED
    shutil.rmtree(local)
    await run_sync(stores)
    assert (local / "a.md").read_text() == "v1"

    # A fresh deletion starts a fresh window — the pre-recovery observation
    # must not corroborate it.
    (local / "a.md").unlink()
    await run_sync(stores)
    assert server.received == []
    clock.now = 2 * ELAPSED
    await run_sync(stores)
    assert server.received == [deleted("a.md", was="v1")]


@pytest.mark.asyncio()
async def test_log_only_mode_logs_the_delete_but_never_sends_it(
    tmp_path: Path, clock: Clock, caplog: pytest.LogCaptureFixture
) -> None:
    """The dry-run setting: the full pipeline runs — window, re-checks, cap —
    but the confirmed delete is logged instead of sent, on every sync while
    the file stays missing."""
    caplog.set_level("INFO", logger=LOGGER)
    local, server, stores = await _downloaded(tmp_path, {"a.md": "v1", "keep.md": "v1"}, sync_deletions="log_only")
    (local / "a.md").unlink()

    await run_sync(stores)
    assert "log-only" not in caplog.text  # still inside the waiting window

    clock.now = ELAPSED
    await run_sync(stores)
    await run_sync(stores)

    assert server.received == []
    assert server.files == {"a.md": "v1", "keep.md": "v1"}
    assert caplog.text.count("log-only: sync would delete this memory on the server path=a.md") == 2


@pytest.mark.asyncio()
async def test_finish_runs_once_and_a_second_call_raises(tmp_path: Path) -> None:
    local, server, stores = await _downloaded(tmp_path, {"a.md": "v1"})
    (local / "a.md").write_text("v2")

    await stores.finish()
    assert server.files == {"a.md": "v2"}

    with pytest.raises(RuntimeError, match="finish"):
        await stores.finish()
