"""Tests for `iter_work` / `aiter_work` (the implementations behind
`client.beta.environments.work.poller()`).

We don't need a real HTTP mock here because the generators only ever talk to
a `Work`/`AsyncWork` resource through three methods (`poll`, `ack`,
`stop`). The fakes below stand in for that resource and let each test feed
a script of poll responses while recording ack/stop call sites.
"""

from __future__ import annotations

import time
import asyncio
import logging
from types import SimpleNamespace
from typing import Any, cast
from collections.abc import AsyncIterator
from typing_extensions import override

import httpx2
import pytest
from respx import MockRouter
from opentelemetry import trace
from opentelemetry.trace import SpanKind, StatusCode
from opentelemetry.sdk.trace import TracerProvider, sampling
from opentelemetry.sdk.trace.export import SimpleSpanProcessor

from anthropic import Anthropic, APIStatusError, AsyncAnthropic
from anthropic.lib.environments import _poller as poller_mod
from anthropic.lib.environments._poller import iter_work, aiter_work

from ...test_open_telemetry import TRACING_FAILURES, failing_tracing
from ..tools.test_open_telemetry import Spans, span_id, parent_id, attributes

base_url = "http://127.0.0.1:4010"


class _StubWorkData:
    type = "session"


class _StubWork:
    """Minimal stand-in for `BetaSelfHostedWork` — only fields the poller reads."""

    def __init__(self, *, id: str = "work_1") -> None:
        self.id = id
        self.data = _StubWorkData()


def _api_status_error(code: int) -> APIStatusError:
    request = httpx2.Request("POST", "https://api.example/poll")
    response = httpx2.Response(status_code=code, request=request, content=b"{}")
    return APIStatusError("boom", response=response, body=None)


class FakeWork:
    """Sync resource fake. `poll_script` is consumed in order; values are
    either `BetaSelfHostedWork`-shaped stubs, `None` (no work available),
    `Exception` instances (raised from poll), or callables producing one of
    those (so a script step can also move a fake clock).
    """

    _client = SimpleNamespace(_tracer=None)

    def __init__(self, poll_script: list[Any]) -> None:
        self._poll_script = list(poll_script)
        self.poll_calls: list[dict[str, Any]] = []
        self.ack_calls: list[tuple[str, dict[str, Any]]] = []
        self.stop_calls: list[tuple[str, dict[str, Any]]] = []

    def poll(self, environment_id: str, **kwargs: Any) -> Any:
        self.poll_calls.append({"environment_id": environment_id, **kwargs})
        return _next_poll_result(self._poll_script)

    def ack(self, work_id: str, **kwargs: Any) -> None:
        self.ack_calls.append((work_id, kwargs))

    def stop(self, work_id: str, **kwargs: Any) -> None:
        self.stop_calls.append((work_id, kwargs))


class FakeAsyncWork:
    _client = SimpleNamespace(_tracer=None)

    def __init__(self, poll_script: list[Any]) -> None:
        self._poll_script = list(poll_script)
        self.poll_calls: list[dict[str, Any]] = []
        self.ack_calls: list[tuple[str, dict[str, Any]]] = []
        self.stop_calls: list[tuple[str, dict[str, Any]]] = []

    async def poll(self, environment_id: str, **kwargs: Any) -> Any:
        self.poll_calls.append({"environment_id": environment_id, **kwargs})
        return _next_poll_result(self._poll_script)

    async def ack(self, work_id: str, **kwargs: Any) -> None:
        self.ack_calls.append((work_id, kwargs))

    async def stop(self, work_id: str, **kwargs: Any) -> None:
        self.stop_calls.append((work_id, kwargs))


class _StopTest(BaseException):
    """Sentinel used to break a poller out of its infinite loop in tests.

    Inherits from BaseException so it bypasses the generator's
    `except Exception` arms (which would otherwise treat the empty-script
    error as a transient poll failure and retry forever).
    """


def _next_poll_result(script: list[Any]) -> Any:
    if not script:
        raise _StopTest("poll script exhausted")
    nxt = script.pop(0)
    if callable(nxt):
        nxt = nxt()
    if isinstance(nxt, BaseException):
        raise nxt
    return nxt


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


@pytest.mark.parametrize("status", [500, 409])
def test_iter_work_backs_off_on_transient_error(status: int) -> None:
    fake = FakeWork(poll_script=[_api_status_error(status), _StubWork(id="work_2")])
    it = iter_work(cast(Any, fake), environment_id="env_1")

    item = _drain_one(it)
    assert item.id == "work_2"
    assert len(fake.poll_calls) == 2


def test_iter_work_raises_on_permanent_4xx() -> None:
    fake = FakeWork(poll_script=[_api_status_error(401)])
    it = iter_work(cast(Any, fake), environment_id="env_1")

    with pytest.raises(APIStatusError):
        next(it)


def test_iter_work_stop_conflict_is_silent(caplog: pytest.LogCaptureFixture) -> None:
    """A 409 from `stop` means the work already ended; it is neither logged
    nor allowed to break the loop."""
    fake = FakeWork(poll_script=[_StubWork(id="work_done")])

    def _stop(_work_id: str, **_kwargs: Any) -> None:
        raise _api_status_error(409)

    fake.stop = _stop  # type: ignore[method-assign]
    it = iter_work(cast(Any, fake), environment_id="env_1")

    _drain_one(it)
    with pytest.raises(_StopTest):
        next(it)
    assert len(fake.poll_calls) == 2
    assert not [r for r in caplog.records if "stop failed" in r.getMessage()]


def test_iter_work_backs_off_on_httpx_transport_error() -> None:
    """A raw `httpx` transport error (not wrapped in an SDK `APIError`) is
    still transient and must be retried, not propagated."""
    fake = FakeWork(poll_script=[httpx2.ConnectError("connection refused"), _StubWork(id="work_2")])
    it = iter_work(cast(Any, fake), environment_id="env_1")

    item = _drain_one(it)
    assert item.id == "work_2"
    assert len(fake.poll_calls) == 2


def test_iter_work_propagates_non_api_error_instead_of_retrying() -> None:
    """A programming error (here `KeyError`) is not a transient API/transport
    failure, so it must propagate immediately rather than be swallowed and
    retried forever. `poll` is only called once — no backoff/retry."""
    fake = FakeWork(poll_script=[KeyError("bug"), _StubWork(id="work_2")])
    it = iter_work(cast(Any, fake), environment_id="env_1")

    with pytest.raises(KeyError):
        next(it)
    assert len(fake.poll_calls) == 1


def test_iter_work_propagates_non_api_error_from_ack() -> None:
    """Same for a non-API error raised by `ack` — it propagates rather than
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


# ---------- idle-loop visibility ------------------------------------------
#
# An idle poller must show up in the logs without an INFO line per poll: one
# INFO line when it goes idle (after start-up or after releasing an item),
# DEBUG per empty poll after that, and an INFO reminder every 5 minutes.


class _FakeClock:
    """Stands in for the `time` module inside the poller: a settable
    monotonic clock plus a no-op `sleep`."""

    def __init__(self) -> None:
        self.now = 0.0

    def monotonic(self) -> float:
        return self.now

    def sleep(self, _seconds: float) -> None:
        return None

    def advance(self, seconds: float) -> None:
        self.now += seconds


def _idle_script(clock: _FakeClock) -> list[Any]:
    """Three empty polls, a fourth 301s later, a fifth, one claim, then one
    more empty poll before the script runs out."""

    def empty_poll_301s_later() -> None:
        clock.advance(301)

    return [None, None, None, empty_poll_301s_later, None, _StubWork(id="work_a"), None]


_EXPECTED_IDLE_INFO_LINES = [
    "idle; polling environment_id=env_1 for work",
    "still polling environment_id=env_1; idle for 301s",
    "claimed work work_id=work_a work_type=session",
    "idle; polling environment_id=env_1 for work",
]


def _poller_records(caplog: pytest.LogCaptureFixture, level: int) -> list[str]:
    return [
        r.getMessage()
        for r in caplog.records
        if r.name == poller_mod.__name__ and r.levelno == level and not r.getMessage().startswith("poller starting")
    ]


def test_iter_work_logs_idle_polling(monkeypatch: pytest.MonkeyPatch, caplog: pytest.LogCaptureFixture) -> None:
    clock = _FakeClock()
    monkeypatch.setattr(poller_mod, "time", clock)
    fake = FakeWork(poll_script=_idle_script(clock))
    caplog.set_level(logging.DEBUG, logger=poller_mod.__name__)

    with pytest.raises(_StopTest):
        for _ in iter_work(cast(Any, fake), environment_id="env_1", auto_stop=False):
            pass

    assert _poller_records(caplog, logging.INFO) == _EXPECTED_IDLE_INFO_LINES
    assert len(_poller_records(caplog, logging.DEBUG)) == 3


@pytest.mark.asyncio()
async def test_aiter_work_logs_idle_polling(monkeypatch: pytest.MonkeyPatch, caplog: pytest.LogCaptureFixture) -> None:
    clock = _FakeClock()
    monkeypatch.setattr(poller_mod, "time", clock)
    monkeypatch.setattr(poller_mod.anyio, "sleep", _async_noop)
    fake = FakeAsyncWork(poll_script=_idle_script(clock))
    caplog.set_level(logging.DEBUG, logger=poller_mod.__name__)

    with pytest.raises(_StopTest):
        async for _ in aiter_work(cast(Any, fake), environment_id="env_1", auto_stop=False):
            pass

    assert _poller_records(caplog, logging.INFO) == _EXPECTED_IDLE_INFO_LINES
    assert len(_poller_records(caplog, logging.DEBUG)) == 3


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
@pytest.mark.parametrize("status", [500, 409])
async def test_aiter_work_backs_off_on_transient_error(status: int) -> None:
    fake = FakeAsyncWork(poll_script=[_api_status_error(status), _StubWork(id="work_2")])
    ait = aiter_work(cast(Any, fake), environment_id="env_1")

    item = await _adrain_one(ait)
    assert item.id == "work_2"
    assert len(fake.poll_calls) == 2


@pytest.mark.asyncio()
async def test_aiter_work_stop_conflict_is_silent(caplog: pytest.LogCaptureFixture) -> None:
    fake = FakeAsyncWork(poll_script=[_StubWork(id="work_done")])

    async def _stop(_work_id: str, **_kwargs: Any) -> None:
        raise _api_status_error(409)

    fake.stop = _stop  # type: ignore[method-assign]
    ait = aiter_work(cast(Any, fake), environment_id="env_1")

    await _adrain_one(ait)
    with pytest.raises(_StopTest):
        await ait.__anext__()
    assert len(fake.poll_calls) == 2
    assert not [r for r in caplog.records if "stop failed" in r.getMessage()]


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
# These assert the caller-supplied `extra_headers` actually reaches every
# underlying `poll` / `ack` / `stop` call (the resource methods route it
# through `make_request_options`). The fakes record the kwargs each method
# was called with, so a missing thread-through shows up as `None`.

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


# ---------- the OpenTelemetry span of each work item -------------------------
#
# These go through a real client, so that the spans of the poller's own requests
# are there to be the children of the item's span.


def _work_json(work_id: str) -> dict[str, Any]:
    return {
        "id": work_id,
        "type": "work",
        "environment_id": "env_1",
        "state": "active",
        "created_at": "2026-01-01T00:00:00Z",
        "metadata": {},
        "data": {"type": "session", "id": f"sesn_{work_id}"},
    }


NO_WORK = httpx2.Response(200, content=b"null", headers={"content-type": "application/json"})


def _mock_work_api(
    respx_mock: MockRouter, polls: list[httpx2.Response], actions: tuple[str, ...] = ("ack", "stop")
) -> None:
    respx_mock.get("/v1/environments/env_1/work/poll").mock(side_effect=polls)
    for action in actions:
        respx_mock.post(path__regex=rf"/v1/environments/env_1/work/\w+/{action}").mock(
            return_value=httpx2.Response(200, json=_work_json("work_1"))
        )


class _StartAttributes(sampling.Sampler):
    """Keeps the attributes that each span starts with, which is all that a sampler is given."""

    def __init__(self) -> None:
        self.started: dict[str, dict[str, Any]] = {}

    @override
    def should_sample(self, *args: Any, **kwargs: Any) -> sampling.SamplingResult:
        name, attributes = kwargs.get("name", args[2] if len(args) > 2 else None), kwargs.get("attributes")
        self.started[str(name)] = dict(attributes or (args[4] if len(args) > 4 else None) or {})
        return sampling.ALWAYS_ON.should_sample(*args, **kwargs)

    @override
    def get_description(self) -> str:
        return "start attributes"


@pytest.mark.respx(base_url=base_url)
@pytest.mark.parametrize("sync", [True, False], ids=["sync", "async"])
async def test_each_work_item_has_a_span_until_the_next_item(sync: bool, respx_mock: MockRouter) -> None:
    spans = Spans()
    sampler = _StartAttributes()
    spans.provider = TracerProvider(sampler=sampler)
    spans.provider.add_span_processor(SimpleSpanProcessor(spans.exporter))
    _mock_work_api(
        respx_mock,
        [
            httpx2.Response(200, json=_work_json("work_1")),
            httpx2.Response(200, json=_work_json("work_2")),
            NO_WORK,
        ],
    )
    # What the consumer sees while it has each item: the current span, and how many item spans have ended.
    seen: list[tuple[str, int, int]] = []

    def consume(item: Any) -> None:
        seen.append((item.id, span_id(trace.get_current_span()), len(spans.named("anthropic.environment.work"))))
        with app.start_as_current_span("app.handle"):
            pass

    app = spans.provider.get_tracer("app")
    with app.start_as_current_span("app") as app_span:
        if sync:
            client = Anthropic(base_url=base_url, api_key="key", open_telemetry=spans.option())
            for item in iter_work(client.beta.environments.work, environment_id="env_1", block_ms=None, drain=True):
                consume(item)
        else:
            async_client = AsyncAnthropic(base_url=base_url, api_key="key", open_telemetry=spans.option())
            async for item in async_client.beta.environments.work.poller(
                environment_id="env_1", environment_key="env_key", block_ms=None, drain=True
            ):
                consume(item)

    # An item's span is open, and not current, in the consumer's code, and asking for the next item ends it.
    assert seen == [("work_1", span_id(app_span), 0), ("work_2", span_id(app_span), 1)]
    first, second = spans.named("anthropic.environment.work")
    for work_span, work_id in ((first, "work_1"), (second, "work_2")):
        assert parent_id(work_span) == span_id(app_span)
        assert work_span.kind == SpanKind.INTERNAL
        assert work_span.status.status_code == StatusCode.OK
        assert attributes(work_span) == {
            "gen_ai.provider.name": "anthropic",
            "anthropic.environment.id": "env_1",
            "anthropic.environment.work.id": work_id,
            "anthropic.session.id": f"sesn_{work_id}",
        }
    assert sampler.started["anthropic.environment.work"] == attributes(second)
    # The requests for an item are in its span, and a poll is in the span that is current when it is sent.
    for name in ("anthropic.environments.work.ack", "anthropic.environments.work.stop"):
        assert [parent_id(span) for span in spans.named(name)] == [span_id(first), span_id(second)]
    assert {parent_id(span) for span in spans.named("anthropic.environments.work.poll")} == {span_id(app_span)}
    # So is a span that the consumer starts for an item, which makes it a sibling of the item's span.
    assert [parent_id(span) for span in spans.named("app.handle")] == [span_id(app_span)] * 2


@pytest.mark.respx(base_url=base_url)
@pytest.mark.parametrize("sync", [True, False], ids=["sync", "async"])
async def test_work_span_ends_ok_when_the_consumer_stops_polling(sync: bool, respx_mock: MockRouter) -> None:
    spans = Spans()
    # The consumer owns the stop request, so the poller sends none.
    _mock_work_api(respx_mock, [httpx2.Response(200, json=_work_json("work_1"))], actions=("ack",))

    if sync:
        client = Anthropic(base_url=base_url, api_key="key", open_telemetry=spans.option())
        items = iter_work(client.beta.environments.work, environment_id="env_1", auto_stop=False)
        next(items)
        assert spans.named("anthropic.environment.work") == []
        cast(Any, items).close()
    else:
        async_client = AsyncAnthropic(base_url=base_url, api_key="key", open_telemetry=spans.option())
        async_items = async_client.beta.environments.work.poller(
            environment_id="env_1", environment_key="env_key", auto_stop=False
        )
        await async_items.__anext__()
        assert spans.named("anthropic.environment.work") == []
        await cast(Any, async_items).aclose()

    work_span = spans.one("anthropic.environment.work")
    assert work_span.status.status_code == StatusCode.OK
    # No span was current around the consumer's calls, so the item's span is a root span.
    assert work_span.parent is None


@pytest.mark.respx(base_url=base_url)
@pytest.mark.parametrize("sync", [True, False], ids=["sync", "async"])
async def test_work_span_fails_when_the_item_cannot_be_acked(sync: bool, respx_mock: MockRouter) -> None:
    spans = Spans()
    respx_mock.get("/v1/environments/env_1/work/poll").mock(
        side_effect=[httpx2.Response(200, json=_work_json("work_1")), NO_WORK]
    )
    error = {"type": "error", "error": {"type": "not_found_error", "message": "No such work."}}
    respx_mock.post("/v1/environments/env_1/work/work_1/ack").mock(return_value=httpx2.Response(404, json=error))
    respx_mock.post("/v1/environments/env_1/work/work_1/stop").mock(
        return_value=httpx2.Response(200, json=_work_json("work_1"))
    )

    if sync:
        client = Anthropic(base_url=base_url, api_key="key", open_telemetry=spans.option())
        work = client.beta.environments.work
        assert list(iter_work(work, environment_id="env_1", block_ms=None, drain=True)) == []
    else:
        async_client = AsyncAnthropic(base_url=base_url, api_key="key", open_telemetry=spans.option())
        poller = async_client.beta.environments.work.poller(
            environment_id="env_1", environment_key="env_key", block_ms=None, drain=True
        )
        assert [item async for item in poller] == []

    work_span = spans.one("anthropic.environment.work")
    assert work_span.status.status_code == StatusCode.ERROR
    # The type of the failed request's span.
    ack = spans.one("anthropic.environments.work.ack")
    assert attributes(work_span)["error.type"] == attributes(ack)["error.type"] == "not_found_error"
    assert parent_id(spans.one("anthropic.environments.work.stop")) == span_id(work_span)


# The router does not count a request that its route interrupts.
@pytest.mark.respx(base_url=base_url, assert_all_called=False)
@pytest.mark.parametrize("sync", [True, False], ids=["sync", "async"])
async def test_work_span_has_no_status_when_polling_is_interrupted_during_the_ack(
    sync: bool, respx_mock: MockRouter
) -> None:
    spans = Spans()
    respx_mock.get("/v1/environments/env_1/work/poll").mock(
        return_value=httpx2.Response(200, json=_work_json("work_1"))
    )
    # Neither is an `Exception`: each is the application stopping the poller, as `KeyboardInterrupt` is.
    interrupt = _StopTest if sync else asyncio.CancelledError

    def interrupted(_request: httpx2.Request) -> httpx2.Response:
        raise interrupt

    respx_mock.post("/v1/environments/env_1/work/work_1/ack").mock(side_effect=interrupted)

    with pytest.raises(interrupt):
        if sync:
            client = Anthropic(base_url=base_url, api_key="key", open_telemetry=spans.option())
            next(iter_work(client.beta.environments.work, environment_id="env_1"))
        else:
            async_client = AsyncAnthropic(base_url=base_url, api_key="key", open_telemetry=spans.option())
            poller = async_client.beta.environments.work.poller(environment_id="env_1", environment_key="env_key")
            await poller.__anext__()

    work_span = spans.one("anthropic.environment.work")
    assert work_span.status.status_code == StatusCode.UNSET
    assert "error.type" not in attributes(work_span)


async def _polled_work_ids(sync: bool, open_telemetry: Any) -> list[str]:
    """The IDs of the items that a draining poller of a client with `open_telemetry` gives."""
    if sync:
        client = Anthropic(base_url=base_url, api_key="key", open_telemetry=open_telemetry)
        work = client.beta.environments.work
        return [item.id for item in iter_work(work, environment_id="env_1", block_ms=None, drain=True)]
    async_client = AsyncAnthropic(base_url=base_url, api_key="key", open_telemetry=open_telemetry)
    poller = async_client.beta.environments.work.poller(
        environment_id="env_1", environment_key="env_key", block_ms=None, drain=True
    )
    return [item.id async for item in poller]


@pytest.mark.respx(base_url=base_url)
@pytest.mark.parametrize("sync", [True, False], ids=["sync", "async"])
async def test_a_work_item_without_data_is_acked_and_given_with_a_span(sync: bool, respx_mock: MockRouter) -> None:
    spans = Spans()
    _mock_work_api(respx_mock, [httpx2.Response(200, json={**_work_json("work_1"), "data": None}), NO_WORK])

    assert await _polled_work_ids(sync, spans.option()) == ["work_1"]

    assert respx_mock.calls.call_count == 4
    work_span = spans.one("anthropic.environment.work")
    assert work_span.status.status_code == StatusCode.OK
    assert attributes(work_span) == {
        "gen_ai.provider.name": "anthropic",
        "anthropic.environment.id": "env_1",
        "anthropic.environment.work.id": "work_1",
    }


@TRACING_FAILURES
@pytest.mark.respx(base_url=base_url)
@pytest.mark.parametrize("sync", [True, False], ids=["sync", "async"])
async def test_tracing_that_fails_leaves_the_poller_as_it_is(sync: bool, failure: str, respx_mock: MockRouter) -> None:
    _mock_work_api(
        respx_mock,
        [
            httpx2.Response(200, json=_work_json("work_1")),
            httpx2.Response(200, json=_work_json("work_2")),
            NO_WORK,
        ],
    )

    assert await _polled_work_ids(sync, failing_tracing(failure)) == ["work_1", "work_2"]

    # Three polls, and an ack and a stop for each item.
    assert respx_mock.calls.call_count == 7
