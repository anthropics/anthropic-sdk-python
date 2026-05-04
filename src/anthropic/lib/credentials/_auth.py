from __future__ import annotations

import logging
import threading
from typing import Generator, AsyncGenerator
from typing_extensions import override

import httpx

from ._cache import TokenCache
from ..._utils import asyncify
from ._constants import OAUTH_API_BETA_HEADER

__all__ = ["AccessTokenAuth"]

log: logging.Logger = logging.getLogger(__name__)

_warn_once_lock = threading.Lock()
_warn_once_seen: set[str] = set()


def _warn_once(key: str, message: str, *args: object) -> None:
    """Emit a log warning at most once per ``key`` per process."""
    with _warn_once_lock:
        if key in _warn_once_seen:
            return
        _warn_once_seen.add(key)
    log.warning(message, *args)


def warn_explicit_static_shadows_credentials(param: str) -> None:
    """Warn that an explicit ``api_key=`` / ``auth_token=`` argument shadows
    an explicit ``credentials=`` provider passed to the same constructor or
    ``copy()`` call. The static credential wins at the request-header level
    (``AccessTokenAuth.sync_auth_flow`` short-circuits on the pre-set header),
    which silently disables the credentials provider.
    """
    _warn_once(
        f"explicit-shadow:{param}",
        "`%s=` was passed alongside `credentials=`; the static credential "
        "takes precedence and the credentials provider is silently disabled. "
        "Pass only one.",
        param,
    )


def warn_env_static_shadows_auto_discovery(env_var: str) -> None:
    """Warn that an ``ANTHROPIC_API_KEY`` / ``ANTHROPIC_AUTH_TOKEN`` from the
    environment is shadowing the SDK's profile / federation auto-discovery.

    Per the credential-precedence spec, a static-credential env var silently
    disables the auto-discovered federation and profile paths. Surface a
    one-shot warning so migrating users can see why their ``ANTHROPIC_PROFILE``
    or WIF env vars are being ignored.
    """
    _warn_once(
        f"env-shadow:{env_var}",
        "%s is set and takes precedence over the SDK's profile / federation "
        "auto-discovery; unset %s to use the auto-discovered credential.",
        env_var,
        env_var,
    )


class AccessTokenAuth(httpx.Auth):
    """Adapts a :class:`TokenCache` to httpx's :class:`~httpx.Auth` protocol.

    Used by :meth:`anthropic.Anthropic.custom_auth` to inject ``Authorization: Bearer``
    plus the OAuth beta header on every request, with proactive refresh handled by
    :class:`TokenCache`.

    Static credentials shadow federation: if the outgoing request already carries
    an ``X-Api-Key`` or ``Authorization`` header (set by the client's api_key /
    auth_token path), this auth flow is a no-op. That matches the Go SDK's
    ``authMiddleware`` and the documented precedence in the WIF user guide —
    a static ``ANTHROPIC_API_KEY`` shadows any credentials provider.
    """

    requires_response_body = False

    def __init__(self, token_cache: TokenCache) -> None:
        self._token_cache = token_cache

    @staticmethod
    def _has_static_credential(request: httpx.Request) -> bool:
        return bool(request.headers.get("X-Api-Key") or request.headers.get("Authorization"))

    def _apply(self, request: httpx.Request, token: str) -> None:
        request.headers["Authorization"] = f"Bearer {token}"
        existing_beta = request.headers.get("anthropic-beta", "")
        # Tokenize the comma-separated header so dedupe matches whole flag
        # names rather than substrings — `oauth-2025-04-20` would otherwise
        # spuriously match a future `oauth-2025-04-20b`.
        #
        # The flag we inject here is the *API* beta (oauth-2025-04-20), which
        # unlocks `Authorization: Bearer` auth on the API. The *federation*
        # beta (oidc-federation-2026-04-01) is a separate routing switch used
        # only on jwt-bearer POSTs to /v1/oauth/token — see _workload.py.
        existing_flags = [flag.strip() for flag in existing_beta.split(",") if flag.strip()]
        if OAUTH_API_BETA_HEADER not in existing_flags:
            existing_flags.append(OAUTH_API_BETA_HEADER)
            request.headers["anthropic-beta"] = ", ".join(existing_flags)

    @override
    def sync_auth_flow(self, request: httpx.Request) -> Generator[httpx.Request, httpx.Response, None]:
        if self._has_static_credential(request):
            yield request
            return
        token = self._token_cache.get_token()
        self._apply(request, token)
        yield request

    @override
    async def async_auth_flow(self, request: httpx.Request) -> AsyncGenerator[httpx.Request, httpx.Response]:
        if self._has_static_credential(request):
            yield request
            return
        # TokenCache.get_token is sync (and may make a blocking HTTP call); run it
        # in a worker thread to avoid blocking the event loop. Uses the same
        # ``asyncify`` helper as the rest of the SDK (see lib/vertex).
        token = await asyncify(self._token_cache.get_token)()
        self._apply(request, token)
        yield request
