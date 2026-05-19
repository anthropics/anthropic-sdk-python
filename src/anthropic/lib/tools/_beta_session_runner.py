"""The sessions-side tool runner — the managed-agents counterpart to
``client.beta.messages.tool_runner``.

:class:`SessionToolRunner` attaches to a managed-agents session's event stream,
reconciles against the events-list endpoint, dispatches every ``agent.tool_use``
*and* ``agent.custom_tool_use`` event against a local tool registry, posts the
matching result event back (``user.tool_result`` / ``user.custom_tool_result``),
and yields one :class:`DispatchedToolCall` per completed call. It also stops
itself once the session has been idle (``stop_reason`` ``end_turn``) for
``max_idle`` seconds. It does **not** touch the work-item lease — wrap it in
:class:`anthropic.lib.environments.EnvironmentWorker` if you need heartbeating /
force-stop.
"""

from __future__ import annotations

import json
import math
import time
import logging
import contextlib
from typing import TYPE_CHECKING, Union, cast
from dataclasses import dataclass
from collections.abc import Sequence, AsyncIterator

import anyio

from .._retry import TRANSIENT_ERRORS, is_fatal_status_error
from ..._types import Headers
from ._tool_dispatch import tool_registry, run_runnable_tool, tool_error_content
from .._scoped_client import HelperTag, _copy_client_with_bearer_auth
from ._beta_functions import (
    ToolError,
    BetaRunnableTool,
    BetaAsyncRunnableTool,
    BetaFunctionToolResultType,
    aclose_runnable_tool,
)
from ...types.beta.sessions import BetaManagedAgentsAgentToolUseEvent, BetaManagedAgentsAgentCustomToolUseEvent
from ...types.beta.sessions.beta_managed_agents_user_tool_result_event_params import (
    Content as _SessionContent,
    BetaManagedAgentsUserToolResultEventParams,
)
from ...types.beta.sessions.beta_managed_agents_user_custom_tool_result_event_params import (
    BetaManagedAgentsUserCustomToolResultEventParams,
)

if TYPE_CHECKING:
    from ..._client import AsyncAnthropic
    from ...resources.beta.sessions.events import AsyncEvents

__all__ = [
    "SessionToolRunner",
    "DispatchedToolCall",
    "DispatchedToolUseEvent",
    "DispatchedToolResultParams",
    "BetaAnyRunnableTool",
    "MANAGED_AGENTS_BETA",
    "DEFAULT_MAX_IDLE",
    # Re-exported for ``anthropic.lib.environments._worker``, which drives the
    # runner as an async context manager inside its own task group.
    "_run_session_tools",
]

# Either sync or async runnable tool — the union the session-side runners
# accept. ``Beta``-prefixed for consistency with the released
# ``BetaRunnableTool`` (sync) / ``BetaAsyncRunnableTool`` (async) members it
# unions; those two are unchanged.
BetaAnyRunnableTool = Union[BetaRunnableTool, BetaAsyncRunnableTool]

# The two tool-call event kinds the runner dispatches against the local tool
# registry, and the matching result-event params it posts back for each:
#
#   agent.tool_use         -> user.tool_result          (builtin agent_toolset tools)
#   agent.custom_tool_use  -> user.custom_tool_result   (custom, user-defined tools)
#
# ``agent.mcp_tool_use`` is intentionally absent — MCP tools run server-side and
# the runner never sees a result to post for them.
DispatchedToolUseEvent = Union[BetaManagedAgentsAgentToolUseEvent, BetaManagedAgentsAgentCustomToolUseEvent]
DispatchedToolResultParams = Union[
    BetaManagedAgentsUserToolResultEventParams,
    BetaManagedAgentsUserCustomToolResultEventParams,
]

# anthropic-beta gating Sessions access to self-hosted environments. The Sessions
# resource auto-injects this header on its own requests; this constant is kept
# for the work-item ``stop`` call the worker issues against the Work resource.
MANAGED_AGENTS_BETA = "managed-agents-2026-04-01"

STREAM_BACKOFF_START = 0.5
STREAM_BACKOFF_CAP = 10.0
# Outer per-tool-call timeout. This MUST stay strictly greater than the bash
# tool's own ``agent_toolset.BASH_DEFAULT_TIMEOUT`` (120s). The bash tool wraps
# its read in its own ``anyio.fail_after(BASH_DEFAULT_TIMEOUT)`` and, on
# ``TimeoutError``, tears down the subprocess. If this outer deadline equalled
# the inner one, the *outer* fail_after could win the race; anyio then raises
# the parent scope's cancel as a plain ``Cancelled`` (NOT ``TimeoutError``), so
# the bash tool's ``except TimeoutError`` cleanup never runs and its subprocess
# is left alive with the timed-out command still queued — the next bash call
# then reads stale output. The 30s margin gives the inner fail_after room to
# fire and clean up before this one. (BashSession also now closes on any
# outer-scope cancel as a belt-and-braces backstop, but these two timeouts must
# still never be equal.) Invariant covered by
# tests/lib/tools/test_session_runner.py::test_tool_timeout_exceeds_bash_default.
TOOL_TIMEOUT = 150.0
SEND_RETRIES = 3
# Grace period, in seconds, that the runner keeps running after the session goes
# idle with stop_reason ``end_turn`` before it stops; any new event in that
# window resets it. ``max_idle=None`` disables it (run until the session ends).
DEFAULT_MAX_IDLE = 60.0

log = logging.getLogger(__name__)


class _IdleClock:
    """Tracks how long the session has been idle after an ``end_turn`` stop.

    :attr:`end_turn_at` is the monotonic timestamp of the most recent
    ``session.status_idle`` event with ``stop_reason.type == "end_turn"`` for
    which no newer event has since arrived; ``None`` whenever the session is not
    in that state. :meth:`SessionToolRunner._idle_watchdog` stops the runner
    once it has been set for ``max_idle`` seconds.

    The clock is event-driven, not polled: every armed-state change signals the
    :attr:`wake` event so the watchdog wakes immediately instead of waiting out
    a poll interval. The watchdog captures :attr:`wake` *before* it reads
    :attr:`end_turn_at`, so a change landing between the read and the wait still
    wakes it.
    """

    __slots__ = ("end_turn_at", "wake")

    def __init__(self) -> None:
        self.end_turn_at: float | None = None
        self.wake = anyio.Event()

    def _signal(self) -> None:
        # Wake any current waiter and arm a fresh event for the next wait.
        self.wake.set()
        self.wake = anyio.Event()

    def note_event(self, ev: object) -> None:
        """Arm the clock on an ``end_turn`` idle, disarm it on anything else."""
        if (
            getattr(ev, "type", None) == "session.status_idle"
            and getattr(getattr(ev, "stop_reason", None), "type", None) == "end_turn"
        ):
            self.arm()
        else:
            self.disarm()

    def arm(self) -> None:
        """(Re)start the idle countdown from now and wake the watchdog."""
        self.end_turn_at = time.monotonic()
        self._signal()

    def disarm(self) -> None:
        """Cancel the idle countdown; only signals on an actual transition."""
        if self.end_turn_at is not None:
            self.end_turn_at = None
            self._signal()


@dataclass(frozen=True)
class DispatchedToolCall:
    """One tool call observed by :class:`SessionToolRunner`.

    Covers both tool-call event kinds — a builtin ``agent.tool_use`` and a
    custom ``agent.custom_tool_use``. The originating event is in :attr:`event`
    (with its input) and the posted-back result in :attr:`result`; ``name`` and
    ``tool_use_id`` are flat conveniences mirroring ``event``.
    """

    event: DispatchedToolUseEvent
    """The full ``agent.tool_use`` / ``agent.custom_tool_use`` event the agent
    emitted. The tool input is ``event.input``."""

    result: DispatchedToolResultParams
    """The result event the runner computed and attempted to post back to the
    session — ``user.tool_result`` for an ``agent.tool_use`` call,
    ``user.custom_tool_result`` for an ``agent.custom_tool_use`` call. The
    computed content is ``result["content"]``."""

    tool_use_id: str
    """Convenience: the id of the originating tool-call event — the same value
    as ``event.id`` for both event kinds."""

    name: str
    """Convenience: the tool name — the same value as ``event.name``."""

    is_error: bool
    """Convenience: whether the result is an error — the same value as
    ``result["is_error"]``."""

    posted: bool = True
    """``True`` if the result event made it to the session, ``False`` if all
    retries were exhausted or the server returned a permanent 4xx — in which
    case the session-side agent will *not* see this result and the consumer may
    want to surface that or retry at a higher level."""


_HELPER: HelperTag = "session-tool-runner"


def _scoped_client(client: AsyncAnthropic, environment_key: str | None) -> AsyncAnthropic:
    """Build the runner's request client.

    With an environment key, defer to :func:`_copy_client_with_bearer_auth`
    for a Bearer-only sub-client. Without one, layer the helper-telemetry
    header onto the caller's client via ``with_options`` (parent is not
    mutated).
    """
    if environment_key is not None:
        return _copy_client_with_bearer_auth(client, auth_token=environment_key, helper=_HELPER)
    return client.with_options(default_headers={"x-stainless-helper": _HELPER})


def _to_session_content(content: BetaFunctionToolResultType) -> list[_SessionContent]:
    """Bridge Messages-API tool-result content to the narrower Sessions-API content union.

    The two APIs share text/image/document/search_result block shapes but use
    distinct nominal TypedDicts; ToolReference blocks have no Sessions equivalent
    so they are stringified.
    """
    if isinstance(content, str):
        return [{"type": "text", "text": content or "(no output)"}]
    out: list[_SessionContent] = []
    for block in content:
        kind = block.get("type")
        if kind == "text":
            text = cast("str", block.get("text") or "(no output)")
            out.append({"type": "text", "text": text})
        elif kind in ("image", "document", "search_result"):
            out.append(cast("_SessionContent", block))
        else:
            out.append({"type": "text", "text": json.dumps(block)})
    return out or [{"type": "text", "text": "(no output)"}]


def _build_result_event(
    ev: DispatchedToolUseEvent,
    content: BetaFunctionToolResultType,
    is_error: bool,
) -> DispatchedToolResultParams:
    """Build the result-event params matching ``ev``'s tool-call kind.

    A custom tool call (``agent.custom_tool_use``) is answered with a
    ``user.custom_tool_result`` keyed by ``custom_tool_use_id``; a builtin tool
    call (``agent.tool_use``) with a ``user.tool_result`` keyed by
    ``tool_use_id``. Both use the codegen'd event-params TypedDicts.
    """
    session_content = _to_session_content(content)
    if ev.type == "agent.custom_tool_use":
        custom_result: BetaManagedAgentsUserCustomToolResultEventParams = {
            "type": "user.custom_tool_result",
            "custom_tool_use_id": ev.id,
            "is_error": is_error,
            "content": session_content,
        }
        return custom_result
    builtin_result: BetaManagedAgentsUserToolResultEventParams = {
        "type": "user.tool_result",
        "tool_use_id": ev.id,
        "is_error": is_error,
        "content": session_content,
    }
    return builtin_result


class SessionToolRunner:
    """Attach to a managed-agents session and dispatch its tool calls locally.

    The sessions-side counterpart to ``client.beta.messages.tool_runner``: an
    async iterable that, for each ``agent.tool_use`` or ``agent.custom_tool_use``
    event the agent emits, executes the matching tool from ``tools``, posts the
    matching result event back (``user.tool_result`` for a builtin tool call,
    ``user.custom_tool_result`` for a custom one), and yields one
    :class:`DispatchedToolCall`. Internally drives event-stream reconnect (with
    capped backoff) and result posting via an ``anyio`` task group, so it works
    under both ``asyncio`` and ``trio``.

    Iteration ends when the session terminates (``session.status_terminated`` /
    ``session.deleted``), when the consumer breaks out of the loop, or — once
    the session has gone idle with ``stop_reason`` ``end_turn`` — when
    ``max_idle`` seconds elapse with no new event (any new event resets the
    countdown; it re-arms on the next ``end_turn`` idle). ``max_idle=None``
    disables that last condition. On exit it runs each tool's optional cleanup:
    the ``close`` hook and, for tools defined as an (async) context manager, its
    ``__exit__`` / ``__aexit__``. It does **not** touch the work-item lease —
    wrap it in an
    :class:`~anthropic.lib.environments.EnvironmentWorker` for heartbeating /
    force-stop.

    Pass ``environment_key`` to authenticate the event stream / list / send
    calls with the self-hosted environment key (bearered, with the client's
    default ``x-api-key`` dropped); leave it unset to use the client's own
    credentials.

    Usage::

        from anthropic.lib.tools.agent_toolset import AgentToolContext, beta_agent_toolset_20260401

        async with AgentToolContext(workdir="/workspace") as env:
            async for call in client.beta.sessions.events.tool_runner(
                work.data.id,
                tools=[*beta_agent_toolset_20260401(env), my_tool],
            ):
                print(f"{call.name} -> {'error' if call.is_error else 'ok'}")
    """

    def __init__(
        self,
        client: AsyncAnthropic,
        session_id: str,
        *,
        tools: Sequence[BetaAnyRunnableTool],
        max_idle: float | None = DEFAULT_MAX_IDLE,
        environment_key: str | None = None,
        extra_headers: Headers | None = None,
    ) -> None:
        self.session_id = session_id
        self.tools: Sequence[BetaAnyRunnableTool] = tools
        self.max_idle = max_idle
        # All event stream / list / send requests are issued via this scoped
        # sub-client: Bearer-only when an environment key is set, otherwise the
        # caller's own client with the helper-telemetry header layered on.
        self._scoped = _scoped_client(client, environment_key)
        # Per-request passthrough headers: threaded into every event stream /
        # list / send via that call's ``extra_headers=`` (make_request_options)
        # — never assigned onto the client, so client state is not mutated.
        # Auth and ``x-stainless-helper`` come from the scoped sub-client and
        # the parent client's ``default_headers`` propagate via its
        # ``client.copy()``; per the SDK's standard ``extra_headers``
        # precedence a caller header overrides the scoped client's same-named
        # default for that request, so this is for caller passthrough (trace
        # ids etc.), not auth.
        self.extra_headers = extra_headers

    async def __aiter__(self) -> AsyncIterator[DispatchedToolCall]:
        async with self._run() as calls:
            async for call in calls:
                yield call

    async def until_done(self) -> None:
        """Drive the runner to completion, discarding the per-call observations.

        Named to match ``BetaToolRunner.until_done`` (and to avoid colliding
        with :meth:`EnvironmentWorker.run`, which is a forever-loop): it returns
        once the session ends / goes idle, rather than running until cancelled.
        """
        async for _ in self:
            pass

    # -- run lifecycle ------------------------------------------------------

    @contextlib.asynccontextmanager
    async def _run(self) -> AsyncIterator[AsyncIterator[DispatchedToolCall]]:
        """Drive the session tool loop, yielding an iterator of
        :class:`DispatchedToolCall`. :meth:`__aiter__` (and the module-level
        :func:`_run_session_tools` shim used by ``EnvironmentWorker``) wrap this.

        Per-run state lives on ``self`` as private attributes so the loops below
        — :meth:`_stream_loop`, :meth:`_dispatch_loop`, :meth:`_reconcile`,
        :meth:`_idle_watchdog`, :meth:`_stop_watcher` — can mutate it as methods
        rather than threading a shared state object through free functions.
        """
        self._events: AsyncEvents = self._scoped.beta.sessions.events
        log.info("session tool runner starting session_id=%s", self.session_id)
        self._tools_by_name: dict[str, BetaAnyRunnableTool] = tool_registry(self.tools)
        # ``_seen`` dedups tool-call events across the stream and the reconcile
        # pass (by event id); ``_answered`` holds the ids whose result post has
        # actually landed, so a failed post is retried on the next reconcile.
        self._seen: set[str] = set()
        self._answered: set[str] = set()
        self._stop = anyio.Event()
        self._idle_clock = _IdleClock()

        self._send_work, self._recv_work = anyio.create_memory_object_stream[DispatchedToolUseEvent](
            max_buffer_size=100,
        )
        self._send_results, self._recv_results = anyio.create_memory_object_stream[DispatchedToolCall](
            max_buffer_size=math.inf,
        )

        async def iterator() -> AsyncIterator[DispatchedToolCall]:
            # ``_recv_results`` is explicitly closed in the outer ``finally`` to
            # keep cleanup deterministic regardless of whether the consumer
            # iterated at all (e.g. ``async with runner._run(): pass``).
            async for call in self._recv_results:
                yield call

        try:
            # The outer ``CancelScope`` absorbs the task-group cancellation we
            # trigger in the ``finally`` below, so it doesn't surface to the
            # consumer as ``Cancelled``.
            with anyio.CancelScope():
                async with anyio.create_task_group() as tg:
                    # The stop watcher closes ``_send_work`` when ``_stop`` is
                    # set so the dispatch loop's ``receive()`` raises
                    # EndOfStream and the loop exits cleanly without us having
                    # to inject a sentinel or race two awaitables.
                    tg.start_soon(self._stop_watcher)
                    tg.start_soon(self._stream_loop)
                    tg.start_soon(self._dispatch_loop)
                    if self.max_idle is not None:
                        tg.start_soon(self._idle_watchdog)
                    try:
                        yield iterator()
                    finally:
                        # Signal every loop to exit. Most exit voluntarily on
                        # ``_stop``; cancelling the task group's scope wakes
                        # anything still blocked on an unrelated await (e.g. an
                        # uncancellable test fake). anyio absorbs the resulting
                        # cancel via the outer ``CancelScope``.
                        self._stop.set()
                        tg.cancel_scope.cancel()
        finally:
            # Explicitly close every stream so anyio doesn't warn on GC.
            # ``aclose`` is idempotent, so it's fine if the producer already
            # closed its end during normal shutdown.
            with anyio.CancelScope(shield=True):
                for stream in (self._recv_results, self._send_results, self._recv_work, self._send_work):
                    try:
                        await stream.aclose()
                    except Exception:
                        pass
            # Run each tool's optional cleanup (``close`` hook and, for
            # context-manager tools, ``__exit__`` / ``__aexit__``). Shielded so
            # the hooks survive the surrounding cancellation.
            with anyio.CancelScope(shield=True):
                for tool in self.tools:
                    await aclose_runnable_tool(tool)

    # -- event-stream + reconcile ------------------------------------------

    async def _reconcile(self) -> None:
        """Read full history and enqueue every tool-call event still unanswered.

        Two-pass: read the whole history before emitting so a tool-call whose
        result appears later in the same history is not re-dispatched. Pairs
        ``agent.tool_use`` with ``user.tool_result`` and ``agent.custom_tool_use``
        with ``user.custom_tool_result`` when computing which calls are answered.
        """
        pending: list[DispatchedToolUseEvent] = []
        last_was_end_turn = False
        list_failed = False
        try:
            async for ev in self._events.list(self.session_id, limit=1000, extra_headers=self.extra_headers):
                if ev.type == "agent.tool_use" or ev.type == "agent.custom_tool_use":
                    # Mark the event seen so the live stream doesn't re-enqueue it, but
                    # decide whether it still needs executing from ``_answered``, not
                    # ``_seen``: a call whose result post failed is seen-but-unanswered
                    # and must be retried on the next reconcile pass rather than dropped.
                    self._seen.add(ev.id)
                    pending.append(ev)
                elif ev.type == "user.tool_result":
                    self._answered.add(ev.tool_use_id)
                elif ev.type == "user.custom_tool_result":
                    self._answered.add(ev.custom_tool_use_id)
                last_was_end_turn = (
                    ev.type == "session.status_idle"
                    and getattr(getattr(ev, "stop_reason", None), "type", None) == "end_turn"
                )
        except Exception as e:
            # Pagination may have failed partway through; the ``_answered`` set
            # could be incomplete, so dispatching ``pending`` now would risk
            # re-running a tool whose result was on a page we never reached.
            # The next reconnect will retry the reconcile. Leave ``_idle_clock``
            # untouched since the history we read may be incomplete.
            log.warning("reconcile list failed; skipping pending enqueue error=%s", e)
            list_failed = True
        if list_failed:
            # Roll back the ids we added to ``_seen`` so the live stream can
            # re-process them rather than silently dedup what we never finished
            # reading.
            for ev in pending:
                self._seen.discard(ev.id)
            return
        unanswered = [ev for ev in pending if ev.id not in self._answered]
        # If the most recent event in history is an ``end_turn`` idle and there
        # is no outstanding tool work, the session is done — arm the idle clock
        # so the watchdog counts down even if that ``end_turn`` arrived during a
        # disconnect.
        if last_was_end_turn and not unanswered:
            self._idle_clock.arm()
        else:
            self._idle_clock.disarm()
        for ev in unanswered:
            await self._send_work.send(ev)

    async def _stream_loop(self) -> None:
        backoff = STREAM_BACKOFF_START
        while not self._stop.is_set():
            try:
                # Open the stream *before* reconciling: with the stream already
                # attached, an event emitted in the gap between the list call
                # and the attach is delivered live instead of lost. ``_seen``
                # dedups any overlap between the history and the live stream.
                async with await self._events.stream(self.session_id, extra_headers=self.extra_headers) as stream:
                    await self._reconcile()
                    async for ev in stream:
                        backoff = STREAM_BACKOFF_START
                        # Arm/disarm the idle clock: an ``end_turn`` idle starts
                        # the grace countdown, any other event cancels it.
                        self._idle_clock.note_event(ev)
                        if ev.type == "agent.tool_use" or ev.type == "agent.custom_tool_use":
                            if ev.id not in self._seen:
                                self._seen.add(ev.id)
                                await self._send_work.send(ev)
                        elif ev.type == "user.tool_result":
                            self._answered.add(ev.tool_use_id)
                        elif ev.type == "user.custom_tool_result":
                            self._answered.add(ev.custom_tool_use_id)
                        elif ev.type in ("session.status_terminated", "session.deleted"):
                            log.info("session terminated")
                            self._stop.set()
                            return
            except TRANSIENT_ERRORS as e:
                if self._stop.is_set():
                    return
                if is_fatal_status_error(e):
                    # No amount of backoff will fix a 401/403; bail out so the
                    # consumer sees the runner exit instead of looping silently.
                    log.error("stream failed permanently error=%s", e)
                    self._stop.set()
                    return
                log.warning("stream disconnected, reconnecting backoff=%.1fs error=%s", backoff, e)
            with anyio.move_on_after(backoff):
                await self._stop.wait()
            backoff = min(backoff * 2, STREAM_BACKOFF_CAP)

    # -- tool dispatch ------------------------------------------------------

    async def _dispatch_loop(self) -> None:
        try:
            while True:
                try:
                    ev = await self._recv_work.receive()
                except anyio.EndOfStream:
                    # Producer side closed — usually because ``_stop`` was set
                    # (the idle watchdog or stream loop signalled it).
                    return
                if ev.id in self._answered:
                    continue
                # Shielded execute so consumer-side cancellation can't interrupt
                # an in-flight tool. The result will still be posted and the
                # DispatchedToolCall enqueued before the cancel propagates.
                with anyio.CancelScope(shield=True):
                    await self._execute(ev)
        finally:
            # Closing the results stream signals the iterator that no more
            # results will arrive. Wrapped in a shield because we're often in a
            # cancellation path on the way out.
            with anyio.CancelScope(shield=True):
                await self._send_results.aclose()

    async def _execute(self, ev: DispatchedToolUseEvent) -> None:
        log.info("executing tool tool=%s tool_use_id=%s", ev.name, ev.id)
        tool = self._tools_by_name.get(ev.name)
        content: BetaFunctionToolResultType
        is_error = False
        input_ = dict(ev.input)
        if tool is None:
            content = f"tool {ev.name!r} not implemented"
            is_error = True
        else:
            try:
                with anyio.fail_after(TOOL_TIMEOUT):
                    content = await run_runnable_tool(tool, input_)
            except TimeoutError:
                content = f"tool {ev.name!r} timed out"
                is_error = True
            except ToolError as e:
                content = tool_error_content(e)
                is_error = True
            except Exception as e:
                log.exception("tool %s raised", ev.name)
                content = tool_error_content(e)
                is_error = True
        tool_result = _build_result_event(ev, content, is_error)
        sent = await self._send_result(tool_result, ev.id)
        try:
            await self._send_results.send(
                DispatchedToolCall(
                    event=ev,
                    result=tool_result,
                    tool_use_id=ev.id,
                    name=ev.name,
                    is_error=is_error,
                    posted=sent,
                )
            )
        except anyio.BrokenResourceError:
            # The receiver closed early (consumer broke out of the iterator).
            # Result was still posted to the session; we just can't surface
            # the observability event.
            pass

    async def _send_result(self, tool_result: DispatchedToolResultParams, tool_use_id: str) -> bool:
        """Post ``tool_result`` back to the session, retrying transient failures.

        ``tool_use_id`` is the originating tool-call event id — passed
        explicitly because the result params key it differently
        (``tool_use_id`` vs ``custom_tool_use_id``) depending on the kind.
        """
        last_err: Exception | None = None
        for i in range(SEND_RETRIES):
            try:
                await self._events.send(
                    self.session_id,
                    events=[tool_result],
                    extra_headers=self.extra_headers,
                )
                self._answered.add(tool_use_id)
                return True
            except TRANSIENT_ERRORS as e:
                last_err = e
                if is_fatal_status_error(e):
                    break
                # Don't sleep after the final attempt — there is no retry to wait for.
                if i < SEND_RETRIES - 1:
                    await anyio.sleep(i + 1)
        log.error("failed to send tool result tool_use_id=%s error=%s", tool_use_id, last_err)
        return False

    # -- background watchers -----------------------------------------------

    async def _idle_watchdog(self) -> None:
        """Stop the runner once the session has been idle (``end_turn``) for
        ``max_idle`` seconds with no new events.

        Event-driven: it blocks on the idle clock's wake event rather than
        polling. Capturing ``clock.wake`` *before* reading ``clock.end_turn_at``
        closes the race where the clock changes between the read and the wait.
        """
        max_idle = self.max_idle
        assert max_idle is not None
        clock = self._idle_clock
        while not self._stop.is_set():
            wake = clock.wake
            at = clock.end_turn_at
            if at is None:
                # Not armed: block until the clock arms (or the runner stops).
                await _wait_first(wake, self._stop)
                continue
            remaining = max_idle - (time.monotonic() - at)
            if remaining <= 0:
                log.info("session idle after end_turn for %.0fs; stopping", max_idle)
                self._stop.set()
                return
            # Armed: wait out the remaining grace, waking early if the clock
            # changes (disarmed, or re-armed with a fresh timestamp) or the
            # runner stops. Either way, loop back and re-evaluate.
            with anyio.move_on_after(remaining):
                await _wait_first(wake, self._stop)

    async def _stop_watcher(self) -> None:
        """When ``_stop`` is set, close the work stream so :meth:`_dispatch_loop` exits."""
        await self._stop.wait()
        await self._send_work.aclose()


async def _wait_first(*events: anyio.Event) -> None:
    """Return as soon as any of ``events`` is set."""
    async with anyio.create_task_group() as tg:

        async def _waiter(ev: anyio.Event) -> None:
            await ev.wait()
            tg.cancel_scope.cancel()

        for ev in events:
            tg.start_soon(_waiter, ev)


@contextlib.asynccontextmanager
async def _run_session_tools(
    client: AsyncAnthropic,
    session_id: str,
    *,
    tools: Sequence[BetaAnyRunnableTool],
    max_idle: float | None = DEFAULT_MAX_IDLE,
    environment_key: str | None = None,
    extra_headers: Headers | None = None,
) -> AsyncIterator[AsyncIterator[DispatchedToolCall]]:
    """Internal: drive a :class:`SessionToolRunner` as an async context manager.

    Kept as a thin module-level shim because
    :class:`~anthropic.lib.environments.EnvironmentWorker` enters the runner
    inside its own task group and wants the context-manager shape for
    deterministic cleanup. New code should iterate :class:`SessionToolRunner`
    directly.
    """
    runner = SessionToolRunner(
        client,
        session_id,
        tools=tools,
        max_idle=max_idle,
        environment_key=environment_key,
        extra_headers=extra_headers,
    )
    async with runner._run() as calls:  # noqa: SLF001
        yield calls
