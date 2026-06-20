"""Shared backoff / jitter / retry-classification helpers for the runner helpers.

Extracted so the control-plane poller, the session tool runner, and the worker
heartbeat all compute backoff and classify retryable failures the same way.
Consumed by the runner helpers only.
"""

from __future__ import annotations

import random

import httpx

from .._exceptions import APIError, APIStatusError

__all__ = ["backoff", "jitter", "is_fatal_status_error", "TRANSIENT_ERRORS"]

# The only exceptions a runner-helper retry loop should swallow and retry:
# transport-level httpx failures (connect/read timeouts, connection resets) and
# any SDK API error (covers APIConnectionError / APITimeoutError / APIStatusError
# — the 4xx-vs-transient split is then made by ``is_fatal_status_error``).
# Anything else (AttributeError, KeyError, …) is a real bug and must propagate
# instead of being silently retried forever.
TRANSIENT_ERRORS: tuple[type[Exception], ...] = (httpx.HTTPError, APIError)

# 4xx codes that are still worth retrying: request timeout, conflict, and rate
# limit. This matches the core client's retry policy — notably 409 is retryable
# there, so the runner helpers must not treat it as fatal either.
_RETRYABLE_4XX = frozenset({408, 409, 429})


def backoff(attempt: int, *, cap: float, base: float = 2.0) -> float:
    """Exponential backoff for ``attempt`` (1-indexed), capped at ``cap``."""
    return min(cap, base**attempt)


def jitter(low: float, high: float) -> float:
    """Uniform random delay in ``[low, high)`` — spreads out retry storms."""
    return random.uniform(low, high)


def is_fatal_status_error(err: Exception) -> bool:
    """True for a 4xx that retrying will not fix (bad key, missing resource).

    Aligns with the core client's ``_should_retry`` policy: 408 / 409 / 429 are
    transient and worth retrying; every other 4xx is fatal.
    """
    return isinstance(err, APIStatusError) and 400 <= err.status_code < 500 and err.status_code not in _RETRYABLE_4XX
