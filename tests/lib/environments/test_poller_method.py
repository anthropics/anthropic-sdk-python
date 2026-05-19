"""Tests for ``iter_work`` / ``aiter_work`` (the implementations behind
``client.beta.environments.work.poller()``).

We don't need a real HTTP mock here because the generators only ever talk to
a ``Work``/``AsyncWork`` resource through three methods (``poll``, ``ack``,
``stop``). The fakes below stand in for that resource and let each test feed
a script of poll responses while recording ack/stop call sites.
"""

from __future__ import annotations

import time
import asyncio
from typing import Any, cast
from collections.abc import AsyncIterator

import httpx
import pytest

from anthropic import APIStatusError
from anthropic.lib.environments._poller import iter_work, aiter_work


class _StubWorkData:
    type = "session"


class _StubWork:
    """Minimal stand-in for ``BetaSelfHostedWork`` — only fields the poller reads."""

    def __init__(self, *, id: str = "work_1") -> None:
        self.id = id
        self.data = _StubWorkData()


def _api_status_error(code: int) -> APIStatusError:
    request = httpx.Request("POST", "https://api.example/poll")
    response = httpx.Response(status_code=code, request=request, content=b"{}")
    return APIStatusError("boom", response=response, body=None)


class FakeWork:
    """Sync resource fake. ``poll_script`` is consumed in order; values are
    either ``BetaSelfHostedWork``-shaped stubs, ``None`` (no work available),
    or ``Exception`` instances (raised from poll).
    """

    def __init__(self, poll_script: list[Any]) -> None:
        self._poll_script = list(poll_script)
        self.poll_calls: list[dict[str, Any]] = []
        self.ack_calls: list[tuple[str, dict[str, Any]]] = []
        self.stop_calls: list[tuple[str, dict[str, Any]]] = []

    def poll(self, environment_id: str, **kwargs: Any) -> Any:
        self.poll_calls.append({"environment_id": environment_id, **kwargs})
        if not self._poll_script:
            raise _StopTest("poll script exhausted")
        nxt = self._poll_script.pop(0)
        if isinstance(nxt, BaseException):
            raise nxt
        return nxt

    def ack(self, work_id: str, **kwargs: Any) -> None:
        self.ack_calls.append((work_id, kwargs))

    def stop(self, work_id: str, **kwargs: Any) -> None:
        self.stop_calls.append((work_id, kwargs))


class FakeAsyncWork:
    def __init__(self, poll_script: list[Any]) -> None:
        self._poll_script = list(poll_script)
        self.poll_calls: list[dict[str, Any]] = []
        self.ack_calls: list[tuple[str, dict[str, Any]]] = []
        self.stop_calls: list[tuple[str, dict[str, Any]]] = []

    async def poll(self, environment_id: str, **kwargs: Any) -> Any:
        self.poll_calls.append({"environment_id": environment_id, **kwargs})
        if not self._poll_script:
            raise _StopTest("poll script exhausted")
        nxt = self._poll_script.pop(0)
        if isinstance(nxt, BaseException):
            raise nxt
        return nxt

    async def ack(self, work_id: str, **kwargs: Any) -> None:
        self.ack_calls.append((work_id, kwargs))

    async def stop(self, work_id: str, **kwargs: Any) -> None:
        self.stop_calls.append((work_id, kwargs))


class _StopTest(BaseException):
    """Sentinel used to break a poller out of its infinite loop in tests.

    Inherits from BaseException so it bypasses the generator's
    ``except Exception`` arms (which would otherwise treat the empty-script
    error as a transient poll failure and retry forever).
    """


def _sync_noop(_seconds: float) -> None:
    return None


async def _async_noop(_seconds: float) -> None:
    return None


@pytest.fixture(autouse=True)
def _no_sleep(monkeypatch: pytest.MonkeyPatch) -> None:  # pyright: ignore[reportUnusedFunction]
    monkeypatch.setattr(time, "sleep", _sync_noop)
    monkeypatch.setattr(asyncio, "sleep", _async_noop)


def _drain_one(it: Any) -> Any:
    """Pull a single item from a sync iterator; assert there was one."""
    try:
        return next(it)
    except _StopTest:
        pytest.fail("poller exhausted script before yielding any work")


async def _adrain_one(ait: AsyncIterator[Any]) -> Any:
    try:
        return await ait.__anext__()
    except _StopTest:
        pytest.fail("poller exhausted script before yielding any work")


def test_iter_work_yields_acks_and_stops_one_item() -> None:
    work = _StubWork()
    fake = FakeWork(poll_script=[work])
    it = iter_work(cast(Any, fake), environment_id="env_1")

    item = _drain_one(it)
    assert item is work
    assert fake.ack_calls == [("work_1", fake.ack_calls[0][1])]
    assert fake.stop_calls == [], "stop should not be called until body returns"

    with pytest.raises(_StopTest):
        next(it)
    assert len(fake.stop_calls) == 1
    assert fake.stop_calls[0][0] == "work_1"


def test_iter_work_calls_stop_when_body_raises() -> None:
    work = _StubWork(id="work_boom")
    fake = FakeWork(poll_script=[work])
    it = iter_work(cast(Any, fake), environment_id="env_1")

    next(it)
    # Throwing into the generator simulates the consumer's body raising.
    # iter_work returns Iterator publicly but is a Generator internally.
    with pytest.raises(RuntimeError):
        cast(Any, it).throw(RuntimeError("body failed"))
    assert fake.stop_calls == [("work_boom", fake.stop_calls[0][1])]


def test_iter_work_backs_off_on_transient_error() -> None:
    fake = FakeWork(poll_script=[_api_status_error(500), _StubWork(id="work_2")])
    it = iter_work(cast(Any, fake), environment_id="env_1")

    item = _drain_one(it)
    assert item.id == "work_2"
    assert len(fake.poll_calls) == 2


def test_iter_work_raises_on_permanent_4xx() -> None:
    fake = FakeWork(poll_script=[_api_status_error(401)])
    it = iter_work(cast(Any, fake), environment_id="env_1")

    with pytest.raises(APIStatusError):
        next(it)


def test_iter_work_backs_off_on_httpx_transport_error() -> None:
    """A raw ``httpx`` transport error (not wrapped in an SDK ``APIError``) is
    still transient and must be retried, not propagated."""
    fake = FakeWork(poll_script=[httpx.ConnectError("connection refused"), _StubWork(id="work_2")])
    it = iter_work(cast(Any, fake), environment_id="env_1")

    item = _drain_one(it)
    assert item.id == "work_2"
    assert len(fake.poll_calls) == 2


def test_iter_work_propagates_non_api_error_instead_of_retrying() -> None:
    """A programming error (here ``KeyError``) is not a transient API/transport
    failure, so it must propagate immediately rather than be swallowed and
    retried forever. ``poll`` is only called once — no backoff/retry."""
    fake = FakeWork(poll_script=[KeyError("bug"), _StubWork(id="work_2")])
    it = iter_work(cast(Any, fake), environment_id="env_1")

    with pytest.raises(KeyError):
        next(it)
    assert len(fake.poll_calls) == 1


def test_iter_work_propagates_non_api_error_from_ack() -> None:
    """Same for a non-API error raised by ``ack`` — it propagates rather than
    backing off and retrying."""
    fake = FakeWork(poll_script=[_StubWork(id="work_bad")])

    def _ack(_work_id: str, **_kwargs: Any) -> None:
        raise RuntimeError("ack bug")

    fake.ack = _ack  # type: ignore[method-assign]
    it = iter_work(cast(Any, fake), environment_id="env_1")

    with pytest.raises(RuntimeError, match="ack bug"):
        next(it)
    assert fake.stop_calls == []


def test_iter_work_force_stops_on_permanent_ack_failure() -> None:
    """A permanent 4xx on ack force-stops the item rather than re-delivering it."""
    fake = FakeWork(poll_script=[_StubWork(id="work_bad")])

    def _ack(_work_id: str, **_kwargs: Any) -> None:
        raise _api_status_error(403)

    fake.ack = _ack  # type: ignore[method-assign]
    it = iter_work(cast(Any, fake), environment_id="env_1")

    with pytest.raises(_StopTest):
        next(it)
    assert [c[0] for c in fake.stop_calls] == ["work_bad"]
    assert fake.stop_calls[0][1]["force"] is True


def test_iter_work_drain_returns_on_empty_queue() -> None:
    a, b = _StubWork(id="work_a"), _StubWork(id="work_b")
    fake = FakeWork(poll_script=[a, b, None])
    it = iter_work(cast(Any, fake), environment_id="env_1", drain=True)

    items = list(it)
    assert [i.id for i in items] == ["work_a", "work_b"]
    # Generator returned cleanly — no _StopTest raised, script not exhausted.
    assert len(fake.poll_calls) == 3


def test_iter_work_drain_returns_immediately_when_queue_empty() -> None:
    fake = FakeWork(poll_script=[None])
    it = iter_work(cast(Any, fake), environment_id="env_1", drain=True)

    assert list(it) == []
    assert len(fake.poll_calls) == 1


def test_iter_work_auto_stop_false_never_stops() -> None:
    """A dispatcher hands work off to another process that owns the stop call.

    The poller must not stop the lease out from under that process.
    """
    a, b = _StubWork(id="work_a"), _StubWork(id="work_b")
    fake = FakeWork(poll_script=[a, b, None])
    it = iter_work(cast(Any, fake), environment_id="env_1", drain=True, auto_stop=False)

    assert [item.id for item in it] == ["work_a", "work_b"]
    assert [c[0] for c in fake.ack_calls] == ["work_a", "work_b"], "every item should still be ack'd"
    assert fake.stop_calls == []


def test_iter_work_auto_stop_false_does_not_stop_on_body_raise() -> None:
    work = _StubWork(id="work_boom")
    fake = FakeWork(poll_script=[work])
    it = iter_work(cast(Any, fake), environment_id="env_1", auto_stop=False)

    next(it)
    with pytest.raises(RuntimeError):
        cast(Any, it).throw(RuntimeError("body failed"))
    assert fake.stop_calls == []


def test_iter_work_forwards_reclaim_older_than_ms() -> None:
    fake = FakeWork(poll_script=[None])
    it = iter_work(cast(Any, fake), environment_id="env_1", drain=True, reclaim_older_than_ms=2000)

    list(it)
    assert fake.poll_calls[0]["reclaim_older_than_ms"] == 2000


def test_iter_work_block_ms_none_omits_param() -> None:
    """The server rejects block_ms=0; None must translate to the omit sentinel
    so the poll is non-blocking instead of 400ing."""
    from anthropic._types import omit

    fake = FakeWork(poll_script=[None])
    it = iter_work(cast(Any, fake), environment_id="env_1", drain=True, block_ms=None)

    list(it)
    assert fake.poll_calls[0]["block_ms"] is omit


@pytest.mark.asyncio()
async def test_aiter_work_yields_acks_and_stops_one_item() -> None:
    work = _StubWork()
    fake = FakeAsyncWork(poll_script=[work])
    ait = aiter_work(cast(Any, fake), environment_id="env_1")

    item = await _adrain_one(ait)
    assert item is work
    assert fake.ack_calls == [("work_1", fake.ack_calls[0][1])]
    assert fake.stop_calls == []

    with pytest.raises(_StopTest):
        await ait.__anext__()
    assert len(fake.stop_calls) == 1


@pytest.mark.asyncio()
async def test_aiter_work_calls_stop_when_body_raises() -> None:
    work = _StubWork(id="work_boom")
    fake = FakeAsyncWork(poll_script=[work])
    ait = aiter_work(cast(Any, fake), environment_id="env_1")

    await ait.__anext__()
    with pytest.raises(RuntimeError):
        await cast(Any, ait).athrow(RuntimeError("body failed"))
    assert fake.stop_calls == [("work_boom", fake.stop_calls[0][1])]


@pytest.mark.asyncio()
async def test_aiter_work_backs_off_on_transient_error() -> None:
    fake = FakeAsyncWork(poll_script=[_api_status_error(500), _StubWork(id="work_2")])
    ait = aiter_work(cast(Any, fake), environment_id="env_1")

    item = await _adrain_one(ait)
    assert item.id == "work_2"
    assert len(fake.poll_calls) == 2


async def test_aiter_work_propagates_non_api_error_instead_of_retrying() -> None:
    """Async counterpart: a non-API/non-transport error propagates instead of
    being retried forever."""
    fake = FakeAsyncWork(poll_script=[AttributeError("bug"), _StubWork(id="work_2")])
    ait = aiter_work(cast(Any, fake), environment_id="env_1")

    with pytest.raises(AttributeError):
        await ait.__anext__()
    assert len(fake.poll_calls) == 1


@pytest.mark.asyncio()
async def test_aiter_work_drain_auto_stop_false_dispatch_shape() -> None:
    a, b = _StubWork(id="work_a"), _StubWork(id="work_b")
    fake = FakeAsyncWork(poll_script=[a, b, None])
    ait = aiter_work(cast(Any, fake), environment_id="env_1", drain=True, auto_stop=False)

    items = [item async for item in ait]
    assert [i.id for i in items] == ["work_a", "work_b"]
    assert [c[0] for c in fake.ack_calls] == ["work_a", "work_b"]
    assert fake.stop_calls == []
    assert len(fake.poll_calls) == 3


# ---------- extra_headers per-request passthrough ---------------------------
#
# These assert the caller-supplied ``extra_headers`` actually reaches every
# underlying ``poll`` / ``ack`` / ``stop`` call (the resource methods route it
# through ``make_request_options``). The fakes record the kwargs each method
# was called with, so a missing thread-through shows up as ``None``.

_EXTRA = {"x-trace-id": "trace-123"}


def test_iter_work_threads_extra_headers_into_poll_ack_stop() -> None:
    fake = FakeWork(poll_script=[_StubWork(id="work_h")])
    it = iter_work(cast(Any, fake), environment_id="env_1", extra_headers=_EXTRA)

    item = _drain_one(it)
    assert item.id == "work_h"
    assert fake.poll_calls[0]["extra_headers"] == _EXTRA
    assert fake.ack_calls[0][1]["extra_headers"] == _EXTRA

    with pytest.raises(_StopTest):
        next(it)
    assert fake.stop_calls[0][1]["extra_headers"] == _EXTRA


def test_iter_work_threads_extra_headers_into_force_stop() -> None:
    """A permanent ack failure force-stops the item; the passthrough header
    must ride along on that force-stop call too."""
    fake = FakeWork(poll_script=[_StubWork(id="work_bad")])

    def _ack(_work_id: str, **_kwargs: Any) -> None:
        raise _api_status_error(403)

    fake.ack = _ack  # type: ignore[method-assign]
    it = iter_work(cast(Any, fake), environment_id="env_1", extra_headers=_EXTRA)

    with pytest.raises(_StopTest):
        next(it)
    assert fake.stop_calls[0][0] == "work_bad"
    assert fake.stop_calls[0][1]["force"] is True
    assert fake.stop_calls[0][1]["extra_headers"] == _EXTRA


@pytest.mark.asyncio()
async def test_aiter_work_threads_extra_headers_into_poll_ack_stop() -> None:
    fake = FakeAsyncWork(poll_script=[_StubWork(id="work_h")])
    ait = aiter_work(cast(Any, fake), environment_id="env_1", extra_headers=_EXTRA)

    item = await _adrain_one(ait)
    assert item.id == "work_h"
    assert fake.poll_calls[0]["extra_headers"] == _EXTRA
    assert fake.ack_calls[0][1]["extra_headers"] == _EXTRA

    with pytest.raises(_StopTest):
        await ait.__anext__()
    assert fake.stop_calls[0][1]["extra_headers"] == _EXTRA


@pytest.mark.asyncio()
async def test_aiter_work_threads_extra_headers_into_force_stop() -> None:
    fake = FakeAsyncWork(poll_script=[_StubWork(id="work_bad")])

    async def _ack(_work_id: str, **_kwargs: Any) -> None:
        raise _api_status_error(403)

    fake.ack = _ack  # type: ignore[method-assign]
    ait = aiter_work(cast(Any, fake), environment_id="env_1", extra_headers=_EXTRA)

    with pytest.raises(_StopTest):
        await ait.__anext__()
    assert fake.stop_calls[0][0] == "work_bad"
    assert fake.stop_calls[0][1]["force"] is True
    assert fake.stop_calls[0][1]["extra_headers"] == _EXTRA
