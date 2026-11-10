from __future__ import annotations

import os
from typing import TYPE_CHECKING, Any, Union, Mapping, TypeVar, Sequence
from typing_extensions import Self, override

import httpx2

from .._env import with_environment_headers
from ._auth import load_auth, refresh_auth
from ._beta import Beta, AsyncBeta
from ..._types import Omit, NotGiven, OpenTelemetryClientOption, not_given
from ..._utils import is_dict, asyncify, is_given, path_template, get_async_library
from ..._client import _keep_client_header_params
from ..._compat import model_copy, typed_cached_property
from ..._models import FinalRequestOptions
from ..._version import __version__
from ..._constants import ANTHROPIC_API_VERSION
from ..._streaming import Stream, AsyncStream
from ..._exceptions import AnthropicError
from ..._middleware import MiddlewareInput
from ..._base_client import (
    DEFAULT_MAX_RETRIES,
    BaseClient,
    SyncAPIClient,
    AsyncAPIClient,
)
from .._platform_client import copy_platform_client
from ...resources.messages import Messages, AsyncMessages

if TYPE_CHECKING:
    from google.auth.credentials import Credentials as GoogleCredentials  # type: ignore

_HttpxClientT = TypeVar("_HttpxClientT", bound=Union[httpx2.Client, httpx2.AsyncClient])
_DefaultStreamT = TypeVar("_DefaultStreamT", bound=Union[Stream[Any], AsyncStream[Any]])


class BaseVertexClient(BaseClient[_HttpxClientT, _DefaultStreamT]):
    _gen_ai_provider_name = "gcp.vertex_ai"
    _otel_platform = "vertex"

    @typed_cached_property
    def region(self) -> str:
        raise RuntimeError("region not set")

    @typed_cached_property
    def project_id(self) -> str | None:
        project_id = os.environ.get("ANTHROPIC_VERTEX_PROJECT_ID")
        if project_id:
            return project_id

        return None


class AnthropicVertex(BaseVertexClient[httpx2.Client, Stream[Any]], SyncAPIClient):
    messages: Messages
    beta: Beta

    def __init__(
        self,
        *,
        region: str | NotGiven = not_given,
        project_id: str | NotGiven = not_given,
        access_token: str | None = None,
        credentials: GoogleCredentials | None = None,
        base_url: str | httpx2.URL | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
        max_retries: int = DEFAULT_MAX_RETRIES,
        default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        # OpenTelemetry tracing of this client's API calls. `False` disables the spans, and
        # `traces.content_mode` set to `"content"` adds the content of requests and responses to them.
        open_telemetry: OpenTelemetryClientOption = None,
        # Configure a custom httpx client. See the [httpx documentation](https://www.python-httpx.org/api/#client) for more details.
        http_client: httpx2.Client | None = None,
        middleware: Sequence[MiddlewareInput] | None = None,
        _strict_response_validation: bool = False,
    ) -> None:
        if not is_given(region):
            region = os.environ.get("CLOUD_ML_REGION", not_given)
        if not is_given(region):
            raise ValueError(
                "No region was given. The client should be instantiated with the `region` argument or the `CLOUD_ML_REGION` environment variable should be set."
            )
        if region == "":
            raise ValueError(f"Expected a non-empty value for `region` but received {region!r}")

        if base_url is None:
            base_url = os.environ.get("ANTHROPIC_VERTEX_BASE_URL")
            if base_url is None:
                if region == "global":
                    base_url = "https://aiplatform.googleapis.com/v1"
                elif region == "us":
                    base_url = "https://aiplatform.us.rep.googleapis.com/v1"
                elif region == "eu":
                    base_url = "https://aiplatform.eu.rep.googleapis.com/v1"
                else:
                    base_url = f"https://{region}-aiplatform.googleapis.com/v1"

        super().__init__(
            version=__version__,
            base_url=base_url,
            timeout=timeout,
            max_retries=max_retries,
            open_telemetry=open_telemetry,
            custom_headers=with_environment_headers(default_headers),
            custom_query=default_query,
            http_client=http_client,
            middleware=middleware,
            _strict_response_validation=_strict_response_validation,
        )

        if is_given(project_id):
            self.project_id = project_id

        self.region = region
        self.access_token = access_token
        self.credentials = credentials

        self._default_stream_cls = Stream

        self.messages = Messages(self)
        self.beta = Beta(self)

    @property
    @override
    def default_headers(self) -> dict[str, str | Omit]:
        return {
            **super().default_headers,
            "X-Stainless-Async": "false",
            **self._custom_headers,
        }

    @override
    def _prepare_options(self, options: FinalRequestOptions) -> FinalRequestOptions:
        return _prepare_options(options, project_id=self.project_id, region=self.region)

    @override
    def _prepare_request(self, request: httpx2.Request) -> None:
        if request.headers.get("Authorization"):
            # already authenticated, nothing for us to do
            return

        request.headers["Authorization"] = f"Bearer {self._ensure_access_token()}"

    def _ensure_access_token(self) -> str:
        if self.access_token is not None:
            return self.access_token

        if not self.credentials:
            self.credentials, project_id = load_auth(project_id=self.project_id)
            if not self.project_id:
                self.project_id = project_id

        if self.credentials.expired or not self.credentials.token:
            refresh_auth(self.credentials)

        if not self.credentials.token:
            raise RuntimeError("Could not resolve API token from the environment")

        assert isinstance(self.credentials.token, str)
        return self.credentials.token

    def copy(
        self,
        *,
        region: str | NotGiven = not_given,
        project_id: str | NotGiven = not_given,
        access_token: str | None = None,
        credentials: GoogleCredentials | None = None,
        base_url: str | httpx2.URL | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
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
        return copy_platform_client(
            self,
            region=region if is_given(region) else self.region,
            project_id=project_id if is_given(project_id) else self.project_id or not_given,
            access_token=access_token or self.access_token,
            credentials=credentials or self.credentials,
            base_url=base_url or self.base_url,
            timeout=timeout,
            http_client=http_client,
            max_retries=max_retries,
            open_telemetry=open_telemetry,
            default_headers=default_headers,
            set_default_headers=set_default_headers,
            default_query=default_query,
            set_default_query=set_default_query,
            middleware=middleware,
            **_extra_kwargs,
        )

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


class AsyncAnthropicVertex(BaseVertexClient[httpx2.AsyncClient, AsyncStream[Any]], AsyncAPIClient):
    messages: AsyncMessages
    beta: AsyncBeta

    def __init__(
        self,
        *,
        region: str | NotGiven = not_given,
        project_id: str | NotGiven = not_given,
        access_token: str | None = None,
        credentials: GoogleCredentials | None = None,
        base_url: str | httpx2.URL | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
        max_retries: int = DEFAULT_MAX_RETRIES,
        default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        # OpenTelemetry tracing of this client's API calls. `False` disables the spans, and
        # `traces.content_mode` set to `"content"` adds the content of requests and responses to them.
        open_telemetry: OpenTelemetryClientOption = None,
        # Configure a custom httpx client. See the [httpx documentation](https://www.python-httpx.org/api/#client) for more details.
        http_client: httpx2.AsyncClient | None = None,
        middleware: Sequence[MiddlewareInput] | None = None,
        _strict_response_validation: bool = False,
    ) -> None:
        if not is_given(region):
            region = os.environ.get("CLOUD_ML_REGION", not_given)
        if not is_given(region):
            raise ValueError(
                "No region was given. The client should be instantiated with the `region` argument or the `CLOUD_ML_REGION` environment variable should be set."
            )
        if region == "":
            raise ValueError(f"Expected a non-empty value for `region` but received {region!r}")

        if base_url is None:
            base_url = os.environ.get("ANTHROPIC_VERTEX_BASE_URL")
            if base_url is None:
                if region == "global":
                    base_url = "https://aiplatform.googleapis.com/v1"
                elif region == "us":
                    base_url = "https://aiplatform.us.rep.googleapis.com/v1"
                elif region == "eu":
                    base_url = "https://aiplatform.eu.rep.googleapis.com/v1"
                else:
                    base_url = f"https://{region}-aiplatform.googleapis.com/v1"

        super().__init__(
            version=__version__,
            base_url=base_url,
            timeout=timeout,
            max_retries=max_retries,
            open_telemetry=open_telemetry,
            custom_headers=with_environment_headers(default_headers),
            custom_query=default_query,
            http_client=http_client,
            middleware=middleware,
            _strict_response_validation=_strict_response_validation,
        )

        if is_given(project_id):
            self.project_id = project_id

        self.region = region
        self.access_token = access_token
        self.credentials = credentials

        self._default_stream_cls = AsyncStream

        self.messages = AsyncMessages(self)
        self.beta = AsyncBeta(self)

    @property
    @override
    def default_headers(self) -> dict[str, str | Omit]:
        return {
            **super().default_headers,
            "X-Stainless-Async": f"async:{get_async_library()}",
            **self._custom_headers,
        }

    @override
    async def _prepare_options(self, options: FinalRequestOptions) -> FinalRequestOptions:
        return _prepare_options(options, project_id=self.project_id, region=self.region)

    @override
    async def _prepare_request(self, request: httpx2.Request) -> None:
        if request.headers.get("Authorization"):
            # already authenticated, nothing for us to do
            return

        request.headers["Authorization"] = f"Bearer {await self._ensure_access_token()}"

    async def _ensure_access_token(self) -> str:
        if self.access_token is not None:
            return self.access_token

        if not self.credentials:
            self.credentials, project_id = await asyncify(load_auth)(project_id=self.project_id)
            if not self.project_id:
                self.project_id = project_id

        if self.credentials.expired or not self.credentials.token:
            await asyncify(refresh_auth)(self.credentials)

        if not self.credentials.token:
            raise RuntimeError("Could not resolve API token from the environment")

        assert isinstance(self.credentials.token, str)
        return self.credentials.token

    def copy(
        self,
        *,
        region: str | NotGiven = not_given,
        project_id: str | NotGiven = not_given,
        access_token: str | None = None,
        credentials: GoogleCredentials | None = None,
        base_url: str | httpx2.URL | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
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
        return copy_platform_client(
            self,
            region=region if is_given(region) else self.region,
            project_id=project_id if is_given(project_id) else self.project_id or not_given,
            access_token=access_token or self.access_token,
            credentials=credentials or self.credentials,
            base_url=base_url or self.base_url,
            timeout=timeout,
            http_client=http_client,
            max_retries=max_retries,
            open_telemetry=open_telemetry,
            default_headers=default_headers,
            set_default_headers=set_default_headers,
            default_query=default_query,
            set_default_query=set_default_query,
            middleware=middleware,
            **_extra_kwargs,
        )

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


def _prepare_options(input_options: FinalRequestOptions, *, project_id: str | None, region: str) -> FinalRequestOptions:
    options = model_copy(_keep_client_header_params(input_options), deep=True)

    if is_dict(options.json_data):
        options.json_data.setdefault("anthropic_version", ANTHROPIC_API_VERSION)

    if options.url in {"/v1/messages", "/v1/messages?beta=true"} and options.method == "post":
        if project_id is None:
            raise RuntimeError(
                "No project_id was given and it could not be resolved from credentials. The client should be instantiated with the `project_id` argument or the `ANTHROPIC_VERTEX_PROJECT_ID` environment variable should be set."
            )

        if not is_dict(options.json_data):
            raise RuntimeError("Expected json data to be a dictionary for post /v1/messages")

        model = options.json_data.pop("model")
        stream = options.json_data.get("stream", False)
        specifier = "streamRawPredict" if stream else "rawPredict"

        path = "/projects/{project_id}/locations/{region}/publishers/anthropic/models/{model}:{specifier}"
        url = request_path(path, project_id=project_id, region=region, model=model, specifier=specifier)
        parent, _, model_segment = url.rpartition("/")
        # A server that drops `;` and the rest of its segment would drop the specifier.
        options.url = f"{parent}/{model_segment.replace(';', '%3B')}"

    if options.url in {"/v1/messages/count_tokens", "/v1/messages/count_tokens?beta=true"} and options.method == "post":
        if project_id is None:
            raise RuntimeError(
                "No project_id was given and it could not be resolved from credentials. The client should be instantiated with the `project_id` argument or the `ANTHROPIC_VERTEX_PROJECT_ID` environment variable should be set."
            )

        path = "/projects/{project_id}/locations/{region}/publishers/anthropic/models/count-tokens:rawPredict"
        options.url = request_path(path, project_id=project_id, region=region)

    if options.url.startswith("/v1/messages/batches"):
        raise AnthropicError("The Batch API is not supported in the Vertex client yet")

    return options


def request_path(template: str, /, **values: object) -> str:
    for name, value in values.items():
        if value == "":
            raise ValueError(f"Expected a non-empty value for `{name}` but received {value!r}")

    return path_template(template, **values)
