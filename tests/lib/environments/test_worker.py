"""Tests for :class:`EnvironmentWorker`.

The worker composes the control-plane poller, the per-session
``AgentToolContext`` / skill download, the lease heartbeat, and the session tool
runner. We stub ``aiter_work``, the session tool runner, and the worker's
``_copy_client_with_bearer_auth`` helper so each test can drive a single
claimed work item and assert the surrounding plumbing (skip non-session work,
heartbeat the lease, force-stop on exit) — via both the ``run()`` poll loop
and the single-item ``handle_item()`` entry point.

After the auth refactor, heartbeat / force-stop traffic flows through a
Bearer-only sub-client the worker constructs via the shared
``_copy_client_with_bearer_auth`` util. The tests intercept that helper so they
can route those calls to a recording fake without spinning up a real
``AsyncAnthropic`` (and the httpx pool that comes with it).
"""

from __future__ import annotations

import os
import asyncio
import contextlib
from types import SimpleNamespace
from typing import Any
from collections.abc import AsyncIterator
from typing_extensions import override

import pytest

from anthropic import Anthropic, AsyncAnthropic
from anthropic._compat import PYDANTIC_V1
from anthropic.lib.environments import _worker as worker_mod
from anthropic.lib.environments._worker import EnvironmentWorker


class _FakeWorkResource:
    def __init__(self, *, heartbeat_state: str = "stopping") -> None:
        self._heartbeat_state = heartbeat_state
        self.heartbeat_calls: list[dict[str, Any]] = []
        self.stop_calls: list[dict[str, Any]] = []

    async def heartbeat(
        self,
        work_id: str,
        *,
        environment_id: str,
        expected_last_heartbeat: str,  # noqa: ARG002
        extra_headers: Any = None,
    ) -> Any:
        self.heartbeat_calls.append(
            {"work_id": work_id, "environment_id": environment_id, "extra_headers": extra_headers}
        )
        return SimpleNamespace(last_heartbeat="hb-1", ttl_seconds=60, state=self._heartbeat_state, lease_extended=True)

    async def stop(
        self,
        work_id: str,
        *,
        environment_id: str,
        force: bool = False,
        extra_headers: Any = None,
        betas: Any = None,
    ) -> None:
        self.stop_calls.append(
            {
                "work_id": work_id,
                "environment_id": environment_id,
                "force": force,
                "extra_headers": extra_headers,
                "betas": betas,
            }
        )


class _FakeSessions:
    def __init__(self) -> None:
        self.retrieve_calls: list[str] = []

    async def retrieve(self, session_id: str, *, betas: Any = None) -> Any:  # noqa: ARG002
        self.retrieve_calls.append(session_id)
        return SimpleNamespace(agent=SimpleNamespace(skills=[]))


def _fake_client(work: _FakeWorkResource, sessions: _FakeSessions) -> Any:
    return SimpleNamespace(
        beta=SimpleNamespace(sessions=sessions, environments=SimpleNamespace(work=work)),
    )


def _install_scoped_client(
    monkeypatch: pytest.MonkeyPatch, work: _FakeWorkResource, sessions: _FakeSessions | None = None
) -> list[dict[str, Any]]:
    """Intercept the shared bearer-auth client factory.

    Returns the list of args the factory was called with so a test can assert
    on the helper-telemetry tag (one entry per call: poll, worker, …).
    """
    calls: list[dict[str, Any]] = []
    if sessions is None:
        sessions = _FakeSessions()
    fake_scoped = SimpleNamespace(
        beta=SimpleNamespace(sessions=sessions, environments=SimpleNamespace(work=work))
    )

    def fake_factory(client: Any, *, auth_token: str, helper: str) -> Any:  # noqa: ARG001
        calls.append({"auth_token": auth_token, "helper": helper})
        return fake_scoped

    monkeypatch.setattr(worker_mod, "_copy_client_with_bearer_auth", fake_factory)
    return calls


def _work_item(*, work_type: str = "session", work_id: str = "w_1", session_id: str = "s_1") -> Any:
    return SimpleNamespace(id=work_id, environment_id="e_1", data=SimpleNamespace(type=work_type, id=session_id))


def _install_aiter_work(monkeypatch: pytest.MonkeyPatch, items: list[Any]) -> None:
    async def fake_aiter_work(_work: Any, **_kw: Any) -> AsyncIterator[Any]:
        for it in items:
            yield it

    monkeypatch.setattr(worker_mod, "aiter_work", fake_aiter_work)


def _install_run_session_tools(monkeypatch: pytest.MonkeyPatch, record: dict[str, Any]) -> None:
    @contextlib.asynccontextmanager
    async def fake_run_session_tools(
        _client: Any,
        session_id: str,
        *,
        tools: Any,
        max_idle: Any = None,
        environment_key: Any = None,
        extra_headers: Any = None,
    ):
        record["run"] = {
            "session_id": session_id,
            "tools": tools,
            "max_idle": max_idle,
            "environment_key": environment_key,
            "extra_headers": extra_headers,
        }

        async def _iter() -> AsyncIterator[Any]:
            # The session completes on its own (no tool calls). The run then
            # ends via the normal session-completion path; the heartbeat keeps
            # the lease alive throughout and is stopped on the way out.
            return
            yield  # pragma: no cover  (makes this an async generator function)

        yield _iter()

    monkeypatch.setattr(worker_mod, "_run_session_tools", fake_run_session_tools)


@pytest.mark.skipif(PYDANTIC_V1, reason="tool functions are only supported with pydantic v2")
@pytest.mark.asyncio()
async def test_environment_worker_serves_session(monkeypatch: pytest.MonkeyPatch) -> None:
    work = _FakeWorkResource(heartbeat_state="running")
    sessions = _FakeSessions()
    client = _fake_client(work, sessions)
    _install_aiter_work(monkeypatch, [_work_item()])
    scoped_calls = _install_scoped_client(monkeypatch, work, sessions)
    record: dict[str, Any] = {}
    _install_run_session_tools(monkeypatch, record)

    worker = EnvironmentWorker(
        client=client,
        environment_id="e_1",
        environment_key="env_key",
        workdir=".",
        max_idle=12.0,
    )
    await asyncio.wait_for(worker.run(), timeout=5)

    # AgentToolContext set up skills for the claimed session.
    assert sessions.retrieve_calls == ["s_1"]
    # The session tool runner ran with the right session + max_idle, the
    # environment key was threaded through, and the default toolset (a list of 6
    # tools) was bound.
    assert record["run"]["session_id"] == "s_1"
    assert record["run"]["max_idle"] == 12.0
    assert record["run"]["environment_key"] == "env_key"
    assert [t.name for t in record["run"]["tools"]] == ["bash", "read", "write", "edit", "glob", "grep"]
    # The lease was heartbeated.
    assert len(work.heartbeat_calls) >= 1
    # The work item was force-stopped on exit.
    assert len(work.stop_calls) == 1
    assert work.stop_calls[0]["work_id"] == "w_1"
    assert work.stop_calls[0]["force"] is True
    # Auth flows through scoped sub-clients tagged with the right helper.
    # ``run()`` builds an ``environments-work-poller``-tagged client for ``aiter_work``;
    # each handled item builds an ``environments-worker``-tagged client for the
    # heartbeat and force-stop. The environment key flows into both.
    assert scoped_calls == [
        {"auth_token": "env_key", "helper": "environments-work-poller"},
        {"auth_token": "env_key", "helper": "environments-worker"},
    ]


@pytest.mark.asyncio()
async def test_environment_worker_accepts_tools_factory(monkeypatch: pytest.MonkeyPatch) -> None:
    work = _FakeWorkResource(heartbeat_state="running")
    sessions = _FakeSessions()
    client = _fake_client(work, sessions)
    _install_aiter_work(monkeypatch, [_work_item()])
    _install_scoped_client(monkeypatch, work, sessions)
    record: dict[str, Any] = {}
    _install_run_session_tools(monkeypatch, record)

    sentinel = SimpleNamespace(name="custom")

    def factory(_env: Any) -> list[Any]:
        return [sentinel]

    worker = EnvironmentWorker(
        client=client,
        environment_id="e_1",
        environment_key="env_key",
        tools=factory,
    )
    await asyncio.wait_for(worker.run(), timeout=5)

    assert record["run"]["tools"] == [sentinel]


@pytest.mark.asyncio()
async def test_run_requires_environment_id_and_environment_key() -> None:
    work = _FakeWorkResource()
    sessions = _FakeSessions()
    client = _fake_client(work, sessions)

    worker = EnvironmentWorker(client, workdir=".")
    with pytest.raises(ValueError, match="environment_id and environment_key are required"):
        await worker.run()


@pytest.mark.skipif(PYDANTIC_V1, reason="tool functions are only supported with pydantic v2")
@pytest.mark.asyncio()
async def test_handle_item_services_a_single_claimed_item(monkeypatch: pytest.MonkeyPatch) -> None:
    work = _FakeWorkResource(heartbeat_state="running")
    sessions = _FakeSessions()
    client = _fake_client(work, sessions)
    scoped_calls = _install_scoped_client(monkeypatch, work, sessions)
    record: dict[str, Any] = {}
    _install_run_session_tools(monkeypatch, record)
    # handle_item should not poll for work at all.
    _install_aiter_work(monkeypatch, [])

    # No environment_id needed for the single-item flow.
    worker = EnvironmentWorker(client, workdir=".", max_idle=7.0)
    await asyncio.wait_for(
        worker.handle_item(work_id="w_1", environment_id="e_1", session_id="s_1", environment_key="env_key"),
        timeout=5,
    )

    assert sessions.retrieve_calls == ["s_1"]
    assert record["run"]["session_id"] == "s_1"
    assert record["run"]["max_idle"] == 7.0
    assert record["run"]["environment_key"] == "env_key"
    assert len(work.heartbeat_calls) >= 1
    # Auth lives on the scoped sub-client now, not in extra_headers — so the
    # heartbeat goes out with no per-call extras (None) unless the worker was
    # constructed with passthrough headers.
    assert work.heartbeat_calls[0] == {
        "work_id": "w_1",
        "environment_id": "e_1",
        "extra_headers": None,
    }
    assert len(work.stop_calls) == 1
    assert work.stop_calls[0]["work_id"] == "w_1"
    assert work.stop_calls[0]["force"] is True
    # ``handle_item`` doesn't poll, so only the heartbeat/force-stop scoped
    # client is built — tagged ``environments-worker``.
    assert scoped_calls == [{"auth_token": "env_key", "helper": "environments-worker"}]


@pytest.mark.skipif(PYDANTIC_V1, reason="tool functions are only supported with pydantic v2")
@pytest.mark.asyncio()
async def test_handle_item_falls_back_to_env_vars(monkeypatch: pytest.MonkeyPatch) -> None:
    work = _FakeWorkResource(heartbeat_state="running")
    sessions = _FakeSessions()
    client = _fake_client(work, sessions)
    scoped_calls = _install_scoped_client(monkeypatch, work, sessions)
    record: dict[str, Any] = {}
    _install_run_session_tools(monkeypatch, record)

    monkeypatch.setenv("ANTHROPIC_WORK_ID", "w_env")
    monkeypatch.setenv("ANTHROPIC_ENVIRONMENT_ID", "e_env")
    monkeypatch.setenv("ANTHROPIC_SESSION_ID", "s_env")
    monkeypatch.setenv("ANTHROPIC_ENVIRONMENT_KEY", "key_env")

    worker = EnvironmentWorker(client, workdir=".")
    await asyncio.wait_for(worker.handle_item(), timeout=5)

    assert sessions.retrieve_calls == ["s_env"]
    assert record["run"]["session_id"] == "s_env"
    assert record["run"]["environment_key"] == "key_env"
    assert work.heartbeat_calls[0] == {
        "work_id": "w_env",
        "environment_id": "e_env",
        "extra_headers": None,
    }
    assert work.stop_calls[0]["work_id"] == "w_env"
    assert scoped_calls == [{"auth_token": "key_env", "helper": "environments-worker"}]


@pytest.mark.skipif(PYDANTIC_V1, reason="tool functions are only supported with pydantic v2")
@pytest.mark.asyncio()
async def test_handle_item_uses_constructor_environment_key(monkeypatch: pytest.MonkeyPatch) -> None:
    """``environment_key`` resolves to the worker's own key when not passed and
    no env var is set."""
    work = _FakeWorkResource(heartbeat_state="running")
    sessions = _FakeSessions()
    client = _fake_client(work, sessions)
    scoped_calls = _install_scoped_client(monkeypatch, work, sessions)
    record: dict[str, Any] = {}
    _install_run_session_tools(monkeypatch, record)

    monkeypatch.delenv("ANTHROPIC_ENVIRONMENT_KEY", raising=False)

    worker = EnvironmentWorker(client, environment_key="ctor_key", workdir=".")
    await asyncio.wait_for(
        worker.handle_item(work_id="w_1", environment_id="e_1", session_id="s_1"),
        timeout=5,
    )

    assert record["run"]["environment_key"] == "ctor_key"
    assert scoped_calls == [{"auth_token": "ctor_key", "helper": "environments-worker"}]


@pytest.mark.asyncio()
async def test_handle_item_missing_required_raises(monkeypatch: pytest.MonkeyPatch) -> None:
    work = _FakeWorkResource()
    sessions = _FakeSessions()
    client = _fake_client(work, sessions)

    for var in ("ANTHROPIC_WORK_ID", "ANTHROPIC_ENVIRONMENT_ID", "ANTHROPIC_SESSION_ID", "ANTHROPIC_ENVIRONMENT_KEY"):
        monkeypatch.delenv(var, raising=False)

    worker = EnvironmentWorker(client, workdir=".")

    # Nothing supplied at all -> the first missing one (work_id) is named.
    with pytest.raises(ValueError, match=r"handle_item: work_id is required — pass it or set ANTHROPIC_WORK_ID"):
        await worker.handle_item()

    # environment_key still missing even though the others are supplied.
    with pytest.raises(
        ValueError, match=r"handle_item: environment_key is required — pass it or set ANTHROPIC_ENVIRONMENT_KEY"
    ):
        await worker.handle_item(work_id="w_1", environment_id="e_1", session_id="s_1")


@pytest.mark.skipif(PYDANTIC_V1, reason="tool functions are only supported with pydantic v2")
@pytest.mark.asyncio()
async def test_worker_threads_extra_headers_into_poll_heartbeat_stop_and_runner(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A worker-level ``extra_headers`` is threaded, unchanged, into every
    per-request call the worker drives: the poll loop (forwarded to
    ``aiter_work``), the lease heartbeat, the force-stop, and the session
    tool runner.

    The worker does no header munging — it passes the caller's mapping
    through to each call's ``extra_headers=``. Auth stays on the scoped
    sub-clients the worker builds (``env_key`` Bearer), independent of this
    passthrough.
    """
    work = _FakeWorkResource(heartbeat_state="running")
    sessions = _FakeSessions()
    client = _fake_client(work, sessions)
    scoped_calls = _install_scoped_client(monkeypatch, work, sessions)

    aiter_kwargs: dict[str, Any] = {}

    async def fake_aiter_work(_work: Any, **kw: Any) -> AsyncIterator[Any]:
        aiter_kwargs.update(kw)
        yield _work_item()

    monkeypatch.setattr(worker_mod, "aiter_work", fake_aiter_work)
    record: dict[str, Any] = {}
    _install_run_session_tools(monkeypatch, record)

    extras = {"x-trace-id": "abc123"}
    worker = EnvironmentWorker(
        client=client,
        environment_id="e_1",
        environment_key="env_key",
        workdir=".",
        extra_headers=extras,
    )
    await asyncio.wait_for(worker.run(), timeout=5)

    # The poll loop, heartbeat and force-stop each receive the caller's
    # passthrough mapping unchanged.
    assert aiter_kwargs["extra_headers"] == extras
    assert work.heartbeat_calls[0]["extra_headers"] == extras
    assert work.stop_calls[0]["extra_headers"] == extras
    # The session tool runner is handed the same passthrough mapping (and the
    # environment key, which it uses to build its own scoped sub-client).
    assert record["run"]["extra_headers"] == extras
    assert record["run"]["environment_key"] == "env_key"
    # Two scoped sub-clients are constructed per run() pass: one for the
    # poller, one for the worker (heartbeat / force-stop). Both use the same
    # environment key as their Bearer credential.
    assert scoped_calls == [
        {"auth_token": "env_key", "helper": "environments-work-poller"},
        {"auth_token": "env_key", "helper": "environments-worker"},
    ]


def test_work_resource_worker_builds_environment_worker() -> None:
    """``client.beta.environments.work.worker(...)`` builds an ``EnvironmentWorker``
    bound to the client, with the options threaded through (mirrors ``poller``)."""
    client = AsyncAnthropic(api_key="x")
    worker = client.beta.environments.work.worker(
        environment_id="e_1",
        environment_key="env_key",
        workdir="/workspace",
        unrestricted_paths=True,
        max_idle=12.0,
        worker_id="w-test",
        extra_headers={"x-trace-id": "abc123"},
    )
    assert isinstance(worker, EnvironmentWorker)
    assert worker._client is client
    assert worker._environment_id == "e_1"
    assert worker._environment_key == "env_key"
    assert worker._workdir == "/workspace"
    assert worker._unrestricted_paths is True
    assert worker._max_idle == 12.0
    assert worker._worker_id == "w-test"
    assert worker._extra_headers == {"x-trace-id": "abc123"}


def test_work_resource_worker_defaults() -> None:
    worker = AsyncAnthropic(api_key="x").beta.environments.work.worker()
    assert isinstance(worker, EnvironmentWorker)
    assert worker._environment_id is None
    assert worker._environment_key is None
    assert worker._tools is None
    # Default workdir is the cwd snapshotted at construction (not a lazily
    # resolved ".") — TS parity with process.cwd()-at-construction.
    assert worker._workdir == os.getcwd()
    assert worker._unrestricted_paths is False
    assert worker._max_idle == 60.0


def test_work_resource_worker_and_poller_async_only() -> None:
    """``worker()`` / ``poller()`` build an async-only ``EnvironmentWorker`` /
    ``aiter_work`` generator, so they live on ``AsyncWork`` and are NOT exposed
    on the sync ``Work`` resource (calling them from the sync client would hand
    back coroutines/async iterators that can't run without an event loop)."""
    async_work = AsyncAnthropic(api_key="x").beta.environments.work
    assert hasattr(async_work, "worker")
    assert hasattr(async_work, "poller")

    sync_work = Anthropic(api_key="x").beta.environments.work
    assert not hasattr(sync_work, "worker")
    assert not hasattr(sync_work, "poller")


@pytest.mark.skipif(PYDANTIC_V1, reason="tool functions are only supported with pydantic v2")
@pytest.mark.asyncio()
async def test_heartbeat_starts_before_skill_download(monkeypatch: pytest.MonkeyPatch) -> None:
    """Regression: the lease heartbeat must already be running while skills are
    downloaded.

    Skill setup (``AgentToolContext.__aenter__``) can take longer than the
    lease TTL. If the first heartbeat only fired *after* that download (the old
    ordering) the lease could lapse mid-download and another worker would
    reclaim the item — both then serve the same session (split-brain). We make
    skill setup block until a heartbeat has fired: with the correct ordering it
    proceeds; with the old ordering it would hang and time out.
    """
    import anthropic.lib.tools.agent_toolset as ats

    heartbeat_fired = asyncio.Event()
    order: list[str] = []

    class _HeartbeatFirstWork(_FakeWorkResource):
        @override
        async def heartbeat(
            self,
            work_id: str,  # noqa: ARG002
            *,
            environment_id: str,  # noqa: ARG002
            expected_last_heartbeat: str,  # noqa: ARG002
            extra_headers: Any = None,  # noqa: ARG002
        ) -> Any:
            order.append("heartbeat")
            heartbeat_fired.set()
            # state="running" so the heartbeat loop keeps going (does not stop
            # the run before skill setup / the session runner get to execute).
            return SimpleNamespace(last_heartbeat="hb-1", ttl_seconds=60, state="running", lease_extended=True)

    work = _HeartbeatFirstWork()
    sessions = _FakeSessions()
    client = _fake_client(work, sessions)
    _install_aiter_work(monkeypatch, [_work_item()])
    _install_scoped_client(monkeypatch, work, sessions)

    async def slow_setup_skills(_self: Any) -> None:
        order.append("setup_start")
        # If the heartbeat hasn't started yet (old bug) this hangs → timeout.
        await asyncio.wait_for(heartbeat_fired.wait(), timeout=5)
        order.append("setup_end")

    monkeypatch.setattr(ats.AgentToolContext, "setup_skills", slow_setup_skills)

    @contextlib.asynccontextmanager
    async def fake_run_session_tools(
        _client: Any,
        session_id: str,  # noqa: ARG001
        *,
        tools: Any,  # noqa: ARG001
        max_idle: Any = None,  # noqa: ARG001
        environment_key: Any = None,  # noqa: ARG001
        extra_headers: Any = None,  # noqa: ARG001
    ):
        async def _iter() -> AsyncIterator[Any]:
            return
            yield  # pragma: no cover  (makes this an async generator function)

        yield _iter()

    monkeypatch.setattr(worker_mod, "_run_session_tools", fake_run_session_tools)

    worker = EnvironmentWorker(client=client, environment_id="e_1", environment_key="env_key", workdir=".")
    await asyncio.wait_for(worker.run(), timeout=5)

    assert "heartbeat" in order
    assert "setup_end" in order
    # The heartbeat fired before skill setup was allowed to finish.
    assert order.index("heartbeat") < order.index("setup_end")
    # The work item was still force-stopped on exit.
    assert len(work.stop_calls) == 1
