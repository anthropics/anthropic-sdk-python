"""The self-hosted environment worker — the full composition of the
control-plane poller and the per-session tool runner.

:class:`EnvironmentWorker` claims work items from a self-hosted environment, and
for each claimed ``session`` work item: builds the per-session
:class:`~anthropic.lib.tools.agent_toolset.AgentToolContext` and downloads the
session agent's skills, then runs a
:class:`~anthropic.lib.tools._beta_session_runner.SessionToolRunner` for the
session *while* heartbeating the work-item lease in parallel; on exit it
force-stops the work item and loops to the next one. The lease heartbeat
reporting ``state == "stopping"`` (or a lost lease) ends the session run.

Build one from the generated work resource::

    client.beta.environments.work.worker(environment_id=..., environment_key=...)

or construct it directly::

    from anthropic.lib.environments import EnvironmentWorker

    EnvironmentWorker(client, environment_id=..., environment_key=...)

:meth:`EnvironmentWorker.handle_item` runs that same per-work-item flow for a
single work item you've already claimed (e.g. a ``worker poll --on-work`` script
handed one to a fresh process); with no arguments it reads the ``ANTHROPIC_*``
env vars that command sets.
"""

from __future__ import annotations

import os
import time
import logging
from typing import TYPE_CHECKING, Union, Callable
from collections.abc import Sequence

import anyio

from .._retry import TRANSIENT_ERRORS
from ._poller import _is_status, aiter_work, _is_fatal_4xx
from ..._types import Headers, NotGiven, not_given
from .._scoped_client import _copy_client_with_bearer_auth
from ...types.beta.environments import BetaSelfHostedWork, BetaSessionWorkData
from ..tools._beta_session_runner import (
    DEFAULT_MAX_IDLE,
    BetaAnyRunnableTool,
    _run_session_tools,
)

if TYPE_CHECKING:
    from ..._client import AsyncAnthropic
    from ..tools.agent_toolset import AgentToolContext
    from ...resources.beta.environments.work import AsyncWork

# ``agent_toolset`` pulls in host-only modules (``subprocess``, ``tarfile``, …),
# so it is never imported at module level here — only as a type above, and
# lazily for its values inside ``_tools_for`` / ``_handle_item``. That keeps this
# module host-dep-free so the generated ``work`` resource can expose
# ``EnvironmentWorker`` without dragging those imports into ``import anthropic``.

__all__ = ["EnvironmentWorker", "EnvironmentWorkerTools"]

log = logging.getLogger(__name__)

_HEARTBEAT_DEFAULT = 30.0
# Assumed lease TTL before the server's first heartbeat response tells us the
# real value — used to decide when a run of transient failures means the lease
# is gone.
_HEARTBEAT_TTL_DEFAULT = 90.0
_NO_HEARTBEAT_SENTINEL = "NO_HEARTBEAT"

# A fixed tool list, or a factory invoked once per claimed session with that
# session's ``AgentToolContext`` — use the factory form to bind
# :func:`beta_agent_toolset_20260401` (or any tool that needs the workdir /
# session id) to the right session.
EnvironmentWorkerTools = Union[
    Sequence[BetaAnyRunnableTool], Callable[["AgentToolContext"], Sequence[BetaAnyRunnableTool]]
]

# Transient errors the heartbeat loop retries on top of ``TRANSIENT_ERRORS``:
# ``anyio.fail_after`` (which bounds each heartbeat) raises the builtin
# ``TimeoutError`` rather than an ``APIError``, so it would otherwise fall
# through to the un-retried branch. Declared at module level with an explicit
# type so mypy can verify the ``except`` clause; an inline
# ``except (*TRANSIENT_ERRORS, TimeoutError)`` types as ``tuple[Any, ...]``
# and mypy rejects it as not-an-exception-tuple.
_HEARTBEAT_TRANSIENT_ERRORS: tuple[type[Exception], ...] = (*TRANSIENT_ERRORS, TimeoutError)


async def _heartbeat_loop(
    work: AsyncWork,
    *,
    work_id: str,
    environment_id: str,
    stop: anyio.Event,
    extra_headers: Headers | None = None,
) -> None:
    """Keep the work-item lease alive while a session is being served.

    ``work`` must be bound to a sub-client authenticated for the environment;
    this loop adds no auth of its own. Sets ``stop`` when the control plane
    reports the work is ``stopping`` / ``stopped``, when the lease is no
    longer extended, on a permanent heartbeat failure, or when transient
    failures have run long enough that the lease must be assumed lost (so two
    runners don't end up serving the same work).
    """
    interval = _HEARTBEAT_DEFAULT
    ttl = _HEARTBEAT_TTL_DEFAULT
    last = _NO_HEARTBEAT_SENTINEL
    last_success = time.monotonic()
    while not stop.is_set():
        try:
            # Bound each heartbeat: a network blackhole must not leave us
            # awaiting for the SDK's multi-minute default while the lease TTL
            # (tens of seconds) expires out from under us.
            with anyio.fail_after(interval):
                resp = await work.heartbeat(
                    work_id,
                    environment_id=environment_id,
                    expected_last_heartbeat=last,
                    extra_headers=extra_headers,
                )
        # Anything outside ``_HEARTBEAT_TRANSIENT_ERRORS`` is a real bug and
        # propagates rather than being swallowed and retried until the lease
        # is assumed lost.
        except _HEARTBEAT_TRANSIENT_ERRORS as e:
            if _is_fatal_4xx(e):
                log.error("permanent heartbeat failure error=%s", e)
                stop.set()
                return
            # A transient failure (5xx, timeout, connection error) is not a 4xx,
            # so retrying forever risks split-brain once the lease expires. If no
            # heartbeat has succeeded within the lease TTL, assume it's lost.
            if time.monotonic() - last_success > ttl:
                log.error("lease assumed lost: no successful heartbeat in %.0fs error=%s", ttl, e)
                stop.set()
                return
            log.warning("transient heartbeat failure error=%s", e)
        else:
            last = resp.last_heartbeat
            last_success = time.monotonic()
            if resp.ttl_seconds > 0:
                ttl = resp.ttl_seconds
                interval = max(1.0, min(resp.ttl_seconds / 2, _HEARTBEAT_DEFAULT))
            if resp.state in ("stopping", "stopped") or not resp.lease_extended:
                log.info("heartbeat signals shutdown state=%s lease_extended=%s", resp.state, resp.lease_extended)
                stop.set()
                return
        # Sleep up to `interval` seconds, but wake immediately if stop is set.
        with anyio.move_on_after(interval):
            await stop.wait()


def _require(value: str | None, *, name: str, env_var: str) -> str:
    """Fall back to ``env_var`` for ``value``; raise a clear error if still empty.

    The ``ANTHROPIC_*`` env vars are the ones the ``ant worker poll --on-work``
    command sets on the process it spawns for a claimed work item.
    """
    resolved = value or os.environ.get(env_var)
    if not resolved:
        raise ValueError(f"handle_item: {name} is required — pass it or set {env_var}")
    return resolved


class EnvironmentWorker:
    """Run a self-hosted environment worker.

    Composed from the control-plane poller (``client.beta.environments.work.poller``)
    and the per-session :class:`SessionToolRunner`. For each claimed ``session``
    work item it builds the per-session :class:`AgentToolContext` and downloads
    the session agent's skills, then runs a session tool runner for the session
    *while* heartbeating the work-item lease in parallel; on exit it force-stops
    the work item and loops to the next one.

    A single ``environment_key`` is the worker's only credential: a Bearer-only
    scoped sub-client is built once per call (one for polling, one for
    heartbeat / force-stop, and the session tool runner builds its own
    internally), so every request the worker issues is authenticated by the
    environment key with the parent client's ``X-Api-Key`` cleared.

    Async only — :meth:`run` loops forever, so bound it (cancel the task or wrap
    it in :func:`asyncio.wait_for`) when you want it to stop.

    Use :meth:`handle_item` if you already hold a claimed work item (e.g. a
    ``worker poll --on-work`` script handed one to a fresh process) and just
    want the per-item flow without the poll loop — with no arguments it reads the
    ``ANTHROPIC_*`` env vars that command sets, so ``environment_id`` (only used
    by :meth:`run`) isn't needed.

    Prefer ``client.beta.environments.work.worker(...)`` to build one; the direct
    constructor below is equivalent.

    Example::

        from anthropic import AsyncAnthropic

        client = AsyncAnthropic()

        # Long-running daemon: poll for work, serve each session, loop.
        await client.beta.environments.work.worker(
            environment_id=environment_id,
            environment_key=environment_key,
            workdir="/workspace",
        ).run()

        # Already-claimed item (e.g. inside `ant worker poll --on-work ...`):
        await client.beta.environments.work.worker(workdir="/workspace").handle_item()

        # Equivalent, constructing the worker directly:
        from anthropic.lib.environments import EnvironmentWorker

        await EnvironmentWorker(client, workdir="/workspace").handle_item()

    Args:
      client: The async Anthropic client.
      environment_id: The self-hosted environment to poll for work. Required by
        :meth:`run`; not used by :meth:`handle_item`.
      environment_key: The environment key — the worker's single credential.
        Used as the Bearer credential on the scoped sub-clients the worker
        constructs for the control-plane (poll / ack / stop) and session-level
        (events stream / list / send + heartbeat / force-stop) calls.
        Required by :meth:`run`; :meth:`handle_item` falls back to it (then to
        ``ANTHROPIC_ENVIRONMENT_KEY``) when not passed one.
      tools: Tools to expose to each claimed session. Either a fixed list, or a
        factory invoked once per session with that session's
        :class:`AgentToolContext`. Defaults to
        ``beta_agent_toolset_20260401(env)`` (the standard
        ``agent_toolset_20260401`` set bound to the per-session context).
      workdir: Base directory for the per-session :class:`AgentToolContext`.
        Defaults to :func:`os.getcwd` captured when the worker is constructed
        (matches the TS worker's ``process.cwd()``-at-construction), so a
        ``chdir`` between constructing the worker and serving a session does not
        change where tools resolve paths.
      unrestricted_paths: Forwarded to the per-session :class:`AgentToolContext`.
      max_idle: Forwarded to the session tool runner — seconds to keep running
        after the session goes idle with ``stop_reason`` ``end_turn``. Defaults
        to :data:`~anthropic.lib.environments.DEFAULT_MAX_IDLE` (60s). ``None``
        disables it.
      worker_id: Optional identifier sent on each poll. Defaults to a unique,
        hostname-prefixed id.
      extra_headers: Optional headers passed through per request on every
        call the worker makes (poll / ack / stop / heartbeat and the session
        tool runner's event stream / list / send). They are threaded into
        each call's ``extra_headers=`` and never assigned onto the client, so
        client state is not mutated. Auth and ``x-stainless-helper`` are
        supplied by the worker's scoped sub-clients (and the parent client's
        ``default_headers`` propagate via their ``client.copy()``); a header
        given here overrides a scoped client's same-named default for that
        request, so use it for caller passthrough (e.g. trace ids), not auth.
    """

    def __init__(
        self,
        client: AsyncAnthropic,
        *,
        environment_id: str | None = None,
        environment_key: str | None = None,
        tools: EnvironmentWorkerTools | None = None,
        workdir: str | os.PathLike[str] | None = None,
        unrestricted_paths: bool = False,
        max_file_bytes: int | None | NotGiven = not_given,
        max_idle: float | None = DEFAULT_MAX_IDLE,
        worker_id: str | None = None,
        extra_headers: Headers | None = None,
    ) -> None:
        self._client = client
        self._environment_id = environment_id
        self._environment_key = environment_key
        self._tools = tools
        # Snapshot the cwd at construction time when no explicit workdir was
        # given (TS parity: ``process.cwd()`` captured up front). Resolving "."
        # lazily at first tool use would instead pick up any intervening chdir.
        self._workdir: str | os.PathLike[str] = os.getcwd() if workdir is None else workdir
        self._unrestricted_paths = unrestricted_paths
        self._max_file_bytes = max_file_bytes
        self._max_idle = max_idle
        self._worker_id = worker_id
        self._extra_headers = extra_headers

    def _tools_for(self, env: AgentToolContext) -> Sequence[BetaAnyRunnableTool]:
        if callable(self._tools):
            return self._tools(env)
        if self._tools is not None:
            return self._tools
        # Lazy import: keeps the host-only ``agent_toolset`` module out of this
        # module's import graph (see the note next to the imports).
        from ..tools.agent_toolset import beta_agent_toolset_20260401

        return beta_agent_toolset_20260401(env)

    async def run(self) -> None:
        """Poll the environment and service each claimed session until cancelled.

        Loops forever; cancel the task (or wrap it in :func:`asyncio.wait_for`)
        to stop it. Equivalent to claiming work items via
        ``client.beta.environments.work.poller`` and running the per-item flow
        for each.

        Raises:
          ValueError: if ``environment_id`` / ``environment_key`` were not passed
            to the constructor.
        """
        environment_id = self._environment_id
        environment_key = self._environment_key
        if environment_id is None or environment_key is None:
            raise ValueError("EnvironmentWorker.run: environment_id and environment_key are required to poll for work")
        # Poll/ack/stop calls run through a Bearer-only sub-client tagged with
        # the poller's helper telemetry. ``_handle_item`` builds its own
        # ``environments-worker``-tagged sub-client for the heartbeat / force-stop.
        poll_client = _copy_client_with_bearer_auth(
            self._client, auth_token=environment_key, helper="environments-work-poller"
        )
        async for work_item in aiter_work(
            poll_client.beta.environments.work,
            environment_id=environment_id,
            worker_id=self._worker_id,
            auto_stop=False,
            extra_headers=self._extra_headers,
        ):
            await self._handle_item(work_item, environment_key)

    async def handle_item(
        self,
        *,
        work_id: str | None = None,
        environment_id: str | None = None,
        session_id: str | None = None,
        environment_key: str | None = None,
    ) -> None:
        """Service a single, already-claimed work item without the poll loop.

        Builds the per-session :class:`AgentToolContext` (workdir from this
        worker's options) and downloads the session agent's skills, then runs a
        :class:`SessionToolRunner` for the session *while* heartbeating the
        work-item lease in parallel, and force-stops the work item on exit
        (whether the runner finishes normally, raises, or the heartbeat loop
        signals shutdown).

        Use this when something else does the claiming — e.g. a
        ``worker poll --on-work`` script that hands an already-claimed item to a
        fresh process. ``work_id`` / ``environment_id`` / ``session_id`` fall
        back to ``ANTHROPIC_WORK_ID`` / ``ANTHROPIC_ENVIRONMENT_ID`` /
        ``ANTHROPIC_SESSION_ID`` (the env vars that command sets) when not
        passed; ``environment_key`` resolves in order: the explicit argument,
        then this worker's own ``environment_key``, then
        ``ANTHROPIC_ENVIRONMENT_KEY`` — so with no arguments inside that command
        it just works. Non-session work items are ignored (but still
        force-stopped so the lease doesn't sit until TTL).

        Raises:
          ValueError: if any of ``work_id`` / ``environment_id`` / ``session_id``
            / ``environment_key`` is still empty after the fallbacks.
        """
        work_id = _require(work_id, name="work_id", env_var="ANTHROPIC_WORK_ID")
        environment_id = _require(environment_id, name="environment_id", env_var="ANTHROPIC_ENVIRONMENT_ID")
        session_id = _require(session_id, name="session_id", env_var="ANTHROPIC_SESSION_ID")
        # environment_key resolves: explicit arg -> this worker's own key ->
        # ANTHROPIC_ENVIRONMENT_KEY -> a clear "required" error.
        environment_key = _require(
            environment_key or self._environment_key,
            name="environment_key",
            env_var="ANTHROPIC_ENVIRONMENT_KEY",
        )

        # The per-item flow only reads work.id / work.environment_id /
        # work.data.type / work.data.id, so a minimally populated model is
        # enough.
        work_item = BetaSelfHostedWork.model_construct(
            id=work_id,
            environment_id=environment_id,
            data=BetaSessionWorkData.model_construct(type="session", id=session_id),
        )
        await self._handle_item(work_item, environment_key)

    async def _handle_item(self, work_item: BetaSelfHostedWork, environment_key: str) -> None:
        """The per-item body shared by :meth:`run`'s poll loop and :meth:`handle_item`.

        Runs a :class:`SessionToolRunner` for the work item's session while
        heartbeating its lease, force-stopping the work item on exit. All
        control-plane traffic for this work item — heartbeat + force-stop —
        flows through a
        Bearer-only sub-client built here; the session tool runner builds its
        own ``session-tool-runner``-tagged sub-client internally.
        """
        # Lazy import: keeps the host-only ``agent_toolset`` module out of this
        # module's import graph (see the note next to the imports).
        from ..tools.agent_toolset import AgentToolContext

        # ``environments-worker``-scoped sub-client for the heartbeat and
        # force-stop calls this item drives. The session tool runner is given
        # the parent client + environment_key and builds its own sub-client.
        worker_client = _copy_client_with_bearer_auth(
            self._client, auth_token=environment_key, helper="environments-worker"
        )
        work_res = worker_client.beta.environments.work
        try:
            session_id = work_item.data.id
            async with anyio.create_task_group() as tg:
                stop = anyio.Event()

                async def _heartbeat(
                    work_id: str = work_item.id,
                    environment_id: str = work_item.environment_id,
                    stop_ev: anyio.Event = stop,
                ) -> None:
                    try:
                        await _heartbeat_loop(
                            work_res,
                            work_id=work_id,
                            environment_id=environment_id,
                            stop=stop_ev,
                            extra_headers=self._extra_headers,
                        )
                    finally:
                        tg.cancel_scope.cancel()

                # Start the lease heartbeat BEFORE entering AgentToolContext.
                # AgentToolContext.__aenter__ downloads and extracts every skill
                # the session agent has; that can take longer than the lease
                # TTL. If the first heartbeat only fired *after* the download
                # (the old ordering), a slow download would let the lease lapse
                # and another worker reclaim the item — both workers then serve
                # the same session (split-brain). Heartbeating concurrently with
                # the download keeps the lease ours the entire time. The
                # heartbeat only needs work_id / environment_id, both available
                # before any download.
                tg.start_soon(_heartbeat)

                # Drive AgentToolContext's enter/exit explicitly rather than via
                # ``async with`` so its async cleanup (bash subprocess teardown
                # + downloaded-skill removal) runs *shielded*: by the time we
                # tear down, the heartbeat may have cancelled the task-group
                # scope (lost lease), and that cancel must not abort the
                # subprocess kill / skill rmtree. A heartbeat-driven cancel
                # during __aenter__ still interrupts an in-progress skill
                # download (the desired split-brain protection) — __aexit__ is
                # then a no-op since no bash/skills were set up.
                env = AgentToolContext(
                    workdir=self._workdir,
                    unrestricted_paths=self._unrestricted_paths,
                    max_file_bytes=self._max_file_bytes,
                    client=worker_client,
                    session_id=session_id,
                )
                try:
                    await env.__aenter__()
                    tools = self._tools_for(env)
                    try:
                        async with _run_session_tools(
                            self._client,
                            session_id,
                            tools=tools,
                            max_idle=self._max_idle,
                            environment_key=environment_key,
                            extra_headers=self._extra_headers,
                        ) as calls:
                            async for _ in calls:
                                pass
                    finally:
                        stop.set()
                        tg.cancel_scope.cancel()
                finally:
                    with anyio.CancelScope(shield=True):
                        await env.__aexit__(None, None, None)
        finally:
            # Best-effort: force-stop the work item so the lease doesn't sit
            # until TTL expiry. Idempotent server-side; a 409 just means the
            # work already stopped. Shielded so the post survives any
            # surrounding cancellation.
            with anyio.CancelScope(shield=True):
                try:
                    await work_res.stop(
                        work_item.id,
                        environment_id=work_item.environment_id,
                        force=True,
                        extra_headers=self._extra_headers,
                    )
                except Exception as e:
                    if not _is_status(e, 409):
                        log.error("force-stop on exit failed work_id=%s error=%s", work_item.id, e)
