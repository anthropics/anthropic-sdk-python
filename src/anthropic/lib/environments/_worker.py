"""The self-hosted environment worker — the full composition of the
control-plane poller and the per-session tool runner.

:class:`EnvironmentWorker` claims work items from a self-hosted environment, and
for each claimed ``session`` work item: builds the per-session
:class:`~anthropic.lib.tools.agent_toolset.AgentToolContext` and downloads the
session agent's skills, then runs a
:class:`~anthropic.lib.tools._beta_session_runner.SessionToolRunner` for the
session *while* heartbeating the work-item lease in parallel; on exit it
force-stops the work item (unless the lease was lost, in which case the item is
left to whoever holds it now) and loops to the next one. The lease heartbeat
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
import enum
import json
import time
import base64
import logging
from typing import TYPE_CHECKING, Union, Callable, cast, overload
from collections.abc import Mapping, Sequence
from typing_extensions import deprecated

import anyio

from .._retry import TRANSIENT_ERRORS
from ._poller import _is_status, aiter_work, _is_fatal_4xx
from ..._types import Headers, NotGiven, not_given
from ..._utils import is_mapping
from ..._exceptions import APIStatusError
from .._scoped_client import _copy_client_with_bearer_auth
from ..tools._memories import (
    MEMORY_FLUSH_TIMEOUT,
    MIN_MEMORY_SYNC_INTERVAL,
    DEFAULT_MEMORY_SYNC_INTERVAL,
    MemoryDeleteMode,
    SessionMemoryError,
    SessionMemoryStores,
    _check_sync_interval,
)
from ..tools._deprecations import UNRESTRICTED_PATHS_DEPRECATION, reject_unrestricted_paths
from ...types.beta.environments import BetaSelfHostedWork, BetaSessionWorkData
from ..tools._beta_session_runner import (
    DEFAULT_MAX_IDLE,
    BetaAnyRunnableTool,
    _run_session_tools,
)

if TYPE_CHECKING:
    from ..._client import AsyncAnthropic
    from ...types.beta import BetaManagedAgentsSession
    from ..tools.agent_toolset import AgentToolContext
    from ...resources.beta.environments.work import AsyncWork

# ``agent_toolset`` pulls in host-only modules (``subprocess``, ``tarfile``, …),
# so it is never imported at module level here — only as a type above, and
# lazily for its values inside ``_tools_for`` / ``_handle_item``. That keeps this
# module host-dep-free so the generated ``work`` resource can expose
# ``EnvironmentWorker`` without dragging those imports into ``import anthropic``.

__all__ = [
    "EnvironmentWorker",
    "EnvironmentWorkerTools",
    "DEFAULT_MEMORY_SYNC_INTERVAL",
    "MIN_MEMORY_SYNC_INTERVAL",
    "MEMORY_FLUSH_TIMEOUT",
]

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


class _LeaseEndReason(enum.Enum):
    """Why heartbeating of a work item ended, as recorded on its :class:`_Lease`."""

    RUNNER_DONE = "runner_done"  # the session run ended first; the lease was held throughout
    CONTROL_PLANE_STOP = "control_plane_stop"  # state stopping / stopped, or lease_extended false
    LEASE_LOST = "lease_lost"  # a heartbeat met 412: the item was re-queued or another worker holds it
    HEARTBEAT_REJECTED = "heartbeat_rejected"  # a heartbeat met another 4xx that retrying will not fix
    ASSUMED_LOST = "assumed_lost"  # no heartbeat succeeded for a full lease TTL


class _Lease:
    """This worker's view of one work-item lease: whether it has ended, and why.

    Shared by :func:`_heartbeat_loop` and the code serving the item. The first
    recorded reason wins, so a run cancelled *because* the lease was lost still
    reads as lost afterwards.
    """

    _end_reason: _LeaseEndReason | None

    def __init__(self) -> None:
        self._end_reason = None
        self._ended = anyio.Event()

    def finish(self, reason: _LeaseEndReason) -> None:
        if self._end_reason is None:
            self._end_reason = reason
        self._ended.set()

    @property
    def ended(self) -> bool:
        return self._ended.is_set()

    async def wait_ended(self) -> None:
        await self._ended.wait()

    @property
    def lost(self) -> bool:
        """True once the item belongs to the queue or another worker, so this one must not stop it."""
        return self._end_reason in (_LeaseEndReason.LEASE_LOST, _LeaseEndReason.ASSUMED_LOST)


def _server_lease_state(err: APIStatusError) -> Mapping[str, object]:
    """The server's view of the lease carried by a 412 heartbeat response, or empty if absent."""
    node: object = err.body
    for key in ("error", "details", "current_state"):
        if not is_mapping(node):
            return {}
        node = node.get(key)
    return node if is_mapping(node) else {}


async def _heartbeat_loop(
    work: AsyncWork,
    *,
    work_id: str,
    environment_id: str,
    lease: _Lease,
    extra_headers: Headers | None = None,
    on_lease_ttl: Callable[[float], object] | None = None,
) -> None:
    """Keep the work-item lease alive while a session is being served.

    ``work`` must be bound to a sub-client authenticated for the environment;
    this loop adds no auth of its own. Returns once ``lease`` has ended, and
    ends it itself when the control plane reports the work is ``stopping`` /
    ``stopped`` or no longer extends the lease, when a heartbeat is rejected
    (a 412 means the lease already belongs to someone else), or when
    transient failures have run long enough that the lease must be assumed
    lost (so two runners don't end up serving the same work). ``on_lease_ttl``
    is called with the server-reported TTL after every successful beat.
    """
    interval = _HEARTBEAT_DEFAULT
    ttl = _HEARTBEAT_TTL_DEFAULT
    last = _NO_HEARTBEAT_SENTINEL
    last_success = time.monotonic()
    while not lease.ended:
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
            if _is_status(e, 412):
                server = _server_lease_state(e)
                log.error(
                    "lease lost: heartbeat precondition failed work_id=%s "
                    "server_state=%s server_ttl_seconds=%s server_last_heartbeat=%s",
                    work_id,
                    server.get("state"),
                    server.get("ttl_seconds"),
                    server.get("last_heartbeat"),
                )
                lease.finish(_LeaseEndReason.LEASE_LOST)
                return
            if _is_fatal_4xx(e):
                log.error("permanent heartbeat failure error=%s", e)
                lease.finish(_LeaseEndReason.HEARTBEAT_REJECTED)
                return
            # A transient failure (5xx, timeout, connection error) is not a 4xx,
            # so retrying forever risks split-brain once the lease expires. If no
            # heartbeat has succeeded within the lease TTL, assume it's lost.
            if time.monotonic() - last_success > ttl:
                log.error("lease assumed lost: no successful heartbeat in %.0fs error=%s", ttl, e)
                lease.finish(_LeaseEndReason.ASSUMED_LOST)
                return
            log.warning("transient heartbeat failure error=%s", e)
        else:
            last = resp.last_heartbeat
            last_success = time.monotonic()
            if resp.ttl_seconds > 0:
                ttl = resp.ttl_seconds
                interval = max(1.0, min(resp.ttl_seconds / 2, _HEARTBEAT_DEFAULT))
                if on_lease_ttl is not None:
                    on_lease_ttl(ttl)
            if resp.state in ("stopping", "stopped") or not resp.lease_extended:
                log.info("heartbeat signals shutdown state=%s lease_extended=%s", resp.state, resp.lease_extended)
                lease.finish(_LeaseEndReason.CONTROL_PLANE_STOP)
                return
        with anyio.move_on_after(interval):
            await lease.wait_ended()


def _flattened_causes(exc: BaseException) -> str:
    """The causes under an exception group — anyio's wrapper message says nothing."""
    inner = getattr(exc, "exceptions", None)
    if not inner:
        return str(exc)
    return "; ".join(_flattened_causes(e) for e in inner)


def _has_memory_store(session: BetaManagedAgentsSession) -> bool:
    """True when the session has at least one memory store attached."""
    return any(r.type == "memory_store" for r in session.resources)


def _sessions_token_from_secret(secret: str | None) -> str | None:
    """Extract the per-item sessions token from a work item's ``secret`` payload.

    The ``secret`` the poll response populates is not itself a credential: it
    is a URL-safe base64 JSON payload bundling the per-item material — the
    ``sessions_token`` (the bearer for this item's work lifecycle and
    session-level calls) plus ingress / source tokens this worker does not
    consume. Returns the sessions token, or ``None`` (meaning: fall back to
    the environment key) when the payload is missing, doesn't decode, or
    carries no token. Never log the payload or anything extracted from it.
    """
    if not secret:
        return None
    try:
        # The payload may arrive without base64 padding; restore it.
        decoded = base64.urlsafe_b64decode(secret + "=" * (-len(secret) % 4))
        parsed: object = json.loads(decoded)
    except (ValueError, TypeError):
        return None
    if not isinstance(parsed, dict):
        return None
    payload = cast("dict[str, object]", parsed)
    token = payload.get("sessions_token")
    return token if isinstance(token, str) and token else None


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
    the work item (unless the lease was lost, in which case the item is left to
    whoever holds it now) and loops to the next one.

    The ``environment_key`` is the worker's standing credential: polling
    always uses it, and per-session calls fall back to it when a work item's
    ``secret`` doesn't yield a sessions token (every request rides a
    Bearer-only scoped sub-client, never the parent client's ``X-Api-Key``).

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
      environment_key: The environment key — the worker's standing credential.
        Used as the Bearer credential on the scoped sub-clients the worker
        constructs for the control-plane (poll / ack / stop) and session-level
        (events stream / list / send + heartbeat / force-stop) calls, except
        where a claimed item's own ``secret`` takes precedence (see the class
        docstring). Required by :meth:`run`; :meth:`handle_item` falls back to
        it (then to ``ANTHROPIC_ENVIRONMENT_KEY``) when not passed one.
      tools: Tools to expose to each claimed session. Either a fixed list, or a
        factory invoked once per session with that session's
        :class:`AgentToolContext`. Defaults to
        ``beta_agent_toolset_20260401(env)`` (the standard
        ``agent_toolset_20260401`` set bound to the per-session context).
        Async tools share the event loop with the lease heartbeat, so keep
        them non-blocking.
      workdir: Base directory for the per-session :class:`AgentToolContext`.
        Defaults to :func:`os.getcwd` captured when the worker is constructed
        (matches the TS worker's ``process.cwd()``-at-construction), so a
        ``chdir`` between constructing the worker and serving a session does not
        change where tools resolve paths.
      unrestricted_paths: Deprecated and no longer accepted; passing either value
        raises :class:`TypeError` (see :class:`AgentToolContext`).
      max_idle: Forwarded to the session tool runner — seconds to keep running
        after the session goes idle with ``stop_reason`` ``end_turn``. Defaults
        to :data:`~anthropic.lib.environments.DEFAULT_MAX_IDLE` (60s). ``None``
        disables it.
      memory_sync_interval: How often (seconds) to sync the session's
        attached memory stores back while it runs — checked after each
        dispatched tool call, plus one final sync when the session ends
        cleanly. Defaults to :data:`DEFAULT_MEMORY_SYNC_INTERVAL` (15s).
        The interval floors at :data:`MIN_MEMORY_SYNC_INTERVAL` (5s): any
        value below it raises :class:`ValueError` — each sync lists every
        attached store, and a tighter cadence would hammer the memory
        endpoints.
        A session that ends on an error or cancel instead gets a
        push-only flush — best-effort, bounded by
        :data:`MEMORY_FLUSH_TIMEOUT` like the final sync, with a warning
        logged when either bound cuts work off; it deletes and pulls
        nothing, so an errored session can still lose its last edits.
        ``None`` disables memory download and sync entirely. Memory
        stores are only touched for work items whose ``secret`` carries a
        ``sessions_token``; while memory sync is enabled, a work item
        without one fails when its session has memory stores attached,
        because those stores cannot be mounted without the token. With
        ``None`` the same item runs, without memory, and nothing is
        logged — disabling sync is the operator's explicit choice.
      memory_sync_deletions: Whether a file deleted locally in a memory
        store's folder may delete its server memory. ``"log_only"`` runs
        the same checks and only logs — use it to watch a deployment
        before trusting ``"enabled"``; ``"disabled"`` never deletes.
        Uploads and pulls are unaffected. Defaults to ``"enabled"``.
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

    @overload
    def __init__(
        self,
        client: AsyncAnthropic,
        *,
        environment_id: str | None = None,
        environment_key: str | None = None,
        tools: EnvironmentWorkerTools | None = None,
        workdir: str | os.PathLike[str] | None = None,
        max_file_bytes: int | None | NotGiven = not_given,
        max_idle: float | None = DEFAULT_MAX_IDLE,
        memory_sync_interval: float | None = DEFAULT_MEMORY_SYNC_INTERVAL,
        memory_sync_deletions: MemoryDeleteMode = "enabled",
        worker_id: str | None = None,
        extra_headers: Headers | None = None,
    ) -> None: ...

    @overload
    @deprecated(UNRESTRICTED_PATHS_DEPRECATION)
    def __init__(
        self,
        client: AsyncAnthropic,
        *,
        environment_id: str | None = None,
        environment_key: str | None = None,
        tools: EnvironmentWorkerTools | None = None,
        workdir: str | os.PathLike[str] | None = None,
        unrestricted_paths: bool,
        max_file_bytes: int | None | NotGiven = not_given,
        max_idle: float | None = DEFAULT_MAX_IDLE,
        memory_sync_interval: float | None = DEFAULT_MEMORY_SYNC_INTERVAL,
        memory_sync_deletions: MemoryDeleteMode = "enabled",
        worker_id: str | None = None,
        extra_headers: Headers | None = None,
    ) -> None: ...

    def __init__(
        self,
        client: AsyncAnthropic,
        *,
        environment_id: str | None = None,
        environment_key: str | None = None,
        tools: EnvironmentWorkerTools | None = None,
        workdir: str | os.PathLike[str] | None = None,
        unrestricted_paths: bool | NotGiven = not_given,
        max_file_bytes: int | None | NotGiven = not_given,
        max_idle: float | None = DEFAULT_MAX_IDLE,
        memory_sync_interval: float | None = DEFAULT_MEMORY_SYNC_INTERVAL,
        memory_sync_deletions: MemoryDeleteMode = "enabled",
        worker_id: str | None = None,
        extra_headers: Headers | None = None,
    ) -> None:
        reject_unrestricted_paths(unrestricted_paths)
        self._client = client
        self._environment_id = environment_id
        self._environment_key = environment_key
        self._tools = tools
        # Snapshot the cwd at construction time when no explicit workdir was
        # given (TS parity: ``process.cwd()`` captured up front). Resolving "."
        # lazily at first tool use would instead pick up any intervening chdir.
        self._workdir: str | os.PathLike[str] = os.getcwd() if workdir is None else workdir
        self._max_file_bytes = max_file_bytes
        self._max_idle = max_idle
        if memory_sync_interval is not None:
            _check_sync_interval(memory_sync_interval)
        self._memory_sync_interval = memory_sync_interval
        self._memory_sync_deletions: MemoryDeleteMode = memory_sync_deletions
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
            try:
                await self._handle_item(work_item, environment_key)
            except Exception as e:  # noqa: BLE001
                # One bad item fails that item, not the worker: the teardown
                # already stopped or released it, so polling continues.
                # Cancellation is a BaseException and still ends the loop.
                log.error("work item failed work_id=%s error=%s", work_item.id, _flattened_causes(e))

    async def handle_item(
        self,
        *,
        work_id: str | None = None,
        environment_id: str | None = None,
        session_id: str | None = None,
        environment_key: str | None = None,
        work_secret: str | None = None,
    ) -> None:
        """Service a single, already-claimed work item without the poll loop.

        Builds the per-session :class:`AgentToolContext` (workdir from this
        worker's options) and downloads the session agent's skills, then runs a
        :class:`SessionToolRunner` for the session *while* heartbeating the
        work-item lease in parallel, and force-stops the work item on exit
        (whether the runner finishes normally, raises, or the control plane
        signals shutdown). The one exception is a lost lease: the item then
        belongs to the queue or another worker and is left alone.

        Use this when something else does the claiming — e.g. a
        ``worker poll --on-work`` script that hands an already-claimed item to a
        fresh process. ``work_id`` / ``environment_id`` / ``session_id`` fall
        back to ``ANTHROPIC_WORK_ID`` / ``ANTHROPIC_ENVIRONMENT_ID`` /
        ``ANTHROPIC_SESSION_ID`` (the env vars that command sets) when not
        passed; ``environment_key`` resolves in order: the explicit argument,
        then this worker's own ``environment_key``, then
        ``ANTHROPIC_ENVIRONMENT_KEY`` — so with no arguments inside that command
        it just works.

        ``work_secret`` is the work item's per-item ``secret`` payload from the
        poll response, falling back to ``ANTHROPIC_WORK_SECRET``. Unlike the
        others it is optional. When present, the sessions token extracted from
        it is preferred as the Bearer credential for this item's heartbeat,
        force-stop, and session calls. When absent or undecodable, those calls
        use ``environment_key``.

        Non-session work items are ignored (but still force-stopped so the
        lease doesn't sit until TTL).

        Raises:
          ValueError: if any of ``work_id`` / ``environment_id`` / ``session_id``
            / ``environment_key`` is still empty after the fallbacks.
          SessionMemoryError: if the session has memory stores attached but
            they cannot be mounted — the work item carried no
            ``sessions_token``, or a store failed to download. May arrive
            wrapped in an ``ExceptionGroup`` by the task group.
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

        # The per-item secret is optional: explicit arg -> ANTHROPIC_WORK_SECRET
        # -> None (use the environment key).
        work_secret = work_secret or os.environ.get("ANTHROPIC_WORK_SECRET")

        # The per-item flow only reads work.id / work.environment_id /
        # work.secret / work.data.type / work.data.id, so a minimally populated
        # model is enough.
        work_item = BetaSelfHostedWork.model_construct(
            id=work_id,
            environment_id=environment_id,
            secret=work_secret,
            data=BetaSessionWorkData.model_construct(type="session", id=session_id),
        )
        await self._handle_item(work_item, environment_key)

    async def _handle_item(self, work_item: BetaSelfHostedWork, environment_key: str) -> None:
        """The per-item body shared by :meth:`run`'s poll loop and :meth:`handle_item`.

        Runs a :class:`SessionToolRunner` for the work item's session while
        heartbeating its lease, force-stopping the work item on exit unless the
        lease was lost. All control-plane traffic for this work item —
        heartbeat + force-stop — flows through a Bearer-only sub-client built
        here; the session tool runner builds its own
        ``session-tool-runner``-tagged sub-client internally.

        When the poll response carried a per-item ``secret`` (a short-lived
        payload scoped to this work item), the sessions token extracted from
        it is preferred over ``environment_key`` as the Bearer credential for
        those per-item calls; a missing/undecodable secret falls back to
        ``environment_key`` unchanged.
        """
        # Lazy import: keeps the host-only ``agent_toolset`` module out of this
        # module's import graph (see the note next to the imports).
        from ..tools.agent_toolset import AgentToolContext

        # The per-item credential: the sessions token carried inside the work
        # item's secret payload when the server issued one, otherwise the
        # environment key. ``getattr`` because items synthesized by older
        # callers (or test fakes) may predate the field. Never log this value.
        secret = getattr(work_item, "secret", None)
        sessions_token = _sessions_token_from_secret(secret)
        if secret and sessions_token is None:
            log.warning(
                "work item carried a secret payload but no sessions token could be extracted; "
                "falling back to the environment key work_id=%s",
                work_item.id,
            )
        item_credential = sessions_token or environment_key

        # ``environments-worker``-scoped sub-client for the heartbeat and
        # force-stop calls this item drives. The session tool runner is given
        # the parent client + the same per-item credential and builds its own
        # sub-client.
        worker_client = _copy_client_with_bearer_auth(
            self._client, auth_token=item_credential, helper="environments-worker"
        )
        work_res = worker_client.beta.environments.work
        # Memory stores: the memory_stores endpoints accept the per-item
        # sessions token but reject the environment key, so download and sync
        # only run when the item carried a usable secret (and the interval is
        # set). ``worker_client`` is already scoped to that token then, so the
        # memory calls ride the same sub-client.
        interval = self._memory_sync_interval
        stores: SessionMemoryStores | None = None
        if sessions_token is not None and interval is not None:
            stores = SessionMemoryStores(
                worker_client,
                workdir=self._workdir,
                sync_interval=interval,
                sync_deletions=self._memory_sync_deletions,
            )
        else:
            log.debug("memory stores disabled for this item work_id=%s", work_item.id)
        lease = _Lease()
        try:
            # The queue also sends "healthcheck" items, which the generated type does not model.
            work_type: str = work_item.data.type
            if work_type != "session":
                log.debug("skipping non-session work item work_id=%s type=%s", work_item.id, work_type)
                return
            session_id = work_item.data.id
            clean_end = False
            async with anyio.create_task_group() as tg:
                # Latest server-reported lease TTL; the runner reads it back as
                # its tool-result send retry window.
                lease_ttl: float | None = None

                def _on_lease_ttl(ttl: float) -> None:
                    nonlocal lease_ttl
                    lease_ttl = ttl

                async def _heartbeat(
                    work_id: str = work_item.id,
                    environment_id: str = work_item.environment_id,
                ) -> None:
                    try:
                        await _heartbeat_loop(
                            work_res,
                            work_id=work_id,
                            environment_id=environment_id,
                            lease=lease,
                            extra_headers=self._extra_headers,
                            on_lease_ttl=_on_lease_ttl,
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
                # One session fetch, shared by the skills download and the
                # memory-store download — two fetches could disagree about the
                # attached resources.
                session = await worker_client.beta.sessions.retrieve(session_id)
                # Only here, after the fetch, can we tell a session that
                # simply has no memory from one whose memory we cannot mount.
                # The interval knob is a deliberate opt-out and stays quiet.
                if stores is None and interval is not None and _has_memory_store(session):
                    raise SessionMemoryError(
                        "this session has memory stores attached, but the work item carried no "
                        "sessions token; the memory endpoints reject the environment key, so the "
                        "session's memories cannot be mounted. The work item was failed rather "
                        "than run without them, matching how hosted sandboxes behave "
                        f"(work_id={work_item.id}, session_id={session_id})"
                    )
                env = AgentToolContext(
                    workdir=self._workdir,
                    max_file_bytes=self._max_file_bytes,
                    client=worker_client,
                    session=session,
                )
                try:
                    await env.__aenter__()
                    if stores is not None:
                        await stores.download(session)
                        # A store mounted outside the workdir must stay reachable
                        # by the file tools; read-only stores still refuse writes
                        # via read_only_roots.
                        env.allowed_roots = stores.roots
                        env.read_only_roots = stores.read_only_roots
                    tools = self._tools_for(env)
                    async with _run_session_tools(
                        self._client,
                        session_id,
                        tools=tools,
                        max_idle=self._max_idle,
                        # Despite the parameter name, this is just the
                        # runner's Bearer credential (see its docstring).
                        environment_key=item_credential,
                        extra_headers=self._extra_headers,
                        send_retry_window=lambda: lease_ttl,
                    ) as calls:
                        async for _ in calls:
                            if stores is not None:
                                await stores.sync_if_due()
                        # The last full sync runs in the teardown below,
                        # after the bash subprocesses are killed — its
                        # waived delete window must not race a writer.
                        clean_end = True
                finally:
                    # The heartbeat keeps the lease alive until this teardown is done.
                    with anyio.CancelScope(shield=True):
                        try:
                            # First — so nothing is still writing when the syncs read.
                            await env.__aexit__(None, None, None)
                        finally:
                            if stores is not None:
                                if clean_end:
                                    with anyio.move_on_after(MEMORY_FLUSH_TIMEOUT) as scope:
                                        await stores.finish()
                                    if scope.cancelled_caught:
                                        log.warning(
                                            "final memory sync cut off after %gs; the flush that follows still "
                                            "uploads changed files work_id=%s session_id=%s",
                                            MEMORY_FLUSH_TIMEOUT,
                                            work_item.id,
                                            session_id,
                                        )
                                # Push whatever is still on disk before dispose
                                # removes it — even after finish(), which may
                                # have failed or timed out; a clean flush is free.
                                with anyio.move_on_after(MEMORY_FLUSH_TIMEOUT) as scope:
                                    await stores.flush_writes()
                                if scope.cancelled_caught:
                                    log.warning(
                                        "memory flush cut off after %gs; changed files it had not uploaded yet "
                                        "are not saved work_id=%s session_id=%s",
                                        MEMORY_FLUSH_TIMEOUT,
                                        work_item.id,
                                        session_id,
                                    )
                                await stores.dispose()
                lease.finish(_LeaseEndReason.RUNNER_DONE)
                tg.cancel_scope.cancel()
        finally:
            # Stop only an item this worker still holds — after a lost lease it
            # belongs to the queue or another worker. A 409 means it already
            # stopped; shielded so the post survives surrounding cancellation.
            if lease.lost:
                log.info(
                    "lease lost; released work_id=%s session_id=%s without stopping it",
                    work_item.id,
                    work_item.data.id,
                )
            else:
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
