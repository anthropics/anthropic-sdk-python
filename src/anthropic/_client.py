# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import TYPE_CHECKING, Any, Mapping
from typing_extensions import Self, override

import httpx2

from . import _constants, _exceptions
from ._qs import Querystring
from ._types import Omit, Timeout, NotGiven, RequestOptions, not_given
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
    merge_headers,
)

if TYPE_CHECKING:
    from .resources import beta, files, models, skills, messages
    from .resources.files import Files, AsyncFiles
    from .resources.models import Models, AsyncModels
    from .resources.beta.beta import Beta, AsyncBeta
    from .resources.skills.skills import Skills, AsyncSkills
    from .resources.messages.messages import Messages, AsyncMessages

__all__ = ["Timeout", "RequestOptions", "Anthropic", "AsyncAnthropic", "Client", "AsyncClient"]


class Anthropic(SyncAPIClient):
    # client options
    api_key: str | None
    auth_token: str | None
    webhook_key: str | None

    # constants
    HUMAN_PROMPT = _constants.HUMAN_PROMPT
    AI_PROMPT = _constants.AI_PROMPT

    def __init__(
        self,
        *,
        api_key: str | None = None,
        auth_token: str | None = None,
        webhook_key: str | None = None,
        base_url: str | httpx2.URL | None = None,
        timeout: float | Timeout | None | NotGiven = not_given,
        max_retries: int = DEFAULT_MAX_RETRIES,
        default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        # Configure a custom httpx2 client.
        # We provide a `DefaultHttpxClient` class that you can pass to retain the default values we use for `limits`, `timeout` & `follow_redirects`.
        # See the [httpx2 documentation](https://httpx2.pydantic.dev/api/#client) for more details.
        http_client: httpx2.Client | None = None,
        # Enable or disable schema validation for data returned by the API.
        # When enabled an error APIResponseValidationError is raised
        # if the API responds with invalid data for the expected schema.
        #
        # This parameter may be removed or changed in the future.
        # If you rely on this feature, please open a GitHub issue
        # outlining your use-case to help us decide if it should be
        # part of our public interface in the future.
        _strict_response_validation: bool = False,
    ) -> None:
        """Construct a new synchronous Anthropic client instance.

        This automatically infers the following arguments from their corresponding environment variables if they are not provided:
        - `api_key` from `ANTHROPIC_API_KEY`
        - `auth_token` from `ANTHROPIC_AUTH_TOKEN`
        - `webhook_key` from `ANTHROPIC_WEBHOOK_SIGNING_KEY`
        """
        if api_key is None:
            api_key = os.environ.get("ANTHROPIC_API_KEY")
        self.api_key = api_key

        if auth_token is None:
            auth_token = os.environ.get("ANTHROPIC_AUTH_TOKEN")
        self.auth_token = auth_token

        if webhook_key is None:
            webhook_key = os.environ.get("ANTHROPIC_WEBHOOK_SIGNING_KEY")
        self.webhook_key = webhook_key

        if base_url is None:
            base_url = os.environ.get("ANTHROPIC_BASE_URL")
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
    def _validate_headers(self, headers: httpx2.Headers, omitted: frozenset[str]) -> None:
        if headers.get("X-Api-Key") or "x-api-key" in omitted:
            return

        if headers.get("Authorization") or "authorization" in omitted:
            return

        raise TypeError(
            '"Could not resolve authentication method. Expected either api_key or auth_token to be set. Or for one of the `X-Api-Key` or `Authorization` headers to be explicitly omitted"'
        )

    def copy(
        self,
        *,
        api_key: str | None = None,
        auth_token: str | None = None,
        webhook_key: str | None = None,
        base_url: str | httpx2.URL | None = None,
        timeout: float | Timeout | None | NotGiven = not_given,
        http_client: httpx2.Client | None = None,
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
            headers = merge_headers(headers, default_headers)
        elif set_default_headers is not None:
            headers = set_default_headers

        params = self._custom_query
        if default_query is not None:
            params = {**params, **default_query}
        elif set_default_query is not None:
            params = set_default_query

        http_client = http_client or self._client
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

        if response.status_code == 422:
            return _exceptions.UnprocessableEntityError(err_msg, response=response, body=body)

        if response.status_code == 429:
            return _exceptions.RateLimitError(err_msg, response=response, body=body)

        if response.status_code >= 500:
            return _exceptions.InternalServerError(err_msg, response=response, body=body)
        return APIStatusError(err_msg, response=response, body=body)


class AsyncAnthropic(AsyncAPIClient):
    # client options
    api_key: str | None
    auth_token: str | None
    webhook_key: str | None

    # constants
    HUMAN_PROMPT = _constants.HUMAN_PROMPT
    AI_PROMPT = _constants.AI_PROMPT

    def __init__(
        self,
        *,
        api_key: str | None = None,
        auth_token: str | None = None,
        webhook_key: str | None = None,
        base_url: str | httpx2.URL | None = None,
        timeout: float | Timeout | None | NotGiven = not_given,
        max_retries: int = DEFAULT_MAX_RETRIES,
        default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        # Configure a custom httpx2 client.
        # We provide a `DefaultAsyncHttpxClient` class that you can pass to retain the default values we use for `limits`, `timeout` & `follow_redirects`.
        # See the [httpx2 documentation](https://httpx2.pydantic.dev/api/#asyncclient) for more details.
        http_client: httpx2.AsyncClient | None = None,
        # Enable or disable schema validation for data returned by the API.
        # When enabled an error APIResponseValidationError is raised
        # if the API responds with invalid data for the expected schema.
        #
        # This parameter may be removed or changed in the future.
        # If you rely on this feature, please open a GitHub issue
        # outlining your use-case to help us decide if it should be
        # part of our public interface in the future.
        _strict_response_validation: bool = False,
    ) -> None:
        """Construct a new async AsyncAnthropic client instance.

        This automatically infers the following arguments from their corresponding environment variables if they are not provided:
        - `api_key` from `ANTHROPIC_API_KEY`
        - `auth_token` from `ANTHROPIC_AUTH_TOKEN`
        - `webhook_key` from `ANTHROPIC_WEBHOOK_SIGNING_KEY`
        """
        if api_key is None:
            api_key = os.environ.get("ANTHROPIC_API_KEY")
        self.api_key = api_key

        if auth_token is None:
            auth_token = os.environ.get("ANTHROPIC_AUTH_TOKEN")
        self.auth_token = auth_token

        if webhook_key is None:
            webhook_key = os.environ.get("ANTHROPIC_WEBHOOK_SIGNING_KEY")
        self.webhook_key = webhook_key

        if base_url is None:
            base_url = os.environ.get("ANTHROPIC_BASE_URL")
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
    def _validate_headers(self, headers: httpx2.Headers, omitted: frozenset[str]) -> None:
        if headers.get("X-Api-Key") or "x-api-key" in omitted:
            return

        if headers.get("Authorization") or "authorization" in omitted:
            return

        raise TypeError(
            '"Could not resolve authentication method. Expected either api_key or auth_token to be set. Or for one of the `X-Api-Key` or `Authorization` headers to be explicitly omitted"'
        )

    def copy(
        self,
        *,
        api_key: str | None = None,
        auth_token: str | None = None,
        webhook_key: str | None = None,
        base_url: str | httpx2.URL | None = None,
        timeout: float | Timeout | None | NotGiven = not_given,
        http_client: httpx2.AsyncClient | None = None,
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
            headers = merge_headers(headers, default_headers)
        elif set_default_headers is not None:
            headers = set_default_headers

        params = self._custom_query
        if default_query is not None:
            params = {**params, **default_query}
        elif set_default_query is not None:
            params = set_default_query

        http_client = http_client or self._client
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

        if response.status_code == 422:
            return _exceptions.UnprocessableEntityError(err_msg, response=response, body=body)

        if response.status_code == 429:
            return _exceptions.RateLimitError(err_msg, response=response, body=body)

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
    def beta(self) -> beta.AsyncBetaWithStreamingResponse:
        from .resources.beta import AsyncBetaWithStreamingResponse

        return AsyncBetaWithStreamingResponse(self._client.beta)


Client = Anthropic

AsyncClient = AsyncAnthropic
