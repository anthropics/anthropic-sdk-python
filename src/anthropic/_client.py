from __future__ import annotations

import os
from typing import TYPE_CHECKING, Any, Mapping, TypeVar, Sequence
from typing_extensions import Self, override

import httpx2

from . import _exceptions
from ._qs import Querystring
from ._types import (
    Omit,
    Timeout,
    NotGiven,
    RequestOptions,
    OpenTelemetryClientOption,
    not_given,
)
from ._utils import (
    is_given,
    is_mapping_t,
    get_async_library,
)
from ._compat import model_copy, cached_property
from ._models import FinalRequestOptions
from ._version import __version__
from ._constants import ANTHROPIC_API_VERSION
from ._streaming import Stream as Stream, AsyncStream as AsyncStream
from ._exceptions import APIStatusError
from ._middleware import MiddlewareInput
from ._base_client import (
    DEFAULT_MAX_RETRIES,
    SyncAPIClient,
    AsyncAPIClient,
    merge_headers,
)
from .lib.credentials import (
    TokenCache,
    InMemoryConfig,
    AccessTokenAuth,
    CredentialsFile,
    AccessTokenProvider,
    BaseURLBoundProvider,
    AsyncAccessTokenProvider,
    default_credentials,
)
from .lib.credentials._auth import (
    warn_env_static_shadows_auto_discovery,
    warn_env_api_key_shadows_env_auth_token,
)
from .lib.credentials._close import has_async_close, close_credentials, async_close_credentials
from .lib.credentials._types import is_async_token_provider
from .lib.credentials._constants import _has_auto_discoverable_credentials


def _is_base_client(client: object) -> bool:
    """True only for the base `Anthropic` / `AsyncAnthropic` classes, not subclasses.

    Subclasses (`AnthropicAWS`, `AnthropicFoundry`) have their own auth paths
    and must not run the credential chain or forward `credentials` through their
    `__init__` (which doesn't accept the kwarg).
    """
    return type(client) in (Anthropic, AsyncAnthropic)


_ProviderT = TypeVar(
    "_ProviderT", "AccessTokenProvider | None", "AccessTokenProvider | AsyncAccessTokenProvider | None"
)


def _bind_credentials_base_url(credentials: _ProviderT, base_url: str) -> _ProviderT:
    """Return the provider this client should exchange tokens through.

    See `BaseURLBoundProvider`; any other provider (plain callables,
    custom impls) is returned untouched and resolves its own exchange URL.
    """
    if isinstance(credentials, BaseURLBoundProvider):
        return credentials.for_base_url(base_url)
    return credentials


def _keeps_base_url(current: httpx2.URL, requested: str | httpx2.URL | None) -> bool:
    """Whether a `copy()` stays on the parent's deployment.

    Tokens are only valid for the deployment that minted them, so the parent's
    `TokenCache` is only shared in that case.
    """
    return requested is None or str(httpx2.URL(requested)).rstrip("/") == str(current).rstrip("/")


def has_explicit_credential(**arguments: object) -> bool:
    """Whether one of a client's credential arguments was passed. Raises `ValueError` for more than one."""
    names = [f"`{name}=`" for name in arguments]
    passed = [f"`{name}=`" for name, value in arguments.items() if value is not None]
    if len(passed) > 1:
        raise ValueError(f"Pass at most one of {', '.join(names[:-1])}, or {names[-1]}. Received {', '.join(passed)}.")
    return bool(passed)


def static_credential_from_env(*, warn: bool) -> tuple[str | None, str | None]:
    """The `(api_key, auth_token)` that the environment supplies. At most one of the two is set.

    With `warn`, logs what that credential shadows: `ANTHROPIC_AUTH_TOKEN`, or the profile or
    federation configuration that auto-discovery would have used. A subclass has its own auth
    and never runs auto-discovery, so it passes `False`.
    """
    api_key = os.environ.get("ANTHROPIC_API_KEY") or None
    auth_token = os.environ.get("ANTHROPIC_AUTH_TOKEN") or None

    if warn and api_key is not None and auth_token is not None:
        warn_env_api_key_shadows_env_auth_token()
    if warn and (api_key is not None or auth_token is not None) and _has_auto_discoverable_credentials():
        warn_env_static_shadows_auto_discovery("ANTHROPIC_API_KEY" if api_key is not None else "ANTHROPIC_AUTH_TOKEN")

    return (api_key, None) if api_key is not None else (None, auth_token)


if TYPE_CHECKING:
    from .resources import beta, files, models, skills, messages, organization, user_profiles
    from .resources.files import Files, AsyncFiles
    from .resources.models import Models, AsyncModels
    from .resources.beta.beta import Beta, AsyncBeta
    from .resources.skills.skills import Skills, AsyncSkills
    from .resources.messages.messages import Messages, AsyncMessages
    from .resources.organization.organization import Organization, AsyncOrganization
    from .resources.user_profiles.user_profiles import UserProfiles, AsyncUserProfiles

__all__ = ["Timeout", "RequestOptions", "Anthropic", "AsyncAnthropic", "Client", "AsyncClient"]


_CLIENT_LEVEL_HEADER_PARAMS = frozenset(("anthropic-workspace-id", "anthropic-user-profile-id"))


def _keep_client_header_params(options: FinalRequestOptions) -> FinalRequestOptions:
    """Per-request header params arrive as `Omit` when unset, which would strip a value the
    client itself sends (e.g. `AnthropicAWS(workspace_id=...)`, a credentials profile's
    `workspace_id`, or `default_headers`). Drop those so the client-level header survives."""
    headers = options.headers
    if not is_given(headers) or not any(
        name.lower() in _CLIENT_LEVEL_HEADER_PARAMS and isinstance(value, Omit) for name, value in headers.items()
    ):
        return options

    options = model_copy(options)
    options.headers = {
        name: value
        for name, value in headers.items()
        if not (name.lower() in _CLIENT_LEVEL_HEADER_PARAMS and isinstance(value, Omit))
    }
    return options


class Anthropic(SyncAPIClient):
    _supports_message_threads = True

    # client options
    api_key: str | None
    auth_token: str | None
    webhook_key: str | None
    credentials: AccessTokenProvider | None
    _token_cache: TokenCache | None
    _custom_auth: AccessTokenAuth | None
    _credential_headers: Mapping[str, str]
    _unchosen_base_url: httpx2.URL | None

    def __init__(
        self,
        *,
        api_key: str | None = None,
        auth_token: str | None = None,
        credentials: AccessTokenProvider | None = None,
        config: Mapping[str, Any] | None = None,
        profile: str | None = None,
        webhook_key: str | None = None,
        base_url: str | httpx2.URL | None = None,
        timeout: float | Timeout | None | NotGiven = not_given,
        max_retries: int = DEFAULT_MAX_RETRIES,
        default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        # OpenTelemetry tracing of this client's API calls. `False` disables the spans, and
        # `traces.content_mode` set to `"content"` adds the content of requests and responses to them.
        open_telemetry: OpenTelemetryClientOption = None,
        # Configure a custom httpx2 client.
        # We provide a `DefaultHttpxClient` class that you can pass to retain the default values we use for `limits`, `timeout` & `follow_redirects`.
        # See the [httpx2 documentation](https://httpx2.pydantic.dev/api/#client) for more details.
        http_client: httpx2.Client | None = None,
        middleware: Sequence[MiddlewareInput] | None = None,
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

        1. An explicit constructor argument — `api_key=`, `auth_token=`,
           `credentials=`, `config=`, or `profile=`. When one of these
           is passed, environment variables are not consulted for credentials.
        2. `ANTHROPIC_API_KEY`, then `ANTHROPIC_AUTH_TOKEN` environment
           variables.
        3. `ANTHROPIC_PROFILE` environment variable — loads the named
           profile from `<config_dir>/configs/<profile>.json`.
        4. Workload identity federation environment variables —
           `ANTHROPIC_IDENTITY_TOKEN[_FILE]` +
           `ANTHROPIC_FEDERATION_RULE_ID` + `ANTHROPIC_ORGANIZATION_ID`.
        5. The active profile on disk — the profile named by
           `<config_dir>/active_config`, or `default`.

        `ANTHROPIC_CONFIG_DIR` sets `<config_dir>`. It does not select a profile.

        `api_key=`, `auth_token=`, `credentials=`, `config=`, and `profile=`
        are mutually exclusive. Passing more than one raises `ValueError`.

        If `ANTHROPIC_API_KEY` / `ANTHROPIC_AUTH_TOKEN` is set alongside a
        profile or federation configuration, the static credential takes
        precedence and a one-shot warning is logged on the `anthropic`
        logger.

        If both `ANTHROPIC_API_KEY` and `ANTHROPIC_AUTH_TOKEN` are set, the
        API key is used and a one-shot warning is logged on the same logger.
        """
        # Explicit ctor args are total. If the caller passed any explicit
        # credential argument, do NOT read credential env vars.
        if not has_explicit_credential(
            api_key=api_key, auth_token=auth_token, credentials=credentials, config=config, profile=profile
        ):
            api_key, auth_token = static_credential_from_env(warn=_is_base_client(self))
        self.api_key = api_key
        self.auth_token = auth_token

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

        credential_headers: dict[str, str] = {}
        credential_base_url: str | None = None
        if config is not None:
            in_memory = InMemoryConfig(dict(config))
            credentials = in_memory
            credential_headers = in_memory.extra_headers()
            credential_base_url = in_memory.resolved_base_url
        elif profile is not None:
            creds_file = CredentialsFile(profile=profile)
            credentials = creds_file
            credential_headers = creds_file.extra_headers()
            credential_base_url = creds_file.resolved_base_url
        if credentials is None and api_key is None and auth_token is None and _is_base_client(self):
            result = default_credentials(base_url=str(base_url) if base_url else "https://api.anthropic.com")
            if result is not None:
                credentials = result.provider
                credential_headers = result.extra_headers
                credential_base_url = result.base_url

        self._credential_headers = credential_headers
        if not base_url_is_explicit and credential_base_url:
            base_url = credential_base_url
        self._unchosen_base_url = None if base_url_is_explicit else self._enforce_trailing_slash(httpx2.URL(base_url))

        if is_async_token_provider(credentials):
            raise TypeError("`Anthropic` cannot await an async `credentials` provider; use `AsyncAnthropic` instead.")
        if has_async_close(credentials):
            raise TypeError(
                "`Anthropic` cannot await this `credentials` provider's `async def close()`; use `AsyncAnthropic` instead."
            )

        credentials = _bind_credentials_base_url(credentials, str(base_url))
        self.credentials = credentials
        if not isinstance(_token_cache, NotGiven):
            self._token_cache = _token_cache
        else:
            self._token_cache = TokenCache(credentials) if credentials is not None else None
        self._custom_auth = AccessTokenAuth(self._token_cache) if self._token_cache is not None else None

        super().__init__(
            version=__version__,
            base_url=base_url,
            max_retries=max_retries,
            timeout=timeout,
            open_telemetry=open_telemetry,
            http_client=http_client,
            custom_headers=default_headers,
            custom_query=default_query,
            middleware=middleware,
            _strict_response_validation=_strict_response_validation,
        )

        self._default_stream_cls = Stream

    @cached_property
    def messages(self) -> Messages:
        from .resources.messages import Messages

        return Messages(self)

    @cached_property
    def models(self) -> Models:
        from .resources.models import Models

        return Models(self)

    @cached_property
    def files(self) -> Files:
        from .resources.files import Files

        return Files(self)

    @cached_property
    def skills(self) -> Skills:
        from .resources.skills import Skills

        return Skills(self)

    @cached_property
    def user_profiles(self) -> UserProfiles:
        from .resources.user_profiles import UserProfiles

        return UserProfiles(self)

    @cached_property
    def organization(self) -> Organization:
        from .resources.organization import Organization

        return Organization(self)

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
        return {**self._bearer_auth, **self._api_key_auth}

    @property
    def _api_key_auth(self) -> dict[str, str]:
        api_key = self.api_key
        if api_key is None:
            return {}
        return {"Authorization": f"Bearer {api_key}"}

    @property
    def _bearer_auth(self) -> dict[str, str]:
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
            "anthropic-version": ANTHROPIC_API_VERSION,
            **self._credential_headers,
            **self._custom_headers,
        }

    @override
    def _prepare_options(self, options: FinalRequestOptions) -> FinalRequestOptions:
        return _keep_client_header_params(super()._prepare_options(options))

    @override
    def _validate_headers(self, headers: httpx2.Headers, omitted: frozenset[str]) -> None:
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

        if headers.get("Authorization") or "authorization" in omitted:
            return

        raise TypeError(
            '"Could not resolve authentication method. Expected one of api_key, auth_token, or credentials to be set. Or for the `Authorization` header to be explicitly omitted"'
        )

    # --- credentials support (hand-written, upstream to Stainless) ---
    @property
    @override
    def custom_auth(self) -> httpx2.Auth | None:
        return self._custom_auth

    @override
    def _should_retry(self, response: httpx2.Response) -> bool:
        # On 401 with a token cache, invalidate and retry once so the request
        # is re-sent with a freshly minted Bearer token. The base-client retry
        # loop rebuilds the request from FinalRequestOptions on each attempt,
        # so body replay is handled for us. The single-shot guard relies on
        # `x-stainless-retry-count` being `"0"` on the first attempt
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
        close_credentials(self.credentials)

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
        base_url: str | httpx2.URL | None = None,
        timeout: float | Timeout | None | NotGiven = not_given,
        http_client: httpx2.Client | None = None,
        max_retries: int | NotGiven = not_given,
        open_telemetry: OpenTelemetryClientOption = None,
        default_headers: Mapping[str, str] | None = None,
        set_default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        set_default_query: Mapping[str, object] | None = None,
        middleware: Sequence[MiddlewareInput] | None | NotGiven = not_given,
        _extra_kwargs: Mapping[str, Any] = {},
    ) -> Self:
        """
        Create a new client instance re-using the same options given to the current client with optional overriding.

        A credential passed here (`api_key=`, `auth_token=`, `credentials=`, `config=`, or `profile=`) replaces
        this client's credential, whichever kind that is. Passing more than one raises `ValueError`.
        A base URL and headers that came with this client's config or profile go with that credential.
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

        http_client = http_client or self._client

        resolved_credentials = None if isinstance(credentials, NotGiven) else credentials
        keeps_credential = False
        if not api_key and not auth_token and resolved_credentials is None and config is None and profile is None:
            keeps_credential = isinstance(credentials, NotGiven)
            # The attributes can be assigned to, so inherit only the credential this client sends.
            api_key = self.api_key
            auth_token = self.auth_token if api_key is None else None
            if isinstance(credentials, NotGiven) and api_key is None and auth_token is None and _is_base_client(self):
                resolved_credentials = self.credentials
        inherits_provider = isinstance(credentials, NotGiven) and resolved_credentials is not None

        if config is not None:
            _extra_kwargs = {"config": config, **_extra_kwargs}
        if profile is not None:
            _extra_kwargs = {"profile": profile, **_extra_kwargs}
        if resolved_credentials is not None:
            _extra_kwargs = {"credentials": resolved_credentials, **_extra_kwargs}
            # Share the parent's TokenCache only while the provider and
            # deployment are unchanged; a new credentials= or base_url= gets
            # its own cache.
            if inherits_provider and _keeps_base_url(self.base_url, base_url):
                _extra_kwargs = {"_token_cache": self._token_cache, **_extra_kwargs}

        # A host that the caller chose stays. Otherwise a new credential brings its own, or gets the default.
        inherited_base_url = None
        if keeps_credential or self.base_url != self._unchosen_base_url:
            inherited_base_url = self.base_url

        client = self.__class__(
            api_key=api_key,
            auth_token=auth_token,
            webhook_key=webhook_key or self.webhook_key,
            base_url=base_url or inherited_base_url,
            timeout=self.timeout if isinstance(timeout, NotGiven) else timeout,
            http_client=http_client,
            max_retries=max_retries if is_given(max_retries) else self.max_retries,
            default_headers=headers,
            default_query=params,
            middleware=self._middleware if isinstance(middleware, NotGiven) else middleware,
            **_extra_kwargs,
        )
        client._timeout_overridden = self._timeout_overridden or is_given(timeout)
        if keeps_credential:
            client._credential_headers = self._credential_headers
            client._unchosen_base_url = self._unchosen_base_url
        # Set on the copy, not through its constructor, which a subclass may define without `open_telemetry`.
        client._set_open_telemetry(self._copy_open_telemetry(open_telemetry))
        return client

    # Alias for `copy` for nicer inline usage, e.g.
    # client.with_options(timeout=10).foo.create(...)
    with_options = copy

    def with_middleware(self, *middleware: MiddlewareInput) -> Self:
        """A new client with the given middleware appended after this client's middleware.

        Convenience for applying extra middleware to a single request:

        ```py
        client.with_middleware(my_middleware).messages.create(...)
        ```
        """
        return self.copy(middleware=[*self._middleware, *middleware])

    @override
    def _make_status_error(
        self,
        err_msg: str,
        *,
        body: object,
        response: httpx2.Response,
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
    _supports_message_threads = True

    # client options
    api_key: str | None
    auth_token: str | None
    webhook_key: str | None
    credentials: AccessTokenProvider | AsyncAccessTokenProvider | None
    _token_cache: TokenCache | None
    _custom_auth: AccessTokenAuth | None
    _credential_headers: Mapping[str, str]
    _unchosen_base_url: httpx2.URL | None

    def __init__(
        self,
        *,
        api_key: str | None = None,
        auth_token: str | None = None,
        credentials: AccessTokenProvider | AsyncAccessTokenProvider | None = None,
        config: Mapping[str, Any] | None = None,
        profile: str | None = None,
        webhook_key: str | None = None,
        base_url: str | httpx2.URL | None = None,
        timeout: float | Timeout | None | NotGiven = not_given,
        max_retries: int = DEFAULT_MAX_RETRIES,
        default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        # OpenTelemetry tracing of this client's API calls. `False` disables the spans, and
        # `traces.content_mode` set to `"content"` adds the content of requests and responses to them.
        open_telemetry: OpenTelemetryClientOption = None,
        # Configure a custom httpx2 client.
        # We provide a `DefaultAsyncHttpxClient` class that you can pass to retain the default values we use for `limits`, `timeout` & `follow_redirects`.
        # See the [httpx2 documentation](https://httpx2.pydantic.dev/api/#asyncclient) for more details.
        http_client: httpx2.AsyncClient | None = None,
        middleware: Sequence[MiddlewareInput] | None = None,
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

        1. An explicit constructor argument — `api_key=`, `auth_token=`,
           `credentials=`, `config=`, or `profile=`. When one of these
           is passed, environment variables are not consulted for credentials.
        2. `ANTHROPIC_API_KEY`, then `ANTHROPIC_AUTH_TOKEN` environment
           variables.
        3. `ANTHROPIC_PROFILE` environment variable — loads the named
           profile from `<config_dir>/configs/<profile>.json`.
        4. Workload identity federation environment variables —
           `ANTHROPIC_IDENTITY_TOKEN[_FILE]` +
           `ANTHROPIC_FEDERATION_RULE_ID` + `ANTHROPIC_ORGANIZATION_ID`.
        5. The active profile on disk — the profile named by
           `<config_dir>/active_config`, or `default`.

        `ANTHROPIC_CONFIG_DIR` sets `<config_dir>`. It does not select a profile.

        `api_key=`, `auth_token=`, `credentials=`, `config=`, and `profile=`
        are mutually exclusive. Passing more than one raises `ValueError`.

        If `ANTHROPIC_API_KEY` / `ANTHROPIC_AUTH_TOKEN` is set alongside a
        profile or federation configuration, the static credential takes
        precedence and a one-shot warning is logged on the `anthropic`
        logger.

        If both `ANTHROPIC_API_KEY` and `ANTHROPIC_AUTH_TOKEN` are set, the
        API key is used and a one-shot warning is logged on the same logger.
        """
        # Explicit ctor args are total. If the caller passed any explicit
        # credential argument, do NOT read credential env vars.
        if not has_explicit_credential(
            api_key=api_key, auth_token=auth_token, credentials=credentials, config=config, profile=profile
        ):
            api_key, auth_token = static_credential_from_env(warn=_is_base_client(self))
        self.api_key = api_key
        self.auth_token = auth_token

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

        credential_headers: dict[str, str] = {}
        credential_base_url: str | None = None
        if config is not None:
            in_memory = InMemoryConfig(dict(config))
            credentials = in_memory
            credential_headers = in_memory.extra_headers()
            credential_base_url = in_memory.resolved_base_url
        elif profile is not None:
            creds_file = CredentialsFile(profile=profile)
            credentials = creds_file
            credential_headers = creds_file.extra_headers()
            credential_base_url = creds_file.resolved_base_url
        if credentials is None and api_key is None and auth_token is None and _is_base_client(self):
            result = default_credentials(base_url=str(base_url) if base_url else "https://api.anthropic.com")
            if result is not None:
                credentials = result.provider
                credential_headers = result.extra_headers
                credential_base_url = result.base_url

        self._credential_headers = credential_headers
        if not base_url_is_explicit and credential_base_url:
            base_url = credential_base_url
        self._unchosen_base_url = None if base_url_is_explicit else self._enforce_trailing_slash(httpx2.URL(base_url))

        credentials = _bind_credentials_base_url(credentials, str(base_url))
        self.credentials = credentials
        if not isinstance(_token_cache, NotGiven):
            self._token_cache = _token_cache
        else:
            self._token_cache = TokenCache(credentials) if credentials is not None else None
        self._custom_auth = AccessTokenAuth(self._token_cache) if self._token_cache is not None else None

        super().__init__(
            version=__version__,
            base_url=base_url,
            max_retries=max_retries,
            timeout=timeout,
            open_telemetry=open_telemetry,
            http_client=http_client,
            custom_headers=default_headers,
            custom_query=default_query,
            middleware=middleware,
            _strict_response_validation=_strict_response_validation,
        )

        self._default_stream_cls = AsyncStream

    @cached_property
    def messages(self) -> AsyncMessages:
        from .resources.messages import AsyncMessages

        return AsyncMessages(self)

    @cached_property
    def models(self) -> AsyncModels:
        from .resources.models import AsyncModels

        return AsyncModels(self)

    @cached_property
    def files(self) -> AsyncFiles:
        from .resources.files import AsyncFiles

        return AsyncFiles(self)

    @cached_property
    def skills(self) -> AsyncSkills:
        from .resources.skills import AsyncSkills

        return AsyncSkills(self)

    @cached_property
    def user_profiles(self) -> AsyncUserProfiles:
        from .resources.user_profiles import AsyncUserProfiles

        return AsyncUserProfiles(self)

    @cached_property
    def organization(self) -> AsyncOrganization:
        from .resources.organization import AsyncOrganization

        return AsyncOrganization(self)

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
        return {**self._bearer_auth, **self._api_key_auth}

    @property
    def _api_key_auth(self) -> dict[str, str]:
        api_key = self.api_key
        if api_key is None:
            return {}
        return {"Authorization": f"Bearer {api_key}"}

    @property
    def _bearer_auth(self) -> dict[str, str]:
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
            "anthropic-version": ANTHROPIC_API_VERSION,
            **self._credential_headers,
            **self._custom_headers,
        }

    @override
    async def _prepare_options(self, options: FinalRequestOptions) -> FinalRequestOptions:
        return _keep_client_header_params(await super()._prepare_options(options))

    @override
    def _validate_headers(self, headers: httpx2.Headers, omitted: frozenset[str]) -> None:
        # --- credentials support (hand-written, upstream to Stainless) ---
        if self._token_cache is not None and not headers.get("X-Api-Key") and not headers.get("Authorization"):
            return
        # --- end credentials support ---
        if headers.get("Authorization") or headers.get("X-Api-Key"):
            # valid
            return

        if headers.get("Authorization") or "authorization" in omitted:
            return

        raise TypeError(
            '"Could not resolve authentication method. Expected one of api_key, auth_token, or credentials to be set. Or for the `Authorization` header to be explicitly omitted"'
        )

    # --- credentials support (hand-written, upstream to Stainless) ---
    @property
    @override
    def custom_auth(self) -> httpx2.Auth | None:
        return self._custom_auth

    @override
    def _should_retry(self, response: httpx2.Response) -> bool:
        # On 401 with a token cache, invalidate and retry once so the request
        # is re-sent with a freshly minted Bearer token. The base-client retry
        # loop rebuilds the request from FinalRequestOptions on each attempt,
        # so body replay is handled for us. The single-shot guard relies on
        # `x-stainless-retry-count` being `"0"` on the first attempt
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
        await async_close_credentials(self.credentials)

    # --- end credentials support ---

    def copy(
        self,
        *,
        api_key: str | None = None,
        auth_token: str | None = None,
        credentials: AccessTokenProvider | AsyncAccessTokenProvider | None | NotGiven = not_given,
        config: Mapping[str, Any] | None = None,
        profile: str | None = None,
        webhook_key: str | None = None,
        base_url: str | httpx2.URL | None = None,
        timeout: float | Timeout | None | NotGiven = not_given,
        http_client: httpx2.AsyncClient | None = None,
        max_retries: int | NotGiven = not_given,
        open_telemetry: OpenTelemetryClientOption = None,
        default_headers: Mapping[str, str] | None = None,
        set_default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        set_default_query: Mapping[str, object] | None = None,
        middleware: Sequence[MiddlewareInput] | None | NotGiven = not_given,
        _extra_kwargs: Mapping[str, Any] = {},
    ) -> Self:
        """
        Create a new client instance re-using the same options given to the current client with optional overriding.

        A credential passed here (`api_key=`, `auth_token=`, `credentials=`, `config=`, or `profile=`) replaces
        this client's credential, whichever kind that is. Passing more than one raises `ValueError`.
        A base URL and headers that came with this client's config or profile go with that credential.
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

        http_client = http_client or self._client

        resolved_credentials = None if isinstance(credentials, NotGiven) else credentials
        keeps_credential = False
        if not api_key and not auth_token and resolved_credentials is None and config is None and profile is None:
            keeps_credential = isinstance(credentials, NotGiven)
            # The attributes can be assigned to, so inherit only the credential this client sends.
            api_key = self.api_key
            auth_token = self.auth_token if api_key is None else None
            if isinstance(credentials, NotGiven) and api_key is None and auth_token is None and _is_base_client(self):
                resolved_credentials = self.credentials
        inherits_provider = isinstance(credentials, NotGiven) and resolved_credentials is not None

        if config is not None:
            _extra_kwargs = {"config": config, **_extra_kwargs}
        if profile is not None:
            _extra_kwargs = {"profile": profile, **_extra_kwargs}
        if resolved_credentials is not None:
            _extra_kwargs = {"credentials": resolved_credentials, **_extra_kwargs}
            # Share the parent's TokenCache only while the provider and
            # deployment are unchanged; a new credentials= or base_url= gets
            # its own cache.
            if inherits_provider and _keeps_base_url(self.base_url, base_url):
                _extra_kwargs = {"_token_cache": self._token_cache, **_extra_kwargs}

        # A host that the caller chose stays. Otherwise a new credential brings its own, or gets the default.
        inherited_base_url = None
        if keeps_credential or self.base_url != self._unchosen_base_url:
            inherited_base_url = self.base_url

        client = self.__class__(
            api_key=api_key,
            auth_token=auth_token,
            webhook_key=webhook_key or self.webhook_key,
            base_url=base_url or inherited_base_url,
            timeout=self.timeout if isinstance(timeout, NotGiven) else timeout,
            http_client=http_client,
            max_retries=max_retries if is_given(max_retries) else self.max_retries,
            default_headers=headers,
            default_query=params,
            middleware=self._middleware if isinstance(middleware, NotGiven) else middleware,
            **_extra_kwargs,
        )
        client._timeout_overridden = self._timeout_overridden or is_given(timeout)
        if keeps_credential:
            client._credential_headers = self._credential_headers
            client._unchosen_base_url = self._unchosen_base_url
        # Set on the copy, not through its constructor, which a subclass may define without `open_telemetry`.
        client._set_open_telemetry(self._copy_open_telemetry(open_telemetry))
        return client

    # Alias for `copy` for nicer inline usage, e.g.
    # client.with_options(timeout=10).foo.create(...)
    with_options = copy

    def with_middleware(self, *middleware: MiddlewareInput) -> Self:
        """A new client with the given middleware appended after this client's middleware.

        Convenience for applying extra middleware to a single request:

        ```py
        client.with_middleware(my_middleware).messages.create(...)
        ```
        """
        return self.copy(middleware=[*self._middleware, *middleware])

    @override
    def _make_status_error(
        self,
        err_msg: str,
        *,
        body: object,
        response: httpx2.Response,
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
    def messages(self) -> messages.MessagesWithRawResponse:
        from .resources.messages import MessagesWithRawResponse

        return MessagesWithRawResponse(self._client.messages)

    @cached_property
    def models(self) -> models.ModelsWithRawResponse:
        from .resources.models import ModelsWithRawResponse

        return ModelsWithRawResponse(self._client.models)

    @cached_property
    def files(self) -> files.FilesWithRawResponse:
        from .resources.files import FilesWithRawResponse

        return FilesWithRawResponse(self._client.files)

    @cached_property
    def skills(self) -> skills.SkillsWithRawResponse:
        from .resources.skills import SkillsWithRawResponse

        return SkillsWithRawResponse(self._client.skills)

    @cached_property
    def user_profiles(self) -> user_profiles.UserProfilesWithRawResponse:
        from .resources.user_profiles import UserProfilesWithRawResponse

        return UserProfilesWithRawResponse(self._client.user_profiles)

    @cached_property
    def organization(self) -> organization.OrganizationWithRawResponse:
        from .resources.organization import OrganizationWithRawResponse

        return OrganizationWithRawResponse(self._client.organization)

    @cached_property
    def beta(self) -> beta.BetaWithRawResponse:
        from .resources.beta import BetaWithRawResponse

        return BetaWithRawResponse(self._client.beta)


class AsyncAnthropicWithRawResponse:
    _client: AsyncAnthropic

    def __init__(self, client: AsyncAnthropic) -> None:
        self._client = client

    @cached_property
    def messages(self) -> messages.AsyncMessagesWithRawResponse:
        from .resources.messages import AsyncMessagesWithRawResponse

        return AsyncMessagesWithRawResponse(self._client.messages)

    @cached_property
    def models(self) -> models.AsyncModelsWithRawResponse:
        from .resources.models import AsyncModelsWithRawResponse

        return AsyncModelsWithRawResponse(self._client.models)

    @cached_property
    def files(self) -> files.AsyncFilesWithRawResponse:
        from .resources.files import AsyncFilesWithRawResponse

        return AsyncFilesWithRawResponse(self._client.files)

    @cached_property
    def skills(self) -> skills.AsyncSkillsWithRawResponse:
        from .resources.skills import AsyncSkillsWithRawResponse

        return AsyncSkillsWithRawResponse(self._client.skills)

    @cached_property
    def user_profiles(self) -> user_profiles.AsyncUserProfilesWithRawResponse:
        from .resources.user_profiles import AsyncUserProfilesWithRawResponse

        return AsyncUserProfilesWithRawResponse(self._client.user_profiles)

    @cached_property
    def organization(self) -> organization.AsyncOrganizationWithRawResponse:
        from .resources.organization import AsyncOrganizationWithRawResponse

        return AsyncOrganizationWithRawResponse(self._client.organization)

    @cached_property
    def beta(self) -> beta.AsyncBetaWithRawResponse:
        from .resources.beta import AsyncBetaWithRawResponse

        return AsyncBetaWithRawResponse(self._client.beta)


class AnthropicWithStreamedResponse:
    _client: Anthropic

    def __init__(self, client: Anthropic) -> None:
        self._client = client

    @cached_property
    def messages(self) -> messages.MessagesWithStreamingResponse:
        from .resources.messages import MessagesWithStreamingResponse

        return MessagesWithStreamingResponse(self._client.messages)

    @cached_property
    def models(self) -> models.ModelsWithStreamingResponse:
        from .resources.models import ModelsWithStreamingResponse

        return ModelsWithStreamingResponse(self._client.models)

    @cached_property
    def files(self) -> files.FilesWithStreamingResponse:
        from .resources.files import FilesWithStreamingResponse

        return FilesWithStreamingResponse(self._client.files)

    @cached_property
    def skills(self) -> skills.SkillsWithStreamingResponse:
        from .resources.skills import SkillsWithStreamingResponse

        return SkillsWithStreamingResponse(self._client.skills)

    @cached_property
    def user_profiles(self) -> user_profiles.UserProfilesWithStreamingResponse:
        from .resources.user_profiles import UserProfilesWithStreamingResponse

        return UserProfilesWithStreamingResponse(self._client.user_profiles)

    @cached_property
    def organization(self) -> organization.OrganizationWithStreamingResponse:
        from .resources.organization import OrganizationWithStreamingResponse

        return OrganizationWithStreamingResponse(self._client.organization)

    @cached_property
    def beta(self) -> beta.BetaWithStreamingResponse:
        from .resources.beta import BetaWithStreamingResponse

        return BetaWithStreamingResponse(self._client.beta)


class AsyncAnthropicWithStreamedResponse:
    _client: AsyncAnthropic

    def __init__(self, client: AsyncAnthropic) -> None:
        self._client = client

    @cached_property
    def messages(self) -> messages.AsyncMessagesWithStreamingResponse:
        from .resources.messages import AsyncMessagesWithStreamingResponse

        return AsyncMessagesWithStreamingResponse(self._client.messages)

    @cached_property
    def models(self) -> models.AsyncModelsWithStreamingResponse:
        from .resources.models import AsyncModelsWithStreamingResponse

        return AsyncModelsWithStreamingResponse(self._client.models)

    @cached_property
    def files(self) -> files.AsyncFilesWithStreamingResponse:
        from .resources.files import AsyncFilesWithStreamingResponse

        return AsyncFilesWithStreamingResponse(self._client.files)

    @cached_property
    def skills(self) -> skills.AsyncSkillsWithStreamingResponse:
        from .resources.skills import AsyncSkillsWithStreamingResponse

        return AsyncSkillsWithStreamingResponse(self._client.skills)

    @cached_property
    def user_profiles(self) -> user_profiles.AsyncUserProfilesWithStreamingResponse:
        from .resources.user_profiles import AsyncUserProfilesWithStreamingResponse

        return AsyncUserProfilesWithStreamingResponse(self._client.user_profiles)

    @cached_property
    def organization(self) -> organization.AsyncOrganizationWithStreamingResponse:
        from .resources.organization import AsyncOrganizationWithStreamingResponse

        return AsyncOrganizationWithStreamingResponse(self._client.organization)

    @cached_property
    def beta(self) -> beta.AsyncBetaWithStreamingResponse:
        from .resources.beta import AsyncBetaWithStreamingResponse

        return AsyncBetaWithStreamingResponse(self._client.beta)


Client = Anthropic

AsyncClient = AsyncAnthropic
