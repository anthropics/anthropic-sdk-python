from __future__ import annotations

import time
import logging
from types import TracebackType
from typing import Any, Dict, Type, Optional
from typing_extensions import override

import httpx

from ._types import AccessToken, IdentityTokenProvider
from ._constants import (
    TOKEN_ENDPOINT,
    DEFAULT_BASE_URL,
    GRANT_TYPE_JWT_BEARER,
    OAUTH_API_BETA_HEADER,
    FEDERATION_BETA_HEADER,
    TOKEN_EXCHANGE_TIMEOUT,
    _user_agent,
    _require_https,
)
from ..._exceptions import AnthropicError

# jwt-bearer POSTs require BOTH beta headers — oauth-2025-04-20 unlocks the
# token endpoint family, and oidc-federation-2026-04-01 routes the POST to the
# Go userauth handler rather than the Python oauth_server.
_JWT_BEARER_BETA_HEADER = f"{OAUTH_API_BETA_HEADER},{FEDERATION_BETA_HEADER}"

# Max characters of response body kept on WorkloadIdentityError.body and in
# exception messages. Token endpoints sometimes echo back the assertion JWT or
# other sensitive material on error; truncating limits the blast radius if the
# exception ends up in user logs or crash reports.
_MAX_ERROR_BODY_CHARS = 256

# Hard limits on the wire size of the assertion JWT we send and the response
# body we accept from the token endpoint. JWTs from real IdPs are <4 KiB; a
# 16 KiB ceiling catches misconfiguration (e.g. a PEM cert path passed as the
# token) before we POST it. The 1 MiB response cap bounds memory if a misrouted
# endpoint streams back something pathological.
_MAX_ASSERTION_BYTES = 16 * 1024
_MAX_TOKEN_RESPONSE_BYTES = 1 << 20


def _request_id(resp: httpx.Response) -> Optional[str]:
    rid: Optional[str] = resp.headers.get("Request-Id") or resp.headers.get("request-id")
    return rid


def _redact_body(body: Any) -> Any:
    """Truncate a token-endpoint error body for safe inclusion in an exception."""
    if body is None:
        return None
    if isinstance(body, str):
        if len(body) <= _MAX_ERROR_BODY_CHARS:
            return body
        return body[:_MAX_ERROR_BODY_CHARS] + f"... <{len(body) - _MAX_ERROR_BODY_CHARS} more chars>"
    # For dict payloads, only keep OAuth standard error fields (RFC 6749 §5.2).
    if isinstance(body, dict):
        kept: Dict[str, Any] = {}
        for key in ("error", "error_description", "error_uri"):
            if key in body:
                kept[key] = body[key]
        return kept
    return None


def _raise_token_endpoint_error(resp: httpx.Response, *, message_prefix: str, hint: Optional[str] = None) -> None:
    """Raise a redacted :class:`WorkloadIdentityError` from a non-200 token-endpoint response.

    Shared between the jwt-bearer exchange path in this module and the
    refresh_token grant path in :mod:`_providers`.

    ``hint`` is an optional caller-supplied diagnostic appended verbatim to the
    error message (after the redacted body). Callers gate it on the response
    status and their own state — this helper does not inspect ``resp`` for it.
    """
    try:
        payload: Any = resp.json()
    except ValueError:
        payload = resp.text
    redacted = _redact_body(payload)
    message = f"{message_prefix} (HTTP {resp.status_code}): {redacted}"
    if hint:
        message = f"{message} {hint}"
    raise WorkloadIdentityError(
        message,
        status_code=resp.status_code,
        body=redacted,
        request_id=_request_id(resp),
    )


__all__ = ["WorkloadIdentityCredentials", "WorkloadIdentityError", "exchange_federation_assertion"]

log: logging.Logger = logging.getLogger(__name__)


class WorkloadIdentityError(AnthropicError):
    """Raised when the OIDC token exchange (``POST /v1/oauth/token``) fails."""

    status_code: Optional[int]
    body: Any
    request_id: Optional[str]

    def __init__(
        self,
        message: str,
        *,
        status_code: Optional[int] = None,
        body: Any = None,
        request_id: Optional[str] = None,
    ) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.body = body
        self.request_id = request_id

    @override
    def __str__(self) -> str:
        base = super().__str__()
        if self.request_id:
            return f"{base} [request_id={self.request_id}]"
        return base


class WorkloadIdentityCredentials:
    """Exchanges an external OIDC JWT for an Anthropic access token via the
    RFC 7523 ``jwt-bearer`` grant.

    This is an :class:`AccessTokenProvider`: calling it performs a *fresh* token
    exchange. Wrap in a :class:`TokenCache` (done automatically when passed as
    ``credentials=`` to :class:`anthropic.Anthropic`) to avoid exchanging on every
    request.

    Args:
        organization_id: The organization's raw UUID string (organizations do
            not use tagged IDs).
        workspace_id: Optional ``wrkspc_*`` tagged ID, or the literal
            ``"default"`` to scope the token to the organization's default
            workspace. When omitted the server picks the rule's sole enabled
            workspace, else the org default if the rule covers it. Required
            when the rule enables more than one non-default workspace, or to
            target a specific workspace other than the one the server would
            pick. The minted token is workspace-scoped: per-request workspace
            selection (the ``anthropic-workspace-id`` header) is not supported
            for federation tokens — switching workspaces requires a new token
            exchange with a different ``workspace_id``.
    """

    def __init__(
        self,
        *,
        identity_token_provider: IdentityTokenProvider,
        federation_rule_id: str,
        organization_id: str,
        service_account_id: Optional[str] = None,
        workspace_id: Optional[str] = None,
        scope: Optional[str] = None,
        http_client: Optional[httpx.Client] = None,
    ) -> None:
        self._identity_token_provider = identity_token_provider
        self._federation_rule_id = federation_rule_id
        self._organization_id = organization_id
        self._service_account_id = service_account_id
        self._workspace_id = workspace_id
        # Scope is informational only for federation: the server derives the
        # effective scope from the matching federation rule and the gateway
        # transform drops unknown body fields, so it is intentionally NOT sent
        # on the jwt-bearer request.
        self._scope = scope
        # The client passing this object as ``credentials=`` calls
        # :meth:`bind_base_url` to set its own endpoint, so the token exchange
        # and the API calls hit the same deployment. There is intentionally no
        # constructor kwarg for this: a token minted by one deployment is only
        # valid against that deployment, so splitting exchange-base from
        # client-base is always a bug.
        self._bound_base_url: Optional[str] = None
        if http_client is None:
            self._http_client = httpx.Client(timeout=TOKEN_EXCHANGE_TIMEOUT)
            self._owns_http_client = True
        else:
            self._http_client = http_client
            self._owns_http_client = False

    @property
    def scope(self) -> Optional[str]:
        return self._scope

    @property
    def _base_url(self) -> str:
        return self._bound_base_url or DEFAULT_BASE_URL

    def bind_base_url(self, base_url: str) -> None:
        """Set the API ``base_url`` the token exchange POSTs to.

        Called by :class:`anthropic.Anthropic` when this object is passed as
        ``credentials=``, so callers don't pass the same URL twice. For
        standalone use (no client) or tests, call this directly.
        """
        bound = base_url.rstrip("/")
        _require_https(bound, field="base_url")
        self._bound_base_url = bound

    def close(self) -> None:
        """Close the underlying ``httpx.Client`` if we created it."""
        if self._owns_http_client:
            self._http_client.close()

    def __enter__(self) -> "WorkloadIdentityCredentials":
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc: Optional[BaseException],
        tb: Optional[TracebackType],
    ) -> None:
        self.close()

    def __call__(self, *, force_refresh: bool = False) -> AccessToken:
        # Re-invoke the identity token provider every time — the underlying
        # file (e.g. a k8s projected SA token) may have rotated. force_refresh
        # is a no-op: this provider has no cache to bypass.
        del force_refresh
        jwt = self._identity_token_provider()

        if len(jwt.encode("utf-8")) > _MAX_ASSERTION_BYTES:
            raise WorkloadIdentityError(
                f"Identity token assertion is {len(jwt.encode('utf-8'))} bytes, which exceeds the "
                f"{_MAX_ASSERTION_BYTES}-byte limit. This is almost certainly not a JWT — check "
                f"that the identity-token path points at the projected token, not a key or cert."
            )

        body: Dict[str, str] = {
            "grant_type": GRANT_TYPE_JWT_BEARER,
            "assertion": jwt,
            "federation_rule_id": self._federation_rule_id,
            "organization_id": self._organization_id,
        }
        if self._service_account_id is not None:
            body["service_account_id"] = self._service_account_id
        if self._workspace_id is not None:
            body["workspace_id"] = self._workspace_id

        url = f"{self._base_url}{TOKEN_ENDPOINT}"
        try:
            resp = self._http_client.post(
                url,
                json=body,
                headers={
                    "anthropic-beta": _JWT_BEARER_BETA_HEADER,
                    "Content-Type": "application/json",
                    "User-Agent": _user_agent(),
                },
            )
        except httpx.HTTPError as err:
            raise WorkloadIdentityError(f"Failed to reach token endpoint {url}: {err}") from err

        request_id = _request_id(resp)

        if len(resp.content) > _MAX_TOKEN_RESPONSE_BYTES:
            raise WorkloadIdentityError(
                f"Token endpoint response body exceeds {_MAX_TOKEN_RESPONSE_BYTES} bytes "
                f"(got {len(resp.content)}); refusing to parse.",
                status_code=resp.status_code,
                request_id=request_id,
            )

        if resp.status_code >= 400:
            # A 401 is almost always a federation-rule mismatch. Point at the
            # rule and the Console auth-event log; when the caller hasn't pinned
            # a workspace, also surface the multi-workspace fix rather than
            # making them dig through docs.
            hint: Optional[str] = None
            if resp.status_code == 401:
                hint = "Ensure your federation rule matches your identity token. "
                if self._workspace_id is None:
                    hint += (
                        "If your federation rule is scoped to multiple workspaces, set the "
                        "ANTHROPIC_WORKSPACE_ID environment variable, the 'workspace_id' "
                        "config key, or the workspace_id= argument. "
                    )
                hint += "View your authentication events in the Workload identity page of Claude Console for more details."
            _raise_token_endpoint_error(resp, message_prefix="Token exchange failed", hint=hint)

        try:
            data = resp.json()
        except ValueError as err:
            redacted = _redact_body(resp.text)
            raise WorkloadIdentityError(
                f"Token endpoint returned non-JSON response (status {resp.status_code}): {redacted}",
                status_code=resp.status_code,
                body=redacted,
                request_id=request_id,
            ) from err

        token_type = data.get("token_type")
        if token_type is not None and str(token_type).lower() != "bearer":
            raise WorkloadIdentityError(
                f"Token endpoint returned unsupported token_type {token_type!r} (expected 'Bearer').",
                status_code=resp.status_code,
                body=_redact_body(data),
                request_id=request_id,
            )

        try:
            token = data["access_token"]
            # ``expires_in`` is a JSON number per RFC 6749 §5.1; coerce to int seconds.
            expires_in = int(data["expires_in"])
        except (KeyError, TypeError, ValueError) as err:
            raise WorkloadIdentityError(
                "Token endpoint response missing required fields (access_token / expires_in).",
                status_code=resp.status_code,
                body=_redact_body(data),
                request_id=request_id,
            ) from err

        return AccessToken(token=token, expires_at=int(time.time()) + expires_in)


def exchange_federation_assertion(
    *,
    assertion: str,
    federation_rule_id: str,
    organization_id: str,
    service_account_id: Optional[str] = None,
    workspace_id: Optional[str] = None,
    base_url: Optional[str] = None,
    http_client: Optional[httpx.Client] = None,
) -> AccessToken:
    """Perform a single RFC 7523 ``jwt-bearer`` exchange and return the resulting
    :class:`AccessToken`.

    This is a one-shot convenience wrapper around :class:`WorkloadIdentityCredentials`
    for callers that already have the assertion JWT in hand and just want the
    Anthropic access token back (no caching, no provider plumbing).
    """
    creds = WorkloadIdentityCredentials(
        identity_token_provider=lambda: assertion,
        federation_rule_id=federation_rule_id,
        organization_id=organization_id,
        service_account_id=service_account_id,
        workspace_id=workspace_id,
        http_client=http_client,
    )
    if base_url is not None:
        creds.bind_base_url(base_url)
    try:
        return creds()
    finally:
        creds.close()
