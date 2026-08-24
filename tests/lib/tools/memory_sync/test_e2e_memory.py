"""Memory-store sync driven end to end through the real ``EnvironmentWorker``.

Real: the worker, ``SessionMemoryStores``, ``FileStore``,
and the filesystem. Faked: the network (an in-memory ``MemoryServer`` plus
stub heartbeat/stop), the session tool-call stream, and the clock. So the
chain worker → gate on the sessions token → download → ``sync_if_due`` per
tool call → ``finish`` → ``dispose`` runs for real against a fake
server; assertions read the server and the disk.
"""

from __future__ import annotations

import json
import time
import base64
import asyncio
import contextlib
from types import SimpleNamespace
from typing import Any
from pathlib import Path
from collections.abc import Callable, AsyncIterator

import pytest

import anthropic.lib.tools._memories as memories_mod
import anthropic.lib.environments._worker as worker_mod
from anthropic.lib.tools._memories import MemoryDeleteMode
from anthropic.lib.environments._worker import EnvironmentWorker

from ._fake_anthropic import MemoryServer, created, updated, fake_anthropic


def _causes(exc: BaseException) -> list[BaseException]:
    """Flatten an exception and any ExceptionGroup members it wraps."""
    inner = getattr(exc, "exceptions", None)
    if inner is None:
        return [exc]
    return [exc, *(c for e in inner for c in _causes(e))]


def fake_session(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    *,
    token: str | None,
    tool_calls: int,
    interval: float | None = 300.0,
    on_call: Callable[[int], None] | None = None,
    then_raise: Exception | None = None,
    clock: Callable[[], float] | None = None,
    no_stores: bool = False,
    sync_deletions: MemoryDeleteMode = "enabled",
    tools: Callable[[Any], list[Any]] | None = None,
) -> tuple[EnvironmentWorker, MemoryServer, Path]:
    """An ``EnvironmentWorker`` pointed at a fake client; one work item queued."""

    class _FakeWork:
        """Stub of ``client.beta.environments.work`` — heartbeat and stop are no-ops."""

        async def heartbeat(self, *_a: Any, **_kw: Any) -> Any:
            return SimpleNamespace(last_heartbeat="hb", ttl_seconds=60, state="running", lease_extended=True)

        async def stop(self, *_a: Any, **_kw: Any) -> None:
            pass

    # One fake client serves every role: sessions.retrieve (for skills +
    # memory download), memory_stores.memories (the MemoryServer), and
    # environments.work (heartbeat + stop). The worker's
    # _copy_client_with_bearer_auth call returns it, and the memory stores
    # ride that same sub-client.
    memory_client, server = fake_anthropic({"note.md": "v1"}, no_stores=no_stores)
    client: Any = SimpleNamespace(
        beta=SimpleNamespace(
            sessions=memory_client.beta.sessions,
            memory_stores=memory_client.beta.memory_stores,
            environments=SimpleNamespace(work=_FakeWork()),
        )
    )

    def _scoped(_client: Any, *, auth_token: str, helper: str) -> Any:  # noqa: ARG001
        return client

    monkeypatch.setattr(worker_mod, "_copy_client_with_bearer_auth", _scoped)

    if clock is not None:
        monkeypatch.setattr(memories_mod, "monotonic", clock)

    # Encode the token the way the poll response carries it: base64url JSON.
    secret = (
        None if token is None else base64.urlsafe_b64encode(json.dumps({"sessions_token": token}).encode()).decode()
    )
    work_item = SimpleNamespace(
        id="w1", environment_id="e1", secret=secret, data=SimpleNamespace(type="session", id="s1")
    )

    async def _aiter_work(*_a: Any, **_kw: Any) -> AsyncIterator[Any]:
        yield work_item

    monkeypatch.setattr(worker_mod, "aiter_work", _aiter_work)

    @contextlib.asynccontextmanager
    async def _run_session_tools(*_a: Any, **_kw: Any) -> AsyncIterator[AsyncIterator[int]]:
        async def _calls() -> AsyncIterator[int]:
            for i in range(tool_calls):
                if on_call is not None:
                    on_call(i)
                yield i
            if then_raise is not None:
                raise then_raise

        yield _calls()

    monkeypatch.setattr(worker_mod, "_run_session_tools", _run_session_tools)

    worker = EnvironmentWorker(
        client,
        environment_id="e1",
        environment_key="ek",
        workdir=tmp_path,
        memory_sync_interval=interval,
        memory_sync_deletions=sync_deletions,
        tools=tools if tools is not None else lambda _env: [],
    )
    return worker, server, tmp_path / "memory" / "notes"


async def _run_timed(worker: EnvironmentWorker) -> float:
    """Run the worker to completion and return the wall-clock seconds it took."""
    start = time.monotonic()
    await asyncio.wait_for(worker.run(), timeout=10)
    return time.monotonic() - start


@pytest.mark.asyncio()
async def test_worker_syncs_on_cadence_finishes_and_disposes(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    now = 0.0

    def on_call(i: int) -> None:
        nonlocal now
        # The agent edits its note, then a long gap passes before the
        # worker's sync_if_due poll — so every poll is due.
        (local / "note.md").write_text(f"edit {i}")
        now += 400.0

    worker, server, local = fake_session(
        monkeypatch, tmp_path, token="tok", tool_calls=3, on_call=on_call, clock=lambda: now
    )

    await asyncio.wait_for(worker.run(), timeout=10)

    # One session fetch, shared by the skills and memory downloads.
    assert server.retrieves == ["s1"]
    # Download happened (the file landed on disk before any edit); three
    # cadence syncs pushed edits 0/1/2; the final sync had nothing new.
    assert server.received == [
        updated("note.md", "edit 0", was="v1"),
        updated("note.md", "edit 1", was="edit 0"),
        updated("note.md", "edit 2", was="edit 1"),
    ]
    # Dispose removed the store dir the download created.
    assert not local.exists()


@pytest.mark.asyncio()
async def test_worker_fails_the_item_when_the_sessions_token_is_missing(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, caplog: pytest.LogCaptureFixture
) -> None:
    """The session has memory stores attached but the work item carried no
    sessions token, so its memories cannot be mounted. The ITEM fails before a
    single tool call is served — running the session anyway would give it
    amnesia, where hosted sandboxes fail the start. The worker keeps polling."""
    caplog.set_level("ERROR", logger="anthropic.lib.environments._worker")
    calls: list[int] = []
    worker, server, local = fake_session(monkeypatch, tmp_path, token=None, tool_calls=2, on_call=calls.append)

    # run() completes: the item failed, the poll loop did not.
    await asyncio.wait_for(worker.run(), timeout=10)

    assert "work item failed" in caplog.text
    assert "carried no sessions token" in caplog.text
    # The session never served a tool call, and memory was never touched.
    assert calls == []
    assert server.received == []
    assert not local.exists()


@pytest.mark.asyncio()
async def test_worker_skips_memory_when_the_interval_is_none(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, caplog: pytest.LogCaptureFixture
) -> None:
    caplog.set_level("ERROR", logger="anthropic.lib.environments._worker")
    worker, server, local = fake_session(monkeypatch, tmp_path, token="tok", tool_calls=2, interval=None)

    await asyncio.wait_for(worker.run(), timeout=10)

    # Even with a sessions token, interval=None turns memory off entirely.
    assert server.received == []
    assert not local.exists()
    # Turning memory off is a deliberate choice, so it says nothing loud.
    assert caplog.text == ""


def test_worker_rejects_a_sub_floor_interval(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    for interval in (4.9, 0, float("nan")):
        with pytest.raises(ValueError, match="at least"):
            fake_session(monkeypatch, tmp_path, token="tok", tool_calls=0, interval=interval)


@pytest.mark.asyncio()
async def test_worker_fails_the_item_when_a_memory_store_cannot_be_downloaded(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, caplog: pytest.LogCaptureFixture
) -> None:
    """A folder already at the store's path is debris from a run that died. The
    download refuses it and the ITEM fails — rather than serving a session whose
    system prompt names a memory folder holding someone else's files. The worker
    itself keeps polling; a killed worker's leftovers must not crashloop it."""
    caplog.set_level("ERROR", logger="anthropic.lib.environments._worker")
    debris = tmp_path / "memory" / "notes"
    debris.mkdir(parents=True)
    (debris / "left-behind.md").write_text("from a dead run")

    worker, server, _local = fake_session(monkeypatch, tmp_path, token="tok", tool_calls=2)

    # run() completes: the item failed, the poll loop did not.
    await asyncio.wait_for(worker.run(), timeout=10)

    assert "work item failed" in caplog.text
    assert "already exists" in caplog.text
    # Nothing was pushed, and the debris is exactly as it was found.
    assert server.received == []
    assert (debris / "left-behind.md").read_text() == "from a dead run"
    assert not (debris / "note.md").exists()


@pytest.mark.asyncio()
async def test_worker_flushes_writes_when_the_stream_raises(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, caplog: pytest.LogCaptureFixture
) -> None:
    caplog.set_level("ERROR", logger="anthropic.lib.environments._worker")
    now = 0.0

    def on_call(i: int) -> None:
        nonlocal now
        (local / "note.md").write_text(f"edit {i}")
        if i == 0:
            # Only the first edit gets a cadence sync; the second is still
            # on disk when the stream breaks.
            now += 400.0

    worker, server, local = fake_session(
        monkeypatch,
        tmp_path,
        token="tok",
        tool_calls=2,
        on_call=on_call,
        then_raise=RuntimeError("stream broke"),
        clock=lambda: now,
    )

    # The item fails; the poll loop does not. anyio wraps the RuntimeError in
    # an ExceptionGroup whose own message says nothing, so the worker flattens
    # it — the log names the real cause.
    await asyncio.wait_for(worker.run(), timeout=10)
    assert "work item failed" in caplog.text
    assert "stream broke" in caplog.text

    # The raise skipped the final sync, but the shutdown flush pushed the
    # pending edit before dispose removed the folder.
    assert server.received == [
        updated("note.md", "edit 0", was="v1"),
        updated("note.md", "edit 1", was="edit 0"),
    ]
    # Dispose still ran (shielded teardown).
    assert not local.exists()


@pytest.mark.asyncio()
async def test_worker_clean_end_syncs_once_and_the_flush_adds_nothing(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, caplog: pytest.LogCaptureFixture
) -> None:
    caplog.set_level("WARNING", logger="anthropic.lib.tools.agent_toolset")
    caplog.set_level("WARNING", logger="anthropic.lib.environments._worker")
    now = 0.0

    def on_call(i: int) -> None:
        nonlocal now
        (local / "note.md").write_text(f"edit {i}")
        if i == 0:
            now += 400.0

    worker, server, local = fake_session(
        monkeypatch, tmp_path, token="tok", tool_calls=2, on_call=on_call, clock=lambda: now
    )

    await asyncio.wait_for(worker.run(), timeout=10)

    # The cadence sync pushed edit 0 and the clean-end final sync pushed
    # edit 1 — exactly once each. The teardown flush runs after them but
    # finds nothing dirty, so nothing more is sent.
    assert server.received == [
        updated("note.md", "edit 0", was="v1"),
        updated("note.md", "edit 1", was="edit 0"),
    ]
    # Neither teardown pass hit its time bound, so nothing says "cut off".
    assert "cut off" not in caplog.text
    assert not local.exists()


@pytest.mark.asyncio()
async def test_worker_flushes_after_a_clean_final_sync_that_failed(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """sync() swallows its own failures, so a clean stream end whose final
    sync broke would silently lose the last edits — the teardown flush is
    their second chance."""

    async def finish_that_breaks(_self: memories_mod.SessionMemoryStores) -> None:
        return  # a store-level failure inside the last sync: logged, nothing pushed

    monkeypatch.setattr(memories_mod.SessionMemoryStores, "finish", finish_that_breaks)

    def on_call(_i: int) -> None:
        (local / "note.md").write_text("last edit")

    worker, server, local = fake_session(monkeypatch, tmp_path, token="tok", tool_calls=1, on_call=on_call)

    await asyncio.wait_for(worker.run(), timeout=10)

    assert server.files["note.md"] == "last edit"
    assert not local.exists()


@pytest.mark.asyncio()
async def test_worker_flush_is_bounded_and_teardown_still_runs(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, caplog: pytest.LogCaptureFixture
) -> None:
    """A flush that hangs is cut off at MEMORY_FLUSH_TIMEOUT and says so; dispose still runs."""
    caplog.set_level("WARNING", logger="anthropic.lib.environments._worker")
    monkeypatch.setattr(worker_mod, "MEMORY_FLUSH_TIMEOUT", 0.05)
    flush_started = asyncio.Event()

    async def hanging_flush(_self: memories_mod.SessionMemoryStores) -> None:
        flush_started.set()
        await asyncio.sleep(5)

    monkeypatch.setattr(memories_mod.SessionMemoryStores, "flush_writes", hanging_flush)

    def on_call(i: int) -> None:
        (local / "note.md").write_text(f"edit {i}")

    worker, _server, local = fake_session(
        monkeypatch,
        tmp_path,
        token="tok",
        tool_calls=1,
        on_call=on_call,
        then_raise=RuntimeError("stream broke"),
    )

    elapsed = await _run_timed(worker)

    assert flush_started.is_set()
    # Without the timeout the hung flush would hold teardown the full 5s.
    assert elapsed < 2.0
    assert "memory flush cut off after" in caplog.text
    assert not local.exists()


@pytest.mark.asyncio()
async def test_worker_final_sync_is_bounded_and_the_flush_still_runs(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, caplog: pytest.LogCaptureFixture
) -> None:
    """A final sync that hangs is cut off at MEMORY_FLUSH_TIMEOUT and says so;
    the flush after it still uploads the last edit."""
    caplog.set_level("WARNING", logger="anthropic.lib.environments._worker")
    # The same bound covers the real flush that follows, which must finish
    # inside it even on a loaded CI machine.
    monkeypatch.setattr(worker_mod, "MEMORY_FLUSH_TIMEOUT", 0.5)

    async def hanging_finish(_self: memories_mod.SessionMemoryStores) -> None:
        await asyncio.sleep(5)

    monkeypatch.setattr(memories_mod.SessionMemoryStores, "finish", hanging_finish)

    def on_call(_i: int) -> None:
        (local / "note.md").write_text("last edit")

    worker, server, local = fake_session(monkeypatch, tmp_path, token="tok", tool_calls=1, on_call=on_call)

    elapsed = await _run_timed(worker)

    assert elapsed < 2.0
    assert "final memory sync cut off after" in caplog.text
    # The flush finished in time, so only the final sync reports a cut-off.
    assert "memory flush cut off after" not in caplog.text
    assert server.files["note.md"] == "last edit"
    assert not local.exists()


@pytest.mark.asyncio()
async def test_worker_logs_what_a_cut_off_flush_left_behind(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, caplog: pytest.LogCaptureFixture
) -> None:
    """One upload never completes: the flush is cut off, the store logs that
    one of its two changed files did not make it, and the other one did."""
    caplog.set_level("WARNING", logger="anthropic.lib.tools.agent_toolset")
    caplog.set_level("WARNING", logger="anthropic.lib.environments._worker")
    monkeypatch.setattr(worker_mod, "MEMORY_FLUSH_TIMEOUT", 0.5)

    def on_call(_i: int) -> None:
        (local / "kept.md").write_text("saved")
        (local / "stuck.md").write_text("only copy")

    worker, server, local = fake_session(
        monkeypatch,
        tmp_path,
        token="tok",
        tool_calls=1,
        on_call=on_call,
        then_raise=RuntimeError("stream broke"),
    )
    never = asyncio.Event()

    async def hook(path: str) -> None:
        if path == "stuck.md":
            await asyncio.wait_for(never.wait(), timeout=5)

    server.upload_hook = hook

    elapsed = await _run_timed(worker)

    assert elapsed < 3.0
    assert server.files["kept.md"] == "saved"
    assert "stuck.md" not in server.files
    assert "1 of 2 changed files had not finished uploading memory_store_id=memstore_notes" in caplog.text
    assert "memory flush cut off after" in caplog.text
    assert not local.exists()


@pytest.mark.asyncio()
async def test_worker_stays_quiet_when_no_memory_store_is_attached(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, caplog: pytest.LogCaptureFixture
) -> None:
    """Most sessions have no memory at all. Missing a sessions token is only
    worth shouting about when there is memory the session cannot reach."""
    caplog.set_level("ERROR", logger="anthropic.lib.environments._worker")
    worker, server, local = fake_session(monkeypatch, tmp_path, token=None, tool_calls=2, no_stores=True)

    await asyncio.wait_for(worker.run(), timeout=10)

    assert server.received == []
    assert not local.exists()
    assert caplog.text == ""


@pytest.mark.asyncio()
async def test_worker_can_turn_sync_deletions_off(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """``memory_sync_deletions="disabled"`` reaches the stores: a local deletion
    never propagates however many syncs run, while uploads still do."""
    now = 0.0

    def on_call(i: int) -> None:
        nonlocal now
        if i == 0:
            (local / "note.md").unlink()
            (local / "new.md").write_text("survives")
        # Every gap dwarfs both the sync interval and the corroboration window.
        now += 400.0

    worker, server, local = fake_session(
        monkeypatch,
        tmp_path,
        token="tok",
        tool_calls=3,
        on_call=on_call,
        clock=lambda: now,
        sync_deletions="disabled",
    )

    await asyncio.wait_for(worker.run(), timeout=10)

    assert server.files["note.md"] == "v1"
    assert server.received == [created("new.md", "survives")]


@pytest.mark.asyncio()
async def test_worker_flushes_and_disposes_even_when_env_teardown_raises(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """A raising env.__aexit__ must not skip the flush or leave the folder
    behind for the next work item to trip over."""
    from anthropic.lib.tools import agent_toolset

    real_aexit = agent_toolset.AgentToolContext.__aexit__

    async def broken_aexit(self: agent_toolset.AgentToolContext, *exc: Any) -> None:
        await real_aexit(self, *exc)
        raise OSError("teardown burp")

    monkeypatch.setattr(agent_toolset.AgentToolContext, "__aexit__", broken_aexit)

    def on_call(_i: int) -> None:
        (local / "note.md").write_text("edit before burp")

    worker, server, local = fake_session(
        monkeypatch, tmp_path, token="tok", tool_calls=1, on_call=on_call, then_raise=RuntimeError("stream died")
    )

    await asyncio.wait_for(worker.run(), timeout=10)

    assert server.files["note.md"] == "edit before burp"
    assert not local.exists()


@pytest.mark.asyncio()
async def test_the_last_sync_runs_after_the_bash_subprocesses_are_killed(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """finish() skips the delete waiting window, so it must only run once
    nothing can still be rewriting files — after env teardown kills the
    session's subprocesses."""
    from anthropic.lib.tools import agent_toolset

    order: list[str] = []
    real_aexit = agent_toolset.AgentToolContext.__aexit__
    real_finish = memories_mod.SessionMemoryStores.finish

    async def recording_aexit(self: agent_toolset.AgentToolContext, *exc: Any) -> None:
        order.append("env_teardown")
        await real_aexit(self, *exc)

    async def recording_finish(self: memories_mod.SessionMemoryStores) -> None:
        order.append("finish")
        await real_finish(self)

    monkeypatch.setattr(agent_toolset.AgentToolContext, "__aexit__", recording_aexit)
    monkeypatch.setattr(memories_mod.SessionMemoryStores, "finish", recording_finish)

    def on_call(_i: int) -> None:
        (local / "note.md").write_text("last edit")

    worker, server, local = fake_session(monkeypatch, tmp_path, token="tok", tool_calls=1, on_call=on_call)

    await asyncio.wait_for(worker.run(), timeout=10)

    assert order == ["env_teardown", "finish"]
    assert server.files["note.md"] == "last edit"
    assert not local.exists()


@pytest.mark.asyncio()
async def test_the_lease_is_heartbeated_until_the_memory_teardown_is_done(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """The lease must not lapse while the final sync, flush and dispose still hold the folder."""
    order: list[str] = []
    real_heartbeat_loop = worker_mod._heartbeat_loop
    real_dispose = memories_mod.SessionMemoryStores.dispose

    async def recording_heartbeat_loop(*args: Any, **kwargs: Any) -> None:
        try:
            await real_heartbeat_loop(*args, **kwargs)
        finally:
            order.append("heartbeat stopped")

    async def recording_dispose(self: memories_mod.SessionMemoryStores) -> None:
        await real_dispose(self)
        order.append("folder removed")

    monkeypatch.setattr(worker_mod, "_heartbeat_loop", recording_heartbeat_loop)
    monkeypatch.setattr(memories_mod.SessionMemoryStores, "dispose", recording_dispose)

    worker, _server, _local = fake_session(monkeypatch, tmp_path, token="tok", tool_calls=1)

    await asyncio.wait_for(worker.run(), timeout=10)

    assert order == ["folder removed", "heartbeat stopped"]


@pytest.mark.asyncio()
async def test_worker_grants_file_tools_access_to_store_folders(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """The tool context handed to the tools factory carries the downloaded
    store folders as allowed roots, so the file tools can reach a memory
    mounted outside the working directory."""
    contexts: list[Any] = []

    def capture(env: Any) -> list[Any]:
        contexts.append(env)
        return []

    worker, _server, local = fake_session(monkeypatch, tmp_path, token="tok", tool_calls=1, tools=capture)

    await asyncio.wait_for(worker.run(), timeout=10)

    (env,) = contexts
    assert env.allowed_roots == [local.resolve()]
    assert env.read_only_roots == []
