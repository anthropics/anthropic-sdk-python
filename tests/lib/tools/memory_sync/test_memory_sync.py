"""The memory-store sync contract.

An agent keeps a folder of notes on disk. The same folder lives on the
server. Each sync makes the two agree: each side gets
the other's changes, and when both changed the same file the server wins.

Each test tells one story with two actors — ``local`` is the agent's
folder on disk, ``server`` is the remote copy. Paths are the same string
on both sides. ``server.received`` holds only what the sync sent;
arranging remote state never touches it.
"""

from __future__ import annotations

import os
from typing import Any
from pathlib import Path

import pytest

from anthropic._compat import PYDANTIC_V1
from anthropic.lib.tools import _memories as memories_mod
from anthropic.lib.tools._memories import SessionMemoryError, SessionMemoryStores

from .conftest import Clock, run_sync
from ._fake_anthropic import MemoryServer, created, deleted, updated, _status_error, fake_anthropic

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
async def test_edits_flow_both_ways_and_the_server_wins_conflicts(
    tmp_path: Path, caplog: pytest.LogCaptureFixture
) -> None:
    caplog.set_level("WARNING", logger=LOGGER)
    local, server, stores = await _downloaded(
        tmp_path, {"push.md": "v1", "pull.md": "v1", "both.md": "v1", "gone.md": "v1"}
    )

    (local / "push.md").write_text("v2 from agent")
    (local / "new.md").write_text("new from agent")
    server.write("pull.md", "v2 from server")
    (local / "both.md").write_text("v2 from agent")
    server.write("both.md", "v2 from server")
    server.delete("gone.md")

    await run_sync(stores)

    # Each side has the other's change; the server won the conflict; the
    # server's deletion took the local copy with it.
    assert server.files["push.md"] == "v2 from agent"
    assert server.files["new.md"] == "new from agent"
    assert (local / "pull.md").read_text() == "v2 from server"
    assert (local / "both.md").read_text() == "v2 from server"
    assert not (local / "gone.md").exists()
    assert "gone.md" not in server.files
    assert "changed both locally and remotely" in caplog.text

    # The push was guarded: overwrite only if the server still had v1.
    sent = [created("new.md", "new from agent"), updated("push.md", "v2 from agent", was="v1")]
    assert server.received == sent

    # Settled: a second sync sends nothing more.
    await run_sync(stores)
    assert server.received == sent


@pytest.mark.asyncio()
async def test_local_deletions_reach_the_server_unless_it_changed(tmp_path: Path, clock: Clock) -> None:
    # One memory's download write fails, so it is never on disk to begin with —
    # that absence is not a deletion.
    from anthropic.lib.tools import _file_store

    real_put = _file_store.LocalFileStore.put

    async def flaky_put(self: _file_store.LocalFileStore, rel: str, content: str) -> None:
        if rel == "never.md":
            raise OSError(5, "I/O error")
        await real_put(self, rel, content)

    # keep.md survives on disk so the pass is not an all-files-gone wipe.
    client, server = fake_anthropic({"drop.md": "v1", "raced.md": "v1", "never.md": "v1", "keep.md": "v1"})
    stores = SessionMemoryStores(client, workdir=tmp_path)
    with pytest.MonkeyPatch.context() as mp:
        mp.setattr(_file_store.LocalFileStore, "put", flaky_put)
        await stores.download(await client.beta.sessions.retrieve("s1"))
    local = tmp_path / "memory" / "notes"

    (local / "drop.md").unlink()
    (local / "raced.md").unlink()
    server.write("raced.md", "v2 from server")

    await run_sync(stores)
    # The first pass only records the deletion; a corroborating pass after
    # the window sends it.
    assert "drop.md" in server.files
    clock.now = memories_mod.DELETE_CORROBORATION_SECONDS + 1
    await run_sync(stores)

    # Only the un-raced deletion went out, guarded by the last-synced content.
    sent = [deleted("drop.md", was="v1")]
    assert server.received == sent
    assert "drop.md" not in server.files
    # The raced deletion lost — the server's edit came back to disk instead.
    assert (local / "raced.md").read_text() == "v2 from server"
    # The never-downloaded file was pulled, not deleted.
    assert (local / "never.md").read_text() == "v1"
    assert server.files["never.md"] == "v1"

    await run_sync(stores)
    assert server.received == sent


@pytest.mark.asyncio()
async def test_read_only_stores_are_never_written(tmp_path: Path) -> None:
    local, server, stores = await _downloaded(
        tmp_path, {"edit.md": "v1", "drop.md": "v1", "pull.md": "v1"}, access="read_only"
    )

    (local / "edit.md").write_text("v2 from agent")
    (local / "drop.md").unlink()
    (local / "new.md").write_text("new from agent")
    server.write("pull.md", "v2 from server")

    await run_sync(stores)

    assert server.received == []
    assert server.files == {"edit.md": "v1", "drop.md": "v1", "pull.md": "v2 from server"}
    # Pulls still happen.
    assert (local / "pull.md").read_text() == "v2 from server"

    # A remote deletion is a pull too, so it removes the local copy even here.
    server.delete("pull.md")
    await run_sync(stores)
    assert server.received == []
    assert not (local / "pull.md").exists()


@pytest.mark.asyncio()
async def test_paths_that_escape_the_store_are_refused(tmp_path: Path, caplog: pytest.LogCaptureFixture) -> None:
    caplog.set_level("WARNING", logger=LOGGER)
    local, server, stores = await _downloaded(tmp_path, {"../evil.md": "boom", "ok.md": "fine"})

    await run_sync(stores)

    assert (local / "ok.md").read_text() == "fine"
    assert list(tmp_path.rglob("evil.md")) == []
    assert server.received == []
    assert "escapes" in caplog.text


@pytest.mark.asyncio()
async def test_worker_lifecycle_cadence_and_dispose(tmp_path: Path, clock: Clock) -> None:
    """The worker's call sequence: download → sync_if_due per call → finish → dispose."""
    # The worker polls sync_if_due after each tool call and
    # runs one final sync on a clean end. A fake clock makes the cadence
    # observable.
    client, server = fake_anthropic({"note.md": "v1"})
    stores = SessionMemoryStores(client, workdir=tmp_path, sync_interval=300.0)
    await stores.download(await client.beta.sessions.retrieve("s1"))
    local = tmp_path / "memory" / "notes"

    (local / "note.md").write_text("edit 1")
    await stores.sync_if_due()
    assert server.received == []

    # One long gap fires exactly once, and not again until another interval.
    clock.now = 2000.0
    await stores.sync_if_due()
    await stores.sync_if_due()
    assert server.received == [updated("note.md", "edit 1", was="v1")]
    clock.now = 2299.0
    await stores.sync_if_due()
    assert len(server.received) == 1

    # The last sync is finish(): unconditional, once.
    (local / "note.md").write_text("edit 2")
    await stores.finish()
    assert server.received[-1] == updated("note.md", "edit 2", was="edit 1")

    # Dispose removes the store dir the download created.
    assert local.exists()
    await stores.dispose()
    assert not local.exists()


@pytest.mark.skipif(PYDANTIC_V1, reason="tool functions are only supported with pydantic v2")
@pytest.mark.asyncio()
async def test_write_and_edit_tools_refuse_read_only_roots(tmp_path: Path) -> None:
    from anthropic.lib.tools.agent_toolset import AgentToolContext, beta_edit_tool, beta_write_tool
    from anthropic.lib.tools._beta_functions import ToolError

    ro = tmp_path / "memory" / "notes"
    ro.mkdir(parents=True)
    (ro / "facts.md").write_text("immutable")

    ctx = AgentToolContext(workdir=str(tmp_path), read_only_roots=[ro.resolve()])
    write = beta_write_tool(ctx)
    edit = beta_edit_tool(ctx)

    with pytest.raises(ToolError, match="read-only"):
        await write.call({"file_path": str(ro / "facts.md"), "content": "overwritten"})
    with pytest.raises(ToolError, match="read-only"):
        await write.call({"file_path": str(ro / "new.md"), "content": "new"})
    with pytest.raises(ToolError, match="read-only"):
        await edit.call({"file_path": str(ro / "facts.md"), "old_string": "immutable", "new_string": "x"})
    assert (ro / "facts.md").read_text() == "immutable"
    assert not (ro / "new.md").exists()

    # Paths outside the read-only root are unaffected.
    await write.call({"file_path": "scratch.txt", "content": "ok"})
    assert (tmp_path / "scratch.txt").read_text() == "ok"


@pytest.mark.asyncio()
async def test_a_binary_local_file_never_blocks_the_other_files(
    tmp_path: Path, caplog: pytest.LogCaptureFixture
) -> None:
    """The store is utf-8-restricted, so a binary file the agent drops in the
    folder is refused at read — warned once and skipped until it changes —
    while every other file keeps syncing."""
    caplog.set_level("WARNING", logger=LOGGER)
    local, server, stores = await _downloaded(tmp_path, {"note.md": "v1"})

    (local / "blob.bin").write_bytes(b"\xff\xfe\x00 not utf-8")
    (local / "note.md").write_text("v2")

    await run_sync(stores)
    await run_sync(stores)

    assert server.received == [updated("note.md", "v2", was="v1")]
    assert "blob.bin" not in server.files
    assert caplog.text.count("stays un-synced until its content changes path=blob.bin") == 1


@pytest.mark.asyncio()
async def test_an_oversized_file_is_skipped_until_it_shrinks(tmp_path: Path, caplog: pytest.LogCaptureFixture) -> None:
    """A file the server refuses as too large is warned once and skipped —
    not retried while unchanged, never blocking the other files — and syncs
    as soon as an edit brings it under the cap."""
    caplog.set_level("WARNING", logger=LOGGER)
    local, server, stores = await _downloaded(tmp_path, {"note.md": "v1"})
    server.max_content_bytes = 64

    (local / "big.md").write_text("x" * 100)
    (local / "note.md").write_text("v2")

    await run_sync(stores)
    await run_sync(stores)

    # The small edit landed; the big file was attempted exactly once.
    assert updated("note.md", "v2", was="v1") in server.received
    assert sum(1 for r in server.received if r[0] == "create") == 1
    assert "big.md" not in server.files
    assert caplog.text.count("stays un-synced until its content changes path=big.md") == 1

    (local / "big.md").write_text("small now")
    await run_sync(stores)
    assert server.files["big.md"] == "small now"


@pytest.mark.asyncio()
@pytest.mark.parametrize("status", [401, 403, 404])
async def test_a_refusal_that_says_nothing_about_the_content_is_retried_next_sync(
    tmp_path: Path, caplog: pytest.LogCaptureFixture, status: int
) -> None:
    """Anything but a content refusal is retried by the next sync."""
    caplog.set_level("WARNING", logger=LOGGER)
    local, server, stores = await _downloaded(tmp_path, {"note.md": "v1"})
    (local / "note.md").write_text("v2")
    (local / "new.md").write_text("fresh")

    async def refuse(_path: str) -> None:
        raise _status_error(status)

    server.upload_hook = refuse
    await run_sync(stores)
    server.upload_hook = None
    await run_sync(stores)

    assert server.files == {"note.md": "v2", "new.md": "fresh"}
    assert "stays un-synced" not in caplog.text


@pytest.mark.asyncio()
async def test_an_upload_that_loses_the_race_pulls_the_winner_next_sync(
    tmp_path: Path, caplog: pytest.LogCaptureFixture
) -> None:
    """The server changes between this sync's list and its update: the
    content_sha256 precondition rejects the push (409), and the next sync
    applies the conflict rule — the winning remote edit is pulled, the
    local edit is never re-pushed."""
    caplog.set_level("WARNING", logger=LOGGER)
    local, server, stores = await _downloaded(tmp_path, {"note.md": "v1"})

    (local / "note.md").write_text("local edit")
    memories = stores._client.beta.memory_stores.memories  # pyright: ignore[reportPrivateUsage]
    real_update = memories.update

    async def racing_update(memory_id: str, **kw: Any) -> Any:
        # Race: the remote changes after this sync's list, before its update.
        server.write("note.md", "raced remote edit")
        return await real_update(memory_id, **kw)

    memories.update = racing_update
    await run_sync(stores)
    memories.update = real_update

    # The precondition rejected the push (one guarded attempt, no retry) and
    # the server kept its raced edit.
    assert server.received == [updated("note.md", "local edit", was="v1")]
    assert server.files["note.md"] == "raced remote edit"
    # The log says what actually happened: the push was refused and the local
    # copy is now stale — nothing was "kept".
    assert "the upload was refused and the local edit loses" in caplog.text
    assert (local / "note.md").read_text() == "local edit"

    # The next sync pulls the winner instead of re-pushing.
    await run_sync(stores)
    assert (local / "note.md").read_text() == "raced remote edit"
    assert len(server.received) == 1


@pytest.mark.asyncio()
async def test_a_broken_store_fails_the_whole_download(tmp_path: Path) -> None:
    """A store that cannot be materialised fails the download outright. A
    session served without a folder its system prompt names would run with
    amnesia; the worker turns this into a failed work item."""
    client, _ = fake_anthropic({"note.md": "v1"}, broken_store=True)
    stores = SessionMemoryStores(client, workdir=tmp_path)

    with pytest.raises(SessionMemoryError, match="memstore_broken"):
        await stores.download(await client.beta.sessions.retrieve("s1"))

    # The half-downloaded folder self-destructed; nothing is tracked.
    assert not (tmp_path / "memory" / "broken").exists()
    assert stores.read_only_roots == []


@pytest.mark.asyncio()
async def test_a_legal_mount_path_is_honored_and_an_unclean_one_is_refused(tmp_path: Path) -> None:
    """mount_path is the location the agent's system prompt names. A clean
    absolute one is honored verbatim, and dispose removes it when the download
    created it. One we cannot use verbatim fails the session rather than
    quietly relocating the store somewhere the agent will never look."""
    mount = tmp_path / "mnt" / "notes"
    client, _ = fake_anthropic({"note.md": "v1"}, mount_path=str(mount))
    stores = SessionMemoryStores(client, workdir=tmp_path / "wd")
    await stores.download(await client.beta.sessions.retrieve("s1"))
    assert (mount / "note.md").read_text() == "v1"
    # The worker feeds these roots to the file tools' allowed roots, so the
    # out-of-workdir mount stays reachable.
    assert stores.roots == [mount.resolve()]
    await stores.dispose()
    assert not mount.exists()


@pytest.mark.asyncio()
async def test_an_unwritable_mount_path_fails_the_download(tmp_path: Path) -> None:
    """A mount the host cannot provide is an environment failure: the download
    raises loudly (failing the work item) instead of degrading to a session
    with silently-empty memory."""
    if os.geteuid() == 0:
        pytest.skip("directory modes do not bind root")
    parent = tmp_path / "mnt"
    parent.mkdir()
    parent.chmod(0o500)  # the worker may not create the store's folder here
    try:
        client, server = fake_anthropic({"note.md": "v1"}, mount_path=str(parent / "notes"))
        stores = SessionMemoryStores(client, workdir=tmp_path / "wd")

        with pytest.raises(SessionMemoryError, match="writable"):
            await stores.download(await client.beta.sessions.retrieve("s1"))
        assert server.received == []
    finally:
        parent.chmod(0o700)


@pytest.mark.parametrize("bad", ["/mnt/../../etc/cron.d", "relative/notes", "", "notes"])
@pytest.mark.asyncio()
async def test_an_unclean_mount_path_fails_the_download(tmp_path: Path, bad: str) -> None:
    # "" means the resource carries no mount_path at all — that one is allowed,
    # and falls back to the workdir, because nothing pointed the agent anywhere.
    client, server = fake_anthropic({"note.md": "v1"}, mount_path=bad or None)
    stores = SessionMemoryStores(client, workdir=tmp_path / "wd")

    if not bad:
        await stores.download(await client.beta.sessions.retrieve("s1"))
        assert (tmp_path / "wd" / "memory" / "notes" / "note.md").read_text() == "v1"
        return

    with pytest.raises(SessionMemoryError, match="not a clean absolute path"):
        await stores.download(await client.beta.sessions.retrieve("s1"))

    # Nothing was written anywhere, and no store is tracked.
    assert not (tmp_path / "wd").exists()
    assert server.received == []
    assert stores.read_only_roots == []


@pytest.mark.asyncio()
async def test_prefix_items_and_foreign_resources_leave_no_trace(tmp_path: Path) -> None:
    """Only ``memory_store`` resources are downloaded and only ``memory``
    items carry content — a ``file`` resource and ``memory_prefix`` rollups
    pass through without touching the disk or the server."""
    client, server = fake_anthropic({"ok.md": "fine"}, noise=True)
    stores = SessionMemoryStores(client, workdir=tmp_path)
    await stores.download(await client.beta.sessions.retrieve("s1"))
    local = tmp_path / "memory" / "notes"

    assert (local / "ok.md").read_text() == "fine"
    assert list((tmp_path / "memory").iterdir()) == [local]
    assert not (local / "projects").exists()
    await run_sync(stores)
    assert server.received == []


@pytest.mark.asyncio()
async def test_a_store_directory_that_already_exists_is_refused(tmp_path: Path) -> None:
    """Nothing but a dead run leaves a folder at the store's path. Syncing into
    it would fold that run's debris into the customer's store, so refuse — and
    leave the folder exactly as it was found."""
    stale = tmp_path / "memory" / "notes"
    stale.mkdir(parents=True)
    (stale / "debris.md").write_text("left by another session")

    client, server = fake_anthropic({"note.md": "v1"})
    stores = SessionMemoryStores(client, workdir=tmp_path)

    with pytest.raises(SessionMemoryError, match="already exists"):
        await stores.download(await client.beta.sessions.retrieve("s1"))

    # Refused, not adopted and not deleted.
    assert (stale / "debris.md").read_text() == "left by another session"
    assert not (stale / "note.md").exists()
    assert server.received == []
    assert stores.read_only_roots == []

    # A sibling folder in the same parent is none of our business.
    other = tmp_path / "memory2" / "notes"
    other.parent.mkdir(parents=True)
    (tmp_path / "memory2" / "unrelated").mkdir()
    client2, _ = fake_anthropic({"note.md": "v1"})
    ok = SessionMemoryStores(client2, workdir=tmp_path / "memory2")
    await ok.download(await client2.beta.sessions.retrieve("s1"))
    assert (tmp_path / "memory2" / "memory" / "notes" / "note.md").read_text() == "v1"


# ---- the sync matrix -------------------------------------------------------
#
# Every combination of (remote moved?, local moved?) for a path the store has
# already downloaded, plus the paths only one side knows about. `local` and
# `remote` say what happened since the last sync; `disk` and `store` are the
# state both sides must agree on afterwards. A `fails` column injects a broken
# upload/download so the row also pins where a failed operation leaves us.

_MISSING = object()


@pytest.mark.parametrize(
    ("name", "local", "remote", "disk", "store", "sent"),
    [
        # baseline "v1" on both sides unless the row says otherwise
        ("untouched", None, None, "v1", "v1", []),
        ("local edit", "v2", None, "v2", "v2", [("update", "v2", "v1")]),
        ("remote edit", None, "v2", "v2", "v2", []),
        ("both edit, server wins", "v2 local", "v2 remote", "v2 remote", "v2 remote", []),
        ("local delete", _MISSING, None, _MISSING, _MISSING, [("delete", None, "v1")]),
        ("remote delete", None, _MISSING, _MISSING, _MISSING, []),
        ("both delete", _MISSING, _MISSING, _MISSING, _MISSING, []),
        ("local delete, remote edit", _MISSING, "v2", "v2", "v2", []),
        ("local edit, remote delete", "v2", _MISSING, "v2", "v2", [("create", "v2", None)]),
    ],
)
@pytest.mark.asyncio()
async def test_sync_matrix(
    tmp_path: Path,
    clock: Clock,
    name: str,
    local: Any,
    remote: Any,
    disk: Any,
    store: Any,
    sent: list[tuple[Any, ...]],
) -> None:
    path, server, stores = await _downloaded(tmp_path, {"f.md": "v1"})

    if local is _MISSING:
        (path / "f.md").unlink()
    elif local is not None:
        (path / "f.md").write_text(local)

    if remote is _MISSING:
        server.delete("f.md")
    elif remote is not None:
        server.write("f.md", remote)

    # Two passes: a local deletion is only sent after its corroboration window.
    await run_sync(stores)
    clock.now = memories_mod.DELETE_CORROBORATION_SECONDS + 1
    await run_sync(stores)

    if disk is _MISSING:
        assert not (path / "f.md").exists(), name
    else:
        assert (path / "f.md").read_text() == disk, name

    if store is _MISSING:
        assert "f.md" not in server.files, name
    else:
        assert server.files["f.md"] == store, name

    expected = [
        created("f.md", v)
        if kind == "create"
        else updated("f.md", v, was=was)
        if kind == "update"
        else deleted("f.md", was=was)
        for kind, v, was in sent
    ]
    assert server.received == expected, name

    # Settled: a second pass sends nothing more and changes nothing.
    await run_sync(stores)
    assert server.received == expected, name


# ---- the failure column ----------------------------------------------------
#
# Same matrix, one operation broken. A failed operation must leave disk and
# server in a state the next sync can still reconcile — never one where the
# retry does the opposite of what was asked.


@pytest.mark.asyncio()
async def test_a_failed_upload_keeps_the_local_edit_and_retries(tmp_path: Path) -> None:
    local, server, stores = await _downloaded(tmp_path, {"f.md": "v1"})
    (local / "f.md").write_text("v2 from agent")

    async def boom(*_a: Any, **_k: Any) -> Any:
        raise RuntimeError("upload exploded")

    original = stores._client.beta.memory_stores.memories.update  # pyright: ignore[reportPrivateUsage]
    stores._client.beta.memory_stores.memories.update = boom  # pyright: ignore[reportPrivateUsage]
    await run_sync(stores)

    # The agent's edit survives; the server is untouched.
    assert (local / "f.md").read_text() == "v2 from agent"
    assert server.files["f.md"] == "v1"

    # The baseline still says v1, so the next (working) sync retries the push.
    stores._client.beta.memory_stores.memories.update = original  # pyright: ignore[reportPrivateUsage]
    await run_sync(stores)
    assert server.files["f.md"] == "v2 from agent"


@pytest.mark.asyncio()
async def test_a_failed_pull_leaves_the_old_file_and_retries(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    from anthropic.lib.tools import _file_store

    local, server, stores = await _downloaded(tmp_path, {"f.md": "v1"})
    server.write("f.md", "v2 from server")

    async def flaky_put(_self: _file_store.LocalFileStore, _rel: str, _content: str) -> None:
        raise OSError(5, "I/O error")

    monkeypatch.setattr(_file_store.LocalFileStore, "put", flaky_put)
    await run_sync(stores)
    monkeypatch.undo()

    # The stale file is still there and the baseline never advanced...
    assert (local / "f.md").read_text() == "v1"
    assert server.received == []

    # ...so the next sync pulls it, rather than mistaking v1 for a local edit
    # and pushing it back over the server's v2.
    await run_sync(stores)
    assert (local / "f.md").read_text() == "v2 from server"
    assert server.received == []


@pytest.mark.asyncio()
async def test_a_failed_local_removal_never_re_uploads_the_deleted_memory(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, caplog: pytest.LogCaptureFixture
) -> None:
    """The server deleted the memory; removing our copy fails. The baseline must
    stay put — dropping it would read the leftover file as a new local file and
    create the memory the server just deleted."""
    caplog.set_level("WARNING", logger=LOGGER)
    from anthropic.lib.tools import _file_store

    local, server, stores = await _downloaded(tmp_path, {"f.md": "v1"})
    server.delete("f.md")

    async def flaky_remove(_self: _file_store.LocalFileStore, _rel: str) -> None:
        raise OSError(5, "I/O error")

    monkeypatch.setattr(_file_store.LocalFileStore, "remove", flaky_remove)
    await run_sync(stores)
    monkeypatch.undo()

    assert (local / "f.md").read_text() == "v1"
    assert server.received == []
    assert "f.md" not in server.files
    assert "failed to remove memory deleted remotely" in caplog.text

    # The retry deletes it locally; it is never pushed back.
    await run_sync(stores)
    assert not (local / "f.md").exists()
    assert server.received == []
    assert "f.md" not in server.files


@pytest.mark.asyncio()
async def test_a_store_that_landed_is_disposed_when_a_later_one_fails(tmp_path: Path) -> None:
    """download() raises on the first store it cannot materialise, but the ones
    that already landed are tracked — so the caller's dispose still reaps their
    directories rather than leaking them."""
    client, _ = fake_anthropic({"note.md": "v1"}, broken_store_last=True)
    stores = SessionMemoryStores(client, workdir=tmp_path)

    with pytest.raises(SessionMemoryError, match="memstore_broken"):
        await stores.download(await client.beta.sessions.retrieve("s1"))

    notes = tmp_path / "memory" / "notes"
    assert notes.exists(), "the healthy store landed before the broken one failed"

    await stores.dispose()
    assert not notes.exists()
    # The broken store's own half-download self-destructed at the failure.
    assert not (tmp_path / "memory" / "broken").exists()


@pytest.mark.asyncio()
async def test_stores_sync_in_parallel_and_one_failure_spares_the_rest(
    tmp_path: Path, caplog: pytest.LogCaptureFixture
) -> None:
    """Stores sync concurrently, and one store's failure never blocks another.

    The slow store's listing waits for the fast store's listing to start —
    only a parallel sync satisfies that — then explodes. A serial sync would
    time the wait out instead (a different error message), and the fast
    store's edit must land either way.
    """
    caplog.set_level("WARNING", logger=LOGGER)
    import anyio

    from ._fake_anthropic import _Resource

    slow = MemoryServer({"a.md": "v1"})
    fast = MemoryServer({"b.md": "v1"})
    resources = {"memstore_slow": _Resource(slow), "memstore_fast": _Resource(fast)}
    fast_list_started = anyio.Event()
    syncing = False

    class _Router:
        def list(self, memory_store_id: str, **kwargs: Any) -> Any:
            async def _iter() -> Any:
                if syncing:
                    if memory_store_id == "memstore_fast":
                        fast_list_started.set()
                    else:
                        # Hangs forever under a serial sync (fast hasn't run yet).
                        with anyio.fail_after(10):
                            await fast_list_started.wait()
                        raise RuntimeError("slow store exploded")
                async for item in resources[memory_store_id].list(memory_store_id, **kwargs):
                    yield item

            return _iter()

        async def retrieve(self, memory_id: str, *, memory_store_id: str, **kwargs: Any) -> Any:
            return await resources[memory_store_id].retrieve(memory_id, memory_store_id=memory_store_id, **kwargs)

        async def create(self, memory_store_id: str, **kwargs: Any) -> Any:
            return await resources[memory_store_id].create(memory_store_id, **kwargs)

        async def update(self, memory_id: str, *, memory_store_id: str, **kwargs: Any) -> Any:
            return await resources[memory_store_id].update(memory_id, memory_store_id=memory_store_id, **kwargs)

        async def delete(self, memory_id: str, *, memory_store_id: str, **kwargs: Any) -> Any:
            return await resources[memory_store_id].delete(memory_id, memory_store_id=memory_store_id, **kwargs)

    from types import SimpleNamespace

    session = SimpleNamespace(
        resources=[
            SimpleNamespace(type="memory_store", memory_store_id=ms, mount_path=None, name=name, access=None)
            for ms, name in [("memstore_slow", "slow"), ("memstore_fast", "fast")]
        ]
    )
    client = SimpleNamespace(beta=SimpleNamespace(memory_stores=SimpleNamespace(memories=_Router())))
    stores = SessionMemoryStores(client, workdir=tmp_path)  # type: ignore[arg-type]
    await stores.download(session)  # type: ignore[arg-type]

    syncing = True
    (tmp_path / "memory" / "fast" / "b.md").write_text("v2 from agent")
    await run_sync(stores)

    # The slow store failed *after* seeing the fast store's listing start —
    # proof the two ran concurrently — and the fast store still pushed.
    assert "slow store exploded" in caplog.text
    assert fast.received == [updated("b.md", "v2 from agent", was="v1")]
    # The failed store's baseline was kept, so nothing is re-uploaded once it heals.
    assert (tmp_path / "memory" / "slow" / "a.md").read_text() == "v1"


def test_sync_intervals_below_the_floor_are_rejected(tmp_path: Path) -> None:
    client, _server = fake_anthropic({})
    # NaN fails every comparison, so a validator phrased as ``< floor`` would
    # accept it — and a NaN interval makes every cadence check due.
    for interval in (4.9, 1.0, 0, -1.0, float("nan")):
        with pytest.raises(ValueError, match="at least"):
            SessionMemoryStores(client, workdir=tmp_path, sync_interval=interval)
    # The floor itself and "never due" are fine.
    SessionMemoryStores(client, workdir=tmp_path, sync_interval=5.0)
    SessionMemoryStores(client, workdir=tmp_path, sync_interval=float("inf"))
