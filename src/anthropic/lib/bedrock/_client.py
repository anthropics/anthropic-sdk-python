from __future__ import annotations

import os
from typing import Any, Union, Mapping, TypeVar
from typing_extensions import override

import httpx

from ... import _exceptions
from ..._types import NOT_GIVEN, NotGiven
from ..._utils import is_dict
from ..._version import __version__
from ..._streaming import Stream, AsyncStream
from ..._exceptions import APIStatusError
from ..._base_client import DEFAULT_MAX_RETRIES, BaseClient, SyncAPIClient, AsyncAPIClient, FinalRequestOptions
from ._stream_decoder import AWSEventStreamDecoder
from ...resources.messages import Messages, AsyncMessages
from ...resources.completions import Completions, AsyncCompletions

DEFAULT_VERSION = "bedrock-2023-05-31"

_HttpxClientT = TypeVar("_HttpxClientT", bound=Union[httpx.Client, httpx.AsyncClient])
_DefaultStreamT = TypeVar("_DefaultStreamT", bound=Union[Stream[Any], AsyncStream[Any]])


class BaseBedrockClient(BaseClient[_HttpxClientT, _DefaultStreamT]):
    @override
    def _build_request(
        self,
        options: FinalRequestOptions,
    ) -> httpx.Request:
        if is_dict(options.json_data):
            options.json_data.setdefault("anthropic_version", DEFAULT_VERSION)

        if options.url in {"/v1/complete", "/v1/messages"} and options.method == "post":
            if not is_dict(options.json_data):
                raise RuntimeError("Expected dictionary json_data for post /completions endpoint")

            model = options.json_data.pop("model", None)
            stream = options.json_data.pop("stream", False)
            if stream:
                options.url = f"/model/{model}/invoke-with-response-stream"
            else:
                options.url = f"/model/{model}/invoke"

        return super()._build_request(options)

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

        if response.status_code == 422:
            return _exceptions.UnprocessableEntityError(err_msg, response=response, body=body)

        if response.status_code == 429:
            return _exceptions.RateLimitError(err_msg, response=response, body=body)

        if response.status_code >= 500:
            return _exceptions.InternalServerError(err_msg, response=response, body=body)
        return APIStatusError(err_msg, response=response, body=body)


class AnthropicBedrock(BaseBedrockClient[httpx.Client, Stream[Any]], SyncAPIClient):
    messages: Messages
    completions: Completions

    def __init__(
        self,
        aws_secret_key: str | None = None,
        aws_access_key: str | None = None,
        aws_region: str | None = None,
        aws_session_token: str | None = None,
        base_url: str | httpx.URL | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        max_retries: int = DEFAULT_MAX_RETRIES,
        default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        # Configure a custom httpx client. See the [httpx documentation](https://www.python-httpx.org/api/#client) for more details.
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
    ) -> None:
        self.aws_secret_key = aws_secret_key

        self.aws_access_key = aws_access_key

        if aws_region is None:
            aws_region = os.environ.get("AWS_REGION") or "us-east-1"
        self.aws_region = aws_region

        self.aws_session_token = aws_session_token

        if base_url is None:
            base_url = os.environ.get("ANTHROPIC_BEDROCK_BASE_URL")
        if base_url is None:
            base_url = f"https://bedrock-runtime.{self.aws_region}.amazonaws.com"

        super().__init__(
            version=__version__,
            base_url=base_url,
            timeout=timeout,
            max_retries=max_retries,
            custom_headers=default_headers,
            custom_query=default_query,
            http_client=http_client,
            _strict_response_validation=_strict_response_validation,
        )

        self.messages = Messages(self)
        self.completions = Completions(self)

    @override
    def _make_sse_decoder(self) -> AWSEventStreamDecoder:
        return AWSEventStreamDecoder()

    @override
    def _prepare_request(self, request: httpx.Request) -> None:
        from ._auth import get_auth_headers

        data = request.read().decode()

        headers = get_auth_headers(
            method=request.method,
            url=str(request.url),
            headers=request.headers,
            aws_access_key=self.aws_access_key,
            aws_secret_key=self.aws_secret_key,
            aws_session_token=self.aws_session_token,
            region=self.aws_region or "us-east-1",
            data=data,
        )
        request.headers.update(headers)


class AsyncAnthropicBedrock(BaseBedrockClient[httpx.AsyncClient, AsyncStream[Any]], AsyncAPIClient):
    messages: AsyncMessages
    completions: AsyncCompletions

    def __init__(
        self,
        aws_secret_key: str | None = None,
        aws_access_key: str | None = None,
        aws_region: str | None = None,
        aws_session_token: str | None = None,
        base_url: str | httpx.URL | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        max_retries: int = DEFAULT_MAX_RETRIES,
        default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        # Configure a custom httpx client. See the [httpx documentation](https://www.python-httpx.org/api/#client) for more details.
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
    ) -> None:
        self.aws_secret_key = aws_secret_key

        self.aws_access_key = aws_access_key

        if aws_region is None:
            aws_region = os.environ.get("AWS_REGION") or "us-east-1"
        self.aws_region = aws_region

        self.aws_session_token = aws_session_token

        if base_url is None:
            base_url = os.environ.get("ANTHROPIC_BEDROCK_BASE_URL")
        if base_url is None:
            base_url = f"https://bedrock-runtime.{self.aws_region}.amazonaws.com"

        super().__init__(
            version=__version__,
            base_url=base_url,
            timeout=timeout,
            max_retries=max_retries,
            custom_headers=default_headers,
            custom_query=default_query,
            http_client=http_client,
            _strict_response_validation=_strict_response_validation,
        )

        self.messages = AsyncMessages(self)
        self.completions = AsyncCompletions(self)

    @override
    def _make_sse_decoder(self) -> AWSEventStreamDecoder:
        return AWSEventStreamDecoder()

    @override
    async def _prepare_request(self, request: httpx.Request) -> None:
        from ._auth import get_auth_headers

        data = request.read().decode()

        headers = get_auth_headers(
            method=request.method,
            url=str(request.url),
            headers=request.headers,
            aws_access_key=self.aws_access_key,
            aws_secret_key=self.aws_secret_key,
            aws_session_token=self.aws_session_token,
            region=self.aws_region or "us-east-1",
            data=data,
        )
        request.headers.update(headers)
