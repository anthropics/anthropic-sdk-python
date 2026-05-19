"""Tests for :class:`SessionToolRunner` (the implementation behind
``client.beta.sessions.events.tool_runner()``).

We use lightweight stand-ins for ``AsyncEvents`` so each test can script the
sequence of stream events, list events (for the reconcile pass), and per-call
send failures. ``asyncio.sleep`` is left real so ``await asyncio.sleep(0)`` in
the fake stream actually yields control to the event loop.
"""

from __future__ import annotations

import asyncio
from typing import Any, Optional, cast
from collections.abc import Callable, Awaitable, AsyncIterator

import httpx
import pytest

from anthropic import APIStatusError
from anthropic._compat import PYDANTIC_V1
from anthropic.lib.tools import ToolError, _beta_session_runner as session_runner_mod
from anthropic.lib.tools._beta_session_runner import (
    SessionToolRunner,
    DispatchedToolCall,
)


@pytest.fixture(autouse=True)
def _intercept_scoped_client(monkeypatch: pytest.MonkeyPatch) -> None:  # pyright: ignore[reportUnusedFunction]
    """Make ``_scoped_client`` return the parent client unchanged so the runner's
    requests land on the test fakes.

    The real ``_scoped_client`` builds an ``AsyncAnthropic`` sub-client for
    request scoping; the tests use a ``_FakeClient`` whose only API surface is
    ``.beta.sessions.events``, so the sub-client construction would fail. The
    auth-specific tests further down install their own ``_scoped_client``
    override (via the ``scoped_calls`` fixture) to assert on the args.
    """

    def passthrough(client: Any, _key: str | None) -> Any:
        return client

    monkeypatch.setattr(session_runner_mod, "_scoped_client", passthrough)


@pytest.fixture()
def scoped_calls(monkeypatch: pytest.MonkeyPatch) -> list[dict[str, Any]]:
    """Record every ``_scoped_client(client, environment_key)`` call; still
    returns the parent client (the autouse fixture's behaviour) so the runner
    keeps using the test fakes."""
    calls: list[dict[str, Any]] = []

    def fake_factory(client: Any, environment_key: str | None) -> Any:
        calls.append({"environment_key": environment_key})
        return client

    monkeypatch.setattr(session_runner_mod, "_scoped_client", fake_factory)
    return calls


class _StubEvent:
    """Stand-in for the various session event types — only the fields the
    runner reads are populated."""

    def __init__(self, type: str, **kw: Any) -> None:
        self.type = type
        for k, v in kw.items():
            setattr(self, k, v)


def _tool_use(id: str, name: str, input: dict[str, Any]) -> _StubEvent:
    return _StubEvent("agent.tool_use", id=id, name=name, input=input)


def _tool_result(tool_use_id: str) -> _StubEvent:
    return _StubEvent("user.tool_result", tool_use_id=tool_use_id)


def _custom_tool_use(id: str, name: str, input: dict[str, Any]) -> _StubEvent:
    """A CUSTOM (user-defined) tool call — the agent emits ``agent.custom_tool_use``
    rather than ``agent.tool_use`` for these."""
    return _StubEvent("agent.custom_tool_use", id=id, name=name, input=input)


def _custom_tool_result(custom_tool_use_id: str) -> _StubEvent:
    return _StubEvent("user.custom_tool_result", custom_tool_use_id=custom_tool_use_id)


def _terminated() -> _StubEvent:
    return _StubEvent("session.status_terminated")


def _idle_end_turn() -> _StubEvent:
    return _StubEvent("session.status_idle", stop_reason=_StubEvent("end_turn"))


def _result_content(item: DispatchedToolCall) -> Any:
    """The content blocks the runner computed and posted back, as carried in
    ``result`` (the flat ``content`` convenience field was removed)."""
    return cast(Any, item.result)["content"]


def _result_text(item: DispatchedToolCall) -> str:
    """Concatenated text of the posted-back result's text blocks."""
    return "".join(b.get("text", "") for b in _result_content(item) if b.get("type") == "text")


def _api_status_error(code: int) -> APIStatusError:
    request = httpx.Request("POST", "https://api.example/x")
    response = httpx.Response(status_code=code, request=request, content=b"{}")
    return APIStatusError("boom", response=response, body=None)


class _FakeStream:
    """Stand-in for the AsyncStream returned by ``events.stream()``.

    Yields scripted events in order; once exhausted, blocks forever (the real
    stream stays open until a network event closes it). If ``raise_after`` is
    set, raises ``raise_with`` after producing that many events — used to
    exercise the reconnect-with-backoff path.
    """

    def __init__(
        self,
        events: list[_StubEvent],
        *,
        raise_after: int | None = None,
        raise_with: BaseException | None = None,
    ) -> None:
        self._events = events
        self._raise_after = raise_after
        self._raise_with = raise_with

    async def __aenter__(self) -> _FakeStream:
        return self

    async def __aexit__(self, *exc: object) -> None:
        return None

    def __aiter__(self) -> Any:
        return self._gen()

    async def _gen(self) -> Any:
        for i, ev in enumerate(self._events):
            yield ev
            # Yield control so the dispatch task can pick up the event we just
            # produced before we run on to the next one.
            await asyncio.sleep(0)
            if self._raise_after is not None and i + 1 == self._raise_after:
                assert self._raise_with is not None
                raise self._raise_with
        # Keep the connection "open" until cancelled.
        await asyncio.Event().wait()


class FakeAsyncEvents:
    def __init__(
        self,
        *,
        streams: list[_FakeStream | BaseException] | None = None,
        stream_events: list[_StubEvent] | None = None,
        list_events: list[_StubEvent] | None = None,
        list_raises: BaseException | None = None,
        send_failures: list[BaseException | None] | None = None,
    ) -> None:
        if streams is not None:
            self._streams: list[_FakeStream | BaseException] = list(streams)
        elif stream_events is not None:
            self._streams = [_FakeStream(stream_events)]
        else:
            self._streams = [_FakeStream([])]
        self._list_events = list(list_events or [])
        self._list_raises = list_raises
        self._send_failures: list[BaseException | None] = list(send_failures or [])
        self.send_calls: list[dict[str, Any]] = []
        self.stream_calls: int = 0
        self.stream_headers: list[Any] = []
        self.list_headers: list[Any] = []

    async def stream(self, _session_id: str, *, extra_headers: Any = None) -> _FakeStream:
        self.stream_calls += 1
        self.stream_headers.append(extra_headers)
        if not self._streams:
            return _FakeStream([])  # block forever; mirrors a fresh connection
        nxt = self._streams.pop(0)
        if isinstance(nxt, BaseException):
            raise nxt
        return nxt

    def list(self, _session_id: str, *, limit: int = 1000, extra_headers: Any = None) -> Any:  # noqa: ARG002
        list_raises = self._list_raises
        self.list_headers.append(extra_headers)

        async def _gen() -> Any:
            for ev in self._list_events:
                yield ev
            if list_raises is not None:
                raise list_raises

        return _gen()

    async def send(self, session_id: str, *, events: list[Any], extra_headers: Any = None) -> None:
        idx = len(self.send_calls)
        self.send_calls.append({"session_id": session_id, "events": events, "extra_headers": extra_headers})
        if idx < len(self._send_failures):
            err = self._send_failures[idx]
            if err is not None:
                raise err


class _FakeTool:
    def __init__(
        self,
        name: str,
        fn: Callable[[dict[str, Any]], Awaitable[Any]],
        *,
        close: Callable[[], Any] | None = None,
    ) -> None:
        self.name = name
        self._fn = fn
        if close is not None:
            self.close = close

    def call(self, input: dict[str, Any]) -> Any:
        return self._fn(input)


class _FakeClient:
    """Minimal stand-in for ``AsyncAnthropic`` — only exposes the resource path
    the runner reads."""

    def __init__(self, events: FakeAsyncEvents) -> None:
        self.beta = type(
            "_Beta",
            (),
            {"sessions": type("_Sessions", (), {"events": events})()},
        )()


async def _run_with_fakes(
    *,
    events: FakeAsyncEvents,
    tools: list[Any],
    max_idle: float | None = None,
    environment_key: str | None = None,
    extra_headers: dict[str, Any] | None = None,
) -> AsyncIterator[DispatchedToolCall]:
    client = _FakeClient(events)
    runner = SessionToolRunner(
        cast(Any, client),
        "s_1",
        tools=tools,
        max_idle=max_idle,
        environment_key=environment_key,
        extra_headers=extra_headers,
    )
    async for call in runner:
        yield call


# ---------- happy-path / basic termination ---------------------------------


@pytest.mark.asyncio()
async def test_yields_completed_tool_call() -> None:
    async def echo(input: dict[str, Any]) -> str:
        return f"got {input.get('x')}"

    tool = _FakeTool("echo", echo)
    events = FakeAsyncEvents(stream_events=[_tool_use("tu_1", "echo", {"x": 42}), _terminated()])

    items = [item async for item in _run_with_fakes(events=events, tools=[tool])]

    assert len(items) == 1
    item = items[0]
    assert isinstance(item, DispatchedToolCall)
    assert item.tool_use_id == "tu_1"
    assert item.name == "echo"
    assert item.event.input == {"x": 42}
    assert item.is_error is False
    assert item.posted is True
    assert _result_text(item) == "got 42"
    # The reshaped DispatchedToolCall embeds the originating event and the
    # posted-back result block, alongside the flat convenience fields.
    assert item.event.id == "tu_1"
    assert item.result["type"] == "user.tool_result"
    assert item.result["tool_use_id"] == "tu_1"
    assert item.result.get("is_error") is False

    assert len(events.send_calls) == 1
    sent = events.send_calls[0]["events"][0]
    assert sent["type"] == "user.tool_result"
    assert sent["tool_use_id"] == "tu_1"
    assert sent["is_error"] is False


@pytest.mark.asyncio()
async def test_yields_error_for_failing_tool() -> None:
    async def boom(_input: dict[str, Any]) -> str:
        raise RuntimeError("nope")

    tool = _FakeTool("boom", boom)
    events = FakeAsyncEvents(stream_events=[_tool_use("tu_1", "boom", {}), _terminated()])

    items = [item async for item in _run_with_fakes(events=events, tools=[tool])]

    assert len(items) == 1
    assert items[0].is_error is True
    assert items[0].posted is True
    assert "RuntimeError" in _result_text(items[0])


@pytest.mark.asyncio()
async def test_yields_error_for_unknown_tool() -> None:
    events = FakeAsyncEvents(stream_events=[_tool_use("tu_1", "missing", {}), _terminated()])

    items = [item async for item in _run_with_fakes(events=events, tools=[])]

    assert len(items) == 1
    assert items[0].is_error is True
    assert "not implemented" in _result_text(items[0])


@pytest.mark.asyncio()
async def test_skips_already_answered_events() -> None:
    """Tool result already in history (via reconcile) should suppress
    re-execution of the same tool_use seen on the live stream."""
    counter = {"calls": 0}

    async def increment(_input: dict[str, Any]) -> str:
        counter["calls"] += 1
        return "done"

    tool = _FakeTool("inc", increment)
    events = FakeAsyncEvents(
        list_events=[_tool_use("tu_1", "inc", {}), _tool_result("tu_1")],
        stream_events=[_tool_use("tu_1", "inc", {}), _terminated()],
    )

    items = [item async for item in _run_with_fakes(events=events, tools=[tool])]

    assert counter["calls"] == 0
    assert items == []


# ---------- custom-tool dispatch ------------------------------------------


@pytest.mark.asyncio()
async def test_yields_completed_custom_tool_call() -> None:
    """A CUSTOM (user-defined) tool call arrives as ``agent.custom_tool_use`` and
    must be answered with ``user.custom_tool_result`` — keyed by
    ``custom_tool_use_id`` — not ``user.tool_result``."""

    async def weather(input: dict[str, Any]) -> str:
        return f"sunny in {input.get('city')}"

    tool = _FakeTool("get_weather", weather)
    events = FakeAsyncEvents(stream_events=[_custom_tool_use("ctu_1", "get_weather", {"city": "SF"}), _terminated()])

    items = [item async for item in _run_with_fakes(events=events, tools=[tool])]

    assert len(items) == 1
    item = items[0]
    assert item.tool_use_id == "ctu_1"
    assert item.name == "get_weather"
    assert item.event.input == {"city": "SF"}
    assert item.is_error is False
    assert item.posted is True
    assert _result_text(item) == "sunny in SF"
    # The embedded event is the custom-tool-use event, and the posted-back
    # result is a custom tool result keyed by custom_tool_use_id.
    assert item.event.type == "agent.custom_tool_use"
    result = cast(Any, item.result)
    assert result["type"] == "user.custom_tool_result"
    assert result["custom_tool_use_id"] == "ctu_1"
    assert result.get("is_error") is False

    assert len(events.send_calls) == 1
    sent = events.send_calls[0]["events"][0]
    assert sent["type"] == "user.custom_tool_result"
    assert sent["custom_tool_use_id"] == "ctu_1"
    assert sent["is_error"] is False


@pytest.mark.asyncio()
async def test_dispatches_builtin_and_custom_tools_in_one_stream() -> None:
    """A single stream carrying both an ``agent.tool_use`` and an
    ``agent.custom_tool_use`` dispatches both, each answered with its matching
    result-event type."""

    async def echo(input: dict[str, Any]) -> str:
        return f"echo {input.get('x')}"

    async def weather(_input: dict[str, Any]) -> str:
        return "sunny"

    events = FakeAsyncEvents(
        stream_events=[
            _tool_use("tu_1", "echo", {"x": 1}),
            _custom_tool_use("ctu_1", "get_weather", {}),
            _terminated(),
        ]
    )

    items = [
        item
        async for item in _run_with_fakes(
            events=events, tools=[_FakeTool("echo", echo), _FakeTool("get_weather", weather)]
        )
    ]

    by_id = {it.tool_use_id: it for it in items}
    assert set(by_id) == {"tu_1", "ctu_1"}
    assert by_id["tu_1"].event.type == "agent.tool_use"
    assert by_id["tu_1"].result["type"] == "user.tool_result"
    assert by_id["ctu_1"].event.type == "agent.custom_tool_use"
    assert by_id["ctu_1"].result["type"] == "user.custom_tool_result"
    # Both result events were posted, each with the matching type.
    posted = {call["events"][0]["type"] for call in events.send_calls}
    assert posted == {"user.tool_result", "user.custom_tool_result"}


@pytest.mark.asyncio()
async def test_skips_already_answered_custom_tool() -> None:
    """A custom tool whose ``user.custom_tool_result`` is already in history (via
    reconcile) is not re-executed when the same ``agent.custom_tool_use`` is then
    seen on the live stream."""
    counter = {"calls": 0}

    async def weather(_input: dict[str, Any]) -> str:
        counter["calls"] += 1
        return "sunny"

    events = FakeAsyncEvents(
        list_events=[_custom_tool_use("ctu_1", "get_weather", {}), _custom_tool_result("ctu_1")],
        stream_events=[_custom_tool_use("ctu_1", "get_weather", {}), _terminated()],
    )

    items = [item async for item in _run_with_fakes(events=events, tools=[_FakeTool("get_weather", weather)])]

    assert counter["calls"] == 0
    assert items == []


@pytest.mark.asyncio()
async def test_idle_after_end_turn_ends_iteration() -> None:
    # The session goes idle with stop_reason end_turn and nothing else happens;
    # after ``max_idle`` seconds the runner stops on its own.
    events = FakeAsyncEvents(stream_events=[_idle_end_turn()])

    items = [item async for item in _run_with_fakes(events=events, tools=[], max_idle=0.05)]

    assert items == []


@pytest.mark.asyncio()
async def test_idle_grace_does_not_fire_without_end_turn() -> None:
    # No end_turn idle is ever seen, so the grace timer never arms — the runner
    # only stops because the stream delivers a terminated event.
    async def echo(input: dict[str, Any]) -> str:
        return f"got {input.get('x')}"

    events = FakeAsyncEvents(stream_events=[_tool_use("tu_1", "echo", {"x": 1}), _terminated()])

    items = [item async for item in _run_with_fakes(events=events, tools=[_FakeTool("echo", echo)], max_idle=0.05)]

    assert [it.tool_use_id for it in items] == ["tu_1"]


@pytest.mark.asyncio()
async def test_new_event_resets_idle_grace() -> None:
    # end_turn arms the grace timer, then a tool_use arrives and resets it; the
    # tool is dispatched and the runner only stops on the terminated event.
    async def echo(input: dict[str, Any]) -> str:
        return f"got {input.get('x')}"

    events = FakeAsyncEvents(stream_events=[_idle_end_turn(), _tool_use("tu_1", "echo", {"x": 1}), _terminated()])

    # Generous grace so the timer can't fire between the scripted events.
    items = [item async for item in _run_with_fakes(events=events, tools=[_FakeTool("echo", echo)], max_idle=5.0)]

    assert [it.tool_use_id for it in items] == ["tu_1"]


@pytest.mark.asyncio()
async def test_terminated_event_ends_iteration() -> None:
    events = FakeAsyncEvents(stream_events=[_terminated()])

    items = [item async for item in _run_with_fakes(events=events, tools=[])]

    assert items == []


# ---------- tool cleanup --------------------------------------------------


@pytest.mark.asyncio()
async def test_runs_tool_close_hook_on_exit() -> None:
    """The runner calls each tool's optional ``close`` cleanup hook when the
    iteration ends, regardless of cause."""
    closed = {"count": 0}

    def _close() -> None:
        closed["count"] += 1

    async def echo(_input: dict[str, Any]) -> str:
        return "ok"

    tool = _FakeTool("echo", echo, close=_close)
    events = FakeAsyncEvents(stream_events=[_tool_use("tu_1", "echo", {}), _terminated()])

    [_ async for _ in _run_with_fakes(events=events, tools=[tool])]

    assert closed["count"] == 1


@pytest.mark.asyncio()
async def test_awaits_async_tool_close_hook() -> None:
    closed = {"count": 0}

    async def _aclose() -> None:
        closed["count"] += 1

    async def echo(_input: dict[str, Any]) -> str:
        return "ok"

    tool = _FakeTool("echo", echo, close=_aclose)
    events = FakeAsyncEvents(stream_events=[_terminated()])

    [_ async for _ in _run_with_fakes(events=events, tools=[tool])]

    assert closed["count"] == 1


# ---------- send-result failure surfaces to consumer -----------------------


@pytest.mark.asyncio()
async def test_yields_with_posted_false_on_retry_exhaust() -> None:
    """If ``events.send`` fails on every retry attempt, the consumer should
    still receive the ``DispatchedToolCall`` with ``posted=False`` so they know
    the tool ran but the session-side agent never saw the result."""

    async def echo(_input: dict[str, Any]) -> str:
        return "result"

    tool = _FakeTool("echo", echo)
    events = FakeAsyncEvents(
        stream_events=[_tool_use("tu_1", "echo", {}), _terminated()],
        send_failures=[_api_status_error(500), _api_status_error(500), _api_status_error(500)],
    )

    items = [item async for item in _run_with_fakes(events=events, tools=[tool])]

    assert len(items) == 1
    assert items[0].posted is False
    # The tool itself succeeded — the failure is just the post-back.
    assert items[0].is_error is False
    assert _result_text(items[0]) == "result"
    assert len(events.send_calls) == 3  # used all 3 retries


@pytest.mark.asyncio()
async def test_yields_with_posted_false_on_permanent_4xx() -> None:
    """A permanent 4xx (e.g. 400) on send should short-circuit the retry loop
    after a single attempt and still yield with posted=False."""

    async def echo(_input: dict[str, Any]) -> str:
        return "result"

    tool = _FakeTool("echo", echo)
    events = FakeAsyncEvents(
        stream_events=[_tool_use("tu_1", "echo", {}), _terminated()],
        send_failures=[_api_status_error(400)],
    )

    items = [item async for item in _run_with_fakes(events=events, tools=[tool])]

    assert len(items) == 1
    assert items[0].posted is False
    assert len(events.send_calls) == 1  # no retry on permanent 4xx


# ---------- tool execution edge cases --------------------------------------


@pytest.mark.asyncio()
async def test_tool_timeout(monkeypatch: pytest.MonkeyPatch) -> None:
    """Tool that exceeds ``TOOL_TIMEOUT`` yields with ``is_error=True`` and a
    ``"timed out"`` message — distinct from the generic exception path."""
    monkeypatch.setattr(session_runner_mod, "TOOL_TIMEOUT", 0.05)

    async def slow(_input: dict[str, Any]) -> str:
        await asyncio.Event().wait()  # never resolves
        return "never"

    tool = _FakeTool("slow", slow)
    events = FakeAsyncEvents(stream_events=[_tool_use("tu_1", "slow", {}), _terminated()])

    items = [item async for item in _run_with_fakes(events=events, tools=[tool])]

    assert len(items) == 1
    assert items[0].is_error is True
    assert "timed out" in _result_text(items[0])


def test_tool_timeout_exceeds_bash_default() -> None:
    """``TOOL_TIMEOUT`` MUST stay strictly greater than the bash tool's own
    ``BASH_DEFAULT_TIMEOUT``.

    If they were equal the outer per-tool-call ``fail_after`` could win the
    race against the bash tool's inner ``fail_after``; anyio would then raise a
    plain parent-scope ``Cancelled`` (not ``TimeoutError``), the bash tool's
    ``except TimeoutError`` subprocess cleanup would never run, and the next
    bash call would read the previous (timed-out) command's stale output. This
    test pins the invariant so the two constants can't silently converge.
    """
    from anthropic.lib.tools.agent_toolset import BASH_DEFAULT_TIMEOUT

    assert session_runner_mod.TOOL_TIMEOUT > BASH_DEFAULT_TIMEOUT


@pytest.mark.asyncio()
async def test_tool_error_preserves_structured_content() -> None:
    """``ToolError`` raised by the tool preserves its structured content rather
    than being stringified through ``repr(e)``."""
    structured = [{"type": "text", "text": "structured error"}]

    async def boom(_input: dict[str, Any]) -> str:
        raise ToolError(content=cast(Any, structured))

    tool = _FakeTool("boom", boom)
    events = FakeAsyncEvents(stream_events=[_tool_use("tu_1", "boom", {}), _terminated()])

    items = [item async for item in _run_with_fakes(events=events, tools=[tool])]

    assert len(items) == 1
    assert items[0].is_error is True
    assert _result_content(items[0]) == structured


# ---------- stream-loop edge cases -----------------------------------------


@pytest.mark.asyncio()
async def test_stream_permanent_4xx_ends_iteration() -> None:
    """A permanent 4xx on the stream connect must not loop forever — the
    iterator should exit cleanly."""
    events = FakeAsyncEvents(streams=[_api_status_error(401)])

    items = [item async for item in _run_with_fakes(events=events, tools=[])]

    assert items == []
    # Should not have retried after the permanent 4xx.
    assert events.stream_calls == 1


@pytest.mark.asyncio()
async def test_reconcile_list_error_does_not_dispatch_partial() -> None:
    """If ``events.list`` errors mid-pagination, the partial ``pending`` list
    should not be enqueued — otherwise we'd risk re-running a tool whose result
    was on a page we never reached."""
    counter = {"calls": 0}

    async def increment(_input: dict[str, Any]) -> str:
        counter["calls"] += 1
        return "done"

    tool = _FakeTool("inc", increment)
    # The list yields a tool_use, then raises before we reach the result.
    # Without the fix this tool_use would be enqueued and re-executed.
    events = FakeAsyncEvents(
        list_events=[_tool_use("tu_1", "inc", {})],
        list_raises=_api_status_error(500),
        stream_events=[_terminated()],  # no live tool_use either
    )

    items = [item async for item in _run_with_fakes(events=events, tools=[tool])]

    assert items == []
    assert counter["calls"] == 0


# ---------- environment-key auth -----------------------------------------


@pytest.mark.asyncio()
async def test_environment_key_threads_through_to_scoped_client(scoped_calls: list[dict[str, Any]]) -> None:
    """When an environment key is set, the runner asks ``_scoped_client`` for a
    Bearer-only sub-client keyed to that environment. The actual header shape
    (``Authorization: Bearer …``, no ``X-Api-Key``, helper-telemetry on defaults)
    is the responsibility of ``_scoped_client`` itself — exercised separately in
    integration tests; here we just verify the runner threaded the right key."""

    async def echo(_input: dict[str, Any]) -> str:
        return "ok"

    tool = _FakeTool("echo", echo)
    events = FakeAsyncEvents(
        list_events=[],
        stream_events=[_tool_use("tu_1", "echo", {}), _terminated()],
    )

    [_ async for _ in _run_with_fakes(events=events, tools=[tool], environment_key="env_key")]

    assert scoped_calls == [{"environment_key": "env_key"}]


@pytest.mark.asyncio()
async def test_no_environment_key_threads_none_to_scoped_client(scoped_calls: list[dict[str, Any]]) -> None:
    """Without an environment key the runner still asks ``_scoped_client`` for a
    request client — passing ``None`` so the factory returns the parent client
    unchanged (just with a helper-telemetry header layered on)."""

    async def echo(_input: dict[str, Any]) -> str:
        return "ok"

    tool = _FakeTool("echo", echo)
    events = FakeAsyncEvents(stream_events=[_tool_use("tu_1", "echo", {}), _terminated()])

    [_ async for _ in _run_with_fakes(events=events, tools=[tool])]

    assert scoped_calls == [{"environment_key": None}]


@pytest.mark.asyncio()
async def test_session_runner_threads_extra_headers_into_stream_list_and_send() -> None:
    """A caller-supplied ``extra_headers`` is threaded, unchanged, into every
    per-request call the runner makes: the event ``stream``, the history
    ``list``, and each result ``send``.

    The runner does no header munging — it just passes the caller's mapping
    to each call's ``extra_headers=``. Auth is handled by the scoped
    sub-client the runner builds from ``environment_key``, independent of
    this passthrough."""

    async def echo(_input: dict[str, Any]) -> str:
        return "ok"

    tool = _FakeTool("echo", echo)
    events = FakeAsyncEvents(
        list_events=[],
        stream_events=[_tool_use("tu_1", "echo", {}), _terminated()],
    )

    extras = {"x-trace-id": "abc123"}
    [
        _
        async for _ in _run_with_fakes(
            events=events,
            tools=[tool],
            environment_key="env_key",
            extra_headers=extras,
        )
    ]

    assert events.stream_headers[0] == extras
    assert events.list_headers[0] == extras
    assert events.send_calls[0]["extra_headers"] == extras


@pytest.mark.asyncio()
@pytest.mark.skipif(PYDANTIC_V1, reason="tool functions are only supported with pydantic v2")
async def test_runs_context_manager_tool_cleanup_on_exit() -> None:
    """A tool defined as an ``@asynccontextmanager`` via ``@beta_async_tool``
    has its ``__aexit__`` driven by the runner cleanup path, additively to the
    legacy ``close`` hook."""
    from contextlib import asynccontextmanager

    from anthropic.types.beta import BetaManagedAgentsAgentToolset20260401BashInput
    from anthropic.lib.tools._beta_functions import beta_async_tool

    events_seen: list[str] = []

    @asynccontextmanager
    async def echo_cm() -> AsyncIterator[Callable[..., Awaitable[str]]]:
        events_seen.append("enter")

        # ``Optional[str]`` (not ``str | None``) because ``@beta_async_tool``
        # evaluates these annotations at runtime via pydantic, and PEP 604 union
        # syntax can't be ``eval``'d under Python 3.9 — our minimum version.
        async def echo(command: Optional[str] = None) -> str:
            return f"echo:{command}"

        try:
            yield echo
        finally:
            events_seen.append("exit")

    echo_tool = beta_async_tool(name="echo", input_schema=BetaManagedAgentsAgentToolset20260401BashInput)(
        cast(Any, echo_cm)
    )

    fake_events = FakeAsyncEvents(stream_events=[_tool_use("tu_1", "echo", {"command": "hi"}), _terminated()])
    calls = [c async for c in _run_with_fakes(events=fake_events, tools=[echo_tool])]

    assert [_result_text(c) for c in calls] == ["echo:hi"]
    # Entered lazily on first dispatch, exited on runner cleanup.
    assert events_seen == ["enter", "exit"]


# ---------- resource-method wrapper ---------------------------------------


@pytest.mark.asyncio()
async def test_tool_runner_method_returns_session_tool_runner() -> None:
    from anthropic import AsyncAnthropic

    client = AsyncAnthropic(api_key="dummy")
    runner = client.beta.sessions.events.tool_runner("s_1", tools=[])
    assert isinstance(runner, SessionToolRunner)
    assert runner.session_id == "s_1"


@pytest.mark.asyncio()
async def test_until_done_drives_runner_to_completion() -> None:
    """``until_done()`` (renamed from ``run()`` to match ``BetaToolRunner`` and
    avoid colliding with ``EnvironmentWorker.run``'s forever-loop) drives the
    runner to the session end, discarding per-call observations."""
    calls = {"n": 0}

    async def echo(_input: dict[str, Any]) -> str:
        calls["n"] += 1
        return "ok"

    tool = _FakeTool("echo", echo)
    events = FakeAsyncEvents(stream_events=[_tool_use("tu_1", "echo", {}), _terminated()])
    client = _FakeClient(events)
    runner = SessionToolRunner(cast(Any, client), "s_1", tools=cast(Any, [tool]), max_idle=None)

    # The old name is gone; the new one exists and returns at session end.
    assert not hasattr(runner, "run")
    await runner.until_done()
    assert calls["n"] == 1
    assert len(events.send_calls) == 1


def test_environments_public_reexports() -> None:
    """A user can type their own code against the public runner API without
    reaching into a ``_``-private module."""
    from anthropic.lib import environments as env_pkg

    for name in (
        "BetaAnyRunnableTool",
        "DispatchedToolCall",
        "DispatchedToolUseEvent",
        "DispatchedToolResultParams",
        "download_session_skills",
        "SessionToolRunner",
    ):
        assert name in env_pkg.__all__, name
        assert getattr(env_pkg, name) is not None, name

    # The old ``RunnableTool`` name was renamed to ``BetaAnyRunnableTool``; it
    # must be fully gone (it had no released consumers).
    assert "RunnableTool" not in env_pkg.__all__
    assert not hasattr(env_pkg, "RunnableTool")


# ---------- _to_session_content ---------------------------------------------


def _to_session_content(content: Any) -> list[Any]:
    return cast("list[Any]", session_runner_mod._to_session_content(content))  # pyright: ignore[reportPrivateUsage]


def test_to_session_content_text_passthrough() -> None:
    out = _to_session_content([{"type": "text", "text": "hello"}])
    assert out == [{"type": "text", "text": "hello"}]


def test_to_session_content_image_passthrough() -> None:
    block = {
        "type": "image",
        "source": {"type": "base64", "media_type": "image/png", "data": "QUJD"},
    }
    out = _to_session_content([block])
    assert out == [block], "image blocks should pass through structurally, not be stringified"


def test_to_session_content_document_passthrough() -> None:
    block = {
        "type": "document",
        "source": {"type": "url", "url": "https://example.com/doc.pdf"},
        "title": "doc",
    }
    out = _to_session_content([block])
    assert out == [block], "document blocks should pass through structurally, not be stringified"


def test_to_session_content_search_result_passthrough() -> None:
    """A ``search_result`` block — valid on the Sessions content union — passes
    through structurally so the model retains the typed citation metadata."""
    block = {
        "type": "search_result",
        "source": "https://example.com",
        "title": "result",
        "content": [{"type": "text", "text": "hit"}],
        "citations": {"enabled": True},
    }
    out = _to_session_content([block])
    assert out == [block], "search_result blocks should pass through structurally, not be stringified"


def test_to_session_content_tool_reference_stringified() -> None:
    """``tool_reference`` blocks have no Sessions equivalent and must be stringified."""
    block = {"type": "tool_reference", "tool_name": "weather"}
    out = _to_session_content([block])
    assert out == [{"type": "text", "text": session_runner_mod.json.dumps(block)}]
