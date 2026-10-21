from __future__ import annotations

import os
from typing import Any, Union, Mapping, TypeVar, Sequence
from typing_extensions import Self, override

import httpx2

from ... import _exceptions
from ..._qs import Querystring
from ..._types import Omit, Headers, Timeout, NotGiven, OpenTelemetryClientOption, omit, not_given
from ..._utils import is_dict, asyncify, is_given
from ..._client import _keep_client_header_params
from ..._compat import cached_property
from ..._version import __version__
from ..aws._auth import get_auth_headers
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._constants import ANTHROPIC_API_VERSION
from ..._streaming import Stream, AsyncStream
from ..._exceptions import AnthropicError, APIStatusError
from ..._middleware import MiddlewareInput
from ..._base_client import (
    DEFAULT_MAX_RETRIES,
    BaseClient,
    SyncAPIClient,
    AsyncAPIClient,
    FinalRequestOptions,
    build_headers,
    merge_headers,
)
from ..aws._credentials import (
    resolve_region,
    resolve_api_key,
    resolve_auth_mode,
    validate_credentials,
)
from ...resources.messages import Messages, AsyncMessages
from ...resources.beta.messages import Messages as BetaMessages, AsyncMessages as AsyncBetaMessages

DEFAULT_SERVICE_NAME = "bedrock-mantle"

_MANTLE_API_KEY_ENV_VARS = ("AWS_BEARER_TOKEN_BEDROCK", "ANTHROPIC_AWS_API_KEY")

USER_PROFILE_ID_HEADER = "anthropic-user-profile-id"

USER_PROFILE_ID_BODY_PATHS = frozenset(
    {
        "/v1/messages",
        "/v1/messages?beta=true",
        "/v1/messages/count_tokens",
        "/v1/messages/count_tokens?beta=true",
    }
)

_HttpxClientT = TypeVar("_HttpxClientT", bound=Union[httpx2.Client, httpx2.AsyncClient])
_DefaultStreamT = TypeVar("_DefaultStreamT", bound=Union[Stream[Any], AsyncStream[Any]])


class MantleBeta(SyncAPIResource):
    @cached_property
    def messages(self) -> BetaMessages:
        return BetaMessages(self._client)


class AsyncMantleBeta(AsyncAPIResource):
    @cached_property
    def messages(self) -> AsyncBetaMessages:
        return AsyncBetaMessages(self._client)


class BaseMantleClient(BaseClient[_HttpxClientT, _DefaultStreamT]):
    # Mantle is an Amazon Bedrock endpoint.
    _gen_ai_provider_name = "aws.bedrock"
    _otel_platform = "bedrock"

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

    def _move_user_profile_id_to_body(self, options: FinalRequestOptions) -> FinalRequestOptions:
        """Mantle reads the user profile ID from the body of these requests, and from the header on other routes."""
        body = options.json_data
        if options.url not in USER_PROFILE_ID_BODY_PATHS or not is_dict(body):
            return options

        headers: Headers = options.headers or {}
        user_profile_id = build_headers(self._custom_headers, headers)[0].get(USER_PROFILE_ID_HEADER)
        if user_profile_id is None:
            return options

        options.headers = merge_headers(headers, {USER_PROFILE_ID_HEADER: omit})
        options.json_data = {"user_profile_id": user_profile_id, **body}
        return options


def _resolve_mantle_config(
    *,
    api_key: str | None,
    aws_access_key: str | None,
    aws_secret_key: str | None,
    aws_region: str | None,
    aws_profile: str | None,
    skip_auth: bool,
    base_url: str | httpx2.URL | None,
    default_headers: Mapping[str, str] | None,
) -> tuple[str | None, str | httpx2.URL, bool, dict[str, str]]:
    """Resolve and validate all Mantle client configuration.

    Returns (resolved_api_key, resolved_base_url, use_sigv4, merged_headers).
    """
    if skip_auth:
        use_sigv4 = False
        resolved_api_key = None
    else:
        validate_credentials(aws_access_key=aws_access_key, aws_secret_key=aws_secret_key)

        use_sigv4 = resolve_auth_mode(
            api_key=api_key,
            aws_access_key=aws_access_key,
            aws_secret_key=aws_secret_key,
            aws_profile=aws_profile,
            api_key_env_vars=_MANTLE_API_KEY_ENV_VARS,
        )

        resolved_api_key = resolve_api_key(
            api_key=api_key,
            use_sigv4=use_sigv4,
            api_key_env_vars=_MANTLE_API_KEY_ENV_VARS,
        )

    resolved_region = resolve_region(aws_region)

    if base_url is None:
        base_url = os.environ.get("ANTHROPIC_BEDROCK_MANTLE_BASE_URL")
    if base_url is None:
        if resolved_region is None:
            raise AnthropicError(
                "No AWS region or base URL found. Set `aws_region` in the constructor, "
                "the `AWS_REGION` / `AWS_DEFAULT_REGION` environment variable, or provide "
                "a `base_url` / `ANTHROPIC_BEDROCK_MANTLE_BASE_URL` environment variable."
            )
        base_url = f"https://bedrock-mantle.{resolved_region}.api.aws/anthropic"

    merged_headers: dict[str, str] = {}
    if default_headers:
        merged_headers.update(default_headers)

    return resolved_api_key, base_url, use_sigv4, merged_headers


class AnthropicBedrockMantle(BaseMantleClient[httpx2.Client, Stream[Any]], SyncAPIClient):
    messages: Messages
    beta: MantleBeta

    aws_region: str | None
    aws_access_key: str | None
    aws_secret_key: str | None
    aws_session_token: str | None
    aws_profile: str | None
    skip_auth: bool

    _use_sigv4: bool

    def __init__(
        self,
        *,
        aws_access_key: str | None = None,
        aws_secret_key: str | None = None,
        aws_session_token: str | None = None,
        aws_region: str | None = None,
        aws_profile: str | None = None,
        api_key: str | None = None,
        skip_auth: bool = False,
        base_url: str | httpx2.URL | None = None,
        timeout: float | Timeout | None | NotGiven = not_given,
        max_retries: int = DEFAULT_MAX_RETRIES,
        default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        # OpenTelemetry tracing of this client's API calls. `False` disables the spans, and
        # `traces.content_mode` set to `"content"` adds the content of requests and responses to them.
        open_telemetry: OpenTelemetryClientOption = None,
        http_client: httpx2.Client | None = None,
        middleware: Sequence[MiddlewareInput] | None = None,
        _strict_response_validation: bool = False,
    ) -> None:
        resolved_api_key, resolved_base_url, use_sigv4, merged_headers = _resolve_mantle_config(
            api_key=api_key,
            aws_access_key=aws_access_key,
            aws_secret_key=aws_secret_key,
            aws_region=aws_region,
            aws_profile=aws_profile,
            skip_auth=skip_auth,
            base_url=base_url,
            default_headers=default_headers,
        )

        resolved_region = resolve_region(aws_region)

        super().__init__(
            version=__version__,
            base_url=resolved_base_url,
            timeout=timeout,
            max_retries=max_retries,
            open_telemetry=open_telemetry,
            custom_headers=merged_headers,
            custom_query=default_query,
            http_client=http_client,
            middleware=middleware,
            _strict_response_validation=_strict_response_validation,
        )

        self.api_key = resolved_api_key
        self.aws_region = resolved_region
        self.aws_access_key = aws_access_key
        self.aws_secret_key = aws_secret_key
        self.aws_session_token = aws_session_token
        self.aws_profile = aws_profile
        self.skip_auth = skip_auth
        self._use_sigv4 = use_sigv4

        self.messages = Messages(self)
        self.beta = MantleBeta(self)

    @property
    @override
    def qs(self) -> Querystring:
        return Querystring(array_format="comma")

    @property
    @override
    def auth_headers(self) -> dict[str, str]:
        if self.skip_auth or self._use_sigv4:
            return {}
        api_key = self.api_key
        if api_key is None:
            return {}
        return {"Authorization": f"Bearer {api_key}"}

    @property
    @override
    def default_headers(self) -> dict[str, str | Omit]:
        return {
            **super().default_headers,
            "X-Stainless-Async": "false",
            "anthropic-version": ANTHROPIC_API_VERSION,
            **self._custom_headers,
        }

    @override
    def _validate_headers(self, headers: httpx2.Headers, omitted: frozenset[str]) -> None:
        pass

    @override
    def _prepare_options(self, options: FinalRequestOptions) -> FinalRequestOptions:
        return self._move_user_profile_id_to_body(_keep_client_header_params(options))

    @override
    def _prepare_request(self, request: httpx2.Request) -> None:
        if self.skip_auth or not self._use_sigv4:
            return

        data = request.read()

        headers = get_auth_headers(
            method=request.method,
            url=str(request.url),
            headers=request.headers,
            aws_access_key=self.aws_access_key,
            aws_secret_key=self.aws_secret_key,
            aws_session_token=self.aws_session_token,
            region=self.aws_region,
            profile=self.aws_profile,
            data=data,
            service_name=DEFAULT_SERVICE_NAME,
        )
        request.headers.update(headers)

    def copy(
        self,
        *,
        api_key: str | None = None,
        aws_access_key: str | None = None,
        aws_secret_key: str | None = None,
        aws_session_token: str | None = None,
        aws_region: str | None = None,
        aws_profile: str | None = None,
        skip_auth: bool | None = None,
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

        return self.__class__(
            api_key=api_key or self.api_key,
            aws_access_key=aws_access_key or self.aws_access_key,
            aws_secret_key=aws_secret_key or self.aws_secret_key,
            aws_session_token=aws_session_token or self.aws_session_token,
            aws_region=aws_region or self.aws_region,
            aws_profile=aws_profile or self.aws_profile,
            skip_auth=skip_auth if skip_auth is not None else self.skip_auth,
            base_url=base_url or self.base_url,
            timeout=self.timeout if isinstance(timeout, NotGiven) else timeout,
            http_client=http_client,
            max_retries=max_retries if is_given(max_retries) else self.max_retries,
            open_telemetry=self._copy_open_telemetry(open_telemetry),
            default_headers=headers,
            default_query=params,
            middleware=self._middleware if isinstance(middleware, NotGiven) else middleware,
            **_extra_kwargs,
        )

    with_options = copy

    def with_middleware(self, *middleware: MiddlewareInput) -> Self:
        """A new client with the given middleware appended after this client's middleware.

        Convenience for applying extra middleware to a single request:

        ```py
        client.with_middleware(my_middleware).messages.create(...)
        ```
        """
        return self.copy(middleware=[*self._middleware, *middleware])


class AsyncAnthropicBedrockMantle(BaseMantleClient[httpx2.AsyncClient, AsyncStream[Any]], AsyncAPIClient):
    messages: AsyncMessages
    beta: AsyncMantleBeta

    aws_region: str | None
    aws_access_key: str | None
    aws_secret_key: str | None
    aws_session_token: str | None
    aws_profile: str | None
    skip_auth: bool

    _use_sigv4: bool

    def __init__(
        self,
        *,
        aws_access_key: str | None = None,
        aws_secret_key: str | None = None,
        aws_session_token: str | None = None,
        aws_region: str | None = None,
        aws_profile: str | None = None,
        api_key: str | None = None,
        skip_auth: bool = False,
        base_url: str | httpx2.URL | None = None,
        timeout: float | Timeout | None | NotGiven = not_given,
        max_retries: int = DEFAULT_MAX_RETRIES,
        default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        # OpenTelemetry tracing of this client's API calls. `False` disables the spans, and
        # `traces.content_mode` set to `"content"` adds the content of requests and responses to them.
        open_telemetry: OpenTelemetryClientOption = None,
        http_client: httpx2.AsyncClient | None = None,
        middleware: Sequence[MiddlewareInput] | None = None,
        _strict_response_validation: bool = False,
    ) -> None:
        resolved_api_key, resolved_base_url, use_sigv4, merged_headers = _resolve_mantle_config(
            api_key=api_key,
            aws_access_key=aws_access_key,
            aws_secret_key=aws_secret_key,
            aws_region=aws_region,
            aws_profile=aws_profile,
            skip_auth=skip_auth,
            base_url=base_url,
            default_headers=default_headers,
        )

        resolved_region = resolve_region(aws_region)

        super().__init__(
            version=__version__,
            base_url=resolved_base_url,
            timeout=timeout,
            max_retries=max_retries,
            open_telemetry=open_telemetry,
            custom_headers=merged_headers,
            custom_query=default_query,
            http_client=http_client,
            middleware=middleware,
            _strict_response_validation=_strict_response_validation,
        )

        self.api_key = resolved_api_key
        self.aws_region = resolved_region
        self.aws_access_key = aws_access_key
        self.aws_secret_key = aws_secret_key
        self.aws_session_token = aws_session_token
        self.aws_profile = aws_profile
        self.skip_auth = skip_auth
        self._use_sigv4 = use_sigv4

        self.messages = AsyncMessages(self)
        self.beta = AsyncMantleBeta(self)

    @property
    @override
    def qs(self) -> Querystring:
        return Querystring(array_format="comma")

    @property
    @override
    def auth_headers(self) -> dict[str, str]:
        if self.skip_auth or self._use_sigv4:
            return {}
        api_key = self.api_key
        if api_key is None:
            return {}
        return {"Authorization": f"Bearer {api_key}"}

    @property
    @override
    def default_headers(self) -> dict[str, str | Omit]:
        return {
            **super().default_headers,
            "X-Stainless-Async": "async:asyncio",
            "anthropic-version": ANTHROPIC_API_VERSION,
            **self._custom_headers,
        }

    @override
    def _validate_headers(self, headers: httpx2.Headers, omitted: frozenset[str]) -> None:
        pass

    @override
    async def _prepare_options(self, options: FinalRequestOptions) -> FinalRequestOptions:
        return self._move_user_profile_id_to_body(_keep_client_header_params(options))

    @override
    async def _prepare_request(self, request: httpx2.Request) -> None:
        if self.skip_auth or not self._use_sigv4:
            return

        data = request.read()

        headers = await asyncify(get_auth_headers)(
            method=request.method,
            url=str(request.url),
            headers=request.headers,
            aws_access_key=self.aws_access_key,
            aws_secret_key=self.aws_secret_key,
            aws_session_token=self.aws_session_token,
            region=self.aws_region,
            profile=self.aws_profile,
            data=data,
            service_name=DEFAULT_SERVICE_NAME,
        )
        request.headers.update(headers)

    def copy(
        self,
        *,
        api_key: str | None = None,
        aws_access_key: str | None = None,
        aws_secret_key: str | None = None,
        aws_session_token: str | None = None,
        aws_region: str | None = None,
        aws_profile: str | None = None,
        skip_auth: bool | None = None,
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

        return self.__class__(
            api_key=api_key or self.api_key,
            aws_access_key=aws_access_key or self.aws_access_key,
            aws_secret_key=aws_secret_key or self.aws_secret_key,
            aws_session_token=aws_session_token or self.aws_session_token,
            aws_region=aws_region or self.aws_region,
            aws_profile=aws_profile or self.aws_profile,
            skip_auth=skip_auth if skip_auth is not None else self.skip_auth,
            base_url=base_url or self.base_url,
            timeout=self.timeout if isinstance(timeout, NotGiven) else timeout,
            http_client=http_client,
            max_retries=max_retries if is_given(max_retries) else self.max_retries,
            open_telemetry=self._copy_open_telemetry(open_telemetry),
            default_headers=headers,
            default_query=params,
            middleware=self._middleware if isinstance(middleware, NotGiven) else middleware,
            **_extra_kwargs,
        )

    with_options = copy

    def with_middleware(self, *middleware: MiddlewareInput) -> Self:
        """A new client with the given middleware appended after this client's middleware.

        Convenience for applying extra middleware to a single request:

        ```py
        client.with_middleware(my_middleware).messages.create(...)
        ```
        """
        return self.copy(middleware=[*self._middleware, *middleware])
