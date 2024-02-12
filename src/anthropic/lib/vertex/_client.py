from __future__ import annotations

import os
from typing import TYPE_CHECKING, Any, Union, Mapping, TypeVar
from typing_extensions import override

import httpx

from ... import _exceptions
from ._auth import load_auth, refresh_auth
from ..._types import NOT_GIVEN, NotGiven, Transport, ProxiesTypes, AsyncTransport
from ..._utils import is_dict, asyncify, is_given
from ..._compat import typed_cached_property
from ..._models import FinalRequestOptions
from ..._version import __version__
from ..._streaming import Stream, AsyncStream
from ..._exceptions import APIStatusError
from ..._base_client import DEFAULT_MAX_RETRIES, BaseClient, SyncAPIClient, AsyncAPIClient
from ...resources.messages import Messages, AsyncMessages

if TYPE_CHECKING:
    from google.auth.credentials import Credentials as GoogleCredentials  # type: ignore


DEFAULT_VERSION = "vertex-2023-10-16"
DEFAULT_BETA_TYPES = ["private-messages-testing"]

_HttpxClientT = TypeVar("_HttpxClientT", bound=Union[httpx.Client, httpx.AsyncClient])
_DefaultStreamT = TypeVar("_DefaultStreamT", bound=Union[Stream[Any], AsyncStream[Any]])


class BaseVertexClient(BaseClient[_HttpxClientT, _DefaultStreamT]):
    @override
    def _build_request(
        self,
        options: FinalRequestOptions,
    ) -> httpx.Request:
        if is_dict(options.json_data):
            options.json_data.setdefault("anthropic_version", DEFAULT_VERSION)
            options.json_data.setdefault("anthropic_beta", DEFAULT_BETA_TYPES)

        if options.url == "/v1/messages" and options.method == "post":
            project_id = self.project_id
            if project_id is None:
                raise RuntimeError(
                    "No project_id was given and it could not be resolved from credentials. The client should be instantiated with the `project_id` argument or the `ANTHROPIC_VERTEX_PROJECT_ID` environment variable should be set."
                )

            if not is_dict(options.json_data):
                raise RuntimeError("Expected json data to be a dictionary for post /v1/messages")

            model = options.json_data.pop("model")
            stream = options.json_data.get("stream", False)
            specifier = "streamRawPredict" if stream else "rawPredict"

            options.url = (
                f"/projects/{self.project_id}/locations/{self.region}/publishers/anthropic/models/{model}:{specifier}"
            )

            if is_dict(options.json_data):
                options.json_data.pop("model", None)

        return super()._build_request(options)

    @typed_cached_property
    def region(self) -> str:
        raise RuntimeError("region not set")

    @typed_cached_property
    def project_id(self) -> str | None:
        project_id = os.environ.get("ANTHROPIC_VERTEX_PROJECT_ID")
        if project_id:
            return project_id

        return None

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


class AnthropicVertex(BaseVertexClient[httpx.Client, Stream[Any]], SyncAPIClient):
    messages: Messages

    def __init__(
        self,
        *,
        region: str | NotGiven = NOT_GIVEN,
        project_id: str | NotGiven = NOT_GIVEN,
        access_token: str | None = None,
        base_url: str | httpx.URL | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        max_retries: int = DEFAULT_MAX_RETRIES,
        default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        # Configure a custom httpx client. See the [httpx documentation](https://www.python-httpx.org/api/#client) for more details.
        http_client: httpx.Client | None = None,
        # See httpx documentation for [custom transports](https://www.python-httpx.org/advanced/#custom-transports)
        transport: Transport | None = None,
        # See httpx documentation for [proxies](https://www.python-httpx.org/advanced/#http-proxying)
        proxies: ProxiesTypes | None = None,
        # See httpx documentation for [limits](https://www.python-httpx.org/advanced/#pool-limit-configuration)
        connection_pool_limits: httpx.Limits | None = None,
        _strict_response_validation: bool = False,
    ) -> None:
        if not is_given(region):
            region = os.environ.get("CLOUD_ML_REGION", NOT_GIVEN)
        if not is_given(region):
            raise ValueError(
                "No region was given. The client should be instantiated with the `region` argument or the `CLOUD_ML_REGION` environment variable should be set."
            )

        if base_url is None:
            base_url = os.environ.get("ANTHROPIC_VERTEX_BASE_URL")
            if base_url is None:
                base_url = f"https://{region}-aiplatform.googleapis.com/v1"

        super().__init__(
            version=__version__,
            base_url=base_url,
            timeout=timeout,
            max_retries=max_retries,
            custom_headers=default_headers,
            custom_query=default_query,
            http_client=http_client,
            transport=transport,
            proxies=proxies,
            limits=connection_pool_limits,
            _strict_response_validation=_strict_response_validation,
        )

        if is_given(project_id):
            self.project_id = project_id

        self.region = region
        self.access_token = access_token
        self._credentials: GoogleCredentials | None = None

        self.messages = Messages(self)

    @override
    def _prepare_request(self, request: httpx.Request) -> None:
        access_token = self._ensure_access_token()

        if request.headers.get("Authorization"):
            # already authenticated, nothing for us to do
            return

        request.headers["Authorization"] = f"Bearer {access_token}"

    def _ensure_access_token(self) -> str:
        if self.access_token is not None:
            return self.access_token

        if not self._credentials:
            self._credentials, project_id = load_auth()
            if not self.project_id:
                self.project_id = project_id
        else:
            refresh_auth(self._credentials)

        if not self._credentials.token:
            raise RuntimeError("Could not resolve API token from the environment")

        assert isinstance(self._credentials.token, str)
        return self._credentials.token


class AsyncAnthropicVertex(BaseVertexClient[httpx.AsyncClient, AsyncStream[Any]], AsyncAPIClient):
    messages: AsyncMessages

    def __init__(
        self,
        *,
        region: str | NotGiven = NOT_GIVEN,
        project_id: str | NotGiven = NOT_GIVEN,
        access_token: str | None = None,
        base_url: str | httpx.URL | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        max_retries: int = DEFAULT_MAX_RETRIES,
        default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        # Configure a custom httpx client. See the [httpx documentation](https://www.python-httpx.org/api/#client) for more details.
        http_client: httpx.AsyncClient | None = None,
        # See httpx documentation for [custom transports](https://www.python-httpx.org/advanced/#custom-transports)
        transport: AsyncTransport | None = None,
        # See httpx documentation for [proxies](https://www.python-httpx.org/advanced/#http-proxying)
        proxies: ProxiesTypes | None = None,
        # See httpx documentation for [limits](https://www.python-httpx.org/advanced/#pool-limit-configuration)
        connection_pool_limits: httpx.Limits | None = None,
        _strict_response_validation: bool = False,
    ) -> None:
        if not is_given(region):
            region = os.environ.get("CLOUD_ML_REGION", NOT_GIVEN)
        if not is_given(region):
            raise ValueError(
                "No region was given. The client should be instantiated with the `region` argument or the `CLOUD_ML_REGION` environment variable should be set."
            )

        if base_url is None:
            base_url = os.environ.get("ANTHROPIC_VERTEX_BASE_URL")
            if base_url is None:
                base_url = f"https://{region}-aiplatform.googleapis.com/v1"

        super().__init__(
            version=__version__,
            base_url=base_url,
            timeout=timeout,
            max_retries=max_retries,
            custom_headers=default_headers,
            custom_query=default_query,
            http_client=http_client,
            transport=transport,
            proxies=proxies,
            limits=connection_pool_limits,
            _strict_response_validation=_strict_response_validation,
        )

        if is_given(project_id):
            self.project_id = project_id

        self.region = region
        self.access_token = access_token
        self._credentials: GoogleCredentials | None = None

        self.messages = AsyncMessages(self)

    @override
    async def _prepare_request(self, request: httpx.Request) -> None:
        access_token = await self._ensure_access_token()

        if request.headers.get("Authorization"):
            # already authenticated, nothing for us to do
            return

        request.headers["Authorization"] = f"Bearer {access_token}"

    async def _ensure_access_token(self) -> str:
        if self.access_token is not None:
            return self.access_token

        if not self._credentials:
            self._credentials, project_id = await asyncify(load_auth)()
            if not self.project_id:
                self.project_id = project_id
        else:
            await asyncify(refresh_auth)(self._credentials)

        if not self._credentials.token:
            raise RuntimeError("Could not resolve API token from the environment")

        assert isinstance(self._credentials.token, str)
        return self._credentials.token
