# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import TYPE_CHECKING, Any, Mapping
from typing_extensions import Self, override

import httpx

from . import _constants, _exceptions
from ._qs import Querystring
from ._types import (
    Omit,
    Headers,
    Timeout,
    NotGiven,
    Transport,
    ProxiesTypes,
    RequestOptions,
    not_given,
)
from ._utils import (
    is_given,
    is_mapping_t,
    get_async_library,
)
from ._compat import cached_property
from ._version import __version__
from ._streaming import Stream as Stream, AsyncStream as AsyncStream
from ._exceptions import APIStatusError
from ._base_client import (
    DEFAULT_MAX_RETRIES,
    SyncAPIClient,
    AsyncAPIClient,
)

# --- credentials support (hand-written, upstream to Stainless) ---
from .lib.credentials import (
    TokenCache,
    InMemoryConfig,
    AccessTokenAuth,
    CredentialsFile,
    AccessTokenProvider,
    default_credentials,
)
from .lib.credentials._auth import (
    warn_env_static_shadows_auto_discovery,
    warn_explicit_static_shadows_credentials,
)
from .lib.credentials._constants import _has_auto_discoverable_credentials


def _is_base_client(client: object) -> bool:
    """True only for the base ``Anthropic`` / ``AsyncAnthropic`` classes, not subclasses.

    Subclasses (``AnthropicAWS``, ``AnthropicFoundry``) have their own auth paths
    and must not run the credential chain or forward ``credentials`` through their
    ``__init__`` (which doesn't accept the kwarg).
    """
    return type(client) in (Anthropic, AsyncAnthropic)


def _close_credentials(credentials: object) -> None:
    """Release any resources owned by a credential provider, if it exposes ``close()``."""
    close = getattr(credentials, "close", None)
    if close is not None:
        close()


def _bind_credentials_base_url(credentials: AccessTokenProvider | None, base_url: str) -> None:
    """If the credential provider supports ``bind_base_url``, pass it the
    client's resolved ``base_url`` so the token exchange and API calls hit
    the same deployment without the caller passing the URL twice.

    Providers without the hook (plain callables, custom impls) are left
    untouched and MUST resolve their own token-exchange ``base_url`` — the
    client does not second-guess them.
    """
    bind = getattr(credentials, "bind_base_url", None)
    if callable(bind):
        bind(base_url)


def _warn_explicit_shadow(*, api_key: str | None, auth_token: str | None, credentials: object) -> None:
    """Warn when an explicit ``api_key=`` / ``auth_token=`` argument shadows
    an explicit ``credentials=`` provider. Call *after* any copy-inheritance
    merging so the params reflect the resolved values."""
    if credentials is None:
        return
    if api_key is not None:
        warn_explicit_static_shadows_credentials("api_key")
    if auth_token is not None:
        warn_explicit_static_shadows_credentials("auth_token")


def _warn_env_shadow(*, api_key: str | None, auth_token: str | None) -> None:
    """Warn when an ``ANTHROPIC_API_KEY`` / ``ANTHROPIC_AUTH_TOKEN`` from the
    environment is set alongside signals that would normally drive profile /
    federation auto-discovery (``ANTHROPIC_PROFILE``, a ``configs/`` directory,
    or the workload-identity env trio). Per the credential-precedence spec,
    the static credential wins and auto-discovery is silently skipped."""
    if not _has_auto_discoverable_credentials():
        return
    if api_key is not None and os.environ.get("ANTHROPIC_API_KEY"):
        warn_env_static_shadows_auto_discovery("ANTHROPIC_API_KEY")
    if auth_token is not None and os.environ.get("ANTHROPIC_AUTH_TOKEN"):
        warn_env_static_shadows_auto_discovery("ANTHROPIC_AUTH_TOKEN")


# --- end credentials support ---

if TYPE_CHECKING:
    from .resources import beta, models, messages, completions
    from .resources.models import Models, AsyncModels
    from .resources.beta.beta import Beta, AsyncBeta
    from .resources.completions import Completions, AsyncCompletions
    from .resources.messages.messages import Messages, AsyncMessages

__all__ = [
    "Timeout",
    "Transport",
    "ProxiesTypes",
    "RequestOptions",
    "Anthropic",
    "AsyncAnthropic",
    "Client",
    "AsyncClient",
]


class Anthropic(SyncAPIClient):
    # client options
    api_key: str | None
    auth_token: str | None
    webhook_key: str | None
    credentials: AccessTokenProvider | None
    _token_cache: TokenCache | None
    _custom_auth: AccessTokenAuth | None

    # constants
    HUMAN_PROMPT = _constants.HUMAN_PROMPT
    AI_PROMPT = _constants.AI_PROMPT

    def __init__(
        self,
        *,
        api_key: str | None = None,
        auth_token: str | None = None,
        credentials: AccessTokenProvider | None = None,
        config: Mapping[str, Any] | None = None,
        profile: str | None = None,
        webhook_key: str | None = None,
        base_url: str | httpx.URL | None = None,
        timeout: float | Timeout | None | NotGiven = not_given,
        max_retries: int = DEFAULT_MAX_RETRIES,
        default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        # Configure a custom httpx client.
        # We provide a `DefaultHttpxClient` class that you can pass to retain the default values we use for `limits`, `timeout` & `follow_redirects`.
        # See the [httpx documentation](https://www.python-httpx.org/api/#client) for more details.
        http_client: httpx.Client | None = None,
        # Enable or disable schema validation for data returned by the API.
        # When enabled an error APIResponseValidationError is raised
        # if the API responds with invalid data for the expected schema.
        #
        # This parameter may be removed or changed in the future.
        # If you rely on this feature, please open a GitHub issue
        # outlining your use-case to help us decide if it should be
        # part of our public interface in the future.
        _strict_response_validation: bool = False,
        _token_cache: TokenCache | None | NotGiven = not_given,
    ) -> None:
        """Construct a new synchronous Anthropic client instance.
        
        Credentials are resolved in the following order (first match wins):

        1. Explicit constructor arguments — ``api_key=``, ``auth_token=``,
           ``credentials=``, ``config=``, or ``profile=``. When any of these
           is passed, environment variables are not consulted for credentials.
        2. ``ANTHROPIC_API_KEY`` / ``ANTHROPIC_AUTH_TOKEN`` environment
           variables.
        3. ``ANTHROPIC_PROFILE`` environment variable — loads the named
           profile from ``<config_dir>/configs/<profile>.json``.
        4. Workload identity federation environment variables —
           ``ANTHROPIC_IDENTITY_TOKEN[_FILE]`` +
           ``ANTHROPIC_FEDERATION_RULE_ID`` + ``ANTHROPIC_ORGANIZATION_ID``.
        5. The active profile on disk — the profile named by
           ``<config_dir>/active_config``, or ``default``.

        ``credentials=``, ``config=``, and ``profile=`` are mutually exclusive.

        If a static credential is supplied alongside a credentials provider
        (``credentials=`` / ``config=`` / ``profile=``), or if
        ``ANTHROPIC_API_KEY`` / ``ANTHROPIC_AUTH_TOKEN`` is set alongside a
        profile or federation configuration, the static credential takes
        precedence and a one-shot warning is logged on the ``anthropic``
        logger.
        """
        # --- credentials support (hand-written, upstream to Stainless) ---
        # Explicit ctor args are total. If the caller passed any explicit
        # credential argument, do NOT read credential env vars.
        has_explicit_credential = (
            api_key is not None
            or auth_token is not None
            or credentials is not None
            or config is not None
            or profile is not None
        )
        if not has_explicit_credential:
            api_key = os.environ.get("ANTHROPIC_API_KEY")
            auth_token = os.environ.get("ANTHROPIC_AUTH_TOKEN")
        self.api_key = api_key
        self.auth_token = auth_token
        # --- end credentials support ---

        if webhook_key is None:
            webhook_key = os.environ.get("ANTHROPIC_WEBHOOK_SIGNING_KEY")
        self.webhook_key = webhook_key

        if base_url is None:
            base_url = os.environ.get("ANTHROPIC_BASE_URL")
        # base_url precedence: kwarg > ANTHROPIC_BASE_URL > profile config
        # (filled in below from default_credentials) > hardcoded default.
        # Track whether the user supplied one so the profile only fills the
        # gap, never overrides.
        base_url_is_explicit = base_url is not None
        if base_url is None:
            base_url = f"https://api.anthropic.com"

        custom_headers_env = os.environ.get("ANTHROPIC_CUSTOM_HEADERS")
        if custom_headers_env is not None:
            parsed: dict[str, str] = {}
            for line in custom_headers_env.split("\n"):
                colon = line.find(":")
                if colon >= 0:
                    parsed[line[:colon].strip()] = line[colon + 1 :].strip()
            default_headers = {**parsed, **(default_headers if is_mapping_t(default_headers) else {})}

        # --- credentials support (hand-written, upstream to Stainless) ---
        credential_headers: dict[str, str] = {}
        if config is not None:
            if credentials is not None or profile is not None:
                raise TypeError("Pass at most one of `credentials=`, `config=`, or `profile=`.")
            in_memory = InMemoryConfig(dict(config))
            credentials = in_memory
            credential_headers = in_memory.extra_headers()
            if not base_url_is_explicit and in_memory.resolved_base_url:
                base_url = in_memory.resolved_base_url
        elif profile is not None:
            if credentials is not None:
                raise TypeError("Pass at most one of `credentials=`, `config=`, or `profile=`.")
            creds_file = CredentialsFile(profile=profile)
            credentials = creds_file
            credential_headers = creds_file.extra_headers()
            if not base_url_is_explicit and creds_file.resolved_base_url:
                base_url = creds_file.resolved_base_url
        if credentials is None and api_key is None and auth_token is None and _is_base_client(self):
            result = default_credentials(base_url=str(base_url) if base_url else "https://api.anthropic.com")
            if result is not None:
                credentials = result.provider
                credential_headers = result.extra_headers
                if not base_url_is_explicit and result.base_url:
                    base_url = result.base_url
        _bind_credentials_base_url(credentials, str(base_url))
        self.credentials = credentials
        _warn_explicit_shadow(api_key=api_key, auth_token=auth_token, credentials=credentials)
        _warn_env_shadow(api_key=api_key, auth_token=auth_token)
        if not isinstance(_token_cache, NotGiven):
            self._token_cache = _token_cache
        else:
            self._token_cache = TokenCache(credentials) if credentials is not None else None
        self._custom_auth = AccessTokenAuth(self._token_cache) if self._token_cache is not None else None
        if credential_headers:
            default_headers = {**credential_headers, **(default_headers or {})}
        # --- end credentials support ---

        super().__init__(
            version=__version__,
            base_url=base_url,
            max_retries=max_retries,
            timeout=timeout,
            http_client=http_client,
            custom_headers=default_headers,
            custom_query=default_query,
            _strict_response_validation=_strict_response_validation,
        )

        self._default_stream_cls = Stream

    @cached_property
    def completions(self) -> Completions:
        from .resources.completions import Completions

        return Completions(self)

    @cached_property
    def messages(self) -> Messages:
        from .resources.messages import Messages

        return Messages(self)

    @cached_property
    def models(self) -> Models:
        from .resources.models import Models

        return Models(self)

    @cached_property
    def beta(self) -> Beta:
        from .resources.beta import Beta

        return Beta(self)

    @cached_property
    def with_raw_response(self) -> AnthropicWithRawResponse:
        return AnthropicWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AnthropicWithStreamedResponse:
        return AnthropicWithStreamedResponse(self)

    @property
    @override
    def qs(self) -> Querystring:
        return Querystring(array_format="brackets")

    @property
    @override
    def auth_headers(self) -> dict[str, str]:
        return {**self._api_key_auth, **self._bearer_auth}

    @property
    def _api_key_auth(self) -> dict[str, str]:
        api_key = self.api_key
        if api_key is None:
            return {}
        return {"X-Api-Key": api_key}

    @property
    def _bearer_auth(self) -> dict[str, str]:
        # Symmetric with _api_key_auth: always emit if self.auth_token is set,
        # regardless of whether a TokenCache is also installed. When both a
        # static auth_token and a credentials provider are present, the static
        # credential wins per the documented precedence — AccessTokenAuth
        # short-circuits on a pre-set Authorization header and no token
        # exchange runs.
        auth_token = self.auth_token
        if auth_token is None:
            return {}
        return {"Authorization": f"Bearer {auth_token}"}

    @property
    @override
    def default_headers(self) -> dict[str, str | Omit]:
        return {
            **super().default_headers,
            "X-Stainless-Async": "false",
            "anthropic-version": "2023-06-01",
            **self._custom_headers,
        }

    @override
    def _validate_headers(self, headers: Headers, custom_headers: Headers) -> None:
        # --- credentials support (hand-written, upstream to Stainless) ---
        # The token cache *may* inject an Authorization header per-request via
        # custom_auth, so validation that checks only default_headers would
        # false-negative when credentials are the only auth source. Defer to
        # the static-header check below — if a static api_key or auth_token
        # is set it will already be on default_headers; otherwise custom_auth
        # will fill in Authorization at request time.
        if self._token_cache is not None and not headers.get("X-Api-Key") and not headers.get("Authorization"):
            return
        # --- end credentials support ---
        if headers.get("Authorization") or headers.get("X-Api-Key"):
            # valid
            return

        if headers.get("X-Api-Key") or isinstance(custom_headers.get("X-Api-Key"), Omit):
            return

        if headers.get("Authorization") or isinstance(custom_headers.get("Authorization"), Omit):
            return

        raise TypeError(
            '"Could not resolve authentication method. Expected one of api_key, auth_token, or credentials to be set. Or for one of the `X-Api-Key` or `Authorization` headers to be explicitly omitted"'
        )

    # --- credentials support (hand-written, upstream to Stainless) ---
    @property
    @override
    def custom_auth(self) -> httpx.Auth | None:
        return self._custom_auth

    @override
    def _should_retry(self, response: httpx.Response) -> bool:
        # On 401 with a token cache, invalidate and retry once so the request
        # is re-sent with a freshly minted Bearer token. The base-client retry
        # loop rebuilds the request from FinalRequestOptions on each attempt,
        # so body replay is handled for us. The single-shot guard relies on
        # ``x-stainless-retry-count`` being ``"0"`` on the first attempt
        # (see _base_client.py); if a caller Omit()s that header the guard
        # silently no-ops, which fails safe (no retry, surface the 401).
        if response.status_code == 401 and self._token_cache is not None:
            self._token_cache.invalidate()
            if response.request.headers.get("x-stainless-retry-count") == "0":
                return True
        return super()._should_retry(response)

    @override
    def close(self) -> None:
        super().close()
        _close_credentials(self.credentials)

    # --- end credentials support ---

    def copy(
        self,
        *,
        api_key: str | None = None,
        auth_token: str | None = None,
        credentials: AccessTokenProvider | None | NotGiven = not_given,
        config: Mapping[str, Any] | None = None,
        profile: str | None = None,
        webhook_key: str | None = None,
        base_url: str | httpx.URL | None = None,
        timeout: float | Timeout | None | NotGiven = not_given,
        http_client: httpx.Client | None = None,
        max_retries: int | NotGiven = not_given,
        default_headers: Mapping[str, str] | None = None,
        set_default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        set_default_query: Mapping[str, object] | None = None,
        _extra_kwargs: Mapping[str, Any] = {},
    ) -> Self:
        """
        Create a new client instance re-using the same options given to the current client with optional overriding.
        """
        if default_headers is not None and set_default_headers is not None:
            raise ValueError("The `default_headers` and `set_default_headers` arguments are mutually exclusive")

        if default_query is not None and set_default_query is not None:
            raise ValueError("The `default_query` and `set_default_query` arguments are mutually exclusive")

        headers = self._custom_headers
        if default_headers is not None:
            headers = {**headers, **default_headers}
        elif set_default_headers is not None:
            headers = set_default_headers

        params = self._custom_query
        if default_query is not None:
            params = {**params, **default_query}
        elif set_default_query is not None:
            params = set_default_query

        http_client = http_client or self._client
        # --- credentials support (hand-written, upstream to Stainless) ---
        if config is not None:
            if not isinstance(credentials, NotGiven) or profile is not None:
                raise TypeError("Pass at most one of `credentials=`, `config=`, or `profile=`.")
            _extra_kwargs = {"config": config, **_extra_kwargs}
        elif profile is not None:
            if not isinstance(credentials, NotGiven):
                raise TypeError("Pass at most one of `credentials=`, `config=`, or `profile=`.")
            _extra_kwargs = {"profile": profile, **_extra_kwargs}
        else:
            resolved_credentials = self.credentials if isinstance(credentials, NotGiven) else credentials
            if resolved_credentials is not None and _is_base_client(self):
                _extra_kwargs = {"credentials": resolved_credentials, **_extra_kwargs}
                # Reuse the parent's TokenCache when the credentials provider is
                # unchanged so with_options() copies don't trigger an independent
                # token exchange. A new credentials= gets a fresh cache.
                if isinstance(credentials, NotGiven):
                    _extra_kwargs = {"_token_cache": self._token_cache, **_extra_kwargs}
        # --- end credentials support ---
        return self.__class__(
            api_key=api_key or self.api_key,
            auth_token=auth_token or self.auth_token,
            webhook_key=webhook_key or self.webhook_key,
            base_url=base_url or self.base_url,
            timeout=self.timeout if isinstance(timeout, NotGiven) else timeout,
            http_client=http_client,
            max_retries=max_retries if is_given(max_retries) else self.max_retries,
            default_headers=headers,
            default_query=params,
            **_extra_kwargs,
        )

    # Alias for `copy` for nicer inline usage, e.g.
    # client.with_options(timeout=10).foo.create(...)
    with_options = copy

    @override
    def _make_status_error(
        self,
        err_msg: str,
        *,
        body: object,
        response: httpx.Response,
    ) -> APIStatusError:
        if response.status_code == 400:
            return _exceptions.BadRequestError(err_msg, response=response, body=body)

        if response.status_code == 401:
            return _exceptions.AuthenticationError(err_msg, response=response, body=body)

        if response.status_code == 403:
            return _exceptions.PermissionDeniedError(err_msg, response=response, body=body)

        if response.status_code == 404:
            return _exceptions.NotFoundError(err_msg, response=response, body=body)

        if response.status_code == 409:
            return _exceptions.ConflictError(err_msg, response=response, body=body)

        if response.status_code == 413:
            return _exceptions.RequestTooLargeError(err_msg, response=response, body=body)

        if response.status_code == 422:
            return _exceptions.UnprocessableEntityError(err_msg, response=response, body=body)

        if response.status_code == 429:
            return _exceptions.RateLimitError(err_msg, response=response, body=body)

        if response.status_code == 529:
            return _exceptions.OverloadedError(err_msg, response=response, body=body)

        if response.status_code >= 500:
            return _exceptions.InternalServerError(err_msg, response=response, body=body)
        return APIStatusError(err_msg, response=response, body=body)


class AsyncAnthropic(AsyncAPIClient):
    # client options
    api_key: str | None
    auth_token: str | None
    webhook_key: str | None
    credentials: AccessTokenProvider | None
    _token_cache: TokenCache | None
    _custom_auth: AccessTokenAuth | None

    # constants
    HUMAN_PROMPT = _constants.HUMAN_PROMPT
    AI_PROMPT = _constants.AI_PROMPT

    def __init__(
        self,
        *,
        api_key: str | None = None,
        auth_token: str | None = None,
        credentials: AccessTokenProvider | None = None,
        config: Mapping[str, Any] | None = None,
        profile: str | None = None,
        webhook_key: str | None = None,
        base_url: str | httpx.URL | None = None,
        timeout: float | Timeout | None | NotGiven = not_given,
        max_retries: int = DEFAULT_MAX_RETRIES,
        default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        # Configure a custom httpx client.
        # We provide a `DefaultAsyncHttpxClient` class that you can pass to retain the default values we use for `limits`, `timeout` & `follow_redirects`.
        # See the [httpx documentation](https://www.python-httpx.org/api/#asyncclient) for more details.
        http_client: httpx.AsyncClient | None = None,
        # Enable or disable schema validation for data returned by the API.
        # When enabled an error APIResponseValidationError is raised
        # if the API responds with invalid data for the expected schema.
        #
        # This parameter may be removed or changed in the future.
        # If you rely on this feature, please open a GitHub issue
        # outlining your use-case to help us decide if it should be
        # part of our public interface in the future.
        _strict_response_validation: bool = False,
        _token_cache: TokenCache | None | NotGiven = not_given,
    ) -> None:
        """Construct a new async AsyncAnthropic client instance.

        Credentials are resolved in the following order (first match wins):

        1. Explicit constructor arguments — ``api_key=``, ``auth_token=``,
           ``credentials=``, ``config=``, or ``profile=``. When any of these
           is passed, environment variables are not consulted for credentials.
        2. ``ANTHROPIC_API_KEY`` / ``ANTHROPIC_AUTH_TOKEN`` environment
           variables.
        3. ``ANTHROPIC_PROFILE`` environment variable — loads the named
           profile from ``<config_dir>/configs/<profile>.json``.
        4. Workload identity federation environment variables —
           ``ANTHROPIC_IDENTITY_TOKEN[_FILE]`` +
           ``ANTHROPIC_FEDERATION_RULE_ID`` + ``ANTHROPIC_ORGANIZATION_ID``.
        5. The active profile on disk — the profile named by
           ``<config_dir>/active_config``, or ``default``.

        ``credentials=``, ``config=``, and ``profile=`` are mutually exclusive.

        If a static credential is supplied alongside a credentials provider
        (``credentials=`` / ``config=`` / ``profile=``), or if
        ``ANTHROPIC_API_KEY`` / ``ANTHROPIC_AUTH_TOKEN`` is set alongside a
        profile or federation configuration, the static credential takes
        precedence and a one-shot warning is logged on the ``anthropic``
        logger.
        """
        # --- credentials support (hand-written, upstream to Stainless) ---
        # Explicit ctor args are total. If the caller passed any explicit
        # credential argument, do NOT read credential env vars.
        has_explicit_credential = (
            api_key is not None
            or auth_token is not None
            or credentials is not None
            or config is not None
            or profile is not None
        )
        if not has_explicit_credential:
            api_key = os.environ.get("ANTHROPIC_API_KEY")
            auth_token = os.environ.get("ANTHROPIC_AUTH_TOKEN")
        self.api_key = api_key
        self.auth_token = auth_token
        # --- end credentials support ---

        if webhook_key is None:
            webhook_key = os.environ.get("ANTHROPIC_WEBHOOK_SIGNING_KEY")
        self.webhook_key = webhook_key

        if base_url is None:
            base_url = os.environ.get("ANTHROPIC_BASE_URL")
        # base_url precedence: kwarg > ANTHROPIC_BASE_URL > profile config
        # (filled in below from default_credentials) > hardcoded default.
        # Track whether the user supplied one so the profile only fills the
        # gap, never overrides.
        base_url_is_explicit = base_url is not None
        if base_url is None:
            base_url = f"https://api.anthropic.com"

        custom_headers_env = os.environ.get("ANTHROPIC_CUSTOM_HEADERS")
        if custom_headers_env is not None:
            parsed: dict[str, str] = {}
            for line in custom_headers_env.split("\n"):
                colon = line.find(":")
                if colon >= 0:
                    parsed[line[:colon].strip()] = line[colon + 1 :].strip()
            default_headers = {**parsed, **(default_headers if is_mapping_t(default_headers) else {})}

        # --- credentials support (hand-written, upstream to Stainless) ---
        credential_headers: dict[str, str] = {}
        if config is not None:
            if credentials is not None or profile is not None:
                raise TypeError("Pass at most one of `credentials=`, `config=`, or `profile=`.")
            in_memory = InMemoryConfig(dict(config))
            credentials = in_memory
            credential_headers = in_memory.extra_headers()
            if not base_url_is_explicit and in_memory.resolved_base_url:
                base_url = in_memory.resolved_base_url
        elif profile is not None:
            if credentials is not None:
                raise TypeError("Pass at most one of `credentials=`, `config=`, or `profile=`.")
            creds_file = CredentialsFile(profile=profile)
            credentials = creds_file
            credential_headers = creds_file.extra_headers()
            if not base_url_is_explicit and creds_file.resolved_base_url:
                base_url = creds_file.resolved_base_url
        if credentials is None and api_key is None and auth_token is None and _is_base_client(self):
            result = default_credentials(base_url=str(base_url) if base_url else "https://api.anthropic.com")
            if result is not None:
                credentials = result.provider
                credential_headers = result.extra_headers
                if not base_url_is_explicit and result.base_url:
                    base_url = result.base_url
        _bind_credentials_base_url(credentials, str(base_url))
        self.credentials = credentials
        _warn_explicit_shadow(api_key=api_key, auth_token=auth_token, credentials=credentials)
        _warn_env_shadow(api_key=api_key, auth_token=auth_token)
        if not isinstance(_token_cache, NotGiven):
            self._token_cache = _token_cache
        else:
            self._token_cache = TokenCache(credentials) if credentials is not None else None
        self._custom_auth = AccessTokenAuth(self._token_cache) if self._token_cache is not None else None
        if credential_headers:
            default_headers = {**credential_headers, **(default_headers or {})}
        # --- end credentials support ---

        super().__init__(
            version=__version__,
            base_url=base_url,
            max_retries=max_retries,
            timeout=timeout,
            http_client=http_client,
            custom_headers=default_headers,
            custom_query=default_query,
            _strict_response_validation=_strict_response_validation,
        )

        self._default_stream_cls = AsyncStream

    @cached_property
    def completions(self) -> AsyncCompletions:
        from .resources.completions import AsyncCompletions

        return AsyncCompletions(self)

    @cached_property
    def messages(self) -> AsyncMessages:
        from .resources.messages import AsyncMessages

        return AsyncMessages(self)

    @cached_property
    def models(self) -> AsyncModels:
        from .resources.models import AsyncModels

        return AsyncModels(self)

    @cached_property
    def beta(self) -> AsyncBeta:
        from .resources.beta import AsyncBeta

        return AsyncBeta(self)

    @cached_property
    def with_raw_response(self) -> AsyncAnthropicWithRawResponse:
        return AsyncAnthropicWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncAnthropicWithStreamedResponse:
        return AsyncAnthropicWithStreamedResponse(self)

    @property
    @override
    def qs(self) -> Querystring:
        return Querystring(array_format="brackets")

    @property
    @override
    def auth_headers(self) -> dict[str, str]:
        return {**self._api_key_auth, **self._bearer_auth}

    @property
    def _api_key_auth(self) -> dict[str, str]:
        api_key = self.api_key
        if api_key is None:
            return {}
        return {"X-Api-Key": api_key}

    @property
    def _bearer_auth(self) -> dict[str, str]:
        # Symmetric with _api_key_auth: always emit if self.auth_token is set,
        # regardless of whether a TokenCache is also installed. When both a
        # static auth_token and a credentials provider are present, the static
        # credential wins per the documented precedence — AccessTokenAuth
        # short-circuits on a pre-set Authorization header and no token
        # exchange runs.
        auth_token = self.auth_token
        if auth_token is None:
            return {}
        return {"Authorization": f"Bearer {auth_token}"}

    @property
    @override
    def default_headers(self) -> dict[str, str | Omit]:
        return {
            **super().default_headers,
            "X-Stainless-Async": f"async:{get_async_library()}",
            "anthropic-version": "2023-06-01",
            **self._custom_headers,
        }

    @override
    def _validate_headers(self, headers: Headers, custom_headers: Headers) -> None:
        # --- credentials support (hand-written, upstream to Stainless) ---
        if self._token_cache is not None and not headers.get("X-Api-Key") and not headers.get("Authorization"):
            return
        # --- end credentials support ---
        if headers.get("Authorization") or headers.get("X-Api-Key"):
            # valid
            return

        if headers.get("X-Api-Key") or isinstance(custom_headers.get("X-Api-Key"), Omit):
            return

        if headers.get("Authorization") or isinstance(custom_headers.get("Authorization"), Omit):
            return

        raise TypeError(
            '"Could not resolve authentication method. Expected one of api_key, auth_token, or credentials to be set. Or for one of the `X-Api-Key` or `Authorization` headers to be explicitly omitted"'
        )

    # --- credentials support (hand-written, upstream to Stainless) ---
    @property
    @override
    def custom_auth(self) -> httpx.Auth | None:
        return self._custom_auth

    @override
    def _should_retry(self, response: httpx.Response) -> bool:
        # On 401 with a token cache, invalidate and retry once so the request
        # is re-sent with a freshly minted Bearer token. The base-client retry
        # loop rebuilds the request from FinalRequestOptions on each attempt,
        # so body replay is handled for us. The single-shot guard relies on
        # ``x-stainless-retry-count`` being ``"0"`` on the first attempt
        # (see _base_client.py); if a caller Omit()s that header the guard
        # silently no-ops, which fails safe (no retry, surface the 401).
        if response.status_code == 401 and self._token_cache is not None:
            self._token_cache.invalidate()
            if response.request.headers.get("x-stainless-retry-count") == "0":
                return True
        return super()._should_retry(response)

    @override
    async def close(self) -> None:
        await super().close()
        # Credential providers expose a sync close() even from the async client —
        # they own a sync httpx.Client for the token-exchange POST.
        _close_credentials(self.credentials)

    # --- end credentials support ---

    def copy(
        self,
        *,
        api_key: str | None = None,
        auth_token: str | None = None,
        credentials: AccessTokenProvider | None | NotGiven = not_given,
        config: Mapping[str, Any] | None = None,
        profile: str | None = None,
        webhook_key: str | None = None,
        base_url: str | httpx.URL | None = None,
        timeout: float | Timeout | None | NotGiven = not_given,
        http_client: httpx.AsyncClient | None = None,
        max_retries: int | NotGiven = not_given,
        default_headers: Mapping[str, str] | None = None,
        set_default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        set_default_query: Mapping[str, object] | None = None,
        _extra_kwargs: Mapping[str, Any] = {},
    ) -> Self:
        """
        Create a new client instance re-using the same options given to the current client with optional overriding.
        """
        if default_headers is not None and set_default_headers is not None:
            raise ValueError("The `default_headers` and `set_default_headers` arguments are mutually exclusive")

        if default_query is not None and set_default_query is not None:
            raise ValueError("The `default_query` and `set_default_query` arguments are mutually exclusive")

        headers = self._custom_headers
        if default_headers is not None:
            headers = {**headers, **default_headers}
        elif set_default_headers is not None:
            headers = set_default_headers

        params = self._custom_query
        if default_query is not None:
            params = {**params, **default_query}
        elif set_default_query is not None:
            params = set_default_query

        http_client = http_client or self._client
        # --- credentials support (hand-written, upstream to Stainless) ---
        if config is not None:
            if not isinstance(credentials, NotGiven) or profile is not None:
                raise TypeError("Pass at most one of `credentials=`, `config=`, or `profile=`.")
            _extra_kwargs = {"config": config, **_extra_kwargs}
        elif profile is not None:
            if not isinstance(credentials, NotGiven):
                raise TypeError("Pass at most one of `credentials=`, `config=`, or `profile=`.")
            _extra_kwargs = {"profile": profile, **_extra_kwargs}
        else:
            resolved_credentials = self.credentials if isinstance(credentials, NotGiven) else credentials
            if resolved_credentials is not None and _is_base_client(self):
                _extra_kwargs = {"credentials": resolved_credentials, **_extra_kwargs}
                # Reuse the parent's TokenCache when the credentials provider is
                # unchanged so with_options() copies don't trigger an independent
                # token exchange. A new credentials= gets a fresh cache.
                if isinstance(credentials, NotGiven):
                    _extra_kwargs = {"_token_cache": self._token_cache, **_extra_kwargs}
        # --- end credentials support ---
        return self.__class__(
            api_key=api_key or self.api_key,
            auth_token=auth_token or self.auth_token,
            webhook_key=webhook_key or self.webhook_key,
            base_url=base_url or self.base_url,
            timeout=self.timeout if isinstance(timeout, NotGiven) else timeout,
            http_client=http_client,
            max_retries=max_retries if is_given(max_retries) else self.max_retries,
            default_headers=headers,
            default_query=params,
            **_extra_kwargs,
        )

    # Alias for `copy` for nicer inline usage, e.g.
    # client.with_options(timeout=10).foo.create(...)
    with_options = copy

    @override
    def _make_status_error(
        self,
        err_msg: str,
        *,
        body: object,
        response: httpx.Response,
    ) -> APIStatusError:
        if response.status_code == 400:
            return _exceptions.BadRequestError(err_msg, response=response, body=body)

        if response.status_code == 401:
            return _exceptions.AuthenticationError(err_msg, response=response, body=body)

        if response.status_code == 403:
            return _exceptions.PermissionDeniedError(err_msg, response=response, body=body)

        if response.status_code == 404:
            return _exceptions.NotFoundError(err_msg, response=response, body=body)

        if response.status_code == 409:
            return _exceptions.ConflictError(err_msg, response=response, body=body)

        if response.status_code == 413:
            return _exceptions.RequestTooLargeError(err_msg, response=response, body=body)

        if response.status_code == 422:
            return _exceptions.UnprocessableEntityError(err_msg, response=response, body=body)

        if response.status_code == 429:
            return _exceptions.RateLimitError(err_msg, response=response, body=body)

        if response.status_code == 529:
            return _exceptions.OverloadedError(err_msg, response=response, body=body)

        if response.status_code >= 500:
            return _exceptions.InternalServerError(err_msg, response=response, body=body)
        return APIStatusError(err_msg, response=response, body=body)


class AnthropicWithRawResponse:
    _client: Anthropic

    def __init__(self, client: Anthropic) -> None:
        self._client = client

    @cached_property
    def completions(self) -> completions.CompletionsWithRawResponse:
        from .resources.completions import CompletionsWithRawResponse

        return CompletionsWithRawResponse(self._client.completions)

    @cached_property
    def messages(self) -> messages.MessagesWithRawResponse:
        from .resources.messages import MessagesWithRawResponse

        return MessagesWithRawResponse(self._client.messages)

    @cached_property
    def models(self) -> models.ModelsWithRawResponse:
        from .resources.models import ModelsWithRawResponse

        return ModelsWithRawResponse(self._client.models)

    @cached_property
    def beta(self) -> beta.BetaWithRawResponse:
        from .resources.beta import BetaWithRawResponse

        return BetaWithRawResponse(self._client.beta)


class AsyncAnthropicWithRawResponse:
    _client: AsyncAnthropic

    def __init__(self, client: AsyncAnthropic) -> None:
        self._client = client

    @cached_property
    def completions(self) -> completions.AsyncCompletionsWithRawResponse:
        from .resources.completions import AsyncCompletionsWithRawResponse

        return AsyncCompletionsWithRawResponse(self._client.completions)

    @cached_property
    def messages(self) -> messages.AsyncMessagesWithRawResponse:
        from .resources.messages import AsyncMessagesWithRawResponse

        return AsyncMessagesWithRawResponse(self._client.messages)

    @cached_property
    def models(self) -> models.AsyncModelsWithRawResponse:
        from .resources.models import AsyncModelsWithRawResponse

        return AsyncModelsWithRawResponse(self._client.models)

    @cached_property
    def beta(self) -> beta.AsyncBetaWithRawResponse:
        from .resources.beta import AsyncBetaWithRawResponse

        return AsyncBetaWithRawResponse(self._client.beta)


class AnthropicWithStreamedResponse:
    _client: Anthropic

    def __init__(self, client: Anthropic) -> None:
        self._client = client

    @cached_property
    def completions(self) -> completions.CompletionsWithStreamingResponse:
        from .resources.completions import CompletionsWithStreamingResponse

        return CompletionsWithStreamingResponse(self._client.completions)

    @cached_property
    def messages(self) -> messages.MessagesWithStreamingResponse:
        from .resources.messages import MessagesWithStreamingResponse

        return MessagesWithStreamingResponse(self._client.messages)

    @cached_property
    def models(self) -> models.ModelsWithStreamingResponse:
        from .resources.models import ModelsWithStreamingResponse

        return ModelsWithStreamingResponse(self._client.models)

    @cached_property
    def beta(self) -> beta.BetaWithStreamingResponse:
        from .resources.beta import BetaWithStreamingResponse

        return BetaWithStreamingResponse(self._client.beta)


class AsyncAnthropicWithStreamedResponse:
    _client: AsyncAnthropic

    def __init__(self, client: AsyncAnthropic) -> None:
        self._client = client

    @cached_property
    def completions(self) -> completions.AsyncCompletionsWithStreamingResponse:
        from .resources.completions import AsyncCompletionsWithStreamingResponse

        return AsyncCompletionsWithStreamingResponse(self._client.completions)

    @cached_property
    def messages(self) -> messages.AsyncMessagesWithStreamingResponse:
        from .resources.messages import AsyncMessagesWithStreamingResponse

        return AsyncMessagesWithStreamingResponse(self._client.messages)

    @cached_property
    def models(self) -> models.AsyncModelsWithStreamingResponse:
        from .resources.models import AsyncModelsWithStreamingResponse

        return AsyncModelsWithStreamingResponse(self._client.models)

    @cached_property
    def beta(self) -> beta.AsyncBetaWithStreamingResponse:
        from .resources.beta import AsyncBetaWithStreamingResponse

        return AsyncBetaWithStreamingResponse(self._client.beta)


Client = Anthropic

AsyncClient = AsyncAnthropic
