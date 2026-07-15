from __future__ import annotations

import time
import socket
import logging
from uuid import uuid4
from collections.abc import Iterator, AsyncIterator

import anyio

from .._retry import TRANSIENT_ERRORS, jitter, backoff, is_fatal_status_error
from ..._types import Headers, omit
from ..._exceptions import APIStatusError
from ...types.beta.environments import BetaSelfHostedWork
from ...resources.beta.environments.work import Work, AsyncWork

__all__ = [
    "iter_work",
    "aiter_work",
    "POLL_BLOCK_MS",
]

# API caps block_ms at 999; rely on client-side jitter between empty polls.
POLL_BLOCK_MS = 999
_POLL_BACKOFF_CAP = 60.0

log = logging.getLogger(__name__)


def _backoff(attempt: int) -> float:
    return backoff(attempt, cap=_POLL_BACKOFF_CAP)


def _jitter(low: float, high: float) -> float:
    return jitter(low, high)


def _is_fatal_4xx(err: Exception) -> bool:
    return is_fatal_status_error(err)


def _is_status(err: Exception, code: int) -> bool:
    return isinstance(err, APIStatusError) and err.status_code == code


def _default_worker_id() -> str:
    # The API documents anthropic_worker_id as a *unique* id, and multiple
    # workers can share a host, so the hostname alone is not enough — suffix it
    # with a uuid4 so each process gets a distinct, still-readable id.
    return f"{socket.gethostname()}-{uuid4().hex[:12]}"


def iter_work(
    work: Work,
    *,
    environment_id: str,
    worker_id: str | None = None,
    block_ms: int | None = POLL_BLOCK_MS,
    reclaim_older_than_ms: int | None = None,
    drain: bool = False,
    auto_stop: bool = True,
    extra_headers: Headers | None = None,
) -> Iterator[BetaSelfHostedWork]:
    """Iterate work items claimed from a self-hosted environment.

    Each yielded :class:`BetaSelfHostedWork` has already been ack'd. The ``work``
    resource must be bound to a client authenticated for the environment — the
    poller itself does not handle credentials. Use
    ``client.beta.environments.work.poller(...)`` for the user-facing entry
    point that constructs a scoped sub-client for you.

    Two consumption shapes are supported:

    - **Long-running runner** (``drain=False, auto_stop=True``, the default):
      loops forever, sleeps with jitter on empty polls, and calls ``work.stop``
      when the consuming for-loop body returns or raises. The poller owns the
      whole work-item lifecycle.
    - **Drain-and-dispatch** (``drain=True, auto_stop=False``): returns as soon
      as the queue is empty and never calls ``work.stop`` — use this when each
      yielded item is handed off to another process (e.g. a webhook handler
      that spawns a sandbox per work item) and that process owns ``stop``.

    Args:
      block_ms: How long the server holds an empty poll open (long-poll).
        Pass ``None`` to omit the param for a non-blocking poll — the server
        rejects ``0``. Drain callers usually want ``None`` so the final empty
        poll returns immediately.
      drain: When True, return after the first empty poll instead of sleeping
        and re-polling. Lets a webhook-driven dispatcher drain the queue and
        respond.
      auto_stop: When True (default), call ``work.stop`` after the consumer's
        loop body completes. Set False when the work item is handed off to
        another process that owns the stop call — otherwise the lease is
        terminated out from under it.
      reclaim_older_than_ms: Forwarded to ``work.poll``. Reclaim un-ack'd work
        older than this many ms. Useful in drain mode so a dead runner's
        work re-surfaces on the next webhook delivery.
      extra_headers: Optional headers passed through per request on every
        poll / ack / stop call (including the force-stop of an unprocessable
        item). They are threaded into each call's ``extra_headers=`` and are
        never assigned onto the client, so client state is not mutated.
        Credentials and ``x-stainless-helper`` come from the bound client,
        not this argument; a header given here overrides the bound client's
        same-named default for that one request, so use it for caller
        passthrough (e.g. trace ids), not to set auth.
    """
    worker_id = worker_id or _default_worker_id()
    log.info("poller starting environment_id=%s drain=%s auto_stop=%s", environment_id, drain, auto_stop)
    # Poll and ack each get their own backoff counter so a run of ack failures
    # can't inflate the next poll failure's backoff (and vice versa) — each is
    # reset on its own success, and the ``continue`` paths leave them untouched.
    poll_attempt = 0
    ack_attempt = 0
    while True:
        try:
            item = work.poll(
                environment_id,
                block_ms=block_ms if block_ms is not None else omit,
                reclaim_older_than_ms=reclaim_older_than_ms if reclaim_older_than_ms is not None else omit,
                anthropic_worker_id=worker_id,
                extra_headers=extra_headers,
            )
        except TRANSIENT_ERRORS as e:
            if _is_fatal_4xx(e):
                log.error("poll failed permanently error=%s", e)
                raise
            poll_attempt += 1
            wait = _backoff(poll_attempt) + _jitter(0.0, 1.0)
            log.warning("poll failed attempt=%d backoff=%.1fs error=%s", poll_attempt, wait, e)
            time.sleep(wait)
            continue
        poll_attempt = 0
        if item is None:
            if drain:
                log.info("queue drained environment_id=%s", environment_id)
                return
            time.sleep(_jitter(1.0, 3.0))
            continue
        log.info("claimed work work_id=%s work_type=%s", item.id, getattr(item.data, "type", None))
        try:
            work.ack(
                item.id,
                environment_id=environment_id,
                extra_headers=extra_headers,
            )
        except TRANSIENT_ERRORS as e:
            if _is_fatal_4xx(e):
                log.error("ack failed permanently; force-stopping work_id=%s error=%s", item.id, e)
                _force_stop_quietly(work, item.id, environment_id=environment_id, extra_headers=extra_headers)
                continue
            ack_attempt += 1
            wait = _backoff(ack_attempt) + _jitter(0.0, 1.0)
            log.warning(
                "ack failed, backing off work_id=%s attempt=%d backoff=%.1fs error=%s", item.id, ack_attempt, wait, e
            )
            time.sleep(wait)
            continue
        ack_attempt = 0
        if not auto_stop:
            yield item
            continue
        try:
            yield item
        finally:
            try:
                work.stop(
                    item.id,
                    environment_id=environment_id,
                    extra_headers=extra_headers,
                )
            except Exception as e:
                if not _is_status(e, 409):
                    log.warning("stop failed work_id=%s error=%s", item.id, e)


def _force_stop_quietly(work: Work, work_id: str, *, environment_id: str, extra_headers: Headers | None = None) -> None:
    """Best-effort ``work.stop(force=True)`` for an item that can't be processed.

    A 409 just means the work already stopped; anything else is logged but not
    raised, since the poll loop must keep going regardless.
    """
    try:
        work.stop(work_id, environment_id=environment_id, force=True, extra_headers=extra_headers)
    except Exception as e:
        if not _is_status(e, 409):
            log.error("force-stop of unprocessable work failed work_id=%s error=%s", work_id, e)


async def aiter_work(
    work: AsyncWork,
    *,
    environment_id: str,
    worker_id: str | None = None,
    block_ms: int | None = POLL_BLOCK_MS,
    reclaim_older_than_ms: int | None = None,
    drain: bool = False,
    auto_stop: bool = True,
    extra_headers: Headers | None = None,
) -> AsyncIterator[BetaSelfHostedWork]:
    """Async version of :func:`iter_work`. See its docstring for semantics,
    including how ``extra_headers`` is passed through per request.
    """
    worker_id = worker_id or _default_worker_id()
    log.info("poller starting environment_id=%s drain=%s auto_stop=%s", environment_id, drain, auto_stop)
    poll_attempt = 0
    ack_attempt = 0
    while True:
        try:
            item = await work.poll(
                environment_id,
                block_ms=block_ms if block_ms is not None else omit,
                reclaim_older_than_ms=reclaim_older_than_ms if reclaim_older_than_ms is not None else omit,
                anthropic_worker_id=worker_id,
                extra_headers=extra_headers,
            )
        except TRANSIENT_ERRORS as e:
            if _is_fatal_4xx(e):
                log.error("poll failed permanently error=%s", e)
                raise
            poll_attempt += 1
            wait = _backoff(poll_attempt) + _jitter(0.0, 1.0)
            log.warning("poll failed attempt=%d backoff=%.1fs error=%s", poll_attempt, wait, e)
            await anyio.sleep(wait)
            continue
        poll_attempt = 0
        if item is None:
            if drain:
                log.info("queue drained environment_id=%s", environment_id)
                return
            await anyio.sleep(_jitter(1.0, 3.0))
            continue
        log.info("claimed work work_id=%s work_type=%s", item.id, getattr(item.data, "type", None))
        try:
            await work.ack(
                item.id,
                environment_id=environment_id,
                extra_headers=extra_headers,
            )
        except TRANSIENT_ERRORS as e:
            if _is_fatal_4xx(e):
                log.error("ack failed permanently; force-stopping work_id=%s error=%s", item.id, e)
                await _aforce_stop_quietly(work, item.id, environment_id=environment_id, extra_headers=extra_headers)
                continue
            ack_attempt += 1
            wait = _backoff(ack_attempt) + _jitter(0.0, 1.0)
            log.warning(
                "ack failed, backing off work_id=%s attempt=%d backoff=%.1fs error=%s", item.id, ack_attempt, wait, e
            )
            await anyio.sleep(wait)
            continue
        ack_attempt = 0
        if not auto_stop:
            yield item
            continue
        try:
            yield item
        finally:
            try:
                await work.stop(
                    item.id,
                    environment_id=environment_id,
                    extra_headers=extra_headers,
                )
            except Exception as e:
                if not _is_status(e, 409):
                    log.warning("stop failed work_id=%s error=%s", item.id, e)


async def _aforce_stop_quietly(
    work: AsyncWork, work_id: str, *, environment_id: str, extra_headers: Headers | None = None
) -> None:
    """Async version of :func:`_force_stop_quietly`."""
    try:
        await work.stop(work_id, environment_id=environment_id, force=True, extra_headers=extra_headers)
    except Exception as e:
        if not _is_status(e, 409):
            log.error("force-stop of unprocessable work failed work_id=%s error=%s", work_id, e)
