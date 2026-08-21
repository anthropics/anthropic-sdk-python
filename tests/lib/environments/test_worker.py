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
import json
import base64
import asyncio
import logging
import threading
import contextlib
from types import SimpleNamespace
from typing import Any, Callable, cast
from functools import partial
from collections.abc import Awaitable, AsyncIterator
from typing_extensions import override

import anyio
import httpx2
import pytest

from anthropic import Anthropic, APIStatusError, AsyncAnthropic
from anthropic._compat import PYDANTIC_V1
from anthropic.lib.environments import _worker as worker_mod
from anthropic.lib.environments._worker import (
    EnvironmentWorker,
    _Lease,
    _heartbeat_loop,
    _LeaseEndReason,
    _sessions_token_from_secret,
)
from anthropic.lib.tools._tool_dispatch import run_runnable_tool

from ..tools.test_session_runner import _SyncTool


def _encode_secret(payload: dict[str, Any]) -> str:
    """Build a work-item ``secret`` the way the control plane does: URL-safe
    base64 of a JSON payload, without padding."""
    return base64.urlsafe_b64encode(json.dumps(payload).encode()).decode().rstrip("=")


def _api_status_error(code: int, body: object = None) -> APIStatusError:
    request = httpx2.Request("POST", "https://api.example/heartbeat")
    response = httpx2.Response(status_code=code, request=request, content=json.dumps(body).encode())
    return APIStatusError("boom", response=response, body=body)


def _lease_lost_error() -> APIStatusError:
    """The 412 the control plane answers a heartbeat with once the item's lease
    was cleared (re-queued) or is held by another worker."""
    return _api_status_error(
        412,
        {
            "type": "error",
            "error": {
                "type": "invalid_request_error",
                "message": "Heartbeat precondition failed: expected hb-1, actual was NULL",
                "details": {
                    "error_code": "heartbeat_precondition_failed",
                    "error_visibility": "user_facing",
                    "current_state": {
                        "state": "queued",
                        "last_heartbeat": None,
                        "lease_updated_at": None,
                        "lease_extended": False,
                        "ttl_seconds": 120,
                    },
                },
            },
        },
    )


class _FakeWorkResource:
    def __init__(self, *, heartbeat_state: str = "stopping", heartbeat_error: Exception | None = None) -> None:
        self._heartbeat_state = heartbeat_state
        self._heartbeat_error = heartbeat_error
        # When set, every heartbeat waits for this event before answering, so a
        # test decides *when* in the run the heartbeat's outcome lands.
        self.heartbeat_gate: asyncio.Event | None = None
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
        if self.heartbeat_gate is not None:
            await self.heartbeat_gate.wait()
        if self._heartbeat_error is not None:
            raise self._heartbeat_error
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
        return SimpleNamespace(agent=SimpleNamespace(skills=[]), resources=[])


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
    fake_scoped = SimpleNamespace(beta=SimpleNamespace(sessions=sessions, environments=SimpleNamespace(work=work)))

    def fake_factory(client: Any, *, auth_token: str, helper: str) -> Any:  # noqa: ARG001
        calls.append({"auth_token": auth_token, "helper": helper})
        return fake_scoped

    monkeypatch.setattr(worker_mod, "_copy_client_with_bearer_auth", fake_factory)
    return calls


def _work_item(
    *, work_type: str = "session", work_id: str = "w_1", session_id: str = "s_1", secret: str | None = None
) -> Any:
    return SimpleNamespace(
        id=work_id, environment_id="e_1", secret=secret, data=SimpleNamespace(type=work_type, id=session_id)
    )


def _install_aiter_work(monkeypatch: pytest.MonkeyPatch, items: list[Any]) -> None:
    async def fake_aiter_work(_work: Any, **_kw: Any) -> AsyncIterator[Any]:
        for it in items:
            yield it

    monkeypatch.setattr(worker_mod, "aiter_work", fake_aiter_work)


def _install_run_session_tools(
    monkeypatch: pytest.MonkeyPatch,
    record: dict[str, Any],
    *,
    serve: Callable[[], Awaitable[None]] | None = None,
) -> None:
    @contextlib.asynccontextmanager
    async def fake_run_session_tools(
        _client: Any,
        session_id: str,
        *,
        tools: Any,
        max_idle: Any = None,
        environment_key: Any = None,
        extra_headers: Any = None,
        send_retry_window: Any = None,
    ):
        record["run"] = {
            "session_id": session_id,
            "tools": tools,
            "max_idle": max_idle,
            "environment_key": environment_key,
            "extra_headers": extra_headers,
        }

        async def _iter() -> AsyncIterator[Any]:
            # With no ``serve`` the session completes on its own (no tool
            # calls) once the lease heartbeat has had a chance to land, and
            # the run ends via the normal session-completion path; the
            # heartbeat keeps the lease alive throughout and is stopped on the
            # way out.
            if serve is not None:
                await serve()
            else:
                await asyncio.sleep(0.05)
            record["send_retry_window"] = send_retry_window() if send_retry_window else None
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
    # The lease was heartbeated, and the lease TTL it reported (60s) became the
    # runner's tool-result send retry window.
    assert len(work.heartbeat_calls) >= 1
    assert record["send_retry_window"] == 60
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
async def test_environment_worker_skips_non_session_item(monkeypatch: pytest.MonkeyPatch) -> None:
    """The queue hands the worker a health check instead of a session.

    There is no session to look up or serve, but the item must still be
    stopped so the queue gets it back.
    """
    # A worker whose queue holds a single health-check item.
    work = _FakeWorkResource(heartbeat_state="running")
    sessions = _FakeSessions()
    _install_aiter_work(monkeypatch, [_work_item(work_type="healthcheck")])
    _install_scoped_client(monkeypatch, work, sessions)
    served: dict[str, Any] = {}
    _install_run_session_tools(monkeypatch, served)
    worker = EnvironmentWorker(_fake_client(work, sessions), environment_id="e_1", environment_key="k")

    await asyncio.wait_for(worker.run(), timeout=5)

    # No session was fetched or served...
    assert sessions.retrieve_calls == []
    assert served == {}
    # ...but the item was still stopped.
    assert len(work.stop_calls) == 1


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


@pytest.mark.skipif(PYDANTIC_V1, reason="tool functions are only supported with pydantic v2")
@pytest.mark.asyncio()
async def test_environment_worker_prefers_work_item_secret(
    monkeypatch: pytest.MonkeyPatch, caplog: pytest.LogCaptureFixture
) -> None:
    """A claimed item carrying a per-item ``secret`` payload authenticates that
    item's heartbeat / force-stop / session-runner calls with the sessions
    token extracted from it; polling stays on the environment key. Neither the
    payload nor the token ever reaches the logs."""
    secret = _encode_secret({"sessions_token": "sessions-token-item-1", "session_ingress_token": "ingress-token-1"})
    work = _FakeWorkResource(heartbeat_state="running")
    sessions = _FakeSessions()
    client = _fake_client(work, sessions)
    _install_aiter_work(monkeypatch, [_work_item(secret=secret)])
    scoped_calls = _install_scoped_client(monkeypatch, work, sessions)
    record: dict[str, Any] = {}
    _install_run_session_tools(monkeypatch, record)

    worker = EnvironmentWorker(
        client=client,
        environment_id="e_1",
        environment_key="env_key",
        workdir=".",
    )
    with caplog.at_level(logging.DEBUG, logger="anthropic.lib.environments"):
        await asyncio.wait_for(worker.run(), timeout=5)

    # Polling keeps the environment key; the per-item client switches to the
    # sessions token carried inside the work item's secret payload.
    assert scoped_calls == [
        {"auth_token": "env_key", "helper": "environments-work-poller"},
        {"auth_token": "sessions-token-item-1", "helper": "environments-worker"},
    ]
    # The session tool runner's bearer credential is the sessions token too.
    assert record["run"]["environment_key"] == "sessions-token-item-1"
    # The work item was still heartbeated and force-stopped as usual.
    assert len(work.heartbeat_calls) >= 1
    assert work.stop_calls[0]["force"] is True
    # The credentials are opaque — neither the payload nor the extracted token
    # may appear in log output.
    assert secret not in caplog.text
    assert "sessions-token-item-1" not in caplog.text


@pytest.mark.skipif(PYDANTIC_V1, reason="tool functions are only supported with pydantic v2")
@pytest.mark.asyncio()
async def test_environment_worker_falls_back_when_secret_undecodable(
    monkeypatch: pytest.MonkeyPatch, caplog: pytest.LogCaptureFixture
) -> None:
    """A secret payload that doesn't decode (or carries no sessions token)
    falls back to the environment key, with a warning that doesn't include the
    payload itself."""
    work = _FakeWorkResource(heartbeat_state="running")
    sessions = _FakeSessions()
    client = _fake_client(work, sessions)
    _install_aiter_work(monkeypatch, [_work_item(secret="not-a-valid-payload")])
    scoped_calls = _install_scoped_client(monkeypatch, work, sessions)
    record: dict[str, Any] = {}
    _install_run_session_tools(monkeypatch, record)

    worker = EnvironmentWorker(client=client, environment_id="e_1", environment_key="env_key", workdir=".")
    with caplog.at_level(logging.DEBUG, logger="anthropic.lib.environments"):
        await asyncio.wait_for(worker.run(), timeout=5)

    assert scoped_calls == [
        {"auth_token": "env_key", "helper": "environments-work-poller"},
        {"auth_token": "env_key", "helper": "environments-worker"},
    ]
    assert record["run"]["environment_key"] == "env_key"
    assert "no sessions token could be extracted" in caplog.text
    assert "not-a-valid-payload" not in caplog.text


def test_sessions_token_from_secret() -> None:
    """The secret payload decodes from URL-safe base64 JSON (with or without
    padding); anything malformed or token-less resolves to None."""
    payload = {"sessions_token": "sessions-token-abc", "auth": [{"type": "anthropic_oauth", "token": "oauth"}]}
    unpadded = _encode_secret(payload)
    padded = base64.urlsafe_b64encode(json.dumps(payload).encode()).decode()

    assert _sessions_token_from_secret(unpadded) == "sessions-token-abc"
    assert _sessions_token_from_secret(padded) == "sessions-token-abc"
    assert _sessions_token_from_secret(None) is None
    assert _sessions_token_from_secret("") is None
    assert _sessions_token_from_secret("!!! not base64 !!!") is None
    # Valid base64 but not JSON / not an object / missing or empty token.
    assert _sessions_token_from_secret(base64.urlsafe_b64encode(b"plain text").decode()) is None
    assert _sessions_token_from_secret(_encode_secret({"session_ingress_token": "ingress-token-1"})) is None
    assert _sessions_token_from_secret(_encode_secret({"sessions_token": ""})) is None


@pytest.mark.skipif(PYDANTIC_V1, reason="tool functions are only supported with pydantic v2")
@pytest.mark.asyncio()
async def test_secret_not_logged_on_error_paths(
    monkeypatch: pytest.MonkeyPatch, caplog: pytest.LogCaptureFixture
) -> None:
    """Error-path logging (heartbeat shutdown, force-stop failure) must not leak
    the per-item secret payload or its sessions token."""
    secret = _encode_secret({"sessions_token": "sessions-token-err"})
    work = _FakeWorkResource(heartbeat_state="stopping")

    failing_stop_calls: list[str] = []

    async def failing_stop(work_id: str, **_kw: Any) -> None:
        failing_stop_calls.append(work_id)
        raise RuntimeError("force-stop exploded")

    work.stop = failing_stop  # type: ignore[method-assign]
    sessions = _FakeSessions()
    client = _fake_client(work, sessions)
    _install_aiter_work(monkeypatch, [_work_item(secret=secret)])
    _install_scoped_client(monkeypatch, work, sessions)
    record: dict[str, Any] = {}
    _install_run_session_tools(monkeypatch, record)

    worker = EnvironmentWorker(client=client, environment_id="e_1", environment_key="env_key", workdir=".")
    with caplog.at_level(logging.DEBUG, logger="anthropic.lib.environments"):
        await asyncio.wait_for(worker.run(), timeout=5)

    # The error branches actually ran (heartbeat signalled shutdown, the
    # force-stop failure was logged) ...
    assert failing_stop_calls == ["w_1"]
    assert "force-stop on exit failed" in caplog.text
    # ... and none of them leaked the payload or the token inside it.
    assert secret not in caplog.text
    assert "sessions-token-err" not in caplog.text


def _no_tools(_env: Any) -> list[Any]:
    return []


def _install_session_ended_by_heartbeat(
    monkeypatch: pytest.MonkeyPatch, work: _FakeWorkResource, record: dict[str, Any]
) -> None:
    """A session that never completes on its own, with the fake heartbeat held
    back until the runner is serving it: the heartbeat's outcome — not skill
    setup or session completion — decides how the run ends."""
    serving = asyncio.Event()
    work.heartbeat_gate = serving

    async def serve() -> None:
        serving.set()
        await asyncio.Event().wait()

    _install_run_session_tools(monkeypatch, record, serve=serve)


@pytest.mark.asyncio()
async def test_heartbeat_412_releases_item_without_stopping_it(
    monkeypatch: pytest.MonkeyPatch, caplog: pytest.LogCaptureFixture
) -> None:
    """A 412 on the heartbeat means the server cleared this worker's lease
    (re-queued the item, or another worker holds it). The run ends, the item
    is NOT force-stopped — that would take it away from its new holder — and
    the worker goes back to polling."""
    work = _FakeWorkResource(heartbeat_error=_lease_lost_error())
    sessions = _FakeSessions()
    client = _fake_client(work, sessions)
    _install_scoped_client(monkeypatch, work, sessions)
    record: dict[str, Any] = {}
    _install_session_ended_by_heartbeat(monkeypatch, work, record)

    polls: list[str] = []

    async def fake_aiter_work(_work: Any, **_kw: Any) -> AsyncIterator[Any]:
        polls.append("poll")
        yield _work_item()
        polls.append("poll")

    monkeypatch.setattr(worker_mod, "aiter_work", fake_aiter_work)

    worker = EnvironmentWorker(
        client=client, environment_id="e_1", environment_key="env_key", workdir=".", tools=_no_tools
    )
    with caplog.at_level(logging.INFO, logger="anthropic.lib.environments"):
        await asyncio.wait_for(worker.run(), timeout=5)

    assert record["run"]["session_id"] == "s_1"
    assert len(work.heartbeat_calls) == 1
    assert work.stop_calls == []
    assert polls == ["poll", "poll"], "run() must go back to the poller after releasing the item"
    assert (
        "lease lost: heartbeat precondition failed work_id=w_1 "
        "server_state=queued server_ttl_seconds=120 server_last_heartbeat=None"
    ) in caplog.text
    assert "lease lost; released work_id=w_1 session_id=s_1 without stopping it" in caplog.text
    assert "work item failed" not in caplog.text


@pytest.mark.asyncio()
async def test_control_plane_stop_still_force_stops(
    monkeypatch: pytest.MonkeyPatch, caplog: pytest.LogCaptureFixture
) -> None:
    """A heartbeat reporting ``state == "stopped"`` ends the run and the item
    is still force-stopped on the way out — only a *lost* lease skips that."""
    work = _FakeWorkResource(heartbeat_state="stopped")
    sessions = _FakeSessions()
    client = _fake_client(work, sessions)
    _install_scoped_client(monkeypatch, work, sessions)
    _install_aiter_work(monkeypatch, [_work_item()])
    record: dict[str, Any] = {}
    _install_session_ended_by_heartbeat(monkeypatch, work, record)

    worker = EnvironmentWorker(
        client=client, environment_id="e_1", environment_key="env_key", workdir=".", tools=_no_tools
    )
    with caplog.at_level(logging.INFO, logger="anthropic.lib.environments"):
        await asyncio.wait_for(worker.run(), timeout=5)

    assert record["run"]["session_id"] == "s_1"
    assert "heartbeat signals shutdown state=stopped" in caplog.text
    assert len(work.stop_calls) == 1
    assert work.stop_calls[0]["work_id"] == "w_1"
    assert work.stop_calls[0]["force"] is True
    assert "without stopping it" not in caplog.text


@pytest.mark.asyncio()
async def test_lease_assumed_lost_releases_item_without_stopping_it(
    monkeypatch: pytest.MonkeyPatch, caplog: pytest.LogCaptureFixture
) -> None:
    """Transient heartbeat failures lasting past the lease TTL mean another
    worker may hold the item by now, so it is released without a force-stop."""
    work = _FakeWorkResource(heartbeat_error=_api_status_error(503))
    sessions = _FakeSessions()
    client = _fake_client(work, sessions)
    _install_scoped_client(monkeypatch, work, sessions)
    _install_aiter_work(monkeypatch, [_work_item()])
    record: dict[str, Any] = {}
    _install_session_ended_by_heartbeat(monkeypatch, work, record)

    # Each clock read lands 100s after the previous one, so the very first
    # transient failure is already past the 90s default TTL.
    ticks = iter(range(0, 10_000, 100))
    monkeypatch.setattr(worker_mod, "time", SimpleNamespace(monotonic=lambda: float(next(ticks))))

    worker = EnvironmentWorker(
        client=client, environment_id="e_1", environment_key="env_key", workdir=".", tools=_no_tools
    )
    with caplog.at_level(logging.INFO, logger="anthropic.lib.environments"):
        await asyncio.wait_for(worker.run(), timeout=5)

    assert record["run"]["session_id"] == "s_1"
    assert "lease assumed lost: no successful heartbeat in 90s" in caplog.text
    assert work.stop_calls == []
    assert "lease lost; released work_id=w_1 session_id=s_1 without stopping it" in caplog.text


@pytest.mark.asyncio()
async def test_lease_lost_classification() -> None:
    """Only the two reasons where the item now belongs to someone else read as
    lost; every other reason, and no recorded reason at all, keeps the
    force-stop. The first recorded reason wins over the runner's own finish."""
    for reason, lost in [
        (_LeaseEndReason.LEASE_LOST, True),
        (_LeaseEndReason.ASSUMED_LOST, True),
        (_LeaseEndReason.CONTROL_PLANE_STOP, False),
        (_LeaseEndReason.HEARTBEAT_REJECTED, False),
        (_LeaseEndReason.RUNNER_DONE, False),
    ]:
        lease = _Lease()
        assert not lease.ended
        assert not lease.lost
        lease.finish(reason)
        lease.finish(_LeaseEndReason.RUNNER_DONE)
        assert lease.ended
        assert lease._end_reason is reason
        assert lease.lost is lost, reason


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
    # A leftover per-item secret on the host must not override the explicit key.
    monkeypatch.delenv("ANTHROPIC_WORK_SECRET", raising=False)

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
    monkeypatch.delenv("ANTHROPIC_WORK_SECRET", raising=False)

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
    monkeypatch.delenv("ANTHROPIC_WORK_SECRET", raising=False)

    worker = EnvironmentWorker(client, environment_key="ctor_key", workdir=".")
    await asyncio.wait_for(
        worker.handle_item(work_id="w_1", environment_id="e_1", session_id="s_1"),
        timeout=5,
    )

    assert record["run"]["environment_key"] == "ctor_key"
    assert scoped_calls == [{"auth_token": "ctor_key", "helper": "environments-worker"}]


@pytest.mark.skipif(PYDANTIC_V1, reason="tool functions are only supported with pydantic v2")
@pytest.mark.asyncio()
async def test_handle_item_uses_work_secret_argument(monkeypatch: pytest.MonkeyPatch) -> None:
    """An explicit ``work_secret`` payload supplies the per-item Bearer
    credential (its sessions token); ``environment_key`` is still required but
    only used as the fallback."""
    secret = _encode_secret({"sessions_token": "sessions-token-arg"})
    work = _FakeWorkResource(heartbeat_state="running")
    sessions = _FakeSessions()
    client = _fake_client(work, sessions)
    scoped_calls = _install_scoped_client(monkeypatch, work, sessions)
    record: dict[str, Any] = {}
    _install_run_session_tools(monkeypatch, record)

    worker = EnvironmentWorker(client, workdir=".")
    await asyncio.wait_for(
        worker.handle_item(
            work_id="w_1",
            environment_id="e_1",
            session_id="s_1",
            environment_key="env_key",
            work_secret=secret,
        ),
        timeout=5,
    )

    assert scoped_calls == [{"auth_token": "sessions-token-arg", "helper": "environments-worker"}]
    assert record["run"]["environment_key"] == "sessions-token-arg"


@pytest.mark.skipif(PYDANTIC_V1, reason="tool functions are only supported with pydantic v2")
@pytest.mark.asyncio()
async def test_handle_item_falls_back_to_work_secret_env_var(monkeypatch: pytest.MonkeyPatch) -> None:
    """``work_secret`` falls back to ``ANTHROPIC_WORK_SECRET`` (the env var the
    ``worker poll --on-work`` command sets alongside the others); when neither
    is present the environment key is used — the existing
    ``test_handle_item_*`` cases cover that path."""
    secret = _encode_secret({"sessions_token": "sessions-token-env"})
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
    monkeypatch.setenv("ANTHROPIC_WORK_SECRET", secret)

    worker = EnvironmentWorker(client, workdir=".")
    await asyncio.wait_for(worker.handle_item(), timeout=5)

    assert scoped_calls == [{"auth_token": "sessions-token-env", "helper": "environments-worker"}]
    assert record["run"]["environment_key"] == "sessions-token-env"
    assert work.stop_calls[0]["work_id"] == "w_env"


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
        max_idle=12.0,
        memory_sync_interval=45.0,
        memory_sync_deletions="log_only",
        worker_id="w-test",
        extra_headers={"x-trace-id": "abc123"},
    )
    assert isinstance(worker, EnvironmentWorker)
    assert worker._client is client
    assert worker._environment_id == "e_1"
    assert worker._environment_key == "env_key"
    assert worker._workdir == "/workspace"
    assert worker._max_idle == 12.0
    assert worker._memory_sync_interval == 45.0
    assert worker._memory_sync_deletions == "log_only"
    assert worker._worker_id == "w-test"
    assert worker._extra_headers == {"x-trace-id": "abc123"}


@pytest.mark.parametrize("value", [True, False])
def test_unrestricted_paths_is_rejected_at_construction(value: bool) -> None:
    client = AsyncAnthropic(api_key="x")
    with pytest.raises(TypeError, match="unrestricted_paths is no longer supported"):
        EnvironmentWorker(client, unrestricted_paths=value)  # pyright: ignore[reportDeprecated]
    with pytest.raises(TypeError, match="unrestricted_paths is no longer supported"):
        client.beta.environments.work.worker(unrestricted_paths=value)  # pyright: ignore[reportDeprecated]


def test_work_resource_worker_defaults() -> None:
    worker = AsyncAnthropic(api_key="x").beta.environments.work.worker()
    assert isinstance(worker, EnvironmentWorker)
    assert worker._environment_id is None
    assert worker._environment_key is None
    assert worker._tools is None
    # Default workdir is the cwd snapshotted at construction (not a lazily
    # resolved ".") — TS parity with process.cwd()-at-construction.
    assert worker._workdir == os.getcwd()
    assert worker._max_idle == 60.0
    assert worker._memory_sync_interval == 15.0
    assert worker._memory_sync_deletions == "enabled"


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
        send_retry_window: Any = None,  # noqa: ARG001
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


# ---------- heartbeat loop ---------------------------------------------------
#
# ``_heartbeat_loop`` is driven directly with a scripted ``work`` fake and a
# fake clock, so the lease-staleness ceiling can be crossed without real
# waiting. The first scripted beat reports ``ttl_seconds=0`` so the loop keeps
# the (patched, tiny) default interval instead of the 1 s floor it applies to
# a server-provided ttl.

_HANG = object()
_FAST_INTERVAL = 0.01
_FAKE_TTL = 5.0


class _FakeClock:
    def __init__(self) -> None:
        self.now = 0.0

    def monotonic(self) -> float:
        return self.now


class _ScriptedHeartbeatWork:
    """``heartbeat`` pops ``(clock_advance, outcome)`` per call: an exception is
    raised, ``_HANG`` never returns, anything else is the response."""

    def __init__(self, clock: _FakeClock, script: list[tuple[float, Any]]) -> None:
        self._clock = clock
        self._script = list(script)
        self.calls = 0

    async def heartbeat(self, work_id: str, **_kwargs: Any) -> Any:  # noqa: ARG002
        self.calls += 1
        advance, outcome = self._script.pop(0)
        self._clock.now += advance
        if isinstance(outcome, BaseException):
            raise outcome
        if outcome is _HANG:
            await anyio.sleep_forever()
        return outcome


def _beat_ok(ttl_seconds: int = 0) -> Any:
    return SimpleNamespace(last_heartbeat="hb", ttl_seconds=ttl_seconds, state="running", lease_extended=True)


async def _run_heartbeat_loop(
    monkeypatch: pytest.MonkeyPatch, script: list[tuple[float, Any]]
) -> tuple[_ScriptedHeartbeatWork, _Lease]:
    clock = _FakeClock()
    monkeypatch.setattr(worker_mod, "time", SimpleNamespace(monotonic=clock.monotonic))
    monkeypatch.setattr(worker_mod, "_HEARTBEAT_DEFAULT", _FAST_INTERVAL)
    monkeypatch.setattr(worker_mod, "_HEARTBEAT_TTL_DEFAULT", _FAKE_TTL)
    work = _ScriptedHeartbeatWork(clock, script)
    lease = _Lease()
    with anyio.fail_after(5):
        await _heartbeat_loop(cast(Any, work), work_id="w_1", environment_id="e_1", lease=lease)
    return work, lease


def _messages(caplog: pytest.LogCaptureFixture) -> list[str]:
    return [r.getMessage() for r in caplog.records if r.name == worker_mod.__name__]


@pytest.mark.asyncio()
async def test_heartbeat_conflict_is_retried_until_the_lease_is_stale(
    monkeypatch: pytest.MonkeyPatch, caplog: pytest.LogCaptureFixture
) -> None:
    caplog.set_level(logging.WARNING, logger=worker_mod.__name__)
    work, lease = await _run_heartbeat_loop(
        monkeypatch,
        [(0, _beat_ok()), (_FAKE_TTL - 2, _api_status_error(409)), (_FAKE_TTL, _api_status_error(409))],
    )
    assert work.calls == 3
    assert lease.ended
    assert lease.lost
    messages = _messages(caplog)
    assert any(m.startswith("transient heartbeat failure") for m in messages)
    assert any(m.startswith("lease assumed lost") for m in messages)
    assert not any(m.startswith("permanent heartbeat failure") for m in messages)


@pytest.mark.asyncio()
async def test_heartbeat_that_never_returns_is_cut_off_each_interval(
    monkeypatch: pytest.MonkeyPatch, caplog: pytest.LogCaptureFixture
) -> None:
    caplog.set_level(logging.WARNING, logger=worker_mod.__name__)
    work, lease = await _run_heartbeat_loop(monkeypatch, [(0, _beat_ok()), (_FAKE_TTL - 2, _HANG), (_FAKE_TTL, _HANG)])
    assert work.calls == 3
    assert lease.ended
    assert lease.lost
    assert any(m.startswith("lease assumed lost") for m in _messages(caplog))


@pytest.mark.asyncio()
async def test_heartbeat_permanent_4xx_stops_immediately(
    monkeypatch: pytest.MonkeyPatch, caplog: pytest.LogCaptureFixture
) -> None:
    caplog.set_level(logging.WARNING, logger=worker_mod.__name__)
    work, lease = await _run_heartbeat_loop(monkeypatch, [(0, _api_status_error(401))])
    assert work.calls == 1
    assert lease.ended
    assert not lease.lost
    assert any(m.startswith("permanent heartbeat failure") for m in _messages(caplog))


@pytest.mark.asyncio()
async def test_heartbeat_keeps_beating_while_a_sync_tool_blocks(monkeypatch: pytest.MonkeyPatch) -> None:
    """Heartbeat loop and tool call share one task group, as they do in ``_handle_item``."""
    monkeypatch.setattr(worker_mod, "_HEARTBEAT_DEFAULT", _FAST_INTERVAL)
    in_tool, release = threading.Event(), threading.Event()

    class _Work:
        def __init__(self) -> None:
            self.beats_during_tool = 0

        async def heartbeat(self, work_id: str, **_kwargs: Any) -> Any:  # noqa: ARG002
            if in_tool.is_set() and not release.is_set():
                self.beats_during_tool += 1
                if self.beats_during_tool >= 3:
                    release.set()
            return _beat_ok()

    def blocking(_input: object) -> str:
        in_tool.set()
        if not release.wait(timeout=2):
            raise RuntimeError("no heartbeat fired while the tool ran")
        return "ok"

    work, lease = _Work(), _Lease()
    result: object = None
    try:
        with anyio.fail_after(5):
            async with anyio.create_task_group() as tg:
                tg.start_soon(
                    partial(_heartbeat_loop, cast(Any, work), work_id="w_1", environment_id="e_1", lease=lease)
                )
                result = await run_runnable_tool(_SyncTool("blocking", blocking), {})
                lease.finish(_LeaseEndReason.RUNNER_DONE)
    finally:
        release.set()

    assert result == "ok"
    assert work.beats_during_tool >= 3
