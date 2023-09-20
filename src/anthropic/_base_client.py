from __future__ import annotations

import json
import time
import uuid
import inspect
import platform
from types import TracebackType
from random import random
from typing import (
    Any,
    Dict,
    Type,
    Union,
    Generic,
    Mapping,
    TypeVar,
    Iterable,
    Iterator,
    Optional,
    Generator,
    AsyncIterator,
    cast,
    overload,
)
from functools import lru_cache
from typing_extensions import Literal, get_args, get_origin

import anyio
import httpx
import distro
import pydantic
from httpx import URL, Limits
from pydantic import PrivateAttr

from . import _base_exceptions as exceptions
from ._qs import Querystring
from ._types import (
    NOT_GIVEN,
    Body,
    Omit,
    Query,
    ModelT,
    Headers,
    Timeout,
    NoneType,
    NotGiven,
    ResponseT,
    Transport,
    AnyMapping,
    ProxiesTypes,
    RequestFiles,
    RequestOptions,
    UnknownResponse,
    ModelBuilderProtocol,
)
from ._utils import is_dict, is_mapping
from ._compat import model_copy
from ._models import (
    BaseModel,
    GenericModel,
    FinalRequestOptions,
    validate_type,
    construct_type,
)
from ._streaming import Stream, AsyncStream
from ._base_exceptions import (
    APIStatusError,
    APITimeoutError,
    APIConnectionError,
    APIResponseValidationError,
)

# TODO: make base page type vars covariant
SyncPageT = TypeVar("SyncPageT", bound="BaseSyncPage[Any]")
AsyncPageT = TypeVar("AsyncPageT", bound="BaseAsyncPage[Any]")


_T = TypeVar("_T")
_T_co = TypeVar("_T_co", covariant=True)

_StreamT = TypeVar("_StreamT", bound=Stream[Any])
_AsyncStreamT = TypeVar("_AsyncStreamT", bound=AsyncStream[Any])


# default timeout is 10 minutes
DEFAULT_TIMEOUT = Timeout(timeout=600.0, connect=5.0)
DEFAULT_MAX_RETRIES = 2
DEFAULT_LIMITS = Limits(max_connections=100, max_keepalive_connections=20)


class MissingStreamClassError(TypeError):
    def __init__(self) -> None:
        super().__init__(
            "The `stream` argument was set to `True` but the `stream_cls` argument was not given. See `anthropic._streaming` for reference",
        )


class PageInfo:
    """Stores the necesary information to build the request to retrieve the next page.

    Either `url` or `params` must be set.
    """

    url: URL | NotGiven
    params: Query | NotGiven

    @overload
    def __init__(
        self,
        *,
        url: URL,
    ) -> None:
        ...

    @overload
    def __init__(
        self,
        *,
        params: Query,
    ) -> None:
        ...

    def __init__(
        self,
        *,
        url: URL | NotGiven = NOT_GIVEN,
        params: Query | NotGiven = NOT_GIVEN,
    ) -> None:
        self.url = url
        self.params = params


class BasePage(GenericModel, Generic[ModelT]):
    """
    Base class for paginated pages of data.

    Args:
        GenericModel: The base generic model class.
        Generic[ModelT]: A generic type parameter representing the model type for the page.

    Attributes:
        _options (FinalRequestOptions): The final request options.
        _model (Type[ModelT]): The type of the model.

    Methods:
        has_next_page(): Check if there is a next page of data.
        next_page_info(): Get information about the next page.
        _get_page_items(): Get the items on the current page.
        _params_from_url(url: URL): Extract query parameters from a URL and merge them with options.
        _info_to_options(info: PageInfo): Convert PageInfo to FinalRequestOptions.
    """
    _options: FinalRequestOptions = PrivateAttr()
    _model: Type[ModelT] = PrivateAttr()

    def has_next_page(self) -> bool:
        items = self._get_page_items()
        if not items:
            return False
        return self.next_page_info() is not None

    def next_page_info(self) -> Optional[PageInfo]:
        ...

    def _get_page_items(self) -> Iterable[ModelT]:  # type: ignore[empty-body]
        ...

    def _params_from_url(self, url: URL) -> httpx.QueryParams:
        # TODO: do we have to preprocess params here?
        return httpx.QueryParams(cast(Any, self._options.params)).merge(url.params)

    def _info_to_options(self, info: PageInfo) -> FinalRequestOptions:
        options = model_copy(self._options)

        if not isinstance(info.params, NotGiven):
            options.params = {**options.params, **info.params}
            return options

        if not isinstance(info.url, NotGiven):
            params = self._params_from_url(info.url)
            url = info.url.copy_with(params=params)
            options.params = dict(url.params)
            options.url = str(url)
            return options

        raise ValueError("Unexpected PageInfo state")


class BaseSyncPage(BasePage[ModelT], Generic[ModelT]):
    """
    Synchronous base class for paginated pages of data.

    Args:
        BasePage[ModelT]: The base class for paginated pages.
        Generic[ModelT]: A generic type parameter representing the model type for the page.

    Attributes:
        _client (SyncAPIClient): The synchronous API client.

    Methods:
        _set_private_attributes(client: SyncAPIClient, model: Type[ModelT], options: FinalRequestOptions):
            Set private attributes for the page.
        __iter__(): Provide iterator support for the page's items.
        iter_pages(): Iterate through pages of data.
        get_next_page(): Get the next page of data.
    """
    _client: SyncAPIClient = pydantic.PrivateAttr()

    def _set_private_attributes(
        self,
        client: SyncAPIClient,
        model: Type[ModelT],
        options: FinalRequestOptions,
    ) -> None:
        self._model = model
        self._client = client
        self._options = options

    # Pydantic uses a custom `__iter__` method to support casting BaseModels
    # to dictionaries. e.g. dict(model).
    # As we want to support `for item in page`, this is inherently incompatible
    # with the default pydantic behaviour. It is not possible to support both
    # use cases at once. Fortunately, this is not a big deal as all other pydantic
    # methods should continue to work as expected as there is an alternative method
    # to cast a model to a dictionary, model.dict(), which is used internally
    # by pydantic.
    def __iter__(self) -> Iterator[ModelT]:  # type: ignore
        for page in self.iter_pages():
            for item in page._get_page_items():
                yield item

    def iter_pages(self: SyncPageT) -> Iterator[SyncPageT]:
        page = self
        while True:
            yield page
            if page.has_next_page():
                page = page.get_next_page()
            else:
                return

    def get_next_page(self: SyncPageT) -> SyncPageT:
        info = self.next_page_info()
        if not info:
            raise RuntimeError(
                "No next page expected; please check `.has_next_page()` before calling `.get_next_page()`."
            )

        options = self._info_to_options(info)
        return self._client._request_api_list(self._model, page=self.__class__, options=options)


class AsyncPaginator(Generic[ModelT, AsyncPageT]):
    """
    Asynchronous paginator for retrieving paginated data.

    Args:
        client (AsyncAPIClient): The asynchronous API client.
        options (FinalRequestOptions): The final request options for retrieving data.
        page_cls (Type[AsyncPageT]): The type of the asynchronous page containing paginated data.
        model (Type[ModelT]): The model type for the data.

    Attributes:
        _model (Type[ModelT]): The model type for the data.
        _client (AsyncAPIClient): The asynchronous API client.
        _options (FinalRequestOptions): The final request options for retrieving data.
        _page_cls (Type[AsyncPageT]): The type of the asynchronous page containing paginated data.

    """

    def __init__(
        self,
        client: AsyncAPIClient,
        options: FinalRequestOptions,
        page_cls: Type[AsyncPageT],
        model: Type[ModelT],
    ) -> None:
        """
        Initialize the AsyncPaginator instance.

        Args:
            client (AsyncAPIClient): The asynchronous API client.
            options (FinalRequestOptions): The final request options for retrieving data.
            page_cls (Type[AsyncPageT]): The type of the asynchronous page containing paginated data.
            model (Type[ModelT]): The model type for the data.

        """
        self._model = model
        self._client = client
        self._options = options
        self._page_cls = page_cls

    async def _get_page(self) -> AsyncPageT:
        """
        Internal method to retrieve an asynchronous page containing paginated data.

        Returns:
            AsyncPageT: An asynchronous page with paginated data.

        """
        page = await self._client.request(self._page_cls, self._options)
        page._set_private_attributes(  # pyright: ignore[reportPrivateUsage]
            model=self._model,
            options=self._options,
            client=self._client,
        )
        return page

    async def __aiter__(self) -> AsyncIterator[ModelT]:
        """
        Asynchronously iterate over the paginated data.

        Yields:
            ModelT: An item from the paginated data.

        """
        # https://github.com/microsoft/pyright/issues/3464
        page = cast(
            AsyncPageT,
            await self,  # type: ignore
        )
        async for item in page:
            yield item

    def __await__(self) -> Generator[Any, None, AsyncPageT]:
        """
        Asynchronously retrieve an asynchronous page containing paginated data.

        Returns:
            Generator[Any, None, AsyncPageT]: A generator yielding an asynchronous page with paginated data.

        """
        return self._get_page().__await__()


class BaseAsyncPage(BasePage[ModelT], Generic[ModelT]):
    """
    Asynchronous paginator for retrieving paginated data.

    Args:
        client (AsyncAPIClient): The asynchronous API client.
        options (FinalRequestOptions): The final request options.
        page_cls (Type[AsyncPageT]): The class representing the asynchronous paginated page.
        model (Type[ModelT]): The model type for the paginated data.

    Methods:
        __await__(): Asynchronously retrieve the paginated page.
        _get_page(): Asynchronously fetch and configure the paginated page.
        __aiter__(): Asynchronously iterate through the items in the paginated data.
    """
    _client: AsyncAPIClient = pydantic.PrivateAttr()

    def _set_private_attributes(
        self,
        model: Type[ModelT],
        client: AsyncAPIClient,
        options: FinalRequestOptions,
    ) -> None:
        self._model = model
        self._client = client
        self._options = options

    async def __aiter__(self) -> AsyncIterator[ModelT]:
        async for page in self.iter_pages():
            for item in page._get_page_items():
                yield item

    async def iter_pages(self: AsyncPageT) -> AsyncIterator[AsyncPageT]:
        page = self
        while True:
            yield page
            if page.has_next_page():
                page = await page.get_next_page()
            else:
                return

    async def get_next_page(self: AsyncPageT) -> AsyncPageT:
        info = self.next_page_info()
        if not info:
            raise RuntimeError(
                "No next page expected; please check `.has_next_page()` before calling `.get_next_page()`."
            )

        options = self._info_to_options(info)
        return await self._client._request_api_list(self._model, page=self.__class__, options=options)


class BaseClient:
    """
    Base client for making HTTP requests to an API.

    Args:
        version (str): The version of the API being used.
        _strict_response_validation (bool): Whether strict response validation is enabled.
        max_retries (int, optional): The maximum number of retries for failed requests.
        timeout (float or Timeout or None, optional): The timeout for each HTTP request.
        limits (Limits): The HTTP limits configuration for the client.
        custom_headers (Mapping[str, str] or None, optional): Custom headers to include in requests.
        custom_query (Mapping[str, object] or None, optional): Custom query parameters to include in requests.

    Attributes:
        _version (str): The version of the API being used.
        max_retries (int): The maximum number of retries for failed requests.
        timeout (float or Timeout or None): The timeout for each HTTP request.
        _limits (Limits): The HTTP limits configuration for the client.
        _custom_headers (dict[str, str]): Custom headers to include in requests.
        _custom_query (dict[str, object]): Custom query parameters to include in requests.
        _strict_response_validation (bool): Whether strict response validation is enabled.
        _idempotency_header (str or None): Header for idempotent requests.

    """
    _client: httpx.Client | httpx.AsyncClient
    _version: str
    max_retries: int
    timeout: Union[float, Timeout, None]
    _limits: httpx.Limits
    _strict_response_validation: bool
    _idempotency_header: str | None

    def __init__(
        self,
        *,
        version: str,
        _strict_response_validation: bool,
        max_retries: int = DEFAULT_MAX_RETRIES,
        timeout: float | Timeout | None = DEFAULT_TIMEOUT,
        limits: httpx.Limits,
        custom_headers: Mapping[str, str] | None = None,
        custom_query: Mapping[str, object] | None = None,
    ) -> None:
        """
        Initialize the BaseClient instance.

        Args:
            version (str): The version of the API being used.
            _strict_response_validation (bool): Whether strict response validation is enabled.
            max_retries (int, optional): The maximum number of retries for failed requests.
            timeout (float or Timeout or None, optional): The timeout for each HTTP request.
            limits (Limits): The HTTP limits configuration for the client.
            custom_headers (Mapping[str, str] or None, optional): Custom headers to include in requests.
            custom_query (Mapping[str, object] or None, optional): Custom query parameters to include in requests.

        """
        self._version = version
        self.max_retries = max_retries
        self.timeout = timeout
        self._limits = limits
        self._custom_headers = custom_headers or {}
        self._custom_query = custom_query or {}
        self._strict_response_validation = _strict_response_validation
        self._idempotency_header = None

    def _make_status_error_from_response(
        self,
        request: httpx.Request,
        response: httpx.Response,
    ) -> APIStatusError:
        """
        Create an APIStatusError from an HTTP response.

        Args:
            request (httpx.Request): The HTTP request.
            response (httpx.Response): The HTTP response.

        Returns:
            APIStatusError: An APIStatusError object representing the error.

        """
        err_text = response.text.strip()
        body = err_text

        try:
            body = json.loads(err_text)
            err_msg = f"Error code: {response.status_code} - {body}"
        except Exception:
            err_msg = err_text or f"Error code: {response.status_code}"

        return self._make_status_error(err_msg, body=body, request=request, response=response)

    def _make_status_error(
        self,
        err_msg: str,
        *,
        body: object,
        request: httpx.Request,
        response: httpx.Response,
    ) -> APIStatusError:
        """
        Create an APIStatusError with the provided error message and details.

        Args:
            err_msg (str): The error message.
            body (object): The response body.
            request (httpx.Request): The HTTP request.
            response (httpx.Response): The HTTP response.

        Returns:
            APIStatusError: An APIStatusError object representing the error.

        """
        if response.status_code == 400:
            return exceptions.BadRequestError(err_msg, request=request, response=response, body=body)
        if response.status_code == 401:
            return exceptions.AuthenticationError(err_msg, request=request, response=response, body=body)
        if response.status_code == 403:
            return exceptions.PermissionDeniedError(err_msg, request=request, response=response, body=body)
        if response.status_code == 404:
            return exceptions.NotFoundError(err_msg, request=request, response=response, body=body)
        if response.status_code == 409:
            return exceptions.ConflictError(err_msg, request=request, response=response, body=body)
        if response.status_code == 422:
            return exceptions.UnprocessableEntityError(err_msg, request=request, response=response, body=body)
        if response.status_code == 429:
            return exceptions.RateLimitError(err_msg, request=request, response=response, body=body)
        if response.status_code >= 500:
            return exceptions.InternalServerError(err_msg, request=request, response=response, body=body)
        return APIStatusError(err_msg, request=request, response=response, body=body)

    def _remaining_retries(
        self,
        remaining_retries: Optional[int],
        options: FinalRequestOptions,
    ) -> int:
        """
        Get the number of remaining retries for a request.

        Args:
            remaining_retries (int or None, optional): The remaining retries.
            options (FinalRequestOptions): The request options.

        Returns:
            int: The number of remaining retries.

        """
        return remaining_retries if remaining_retries is not None else options.get_max_retries(self.max_retries)

    def _build_headers(self, options: FinalRequestOptions) -> httpx.Headers:
        """
        Build the HTTP headers for a request.

        Args:
            options (FinalRequestOptions): The request options.

        Returns:
            httpx.Headers: The HTTP headers.

        """
        custom_headers = options.headers or {}
        headers_dict = _merge_mappings(self.default_headers, custom_headers)
        self._validate_headers(headers_dict, custom_headers)

        headers = httpx.Headers(headers_dict)

        idempotency_header = self._idempotency_header
        if idempotency_header and options.method.lower() != "get" and idempotency_header not in headers:
            if not options.idempotency_key:
                options.idempotency_key = self._idempotency_key()

            headers[idempotency_header] = options.idempotency_key

        return headers

    def _prepare_request(self, request: httpx.Request) -> None:
        """This method is used as a callback for mutating the `Request` object
        after it has been constructed.

        This is useful for cases where you want to add certain headers based off of
        the request properties, e.g. `url`, `method` etc.
        """
        return None

    def _build_request(
        self,
        options: FinalRequestOptions,
    ) -> httpx.Request:
        """
        Build an HTTP request.

        Args:
            options (FinalRequestOptions): The request options.

        Returns:
            httpx.Request: The HTTP request.

        """
        headers = self._build_headers(options)

        kwargs: dict[str, Any] = {}

        json_data = options.json_data
        if options.extra_json is not None:
            if json_data is None:
                json_data = cast(Body, options.extra_json)
            elif is_mapping(json_data):
                json_data = _merge_mappings(json_data, options.extra_json)
            else:
                raise RuntimeError(
                    f"Unexpected JSON data type, {type(json_data)}, cannot merge with `extra_body`")

        params = _merge_mappings(self._custom_query, options.params)

        # If the given Content-Type header is multipart/form-data then it
        # has to be removed so that httpx can generate the header with
        # additional information for us as it has to be in this form
        # for the server to be able to correctly parse the request:
        # multipart/form-data; boundary=---abc--
        if headers.get("Content-Type") == "multipart/form-data":
            headers.pop("Content-Type")

            # As we are now sending multipart/form-data instead of application/json
            # we need to tell httpx to use it, https://www.python-httpx.org/advanced/#multipart-file-encoding
            if json_data:
                if not is_dict(json_data):
                    raise TypeError(
                        f"Expected query input to be a dictionary for multipart requests but got {type(json_data)} instead."
                    )
                kwargs["data"] = self._serialize_multipartform(json_data)

        # TODO: report this error to httpx
        request = self._client.build_request(  # pyright: ignore[reportUnknownMemberType]
            headers=headers,
            timeout=self.timeout if isinstance(
                options.timeout, NotGiven) else options.timeout,
            method=options.method,
            url=options.url,
            # the `Query` type that we use is incompatible with qs'
            # `Params` type as it needs to be typed as `Mapping[str, object]`
            # so that passing a `TypedDict` doesn't cause an error.
            # https://github.com/microsoft/pyright/issues/3526#event-6715453066
            params=self.qs.stringify(
                cast(Mapping[str, Any], params)) if params else None,
            json=json_data,
            files=options.files,
            **kwargs,
        )
        self._prepare_request(request)
        return request

    def _serialize_multipartform(self, data: Mapping[object, object]) -> dict[str, object]:
        """
        Serialize data for a multipart form request.

        Args:
            data (Mapping[object, object]): The data to be serialized.

        Returns:
            dict[str, object]: The serialized data.

        Raises:
            ValueError: If a duplicate key is encountered.

        """
        items = self.qs.stringify_items(
            # TODO: type ignore is required as stringify_items is well typed but we can't be
            # well typed without heavy validation.
            data,  # type: ignore
            array_format="brackets",
        )
        serialized: dict[str, object] = {}
        for key, value in items:
            if key in serialized:
                raise ValueError(
                    f"Duplicate key encountered: {key}; This behaviour is not supported")
            serialized[key] = value
        return serialized

    def _extract_stream_chunk_type(self, stream_cls: type) -> type:
        """
        Extract the chunk type from a stream class.

        Args:
            stream_cls (type): The stream class.

        Returns:
            type: The type of chunks in the stream.

        Raises:
            TypeError: If the stream class does not have a generic type argument.

        """
        args = get_args(stream_cls)
        if not args:
            raise TypeError(
                f"Expected stream_cls to have been given a generic type argument, e.g. Stream[Foo] but received {stream_cls}",
            )
        return cast(type, args[0])

    def _process_response(
        self,
        *,
        cast_to: Type[ResponseT],
        options: FinalRequestOptions,
        response: httpx.Response,
    ) -> ResponseT:
        """
        Process an HTTP response and cast it to the specified type.

        Args:
            cast_to (Type[ResponseT]): The type to cast the response to.
            options (FinalRequestOptions): The request options.
            response (httpx.Response): The HTTP response.

        Returns:
            ResponseT: The processed response.

        Raises:
            ValueError: If the cast_to type is invalid.
            ValueError: If the Content-Type response header is not 'application/json'.

        """
        if cast_to is NoneType:
            return cast(ResponseT, None)

        if cast_to == str:
            return cast(ResponseT, response.text)

        origin = get_origin(cast_to) or cast_to

        if inspect.isclass(origin) and issubclass(origin, httpx.Response):
            # Because of the invariance of our ResponseT TypeVar, users can subclass httpx.Response
            # and pass that class to our request functions. We cannot change the variance to be either
            # covariant or contravariant as that makes our usage of ResponseT illegal. We could construct
            # the response class ourselves but that is something that should be supported directly in httpx
            # as it would be easy to incorrectly construct the Response object due to the multitude of arguments.
            if cast_to != httpx.Response:
                raise ValueError(
                    f"Subclasses of httpx.Response cannot be passed to `cast_to`")
            return cast(ResponseT, response)

        # The check here is necessary as we are subverting the the type system
        # with casts as the relationship between TypeVars and Types are very strict
        # which means we must return *exactly* what was input or transform it in a
        # way that retains the TypeVar state. As we cannot do that in this function
        # then we have to resort to using `cast`. At the time of writing, we know this
        # to be safe as we have handled all the types that could be bound to the
        # `ResponseT` TypeVar, however if that TypeVar is ever updated in the future, then
        # this function would become unsafe but a type checker would not report an error.
        if (
            cast_to is not UnknownResponse
            and not origin is list
            and not origin is dict
            and not origin is Union
            and not issubclass(origin, BaseModel)
        ):
            raise RuntimeError(
                f"Invalid state, expected {cast_to} to be a subclass type of {BaseModel}, {dict}, {list} or {Union}."
            )

        # split is required to handle cases where additional information is included
        # in the response, e.g. application/json; charset=utf-8
        content_type, *_ = response.headers.get("content-type").split(";")
        if content_type != "application/json":
            raise ValueError(
                f"Expected Content-Type response header to be `application/json` but received {content_type} instead."
            )

        data = response.json()
        return self._process_response_data(data=data, cast_to=cast_to, response=response)

    def _process_response_data(
        self,
        *,
        data: object,
        cast_to: type[ResponseT],
        response: httpx.Response,
    ) -> ResponseT:
        """
        Process the data from an HTTP response and cast it to the specified type.

        Args:
            data (object): The response data.
            cast_to (type[ResponseT]): The type to cast the data to.
            response (httpx.Response): The HTTP response.

        Returns:
            ResponseT: The processed response data.

        """
        if data is None:
            return cast(ResponseT, None)

        if cast_to is UnknownResponse:
            return cast(ResponseT, data)

        if inspect.isclass(cast_to) and issubclass(cast_to, ModelBuilderProtocol):
            return cast(ResponseT, cast_to.build(response=response, data=data))

        if self._strict_response_validation:
            return cast(ResponseT, validate_type(type_=cast_to, value=data))

        return cast(ResponseT, construct_type(type_=cast_to, value=data))

    @property
    def qs(self) -> Querystring:
        """
        Get the query string object for building query parameters.

        Returns:
            Querystring: The query string object.

        """
        return Querystring()

    @property
    def custom_auth(self) -> httpx.Auth | None:
        """
        Get the custom authentication method.

        Returns:
            httpx.Auth | None: The custom authentication method or None if not defined.

        """
        return None

    @property
    def auth_headers(self) -> dict[str, str]:
        """
        Get the authentication headers.

        Returns:
            dict[str, str]: The authentication headers.

        """
        return {}

    @property
    def default_headers(self) -> dict[str, str | Omit]:
        """
        Get the default headers for HTTP requests.

        Returns:
            dict[str, str | Omit]: The default headers.

        """
        return {
            "Content-Type": "application/json",
            "User-Agent": self.user_agent,
            **self.platform_headers(),
            **self.auth_headers,
            **self._custom_headers,
        }

    def _validate_headers(self, headers: Headers, custom_headers: Headers) -> None:
        """
        Validate the given default headers and custom headers.

        Args:
            headers (Headers): The default headers.
            custom_headers (Headers): The custom headers.

        Does nothing by default.

        """
        return

    @property
    def user_agent(self) -> str:
        """
        Get the user agent string for the client.

        Returns:
            str: The user agent string.

        """
        return f"{self.__class__.__name__}/Python {self._version}"

    @property
    def base_url(self) -> URL:
        """
        Get the base URL for the HTTP client.

        Returns:
            URL: The base URL.

        """
        return self._client.base_url

    @lru_cache(maxsize=None)
    def platform_headers(self) -> Dict[str, str]:
        """
        Get platform-specific headers.

        Returns:
            Dict[str, str]: Platform-specific headers.

        """
        return {
            "X-Stainless-Lang": "python",
            "X-Stainless-Package-Version": self._version,
            "X-Stainless-OS": str(get_platform()),
            "X-Stainless-Arch": str(get_architecture()),
            "X-Stainless-Runtime": platform.python_implementation(),
            "X-Stainless-Runtime-Version": platform.python_version(),
        }

    def _calculate_retry_timeout(
        self,
        remaining_retries: int,
        options: FinalRequestOptions,
        response_headers: Optional[httpx.Headers] = None,
    ) -> float:
        """
        Calculate the retry timeout for failed requests.

        Args:
            remaining_retries (int): The number of remaining retries.
            options (FinalRequestOptions): The request options.
            response_headers (httpx.Headers, optional): The response headers.

        Returns:
            float: The retry timeout.

        """
        max_retries = options.get_max_retries(self.max_retries)
        try:
            # About the Retry-After header: https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Retry-After
            #
            # TODO: we may want to handle the case where the header is using the http-date syntax: "Retry-After:
            # <http-date>". See https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Retry-After#syntax for
            # details.
            retry_after = - \
                1 if response_headers is None else int(
                    response_headers.get("retry-after"))
        except Exception:
            retry_after = -1

        # If the API asks us to wait a certain amount of time (and it's a reasonable amount), just do what it says.
        if 0 < retry_after <= 60:
            return retry_after

        initial_retry_delay = 0.5
        max_retry_delay = 2.0
        nb_retries = max_retries - remaining_retries

        # Apply exponential backoff, but not more than the max.
        sleep_seconds = min(initial_retry_delay *
                            pow(nb_retries - 1, 2), max_retry_delay)

        # Apply some jitter, plus-or-minus half a second.
        jitter = random() - 0.5
        timeout = sleep_seconds + jitter
        return timeout if timeout >= 0 else 0

    def _should_retry(self, response: httpx.Response) -> bool:
        """
        Determine whether a failed request should be retried.

        Args:
            response (httpx.Response): The HTTP response.

        Returns:
            bool: True if the request should be retried, False otherwise.

        """
        # Note: this is not a standard header
        should_retry_header = response.headers.get("x-should-retry")

        # If the server explicitly says whether or not to retry, obey.
        if should_retry_header == "true":
            return True
        if should_retry_header == "false":
            return False

        # Retry on lock timeouts.
        if response.status_code == 409:
            return True

        # Retry on rate limits.
        if response.status_code == 429:
            return True

        # Retry internal errors.
        if response.status_code >= 500:
            return True

        return False

    def _idempotency_key(self) -> str:
        """
        Generate an idempotency key for requests.

        Returns:
            str: The idempotency key.

        """
        return f"stainless-python-retry-{uuid.uuid4()}"


class SyncAPIClient(BaseClient):
    """
    Synchronous API client based on `BaseClient`.

    This class extends `BaseClient` to provide synchronous API request methods.

    Args:
        version (str): The API version.
        base_url (str): The base URL for API requests.
        max_retries (int, optional): The maximum number of retries for failed requests.
        timeout (float | Timeout | None, optional): The request timeout.
        transport (Transport | None, optional): The HTTP transport layer.
        proxies (ProxiesTypes | None, optional): Proxies configuration for HTTP requests.
        limits (Limits | None, optional): Request rate limiting configuration.
        custom_headers (Mapping[str, str] | None, optional): Custom headers to include in requests.
        custom_query (Mapping[str, object] | None, optional): Custom query parameters for requests.
        _strict_response_validation (bool): Whether to perform strict response validation.

    Attributes:
        _client (httpx.Client): The underlying HTTPX client instance.
        _default_stream_cls (type[Stream[Any]] | None): The default stream class for streamed responses.

    Methods:
        is_closed(): Check if the underlying HTTPX client is closed.
        close(): Close the underlying HTTPX client.
        request(): Perform an API request, with optional streaming support.
        _request(): Internal method to handle API requests and retries.
        _retry_request(): Retry an API request with appropriate delay.
        _request_api_list(): Request an API list resource.
        get(): Perform a GET request.
        post(): Perform a POST request.
        patch(): Perform a PATCH request.
        put(): Perform a PUT request.
        delete(): Perform a DELETE request.
        get_api_list(): Get a list resource from the API.
    """

    _client: httpx.Client
    _default_stream_cls: type[Stream[Any]] | None = None

    def __init__(
        self,
        *,
        version: str,
        base_url: str,
        max_retries: int = DEFAULT_MAX_RETRIES,
        timeout: float | Timeout | None = DEFAULT_TIMEOUT,
        transport: Transport | None = None,
        proxies: ProxiesTypes | None = None,
        limits: Limits | None = DEFAULT_LIMITS,
        custom_headers: Mapping[str, str] | None = None,
        custom_query: Mapping[str, object] | None = None,
        _strict_response_validation: bool,
    ) -> None:
        limits = limits or DEFAULT_LIMITS
        super().__init__(
            version=version,
            limits=limits,
            timeout=timeout,
            max_retries=max_retries,
            custom_query=custom_query,
            custom_headers=custom_headers,
            _strict_response_validation=_strict_response_validation,
        )
        self._client = httpx.Client(
            base_url=base_url,
            timeout=timeout,
            proxies=proxies,  # type: ignore
            transport=transport,  # type: ignore
            limits=limits,
            headers={"Accept": "application/json"},
        )

    def is_closed(self) -> bool:
        """
        Check if the underlying HTTPX client is closed.

        Returns:
            bool: True if the client is closed, False otherwise.
        """
        return self._client.is_closed

    def close(self) -> None:
        """
        Close the underlying HTTPX client.

        The client will not be usable after this.
        """
        self._client.close()

    def __enter__(self: _T) -> _T:
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        self.close()

    @overload
    def request(
        self,
        cast_to: Type[ResponseT],
        options: FinalRequestOptions,
        remaining_retries: Optional[int] = None,
        *,
        stream: Literal[True],
        stream_cls: Type[_StreamT],
    ) -> _StreamT:
        ...

    @overload
    def request(
        self,
        cast_to: Type[ResponseT],
        options: FinalRequestOptions,
        remaining_retries: Optional[int] = None,
        *,
        stream: Literal[False] = False,
    ) -> ResponseT:
        ...

    @overload
    def request(
        self,
        cast_to: Type[ResponseT],
        options: FinalRequestOptions,
        remaining_retries: Optional[int] = None,
        *,
        stream: bool = False,
        stream_cls: Type[_StreamT] | None = None,
    ) -> ResponseT | _StreamT:
        ...

    def request(
        self,
        cast_to: Type[ResponseT],
        options: FinalRequestOptions,
        remaining_retries: Optional[int] = None,
        *,
        stream: bool = False,
        stream_cls: type[_StreamT] | None = None,
    ) -> ResponseT | _StreamT:
        """
        Perform an API request.

        This method can perform both synchronous and streaming requests based on the 'stream' parameter.

        Args:
            ... (various): Request parameters, see class docstring for details.

        Returns:
            ResponseT | _StreamT: The API response or a stream, depending on the request type.
        """
        return self._request(
            cast_to=cast_to,
            options=options,
            stream=stream,
            stream_cls=stream_cls,
            remaining_retries=remaining_retries,
        )

    def _request(
        self,
        *,
        cast_to: Type[ResponseT],
        options: FinalRequestOptions,
        remaining_retries: int | None,
        stream: bool,
        stream_cls: type[_StreamT] | None,
    ) -> ResponseT | _StreamT:
        """
        Internal method to handle API requests and retries.

        Args:
            ... (various): Request parameters, see class docstring for details.

        Returns:
            ResponseT | _StreamT: The API response or a stream, depending on the request type.
        """
        retries = self._remaining_retries(remaining_retries, options)
        request = self._build_request(options)

        try:
            response = self._client.send(
                request, auth=self.custom_auth, stream=stream)
            response.raise_for_status()
        except httpx.HTTPStatusError as err:  # thrown on 4xx and 5xx status code
            if retries > 0 and self._should_retry(err.response):
                return self._retry_request(
                    options,
                    cast_to,
                    retries,
                    err.response.headers,
                    stream=stream,
                    stream_cls=stream_cls,
                )

            # If the response is streamed then we need to explicitly read the response
            # to completion before attempting to access the response text.
            err.response.read()
            raise self._make_status_error_from_response(
                request, err.response) from None
        except httpx.TimeoutException as err:
            if retries > 0:
                return self._retry_request(options, cast_to, retries, stream=stream, stream_cls=stream_cls)
            raise APITimeoutError(request=request) from err
        except Exception as err:
            if retries > 0:
                return self._retry_request(options, cast_to, retries, stream=stream, stream_cls=stream_cls)
            raise APIConnectionError(request=request) from err

        if stream:
            if stream_cls:
                return stream_cls(cast_to=self._extract_stream_chunk_type(stream_cls), response=response, client=self)

            stream_cls = cast("type[_StreamT] | None",
                              self._default_stream_cls)
            if stream_cls is None:
                raise MissingStreamClassError()
            return stream_cls(cast_to=cast_to, response=response, client=self)

        try:
            rsp = self._process_response(
                cast_to=cast_to, options=options, response=response)
        except pydantic.ValidationError as err:
            raise APIResponseValidationError(
                request=request, response=response) from err

        return rsp

    def _retry_request(
        self,
        options: FinalRequestOptions,
        cast_to: Type[ResponseT],
        remaining_retries: int,
        response_headers: Optional[httpx.Headers] = None,
        *,
        stream: bool,
        stream_cls: type[_StreamT] | None,
    ) -> ResponseT | _StreamT:
        """
        Retry an API request with an appropriate delay.

        Args:
            ... (various): Request parameters, see class docstring for details.

        Returns:
            ResponseT | _StreamT: The API response or a stream, depending on the request type.
        """
        remaining = remaining_retries - 1
        timeout = self._calculate_retry_timeout(
            remaining, options, response_headers)

        # In a synchronous context we are blocking the entire thread. Up to the library user to run the client in a
        # different thread if necessary.
        time.sleep(timeout)

        return self._request(
            options=options,
            cast_to=cast_to,
            remaining_retries=remaining,
            stream=stream,
            stream_cls=stream_cls,
        )

    def _request_api_list(
        self,
        model: Type[ModelT],
        page: Type[SyncPageT],
        options: FinalRequestOptions,
    ) -> SyncPageT:
        """
        Request an API list resource.

        Args:
            ... (various): Request parameters, see class docstring for details.

        Returns:
            SyncPageT: The API list response.
        """

        resp = self.request(page, options, stream=False)
        resp._set_private_attributes(  # pyright: ignore[reportPrivateUsage]
            client=self,
            model=model,
            options=options,
        )
        return resp

    @overload
    def get(
        self,
        path: str,
        *,
        cast_to: Type[ResponseT],
        options: RequestOptions = {},
        stream: Literal[False] = False,
    ) -> ResponseT:
        ...

    @overload
    def get(
        self,
        path: str,
        *,
        cast_to: Type[ResponseT],
        options: RequestOptions = {},
        stream: Literal[True],
        stream_cls: type[_StreamT],
    ) -> _StreamT:
        ...

    @overload
    def get(
        self,
        path: str,
        *,
        cast_to: Type[ResponseT],
        options: RequestOptions = {},
        stream: bool,
        stream_cls: type[_StreamT] | None = None,
    ) -> ResponseT | _StreamT:
        ...

    def get(
        self,
        path: str,
        *,
        cast_to: Type[ResponseT],
        options: RequestOptions = {},
        stream: bool = False,
        stream_cls: type[_StreamT] | None = None,
    ) -> ResponseT | _StreamT:
        """
        Perform a GET request.

        Returns:
            ResponseT | _StreamT: The GET request response.
        """

        opts = FinalRequestOptions.construct(method="get", url=path, **options)
        # cast is required because mypy complains about returning Any even though
        # it understands the type variables
        return cast(ResponseT, self.request(cast_to, opts, stream=stream, stream_cls=stream_cls))

    @overload
    def post(
        self,
        path: str,
        *,
        cast_to: Type[ResponseT],
        body: Body | None = None,
        options: RequestOptions = {},
        files: RequestFiles | None = None,
        stream: Literal[False] = False,
    ) -> ResponseT:
        """
        Perform a POST request.

        Returns:
            ResponseT | _StreamT: The POST request response.
        """
        ...

    @overload
    def post(
        self,
        path: str,
        *,
        cast_to: Type[ResponseT],
        body: Body | None = None,
        options: RequestOptions = {},
        files: RequestFiles | None = None,
        stream: Literal[True],
        stream_cls: type[_StreamT],
    ) -> _StreamT:
        ...

    @overload
    def post(
        self,
        path: str,
        *,
        cast_to: Type[ResponseT],
        body: Body | None = None,
        options: RequestOptions = {},
        files: RequestFiles | None = None,
        stream: bool,
        stream_cls: type[_StreamT] | None = None,
    ) -> ResponseT | _StreamT:
        ...

    def post(
        self,
        path: str,
        *,
        cast_to: Type[ResponseT],
        body: Body | None = None,
        options: RequestOptions = {},
        files: RequestFiles | None = None,
        stream: bool = False,
        stream_cls: type[_StreamT] | None = None,
    ) -> ResponseT | _StreamT:
        opts = FinalRequestOptions.construct(
            method="post", url=path, json_data=body, files=files, **options)
        return cast(ResponseT, self.request(cast_to, opts, stream=stream, stream_cls=stream_cls))

    def patch(
        self,
        path: str,
        *,
        cast_to: Type[ResponseT],
        body: Body | None = None,
        options: RequestOptions = {},
    ) -> ResponseT:
        """
        Perform a PATCH request.

        Returns:
            ResponseT: The PATCH request response.
        """
        opts = FinalRequestOptions.construct(
            method="patch", url=path, json_data=body, **options)
        return self.request(cast_to, opts)

    def put(
        self,
        path: str,
        *,
        cast_to: Type[ResponseT],
        body: Body | None = None,
        files: RequestFiles | None = None,
        options: RequestOptions = {},
    ) -> ResponseT:
        """
        Perform a PUT request.

        Returns:
            ResponseT: The PUT request response.
        """

        opts = FinalRequestOptions.construct(
            method="put", url=path, json_data=body, files=files, **options)
        return self.request(cast_to, opts)

    def delete(
        self,
        path: str,
        *,
        cast_to: Type[ResponseT],
        body: Body | None = None,
        options: RequestOptions = {},
    ) -> ResponseT:
        """
        Perform a DELETE request.

        Returns:
            ResponseT: The DELETE request response.
        """
        opts = FinalRequestOptions.construct(
            method="delete", url=path, json_data=body, **options)
        return self.request(cast_to, opts)

    def get_api_list(
        self,
        path: str,
        *,
        model: Type[ModelT],
        page: Type[SyncPageT],
        body: Body | None = None,
        options: RequestOptions = {},
        method: str = "get",
    ) -> SyncPageT:
        """
        Get a list resource from the API.

        Returns:
            SyncPageT: The API list response.
        """
        opts = FinalRequestOptions.construct(
            method=method, url=path, json_data=body, **options)
        return self._request_api_list(model, page, opts)


class AsyncAPIClient(BaseClient):
    """
    Asynchronous API Client for making HTTP requests.

    This client provides methods for making various HTTP requests asynchronously.

    Args:
        version (str): The API version.
        base_url (str): The base URL for the API.
        _strict_response_validation (bool): Flag to enable strict response validation.
        max_retries (int, optional): The maximum number of retries for failed requests. Defaults to DEFAULT_MAX_RETRIES.
        timeout (float | Timeout | None, optional): The request timeout. Defaults to DEFAULT_TIMEOUT.
        transport (Transport | None, optional): The HTTP transport. Defaults to None.
        proxies (ProxiesTypes | None, optional): The proxies to use. Defaults to None.
        limits (Limits | None, optional): The request rate limits. Defaults to DEFAULT_LIMITS.
        custom_headers (Mapping[str, str] | None, optional): Custom HTTP headers. Defaults to None.
        custom_query (Mapping[str, object] | None, optional): Custom query parameters. Defaults to None.
    """
    _client: httpx.AsyncClient
    _default_stream_cls: type[AsyncStream[Any]] | None = None

    def __init__(
        self,
        *,
        version: str,
        base_url: str,
        _strict_response_validation: bool,
        max_retries: int = DEFAULT_MAX_RETRIES,
        timeout: float | Timeout | None = DEFAULT_TIMEOUT,
        transport: Transport | None = None,
        proxies: ProxiesTypes | None = None,
        limits: Limits | None = DEFAULT_LIMITS,
        custom_headers: Mapping[str, str] | None = None,
        custom_query: Mapping[str, object] | None = None,
    ) -> None:
        """
        Initialize the AsyncAPIClient.

        Args:
            version (str): The API version.
            base_url (str): The base URL for the API.
            _strict_response_validation (bool): Flag to enable strict response validation.
            max_retries (int, optional): The maximum number of retries for failed requests. Defaults to DEFAULT_MAX_RETRIES.
            timeout (float | Timeout | None, optional): The request timeout. Defaults to DEFAULT_TIMEOUT.
            transport (Transport | None, optional): The HTTP transport. Defaults to None.
            proxies (ProxiesTypes | None, optional): The proxies to use. Defaults to None.
            limits (Limits | None, optional): The request rate limits. Defaults to DEFAULT_LIMITS.
            custom_headers (Mapping[str, str] | None, optional): Custom HTTP headers. Defaults to None.
            custom_query (Mapping[str, object] | None, optional): Custom query parameters. Defaults to None.
        """
        limits = limits or DEFAULT_LIMITS
        super().__init__(
            version=version,
            limits=limits,
            timeout=timeout,
            max_retries=max_retries,
            custom_query=custom_query,
            custom_headers=custom_headers,
            _strict_response_validation=_strict_response_validation,
        )
        self._client = httpx.AsyncClient(
            base_url=base_url,
            timeout=timeout,
            proxies=proxies,  # type: ignore
            transport=transport,  # type: ignore
            limits=limits,
            headers={"Accept": "application/json"},
        )

    def is_closed(self) -> bool:
        """
        Check if the underlying HTTPX client is closed.

        Returns:
            bool: True if the client is closed, False otherwise.
        """
        return self._client.is_closed

    async def close(self) -> None:
        """Close the underlying HTTPX client.

        The client will *not* be usable after this.
        """
        await self._client.aclose()

    async def __aenter__(self: _T) -> _T:
        """
        Asynchronous context manager entry method.
        """
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """
        Make an HTTP request asynchronously.

        Args:
            cast_to (Type[ResponseT]): The expected response type.
            options (FinalRequestOptions): The request options.
            stream (bool, optional): Whether to stream the response. Defaults to False.
            stream_cls (type[_AsyncStreamT] | None, optional): The stream class. Defaults to None.
            remaining_retries (int | None, optional): The remaining retry attempts. Defaults to None.

        Returns:
            ResponseT | _AsyncStreamT: The response or a stream, depending on the 'stream' parameter.
        """
        await self.close()

    @overload
    async def request(
        self,
        cast_to: Type[ResponseT],
        options: FinalRequestOptions,
        *,
        stream: Literal[False] = False,
        remaining_retries: Optional[int] = None,
    ) -> ResponseT:
        ...

    @overload
    async def request(
        self,
        cast_to: Type[ResponseT],
        options: FinalRequestOptions,
        *,
        stream: Literal[True],
        stream_cls: type[_AsyncStreamT],
        remaining_retries: Optional[int] = None,
    ) -> _AsyncStreamT:
        ...

    @overload
    async def request(
        self,
        cast_to: Type[ResponseT],
        options: FinalRequestOptions,
        *,
        stream: bool,
        stream_cls: type[_AsyncStreamT] | None = None,
        remaining_retries: Optional[int] = None,
    ) -> ResponseT | _AsyncStreamT:
        ...

    async def request(
        self,
        cast_to: Type[ResponseT],
        options: FinalRequestOptions,
        *,
        stream: bool = False,
        stream_cls: type[_AsyncStreamT] | None = None,
        remaining_retries: Optional[int] = None,
    ) -> ResponseT | _AsyncStreamT:
        return await self._request(
            cast_to=cast_to,
            options=options,
            stream=stream,
            stream_cls=stream_cls,
            remaining_retries=remaining_retries,
        )

    async def _request(
        self,
        cast_to: Type[ResponseT],
        options: FinalRequestOptions,
        *,
        stream: bool,
        stream_cls: type[_AsyncStreamT] | None,
        remaining_retries: int | None,
    ) -> ResponseT | _AsyncStreamT:
        """
        Internal method for making an HTTP request asynchronously.

        Args:
            cast_to (Type[ResponseT]): The expected response type.
            options (FinalRequestOptions): The request options.
            stream (bool): Whether to stream the response.
            stream_cls (type[_AsyncStreamT] | None): The stream class.
            remaining_retries (int | None): The remaining retry attempts.

        Returns:
            ResponseT | _AsyncStreamT: The response or a stream, depending on the 'stream' parameter.
        """
        retries = self._remaining_retries(remaining_retries, options)
        request = self._build_request(options)

        try:
            response = await self._client.send(request, auth=self.custom_auth, stream=stream)
            response.raise_for_status()
        except httpx.HTTPStatusError as err:  # thrown on 4xx and 5xx status code
            if retries > 0 and self._should_retry(err.response):
                return await self._retry_request(
                    options,
                    cast_to,
                    retries,
                    err.response.headers,
                    stream=stream,
                    stream_cls=stream_cls,
                )

            # If the response is streamed then we need to explicitly read the response
            # to completion before attempting to access the response text.
            await err.response.aread()
            raise self._make_status_error_from_response(
                request, err.response) from None
        except httpx.ConnectTimeout as err:
            if retries > 0:
                return await self._retry_request(options, cast_to, retries, stream=stream, stream_cls=stream_cls)
            raise APITimeoutError(request=request) from err
        except httpx.ReadTimeout as err:
            # We explicitly do not retry on ReadTimeout errors as this means
            # that the server processing the request has taken 60 seconds
            # (our default timeout). This likely indicates that something
            # is not working as expected on the server side.
            raise
        except httpx.TimeoutException as err:
            if retries > 0:
                return await self._retry_request(options, cast_to, retries, stream=stream, stream_cls=stream_cls)
            raise APITimeoutError(request=request) from err
        except Exception as err:
            if retries > 0:
                return await self._retry_request(options, cast_to, retries, stream=stream, stream_cls=stream_cls)
            raise APIConnectionError(request=request) from err

        if stream:
            if stream_cls:
                return stream_cls(cast_to=self._extract_stream_chunk_type(stream_cls), response=response, client=self)

            stream_cls = cast("type[_AsyncStreamT] | None",
                              self._default_stream_cls)
            if stream_cls is None:
                raise MissingStreamClassError()
            return stream_cls(cast_to=cast_to, response=response, client=self)

        try:
            rsp = self._process_response(
                cast_to=cast_to, options=options, response=response)
        except pydantic.ValidationError as err:
            raise APIResponseValidationError(
                request=request, response=response) from err

        return rsp

    async def _retry_request(
        self,
        options: FinalRequestOptions,
        cast_to: Type[ResponseT],
        remaining_retries: int,
        response_headers: Optional[httpx.Headers] = None,
        *,
        stream: bool,
        stream_cls: type[_AsyncStreamT] | None,
    ) -> ResponseT | _AsyncStreamT:
        """
        Retry an HTTP request asynchronously.

        Args:
            options (FinalRequestOptions): The request options.
            cast_to (Type[ResponseT]): The expected response type.
            remaining_retries (int): The remaining retry attempts.
            response_headers (Optional[httpx.Headers], optional): Response headers. Defaults to None.
            stream (bool): Whether to stream the response.
            stream_cls (type[_AsyncStreamT] | None): The stream class.

        Returns:
            ResponseT | _AsyncStreamT: The response or a stream, depending on the 'stream' parameter.
        """
        remaining = remaining_retries - 1
        timeout = self._calculate_retry_timeout(
            remaining, options, response_headers)

        await anyio.sleep(timeout)

        return await self._request(
            options=options,
            cast_to=cast_to,
            remaining_retries=remaining,
            stream=stream,
            stream_cls=stream_cls,
        )

    def _request_api_list(
        self,
        model: Type[ModelT],
        page: Type[AsyncPageT],
        options: FinalRequestOptions,
    ) -> AsyncPaginator[ModelT, AsyncPageT]:
        """
        Request an API list asynchronously and return a paginator.

        Args:
            model (Type[ModelT]): The model type.
            page (Type[AsyncPageT]): The page type.
            options (FinalRequestOptions): The request options.

        Returns:
            AsyncPaginator[ModelT, AsyncPageT]: An asynchronous paginator for the API list.
        """
        return AsyncPaginator(client=self, options=options, page_cls=page, model=model)

    @overload
    async def get(
        self,
        path: str,
        *,
        cast_to: Type[ResponseT],
        options: RequestOptions = {},
        stream: Literal[False] = False,
    ) -> ResponseT:
        ...

    @overload
    async def get(
        self,
        path: str,
        *,
        cast_to: Type[ResponseT],
        options: RequestOptions = {},
        stream: Literal[True],
        stream_cls: type[_AsyncStreamT],
    ) -> _AsyncStreamT:
        ...

    @overload
    async def get(
        self,
        path: str,
        *,
        cast_to: Type[ResponseT],
        options: RequestOptions = {},
        stream: bool,
        stream_cls: type[_AsyncStreamT] | None = None,
    ) -> ResponseT | _AsyncStreamT:
        ...

    async def get(
        self,
        path: str,
        *,
        cast_to: Type[ResponseT],
        options: RequestOptions = {},
        stream: bool = False,
        stream_cls: type[_AsyncStreamT] | None = None,
    ) -> ResponseT | _AsyncStreamT:
        """
        Make an HTTP GET request asynchronously.

        Args:
            path (str): The API endpoint path.
            cast_to (Type[ResponseT]): The expected response type.
            options (RequestOptions, optional): Additional request options. Defaults to {}.
            stream (bool, optional): Whether to stream the response. Defaults to False.
            stream_cls (type[_AsyncStreamT] | None, optional): The stream class. Defaults to None.

        Returns:
            ResponseT | _AsyncStreamT: The response or a stream, depending on the 'stream' parameter.
        """
        opts = FinalRequestOptions.construct(method="get", url=path, **options)
        return await self.request(cast_to, opts, stream=stream, stream_cls=stream_cls)

    @overload
    async def post(
        self,
        path: str,
        *,
        cast_to: Type[ResponseT],
        body: Body | None = None,
        files: RequestFiles | None = None,
        options: RequestOptions = {},
        stream: Literal[False] = False,
    ) -> ResponseT:
        ...

    @overload
    async def post(
        self,
        path: str,
        *,
        cast_to: Type[ResponseT],
        body: Body | None = None,
        files: RequestFiles | None = None,
        options: RequestOptions = {},
        stream: Literal[True],
        stream_cls: type[_AsyncStreamT],
    ) -> _AsyncStreamT:
        ...

    @overload
    async def post(
        self,
        path: str,
        *,
        cast_to: Type[ResponseT],
        body: Body | None = None,
        files: RequestFiles | None = None,
        options: RequestOptions = {},
        stream: bool,
        stream_cls: type[_AsyncStreamT] | None = None,
    ) -> ResponseT | _AsyncStreamT:
        ...

    async def post(
        self,
        path: str,
        *,
        cast_to: Type[ResponseT],
        body: Body | None = None,
        files: RequestFiles | None = None,
        options: RequestOptions = {},
        stream: bool = False,
        stream_cls: type[_AsyncStreamT] | None = None,
    ) -> ResponseT | _AsyncStreamT:
        """
        Make an HTTP POST request asynchronously.

        Args:
            path (str): The API endpoint path.
            cast_to (Type[ResponseT]): The expected response type.
            body (Body | None, optional): The request body. Defaults to None.
            files (RequestFiles | None, optional): Files to include in the request. Defaults to None.
            options (RequestOptions, optional): Additional request options. Defaults to {}.
            stream (bool, optional): Whether to stream the response. Defaults to False.
            stream_cls (type[_AsyncStreamT] | None, optional): The stream class. Defaults to None.

        Returns:
            ResponseT | _AsyncStreamT: The response or a stream, depending on the 'stream' parameter.
        """
        opts = FinalRequestOptions.construct(
            method="post", url=path, json_data=body, files=files, **options)
        return await self.request(cast_to, opts, stream=stream, stream_cls=stream_cls)

    async def patch(
        self,
        path: str,
        *,
        cast_to: Type[ResponseT],
        body: Body | None = None,
        options: RequestOptions = {},
    ) -> ResponseT:
        """
        Make an HTTP PATCH request asynchronously.

        Args:
            path (str): The API endpoint path.
            cast_to (Type[ResponseT]): The expected response type.
            body (Body | None, optional): The request body. Defaults to None.
            options (RequestOptions, optional): Additional request options. Defaults to {}.

        Returns:
            ResponseT: The response.
        """
        opts = FinalRequestOptions.construct(
            method="patch", url=path, json_data=body, **options)
        return await self.request(cast_to, opts)

    async def put(
        self,
        path: str,
        *,
        cast_to: Type[ResponseT],
        body: Body | None = None,
        files: RequestFiles | None = None,
        options: RequestOptions = {},
    ) -> ResponseT:
        """
        Make an HTTP PUT request asynchronously.

        Args:
            path (str): The API endpoint path.
            cast_to (Type[ResponseT]): The expected response type.
            body (Body | None, optional): The request body. Defaults to None.
            files (RequestFiles | None, optional): Files to include in the request. Defaults to None.
            options (RequestOptions, optional): Additional request options. Defaults to {}.

        Returns:
            ResponseT: The response.
        """
        opts = FinalRequestOptions.construct(
            method="put", url=path, json_data=body, files=files, **options)
        return await self.request(cast_to, opts)

    async def delete(
        self,
        path: str,
        *,
        cast_to: Type[ResponseT],
        body: Body | None = None,
        options: RequestOptions = {},
    ) -> ResponseT:
        """
        Make an HTTP DELETE request asynchronously.

        Args:
            path (str): The API endpoint path.
            cast_to (Type[ResponseT]): The expected response type.
            body (Body | None, optional): The request body. Defaults to None.
            options (RequestOptions, optional): Additional request options. Defaults to {}.

        Returns:
            ResponseT: The response.
        """

        opts = FinalRequestOptions.construct(
            method="delete", url=path, json_data=body, **options)
        return await self.request(cast_to, opts)

    def get_api_list(
        self,
        path: str,
        *,
        # TODO: support paginating `str`
        model: Type[ModelT],
        page: Type[AsyncPageT],
        body: Body | None = None,
        options: RequestOptions = {},
        method: str = "get",
    ) -> AsyncPaginator[ModelT, AsyncPageT]:
        """
        Get an API list and return an asynchronous paginator.

        Args:
            path (str): The API endpoint path.
            model (Type[ModelT]): The model type.
            page (Type[AsyncPageT]): The page type.
            body (Body | None, optional): The request body. Defaults to None.
            options (RequestOptions, optional): Additional request options. Defaults to {}.
            method (str, optional): The HTTP method to use. Defaults to "get".

        Returns:
            AsyncPaginator[ModelT, AsyncPageT]: An asynchronous paginator for the API list.
        """
        opts = FinalRequestOptions.construct(
            method=method, url=path, json_data=body, **options)
        return self._request_api_list(model, page, opts)


def make_request_options(
    *,
    query: Query | None = None,
    extra_headers: Headers | None = None,
    extra_query: Query | None = None,
    extra_body: Body | None = None,
    idempotency_key: str | None = None,
    timeout: float | None | NotGiven = NOT_GIVEN,
) -> RequestOptions:
    """
    Create a dictionary of request options without keys of NotGiven values.

    Args:
        query (Query | None, optional): The query parameters. Defaults to None.
        extra_headers (Headers | None, optional): Extra HTTP headers. Defaults to None.
        extra_query (Query | None, optional): Extra query parameters. Defaults to None.
        extra_body (Body | None, optional): Extra request body. Defaults to None.
        idempotency_key (str | None, optional): The idempotency key. Defaults to None.
        timeout (float | None | NotGiven, optional): The request timeout. Defaults to NOT_GIVEN.

    Returns:
        RequestOptions: A dictionary of request options without keys of NotGiven values.
    """
    options: RequestOptions = {}
    if extra_headers is not None:
        options["headers"] = extra_headers

    if extra_body is not None:
        options["extra_json"] = cast(AnyMapping, extra_body)

    if query is not None:
        options["params"] = query

    if extra_query is not None:
        options["params"] = {**options.get("params", {}), **extra_query}

    if not isinstance(timeout, NotGiven):
        options["timeout"] = timeout

    if idempotency_key is not None:
        options["idempotency_key"] = idempotency_key

    return options


class OtherPlatform:
    def __init__(self, name: str) -> None:
        self.name = name

    def __str__(self) -> str:
        return f"Other:{self.name}"


Platform = Union[
    OtherPlatform,
    Literal[
        "MacOS",
        "Linux",
        "Windows",
        "FreeBSD",
        "OpenBSD",
        "iOS",
        "Android",
        "Unknown",
    ],
]


def get_platform() -> Platform:
    """
    Get the platform information.

    Returns:
        Platform: The platform information, which can be one of the following:
            - "MacOS"
            - "Linux"
            - "Windows"
            - "FreeBSD"
            - "OpenBSD"
            - "iOS"
            - "Android"
            - OtherPlatform: Custom platform information for unknown platforms.
            - "Unknown": If the platform cannot be determined.
    """
    system = platform.system().lower()
    platform_name = platform.platform().lower()
    if "iphone" in platform_name or "ipad" in platform_name:
        # Tested using Python3IDE on an iPhone 11 and Pythonista on an iPad 7
        # system is Darwin and platform_name is a string like:
        # - Darwin-21.6.0-iPhone12,1-64bit
        # - Darwin-21.6.0-iPad7,11-64bit
        return "iOS"

    if system == "darwin":
        return "MacOS"

    if system == "windows":
        return "Windows"

    if "android" in platform_name:
        # Tested using Pydroid 3
        # system is Linux and platform_name is a string like 'Linux-5.10.81-android12-9-00001-geba40aecb3b7-ab8534902-aarch64-with-libc'
        return "Android"

    if system == "linux":
        # https://distro.readthedocs.io/en/latest/#distro.id
        distro_id = distro.id()
        if distro_id == "freebsd":
            return "FreeBSD"

        if distro_id == "openbsd":
            return "OpenBSD"

        return "Linux"

    if platform_name:
        return OtherPlatform(platform_name)

    return "Unknown"


class OtherArch:
    def __init__(self, name: str) -> None:
        self.name = name

    def __str__(self) -> str:
        return f"other:{self.name}"


Arch = Union[OtherArch, Literal["x32", "x64", "arm", "arm64", "unknown"]]


def get_architecture() -> Arch:
    """
    Get the architecture information.

    Returns:
        Arch: The architecture information, which can be one of the following:
            - "arm64" for ARM64 architecture.
            - "arm" for ARM architecture (untested).
            - "x64" for x86_64 architecture.
            - "x32" for x32 architecture (untested).
            - OtherArch: Custom architecture information for unknown architectures.
            - "unknown" if the architecture cannot be determined.
    """
    python_bitness, _ = platform.architecture()
    machine = platform.machine().lower()
    if machine in ("arm64", "aarch64"):
        return "arm64"

    # TODO: untested
    if machine == "arm":
        return "arm"

    if machine == "x86_64":
        return "x64"

    # TODO: untested
    if python_bitness == "32bit":
        return "x32"

    if machine:
        return OtherArch(machine)

    return "unknown"


def _merge_mappings(
    obj1: Mapping[_T_co, Union[_T, Omit]],
    obj2: Mapping[_T_co, Union[_T, Omit]],
) -> Dict[_T_co, _T]:
    """
    Merge two mappings of the same type, removing any values that are instances of `Omit`.

    In cases with duplicate keys, the values from the second mapping take precedence.

    Args:
        obj1 (Mapping[_T_co, Union[_T, Omit]]): The first mapping.
        obj2 (Mapping[_T_co, Union[_T, Omit]]): The second mapping.

    Returns:
        Dict[_T_co, _T]: A merged dictionary with omitted values removed.
    """
    merged = {**obj1, **obj2}
    return {key: value for key, value in merged.items() if not isinstance(value, Omit)}
