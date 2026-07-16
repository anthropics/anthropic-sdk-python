from __future__ import annotations

import os
import inspect
import threading
from typing import TYPE_CHECKING, Any, Union, Mapping, TypeVar, Callable, Sequence, Awaitable, cast
from functools import partial, cached_property
from typing_extensions import Self, override

import httpx

from ..._types import NOT_GIVEN, Headers, Timeout, NotGiven
from ..._utils import asyncify, is_given
from ..._client import Anthropic, AsyncAnthropic
from ..._models import FinalRequestOptions
from ..._streaming import Stream, AsyncStream
from ..._exceptions import AnthropicError
from ..._middleware import MiddlewareInput
from ..._base_client import DEFAULT_MAX_RETRIES, BaseClient, merge_headers
from .._extras._google_auth import refresh_credentials, load_default_credentials

# Bind the install-hint extra so a missing google-auth dep points users at
# `pip install anthropic[google_cloud]` rather than the vertex extra.
_load_adc_credentials = partial(load_default_credentials, extra="google_cloud")
_refresh_credentials = partial(refresh_credentials, extra="google_cloud")

if TYPE_CHECKING:
    from google.auth.credentials import Credentials as GoogleCredentials  # type: ignore


# The gateway base URL; stays overridable via the `base_url` argument and env var.
DEFAULT_URL_TEMPLATE = (
    "https://claude.googleapis.com/v1alpha/projects/{project}/locations/{location}/workspaces/{workspace_id}/invoke"
)

# Used when no location is configured; the gateway should always be addressed
# via the global region.
DEFAULT_LOCATION = "global"

TokenProvider = Callable[[], str]
AsyncTokenProvider = Callable[[], "str | Awaitable[str]"]

_HttpxClientT = TypeVar("_HttpxClientT", bound=Union[httpx.Client, httpx.AsyncClient])
_DefaultStreamT = TypeVar("_DefaultStreamT", bound=Union[Stream[Any], AsyncStream[Any]])


class _GoogleCredentialsState:
    """Holder for the Google credentials object, its refresh lock, and the project
    ADC resolved.

    Shared between a client and its ``copy()``/``with_options()`` clones (when the
    credential configuration is inherited) so a lazily-loaded ADC credential is
    minted once — not once per clone — and concurrent loads/refreshes are
    serialized: google-auth credential objects are not safe to ``refresh()``
    concurrently.
    """

    def __init__(self, credentials: GoogleCredentials | None) -> None:
        self._lock = threading.Lock()
        self.credentials: GoogleCredentials | None = credentials
        self.adc_project: str | None = None

    def token(self) -> str:
        """Return a valid access token, loading ADC / refreshing as needed. Blocking."""
        with self._lock:
            if self.credentials is None:
                self.credentials, self.adc_project = _load_adc_credentials()
            elif self.credentials.expired or not self.credentials.token:
                _refresh_credentials(self.credentials)

            token = self.credentials.token
            if not token:
                raise AnthropicError("Could not resolve a GCP access token from the configured Google credentials")
            assert isinstance(token, str)
            return token


class BaseGoogleCloudClient(BaseClient[_HttpxClientT, _DefaultStreamT]):
    """Marker base so ``_is_base_client()`` keeps these clients off the first-party
    credential-discovery chain (it matches only the exact ``Anthropic`` /
    ``AsyncAnthropic`` classes). Auth is handled entirely by this helper."""

    workspace_id: str | None
    _project: str | None
    _location: str
    _creds_state: _GoogleCredentialsState
    _base_url_deferred: bool
    _base_url_overridden: bool

    @property
    @override
    def base_url(self) -> httpx.URL:
        return self._base_url

    @base_url.setter
    def base_url(self, url: httpx.URL | str) -> None:
        # An explicit post-construction assignment wins over (and cancels) the
        # pending project back-fill.
        self._base_url_deferred = False
        self._base_url = self._enforce_trailing_slash(url if isinstance(url, httpx.URL) else httpx.URL(url))

    @property
    def google_credentials(self) -> GoogleCredentials | None:
        """The ``google.auth`` credentials in use (explicit or lazily-loaded ADC), if any.

        Distinct from ``.credentials``, which is the base client's first-party
        credentials provider and is always ``None`` on this client.
        """
        return self._creds_state.credentials

    def _resolve_deferred_base_url(self) -> None:
        """Derive and set the real base URL once the project is known.

        Called on every request (after the project back-fill from ADC, if any);
        a no-op once the base URL has been derived.
        """
        if not self._base_url_deferred:
            return
        if self._project is None:
            raise AnthropicError(
                "No `project` was provided and one could not be resolved from Google credentials. "
                "Pass the `project` argument, set the `ANTHROPIC_GOOGLE_CLOUD_PROJECT` "
                "environment variable, or provide `base_url` directly."
            )
        # Deferred derivation implies auth, and constructing with auth requires a workspace ID.
        assert self.workspace_id is not None
        self.base_url = DEFAULT_URL_TEMPLATE.format(
            project=self._project, location=self._location, workspace_id=self.workspace_id
        )
        self._base_url_deferred = False


def _resolve_base_url(
    *,
    base_url: str | httpx.URL | None,
    project: str | None,
    location: str,
    workspace_id: str | None,
    allow_deferred_project: bool,
) -> str | httpx.URL | None:
    """base_url (arg or ``ANTHROPIC_GOOGLE_CLOUD_BASE_URL``, resolved by the caller)
    > derived template.

    Returns ``None`` when derivation must wait for the project to be back-filled
    from Google credentials on the first request (``allow_deferred_project``).
    """
    if base_url is not None:
        return base_url

    # Derivation needs the workspace ID in the path; the constructors reject a
    # missing workspace before calling this without an explicit base_url.
    assert workspace_id is not None
    if project is None:
        if allow_deferred_project:
            return None
        raise ValueError(
            "No `project` was provided. Pass `project`, set the `ANTHROPIC_GOOGLE_CLOUD_PROJECT` "
            "environment variable, or provide `base_url` directly."
        )
    return DEFAULT_URL_TEMPLATE.format(project=project, location=location, workspace_id=workspace_id)


def _reject_skip_auth_conflict(
    *,
    skip_auth: bool,
    token_provider: object | None,
    credentials: object | None,
) -> None:
    if skip_auth and (token_provider is not None or credentials is not None):
        raise ValueError(
            "`skip_auth` is mutually exclusive with `token_provider` and `credentials`; "
            "`skip_auth` disables authentication entirely."
        )


def _project_from_credentials(credentials: GoogleCredentials) -> str | None:
    """Best-effort project from an explicit credentials object — service-account /
    impersonated credentials usually know theirs."""
    for attr in ("project_id", "quota_project_id"):
        value = getattr(credentials, attr, None)
        if isinstance(value, str) and value:
            return value
    return None


# ==============================================================================


class AnthropicGoogleCloud(BaseGoogleCloudClient[httpx.Client, Stream[Any]], Anthropic):
    """Synchronous client for the first-party Anthropic API served through Google's
    gateway (Claude Platform on Google Cloud).

    The whole first-party surface is proxied verbatim (no URL or body rewriting), so
    this subclasses the full ``Anthropic`` client. Authentication is a GCP bearer
    token; the deprecated Completions endpoint is not exposed.
    """

    workspace_id: str | None
    _skip_auth: bool

    def __init__(
        self,
        *,
        project: str | None = None,
        location: str | None = None,
        workspace_id: str | None = None,
        token_provider: TokenProvider | None = None,
        credentials: GoogleCredentials | None = None,
        skip_auth: bool = False,
        base_url: str | httpx.URL | None = None,
        timeout: float | Timeout | None | NotGiven = NOT_GIVEN,
        max_retries: int = DEFAULT_MAX_RETRIES,
        default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        http_client: httpx.Client | None = None,
        middleware: Sequence[MiddlewareInput] | None = None,
        _strict_response_validation: bool = False,
    ) -> None:
        """Construct a new synchronous Claude Platform on Google Cloud client.

        Auth precedence (first match wins, unless ``skip_auth=True``):
          1. ``token_provider`` — a callable returning a GCP access token, invoked per request.
          2. ``credentials`` — a ``google.auth`` Credentials object, refreshed as needed.
          3. Application Default Credentials (``google.auth.default``).

        Args:
            project: GCP consumer project id (or ``ANTHROPIC_GOOGLE_CLOUD_PROJECT``,
                else ``GOOGLE_CLOUD_PROJECT``). Only needed when the base URL must be
                derived; if omitted there, it is taken from an explicit ``credentials``
                object when it exposes one, or back-filled from ADC on the first request.
            location: GCP location (or ``ANTHROPIC_GOOGLE_CLOUD_LOCATION``). Optional —
                defaults to ``global``, the region the gateway should normally be
                addressed through.
            workspace_id: The Anthropic workspace ID (or ``ANTHROPIC_GOOGLE_CLOUD_WORKSPACE_ID``).
                Required unless ``skip_auth`` is set with an explicit ``base_url``.
            skip_auth: For pre-authenticated proxies — skips token attachment. A
                workspace ID is still needed to derive the base URL; pass ``base_url``
                to construct without one. Mutually exclusive with the credential
                arguments.
        """
        _reject_skip_auth_conflict(skip_auth=skip_auth, token_provider=token_provider, credentials=credentials)

        self._skip_auth = skip_auth
        self._token_provider = token_provider
        self._creds_state = _GoogleCredentialsState(credentials)
        if location is None:
            location = os.environ.get("ANTHROPIC_GOOGLE_CLOUD_LOCATION")
        if location is None:
            location = DEFAULT_LOCATION
        self._location = location
        if project is None:
            project = os.environ.get("ANTHROPIC_GOOGLE_CLOUD_PROJECT")
        if project is None:
            project = os.environ.get("GOOGLE_CLOUD_PROJECT")
        if project is None and credentials is not None:
            project = _project_from_credentials(credentials)
        self._project = project

        if base_url is None:
            base_url = os.environ.get("ANTHROPIC_GOOGLE_CLOUD_BASE_URL")
        # Distinguishes a user-supplied gateway URL from a template-derived one, so
        # `copy(project=..., location=...)` knows whether to re-derive.
        self._base_url_overridden = base_url is not None

        if workspace_id is None:
            workspace_id = os.environ.get("ANTHROPIC_GOOGLE_CLOUD_WORKSPACE_ID")
        # The workspace ID is required unless `skip_auth` is set together with an
        # explicit base URL — no URL to derive.
        if workspace_id is None and not (skip_auth and base_url is not None):
            raise ValueError(
                "No workspace ID found. Set the `workspace_id` argument or the "
                "`ANTHROPIC_GOOGLE_CLOUD_WORKSPACE_ID` environment variable."
            )
        self.workspace_id = workspace_id

        resolved_base_url = _resolve_base_url(
            base_url=base_url,
            project=self._project,
            location=self._location,
            workspace_id=self.workspace_id,
            # Without auth there are no Google credentials to back-fill the project from.
            allow_deferred_project=not skip_auth,
        )
        self._base_url_deferred = resolved_base_url is None

        super().__init__(
            # Deferred case: pass an empty (valid) URL so the parent doesn't fall through to
            # `ANTHROPIC_BASE_URL` / api.anthropic.com; `_prepare_options` derives the real
            # URL (or raises) before the first request is built.
            base_url=resolved_base_url if resolved_base_url is not None else "",
            timeout=timeout,
            max_retries=max_retries,
            default_headers=default_headers,
            default_query=default_query,
            http_client=http_client,
            middleware=middleware,
            _strict_response_validation=_strict_response_validation,
        )
        # Never inherit first-party static credentials from the environment — the
        # base reads ANTHROPIC_API_KEY/ANTHROPIC_AUTH_TOKEN when no explicit
        # credential is passed, which would otherwise leak as `X-Api-Key` to the
        # gateway host. `auth_headers` is also overridden below as a hard guarantee.
        self.api_key = None
        self.auth_token = None

    @cached_property
    @override
    def completions(self) -> None:  # type: ignore[override]
        """Completions endpoint is deprecated and not supported for the Google Cloud client."""
        return None

    @property
    @override
    def auth_headers(self) -> dict[str, str]:
        # Auth is a GCP bearer token attached in `_prepare_request`; never emit
        # first-party `X-Api-Key` / `Authorization` headers from static credentials.
        return {}

    @override
    def _validate_headers(self, headers: Headers, custom_headers: Headers) -> None:
        # The bearer token is attached per-request in `_prepare_request`, not via
        # default headers, so the base auth-presence check would false-negative.
        return

    def _get_token(self) -> str:
        provider = self._token_provider
        if provider is not None:
            token = provider()
            if inspect.isawaitable(token):
                cast(Any, token).close()
                raise AnthropicError(
                    "`token_provider` returned an awaitable. Async token providers are only "
                    "supported on `AsyncAnthropicGoogleCloud`."
                )
            return token

        return self._creds_state.token()

    @override
    def _prepare_options(self, options: FinalRequestOptions) -> FinalRequestOptions:
        if not self._skip_auth and self._base_url_deferred:
            if self._project is None and self._token_provider is None:
                # An ADC load also resolves the credentials' project; do it here —
                # independent of token attachment — so the back-fill happens even
                # when the request carries its own `Authorization` header.
                self._creds_state.token()
                self._project = self._creds_state.adc_project
            self._resolve_deferred_base_url()

        return options

    @override
    def _prepare_request(self, request: httpx.Request) -> None:
        if self._skip_auth:
            return

        if request.headers.get("Authorization") is not None:
            # A caller-supplied Authorization header (per-request, default_headers,
            # or ANTHROPIC_CUSTOM_HEADERS) wins; the check is case-insensitive so
            # we never emit two conflicting Authorization headers.
            return

        request.headers["Authorization"] = f"Bearer {self._get_token()}"

    def copy(  # type: ignore[override]  # pyright: ignore[reportIncompatibleMethodOverride] — subclass uses GCP auth
        self,
        *,
        project: str | None = None,
        location: str | None = None,
        workspace_id: str | None | NotGiven = NOT_GIVEN,
        token_provider: TokenProvider | None | NotGiven = NOT_GIVEN,
        credentials: GoogleCredentials | None | NotGiven = NOT_GIVEN,
        skip_auth: bool | None = None,
        base_url: str | httpx.URL | None = None,
        timeout: float | Timeout | None | NotGiven = NOT_GIVEN,
        http_client: httpx.Client | None = None,
        middleware: Sequence[MiddlewareInput] | None | NotGiven = NOT_GIVEN,
        max_retries: int | NotGiven = NOT_GIVEN,
        default_headers: Mapping[str, str] | None = None,
        set_default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        set_default_query: Mapping[str, object] | None = None,
        _extra_kwargs: Mapping[str, Any] = {},
    ) -> Self:
        """Create a new client re-using the current options, with optional overrides.

        Passing either of ``token_provider`` / ``credentials`` replaces the
        inherited credential configuration wholesale — the source not passed is
        cleared, so an explicit lower-precedence credential takes effect.
        ``workspace_id=None`` clears the workspace ID; ``project`` /
        ``location`` overrides re-derive a template-derived base URL.
        """
        if default_headers is not None and set_default_headers is not None:
            raise ValueError("The `default_headers` and `set_default_headers` arguments are mutually exclusive")

        if default_query is not None and set_default_query is not None:
            raise ValueError("The `default_query` and `set_default_query` arguments are mutually exclusive")

        headers = self._custom_headers
        if default_headers is not None:
            headers = merge_headers(headers, default_headers)
        elif set_default_headers is not None:
            headers = set_default_headers

        params = self._custom_query
        if default_query is not None:
            params = {**params, **default_query}
        elif set_default_query is not None:
            params = set_default_query

        resolved_skip_auth = skip_auth if skip_auth is not None else self._skip_auth
        credential_overridden = is_given(token_provider) or is_given(credentials)
        new_token_provider: TokenProvider | None = None
        new_credentials: GoogleCredentials | None = None
        if credential_overridden:
            new_token_provider = token_provider if is_given(token_provider) else None
            new_credentials = credentials if is_given(credentials) else None
        elif not resolved_skip_auth:  # don't round-trip credentials into a skip_auth clone
            new_token_provider = self._token_provider
            new_credentials = self._creds_state.credentials

        if base_url is None and not self._base_url_overridden:
            # The current URL is template-derived (or still pending); leave it unset
            # so __init__ re-derives from the new project/location.
            new_base_url: str | httpx.URL | None = None
        else:
            new_base_url = base_url if base_url is not None else self.base_url

        client = self.__class__(
            project=project if project is not None else self._project,
            location=location if location is not None else self._location,
            workspace_id=workspace_id if is_given(workspace_id) else self.workspace_id,
            token_provider=new_token_provider,
            credentials=new_credentials,
            skip_auth=resolved_skip_auth,
            base_url=new_base_url,
            timeout=self.timeout if isinstance(timeout, NotGiven) else timeout,
            http_client=http_client or self._client,
            max_retries=max_retries if is_given(max_retries) else self.max_retries,
            default_headers=headers,
            default_query=params,
            middleware=self._middleware if isinstance(middleware, NotGiven) else middleware,
            _strict_response_validation=self._strict_response_validation,
            **_extra_kwargs,
        )
        if not credential_overridden and not resolved_skip_auth:
            # Clones share lazily-loaded ADC credentials (and the refresh lock) so a
            # per-call `with_options()` clone doesn't mint its own token.
            client._creds_state = self._creds_state
        return client

    with_options = copy  # type: ignore[assignment]


class AsyncAnthropicGoogleCloud(BaseGoogleCloudClient[httpx.AsyncClient, AsyncStream[Any]], AsyncAnthropic):
    """Asynchronous client for the first-party Anthropic API served through Google's
    gateway (Claude Platform on Google Cloud). See ``AnthropicGoogleCloud``.
    """

    workspace_id: str | None
    _skip_auth: bool

    def __init__(
        self,
        *,
        project: str | None = None,
        location: str | None = None,
        workspace_id: str | None = None,
        token_provider: AsyncTokenProvider | None = None,
        credentials: GoogleCredentials | None = None,
        skip_auth: bool = False,
        base_url: str | httpx.URL | None = None,
        timeout: float | Timeout | None | NotGiven = NOT_GIVEN,
        max_retries: int = DEFAULT_MAX_RETRIES,
        default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        http_client: httpx.AsyncClient | None = None,
        middleware: Sequence[MiddlewareInput] | None = None,
        _strict_response_validation: bool = False,
    ) -> None:
        """Construct a new asynchronous Claude Platform on Google Cloud client.

        ``token_provider`` may be sync or async; sync providers are run off the
        event loop. See ``AnthropicGoogleCloud`` for the full argument and
        auth-precedence docs.
        """
        _reject_skip_auth_conflict(skip_auth=skip_auth, token_provider=token_provider, credentials=credentials)

        self._skip_auth = skip_auth
        self._token_provider = token_provider
        self._creds_state = _GoogleCredentialsState(credentials)
        if location is None:
            location = os.environ.get("ANTHROPIC_GOOGLE_CLOUD_LOCATION")
        if location is None:
            location = DEFAULT_LOCATION
        self._location = location
        if project is None:
            project = os.environ.get("ANTHROPIC_GOOGLE_CLOUD_PROJECT")
        if project is None:
            project = os.environ.get("GOOGLE_CLOUD_PROJECT")
        if project is None and credentials is not None:
            project = _project_from_credentials(credentials)
        self._project = project

        if base_url is None:
            base_url = os.environ.get("ANTHROPIC_GOOGLE_CLOUD_BASE_URL")
        self._base_url_overridden = base_url is not None

        if workspace_id is None:
            workspace_id = os.environ.get("ANTHROPIC_GOOGLE_CLOUD_WORKSPACE_ID")
        # The workspace ID is required unless `skip_auth` is set together with an
        # explicit base URL — no URL to derive.
        if workspace_id is None and not (skip_auth and base_url is not None):
            raise ValueError(
                "No workspace ID found. Set the `workspace_id` argument or the "
                "`ANTHROPIC_GOOGLE_CLOUD_WORKSPACE_ID` environment variable."
            )
        self.workspace_id = workspace_id

        resolved_base_url = _resolve_base_url(
            base_url=base_url,
            project=self._project,
            location=self._location,
            workspace_id=self.workspace_id,
            # Without auth there are no Google credentials to back-fill the project from.
            allow_deferred_project=not skip_auth,
        )
        self._base_url_deferred = resolved_base_url is None

        super().__init__(
            # Deferred case: pass an empty (valid) URL so the parent doesn't fall through to
            # `ANTHROPIC_BASE_URL` / api.anthropic.com; `_prepare_options` derives the real
            # URL (or raises) before the first request is built.
            base_url=resolved_base_url if resolved_base_url is not None else "",
            timeout=timeout,
            max_retries=max_retries,
            default_headers=default_headers,
            default_query=default_query,
            http_client=http_client,
            middleware=middleware,
            _strict_response_validation=_strict_response_validation,
        )
        self.api_key = None
        self.auth_token = None

    @cached_property
    @override
    def completions(self) -> None:  # type: ignore[override]
        """Completions endpoint is deprecated and not supported for the Google Cloud client."""
        return None

    @property
    @override
    def auth_headers(self) -> dict[str, str]:
        return {}

    @override
    def _validate_headers(self, headers: Headers, custom_headers: Headers) -> None:
        return

    async def _get_token(self) -> str:
        provider = self._token_provider
        if provider is not None:
            if inspect.iscoroutinefunction(provider):
                token = await provider()
                assert isinstance(token, str)
                return token
            # A plain sync provider may block on a token mint; run it off
            # the event loop so concurrent requests aren't stalled.
            token = await asyncify(provider)()
            if inspect.isawaitable(token):
                token = await token
            assert isinstance(token, str)
            return token

        return await asyncify(self._creds_state.token)()

    @override
    async def _prepare_options(self, options: FinalRequestOptions) -> FinalRequestOptions:
        if not self._skip_auth and self._base_url_deferred:
            if self._project is None and self._token_provider is None:
                # An ADC load also resolves the credentials' project; do it here —
                # independent of token attachment — so the back-fill happens even
                # when the request carries its own `Authorization` header.
                await asyncify(self._creds_state.token)()
                self._project = self._creds_state.adc_project
            self._resolve_deferred_base_url()

        return options

    @override
    async def _prepare_request(self, request: httpx.Request) -> None:
        if self._skip_auth:
            return

        if request.headers.get("Authorization") is not None:
            # A caller-supplied Authorization header (per-request, default_headers,
            # or ANTHROPIC_CUSTOM_HEADERS) wins; the check is case-insensitive so
            # we never emit two conflicting Authorization headers.
            return

        request.headers["Authorization"] = f"Bearer {await self._get_token()}"

    def copy(  # type: ignore[override]  # pyright: ignore[reportIncompatibleMethodOverride] — subclass uses GCP auth
        self,
        *,
        project: str | None = None,
        location: str | None = None,
        workspace_id: str | None | NotGiven = NOT_GIVEN,
        token_provider: AsyncTokenProvider | None | NotGiven = NOT_GIVEN,
        credentials: GoogleCredentials | None | NotGiven = NOT_GIVEN,
        skip_auth: bool | None = None,
        base_url: str | httpx.URL | None = None,
        timeout: float | Timeout | None | NotGiven = NOT_GIVEN,
        http_client: httpx.AsyncClient | None = None,
        middleware: Sequence[MiddlewareInput] | None | NotGiven = NOT_GIVEN,
        max_retries: int | NotGiven = NOT_GIVEN,
        default_headers: Mapping[str, str] | None = None,
        set_default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        set_default_query: Mapping[str, object] | None = None,
        _extra_kwargs: Mapping[str, Any] = {},
    ) -> Self:
        """Create a new client re-using the current options, with optional overrides.

        See ``AnthropicGoogleCloud.copy`` for the override semantics.
        """
        if default_headers is not None and set_default_headers is not None:
            raise ValueError("The `default_headers` and `set_default_headers` arguments are mutually exclusive")

        if default_query is not None and set_default_query is not None:
            raise ValueError("The `default_query` and `set_default_query` arguments are mutually exclusive")

        headers = self._custom_headers
        if default_headers is not None:
            headers = merge_headers(headers, default_headers)
        elif set_default_headers is not None:
            headers = set_default_headers

        params = self._custom_query
        if default_query is not None:
            params = {**params, **default_query}
        elif set_default_query is not None:
            params = set_default_query

        resolved_skip_auth = skip_auth if skip_auth is not None else self._skip_auth
        credential_overridden = is_given(token_provider) or is_given(credentials)
        new_token_provider: AsyncTokenProvider | None = None
        new_credentials: GoogleCredentials | None = None
        if credential_overridden:
            new_token_provider = token_provider if is_given(token_provider) else None
            new_credentials = credentials if is_given(credentials) else None
        elif not resolved_skip_auth:  # don't round-trip credentials into a skip_auth clone
            new_token_provider = self._token_provider
            new_credentials = self._creds_state.credentials

        if base_url is None and not self._base_url_overridden:
            # The current URL is template-derived (or still pending); leave it unset
            # so __init__ re-derives from the new project/location.
            new_base_url: str | httpx.URL | None = None
        else:
            new_base_url = base_url if base_url is not None else self.base_url

        client = self.__class__(
            project=project if project is not None else self._project,
            location=location if location is not None else self._location,
            workspace_id=workspace_id if is_given(workspace_id) else self.workspace_id,
            token_provider=new_token_provider,
            credentials=new_credentials,
            skip_auth=resolved_skip_auth,
            base_url=new_base_url,
            timeout=self.timeout if isinstance(timeout, NotGiven) else timeout,
            http_client=http_client or self._client,
            max_retries=max_retries if is_given(max_retries) else self.max_retries,
            default_headers=headers,
            default_query=params,
            middleware=self._middleware if isinstance(middleware, NotGiven) else middleware,
            _strict_response_validation=self._strict_response_validation,
            **_extra_kwargs,
        )
        if not credential_overridden and not resolved_skip_auth:
            # Clones share lazily-loaded ADC credentials (and the refresh lock) so a
            # per-call `with_options()` clone doesn't mint its own token.
            client._creds_state = self._creds_state
        return client

    with_options = copy  # type: ignore[assignment]
