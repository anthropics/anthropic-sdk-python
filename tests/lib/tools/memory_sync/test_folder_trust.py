"""Folder-trust gating: a missing, emptied, or swapped store folder is never
trusted as a basis for deletions or uploads.

``download`` stamps :data:`MARKER_PATH` (holding the store's id) into the
folder. A sync pass that finds the folder destroyed re-downloads it and
pushes nothing; a sync that finds files without a matching marker leaves
the folder as found and syncs nothing at all.
"""

from __future__ import annotations

import shutil
from pathlib import Path

import pytest

import anthropic.lib.tools._memories as memories_mod
from anthropic.lib.tools._memories import MARKER_PATH, SessionMemoryStores

from .conftest import Clock, run_sync, listing_interrupted_by
from ._fake_anthropic import MemoryServer, deleted, updated, fake_anthropic

LOGGER = "anthropic.lib.tools.agent_toolset"

STORE_ID = "memstore_notes"


def marker_stamp(local: Path) -> str:
    return (local / MARKER_PATH).read_text()


async def _downloaded(tmp_path: Path, initial: dict[str, str]) -> tuple[Path, MemoryServer, SessionMemoryStores]:
    """A ``SessionMemoryStores`` with one store already downloaded to disk."""
    client, server = fake_anthropic(initial)
    stores = SessionMemoryStores(client, workdir=tmp_path)
    await stores.download(await client.beta.sessions.retrieve("s1"))
    return tmp_path / "memory" / "notes", server, stores


@pytest.mark.asyncio()
async def test_a_deleted_folder_issues_no_deletes_and_is_rebuilt(
    tmp_path: Path, caplog: pytest.LogCaptureFixture, clock: Clock
) -> None:
    """rm -rf of the whole folder between syncs: the next sync must not read
    the emptiness as "the agent deleted everything" and wipe the server."""
    caplog.set_level("WARNING", logger=LOGGER)
    local, server, stores = await _downloaded(tmp_path, {"a.md": "v1", "b.md": "v1"})
    shutil.rmtree(local)

    await run_sync(stores)

    assert server.received == []
    assert server.files == {"a.md": "v1", "b.md": "v1"}
    assert (local / "a.md").read_text() == "v1"
    assert (local / "b.md").read_text() == "v1"
    assert marker_stamp(local) == f"version 1\n{STORE_ID}"
    assert "the folder or its marker is gone; re-downloading" in caplog.text

    # The rebuilt folder syncs normally: an edit and a deletion both propagate
    # (the deletion after its waiting window).
    (local / "a.md").write_text("v2")
    (local / "b.md").unlink()
    await run_sync(stores)
    clock.now = memories_mod.DELETE_CORROBORATION_SECONDS + 1
    await run_sync(stores)
    assert server.received == [updated("a.md", "v2", was="v1"), deleted("b.md", was="v1")]
    assert server.files == {"a.md": "v2"}


@pytest.mark.asyncio()
async def test_an_emptied_folder_issues_no_deletes_and_is_repopulated(
    tmp_path: Path, caplog: pytest.LogCaptureFixture, clock: Clock
) -> None:
    caplog.set_level("WARNING", logger=LOGGER)
    local, server, stores = await _downloaded(tmp_path, {"a.md": "v1", "b.md": "v1"})
    for child in local.iterdir():
        child.unlink()

    await run_sync(stores)

    assert server.received == []
    assert server.files == {"a.md": "v1", "b.md": "v1"}
    assert (local / "a.md").read_text() == "v1"
    assert marker_stamp(local) == f"version 1\n{STORE_ID}"
    assert "the folder or its marker is gone; re-downloading" in caplog.text

    (local / "a.md").unlink()
    await run_sync(stores)
    clock.now = memories_mod.DELETE_CORROBORATION_SECONDS + 1
    await run_sync(stores)
    assert server.received == [deleted("a.md", was="v1")]


@pytest.mark.asyncio()
async def test_an_emptied_folder_with_the_marker_left_behind_issues_no_deletes(
    tmp_path: Path, caplog: pytest.LogCaptureFixture, clock: Clock
) -> None:
    """``rm <mount>/*``: shell globs skip dotfiles, so the marker survives the
    wipe — an intact marker alone must not clear a folder whose every
    memory file vanished at once."""
    caplog.set_level("WARNING", logger=LOGGER)
    local, server, stores = await _downloaded(tmp_path, {"a.md": "v1", "b.md": "v1"})
    for child in local.iterdir():
        if child.name != MARKER_PATH:
            child.unlink()

    await run_sync(stores)

    assert server.received == []
    assert server.files == {"a.md": "v1", "b.md": "v1"}
    assert (local / "a.md").read_text() == "v1"
    assert "every memory file is gone at once; re-downloading" in caplog.text

    # With files present again, an ordinary single deletion still propagates
    # (after its waiting window).
    (local / "a.md").unlink()
    await run_sync(stores)
    clock.now = memories_mod.DELETE_CORROBORATION_SECONDS + 1
    await run_sync(stores)
    assert server.received == [deleted("a.md", was="v1")]


@pytest.mark.asyncio()
async def test_a_swapped_folder_neither_deletes_nor_uploads_ever(
    tmp_path: Path, caplog: pytest.LogCaptureFixture
) -> None:
    """A folder carrying another store's marker is foreign: the pass must not
    adopt it — no deletes, no uploads, no restamp — on this pass or any later
    one, or the foreign files leak into the customer's store one pass later."""
    caplog.set_level("WARNING", logger=LOGGER)
    local, server, stores = await _downloaded(tmp_path, {"a.md": "v1"})
    shutil.rmtree(local)
    local.mkdir()
    (local / MARKER_PATH).write_text("memstore_other")
    (local / "foreign.md").write_text("someone else's notes")

    await run_sync(stores)
    await run_sync(stores)

    assert server.received == []
    assert server.files == {"a.md": "v1"}
    assert (local / MARKER_PATH).read_text() == "memstore_other"
    assert (local / "foreign.md").read_text() == "someone else's notes"
    assert not (local / "a.md").exists()
    assert "the marker file does not match this store; leaving the memory store folder as found" in caplog.text


@pytest.mark.asyncio()
async def test_files_without_a_marker_are_neither_pushed_nor_pulled_over(
    tmp_path: Path, caplog: pytest.LogCaptureFixture
) -> None:
    """Only the marker was deleted (a dotfile cleanup): the remaining files may
    hold un-pushed edits, so the pass must neither upload them, nor delete by
    them, nor destroy them by re-downloading over the folder."""
    caplog.set_level("WARNING", logger=LOGGER)
    local, server, stores = await _downloaded(tmp_path, {"a.md": "v1", "b.md": "v1"})
    (local / MARKER_PATH).unlink()
    (local / "a.md").write_text("un-pushed edit")
    (local / "b.md").unlink()

    await run_sync(stores)

    assert server.received == []
    assert server.files == {"a.md": "v1", "b.md": "v1"}
    assert (local / "a.md").read_text() == "un-pushed edit"
    assert not (local / MARKER_PATH).exists()
    assert "the marker file is gone; leaving the memory store folder as found" in caplog.text


@pytest.mark.asyncio()
async def test_a_single_local_deletion_with_the_marker_intact_still_propagates(tmp_path: Path, clock: Clock) -> None:
    local, server, stores = await _downloaded(tmp_path, {"a.md": "v1", "b.md": "v1"})
    (local / "a.md").unlink()

    await run_sync(stores)
    clock.now = memories_mod.DELETE_CORROBORATION_SECONDS + 1
    await run_sync(stores)

    assert server.received == [deleted("a.md", was="v1")]
    assert server.files == {"b.md": "v1"}
    assert marker_stamp(local) == f"version 1\n{STORE_ID}"


@pytest.mark.asyncio()
async def test_the_marker_never_syncs_in_either_direction(tmp_path: Path, caplog: pytest.LogCaptureFixture) -> None:
    caplog.set_level("WARNING", logger=LOGGER)
    local, server, stores = await _downloaded(tmp_path, {"a.md": "v1"})

    # The marker sits in the folder yet is never uploaded or remote-deleted.
    await run_sync(stores)
    assert server.received == []

    # A marker path the server lists is refused: skipped with a warning,
    # never written over the real marker on disk.
    server.write(MARKER_PATH, "not a store id")
    await run_sync(stores)
    assert server.received == []
    assert marker_stamp(local) == f"version 1\n{STORE_ID}"
    assert "reserved marker path" in caplog.text


@pytest.mark.asyncio()
async def test_dispose_tolerates_an_already_deleted_folder(tmp_path: Path) -> None:
    local, _server, stores = await _downloaded(tmp_path, {"a.md": "v1"})
    shutil.rmtree(local)

    await stores.dispose()

    assert not local.exists()


@pytest.mark.asyncio()
async def test_dispose_keeps_a_folder_that_fails_the_marker_check(
    tmp_path: Path, caplog: pytest.LogCaptureFixture
) -> None:
    """Sync left the folder as found after a failed marker check; teardown
    must not then delete the files sync refused to touch."""
    caplog.set_level("WARNING", logger=LOGGER)
    local, _server, stores = await _downloaded(tmp_path, {"a.md": "v1"})
    (local / MARKER_PATH).unlink()
    (local / "a.md").write_text("un-pushed edit")

    await stores.dispose()

    assert (local / "a.md").read_text() == "un-pushed edit"
    assert "leaving the memory store folder on disk" in caplog.text


@pytest.mark.asyncio()
async def test_dispose_never_raises_when_a_store_root_is_replaced_by_a_file(tmp_path: Path) -> None:
    """The worker calls dispose() from its teardown: a store whose folder
    something replaced with a regular file must log and be skipped, not
    raise out of the teardown."""
    local, _server, stores = await _downloaded(tmp_path, {"a.md": "v1"})
    shutil.rmtree(local)
    local.write_text("a file where the folder was")

    await stores.dispose()

    assert local.read_text() == "a file where the folder was"


@pytest.mark.asyncio()
async def test_a_marker_from_an_older_format_no_longer_clears_the_folder(
    tmp_path: Path, caplog: pytest.LogCaptureFixture
) -> None:
    """The marker carries a format version so an SDK upgrade can retire every
    folder written before it: a marker in the old format (the bare store id)
    must fail the check, and the folder is left as found."""
    caplog.set_level("WARNING", logger=LOGGER)
    local, server, stores = await _downloaded(tmp_path, {"a.md": "v1", "b.md": "v1"})
    (local / MARKER_PATH).write_text(STORE_ID)
    (local / "a.md").write_text("edit under the old marker")
    (local / "b.md").unlink()

    await run_sync(stores)

    assert server.received == []
    assert server.files == {"a.md": "v1", "b.md": "v1"}
    assert (local / "a.md").read_text() == "edit under the old marker"
    assert "the marker file does not match this store" in caplog.text


@pytest.mark.asyncio()
@pytest.mark.parametrize("rel", ["z.md", "sub/z.md"])
async def test_a_folder_wiped_while_a_pull_is_in_flight_is_rebuilt_not_distrusted(
    tmp_path: Path, caplog: pytest.LogCaptureFixture, rel: str
) -> None:
    """rm -rf lands between a sync's scan and its content write: the write
    must not bring the folder back without its marker, or every later sync
    reads the folder as foreign and the session's memory writes are lost."""
    caplog.set_level("WARNING", logger=LOGGER)
    local, server, stores = await _downloaded(tmp_path, {"x.md": "v1", "y.md": "v1", rel: "v1"})
    server.write(rel, "v2")
    server.fetch_hook = lambda _p: shutil.rmtree(local)

    await run_sync(stores)

    assert not local.exists()
    assert server.received == []

    server.fetch_hook = None
    await run_sync(stores)

    assert marker_stamp(local) == f"version 1\n{STORE_ID}"
    assert (local / "x.md").read_text() == "v1"
    assert (local / rel).read_text() == "v2"
    assert "re-downloading the memory store folder" in caplog.text
    assert "leaving the memory store folder as found" not in caplog.text

    await stores.finish()
    await stores.flush_writes()
    await stores.dispose()
    assert not local.exists()
    assert server.received == []
    assert server.files == {"x.md": "v1", "y.md": "v1", rel: "v2"}


@pytest.mark.asyncio()
async def test_a_folder_wiped_while_a_locally_deleted_memory_is_being_restored_is_rebuilt(
    tmp_path: Path, caplog: pytest.LogCaptureFixture, clock: Clock
) -> None:
    """A file deleted locally but changed on the server is restored by the
    next sync; an rm -rf that lands while that restore is downloading must
    leave no folder behind, the sync after it must rebuild the whole store,
    and the earlier absence must never become a server delete."""
    caplog.set_level("WARNING", logger=LOGGER)
    local, server, stores = await _downloaded(tmp_path, {"x.md": "v1", "y.md": "v1", "z.md": "v1"})
    (local / "z.md").unlink()
    server.write("z.md", "v2")
    server.fetch_hook = lambda _p: shutil.rmtree(local)

    await run_sync(stores)
    assert not local.exists()

    server.fetch_hook = None
    await run_sync(stores)
    assert marker_stamp(local) == f"version 1\n{STORE_ID}"
    assert (local / "x.md").read_text() == "v1"
    assert (local / "y.md").read_text() == "v1"
    assert (local / "z.md").read_text() == "v2"

    clock.now = memories_mod.DELETE_CORROBORATION_SECONDS + 1
    await run_sync(stores)
    assert server.received == []
    assert server.files == {"x.md": "v1", "y.md": "v1", "z.md": "v2"}
    assert "leaving the memory store folder as found" not in caplog.text


@pytest.mark.asyncio()
async def test_a_folder_wiped_again_mid_recovery_is_rebuilt_by_the_next_sync(
    tmp_path: Path, caplog: pytest.LogCaptureFixture
) -> None:
    """A re-download writes the marker first and the memories after it; a
    second rm -rf between those writes must not leave memories on disk
    without a marker — the next sync re-downloads once more instead."""
    caplog.set_level("WARNING", logger=LOGGER)
    local, server, stores = await _downloaded(tmp_path, {"a.md": "v1", "b.md": "v1", "c.md": "v1"})
    shutil.rmtree(local)

    with listing_interrupted_by(stores, lambda: shutil.rmtree(local), after_items=1):
        await run_sync(stores)

    assert not local.exists()
    assert server.received == []

    await run_sync(stores)

    assert marker_stamp(local) == f"version 1\n{STORE_ID}"
    for name in ("a.md", "b.md", "c.md"):
        assert (local / name).read_text() == "v1"
    assert caplog.text.count("re-downloading the memory store folder") == 2
    assert "leaving the memory store folder as found" not in caplog.text
    assert server.received == []

    await stores.dispose()
    assert not local.exists()
