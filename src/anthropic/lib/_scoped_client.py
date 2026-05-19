"""Shared util for building a Bearer-only sub-client for a helper.

Several helpers (the environment poller, the environment worker, the session
tool runner) need to issue requests authenticated by a per-helper credential
(a self-hosted environment key, today) rather than the parent client's own
``X-Api-Key``. They each want to inherit the parent's full configuration —
``timeout``, ``max_retries``, ``http_client``, custom ``default_headers``,
``default_query`` — and override only the auth bits, plus tag every request
with their own ``x-stainless-helper`` value.

:func:`_copy_client_with_bearer_auth` is the one shared construction.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Dict, Literal, TypeVar, cast

if TYPE_CHECKING:
    from .._client import Anthropic, AsyncAnthropic


__all__ = ["HelperTag", "_copy_client_with_bearer_auth"]


# The closed set of ``x-stainless-helper`` telemetry tags the runner helpers
# stamp on outgoing requests. Constrained via ``Literal`` so a typo at any
# call site is a type error rather than silently mistagged telemetry.
HelperTag = Literal["environments-work-poller", "environments-worker", "session-tool-runner"]


ClientT = TypeVar("ClientT", "Anthropic", "AsyncAnthropic")


def _copy_client_with_bearer_auth(client: ClientT, *, auth_token: str, helper: HelperTag) -> ClientT:
    """Return a copy of ``client`` authenticated with ``auth_token`` as Bearer.

    The returned sub-client inherits the parent's full configuration via
    ``client.copy()`` (``base_url``, ``timeout``, ``max_retries``,
    ``http_client``, ``default_query``, and any custom ``default_headers``).
    Overrides applied:

    - ``auth_token=auth_token`` — the new credential.
    - ``credentials=None`` — any inherited credentials provider is cleared so
      the bearer is the unambiguous auth.
    - ``default_headers`` merges in ``x-stainless-helper: <helper>`` so every
      request the sub-client issues is tagged for SDK telemetry without
      per-call plumbing.
    - ``api_key=None`` — the parent's ``X-Api-Key`` is cleared via a post-hoc
      mutation; today's ``copy()`` treats ``api_key=None`` as "inherit" via
      truthy-or, so the assignment is the only way to drop the parent's API
      key from the sub-client.
    - Any inherited ``Authorization`` / ``X-Api-Key`` entries in the parent's
      custom default-headers are stripped from the sub-client. They would
      otherwise win over the bearer we just set, because
      :meth:`AsyncAnthropic.default_headers` merges ``_custom_headers`` after
      ``auth_headers`` (and so beats the ``Authorization`` value produced by
      ``auth_token``).
    """
    if not auth_token:
        raise ValueError(f"Expected a non-empty value for `auth_token` but received {auth_token!r}")
    scoped = client.copy(
        auth_token=auth_token,
        credentials=None,
        default_headers={"x-stainless-helper": helper},
    )
    scoped.api_key = None
    # ``_custom_headers`` is typed as ``Mapping[str, str]`` (immutable
    # interface) but is constructed as a plain ``dict`` at runtime — cast
    # so we can ``pop()`` keys without re-typing the base client.
    custom: Dict[str, str] = cast("Dict[str, str]", scoped._custom_headers)
    for key in list(custom):
        if key.lower() in ("authorization", "x-api-key"):
            custom.pop(key)
    return scoped
