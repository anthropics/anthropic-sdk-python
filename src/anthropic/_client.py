# File generated from our OpenAPI spec by Stainless.

from __future__ import annotations

import os
from typing import Union, Mapping, Optional

import httpx
from tokenizers import Tokenizer  # type: ignore[import]

from . import resources
from ._qs import Querystring
from ._types import (
    NOT_GIVEN,
    Omit,
    Headers,
    Timeout,
    NotGiven,
    Transport,
    ProxiesTypes,
    RequestOptions,
)
from ._version import __version__
from ._streaming import Stream as Stream
from ._streaming import AsyncStream as AsyncStream
from ._tokenizers import sync_get_tokenizer, async_get_tokenizer
from ._base_client import (
    DEFAULT_LIMITS,
    DEFAULT_TIMEOUT,
    DEFAULT_MAX_RETRIES,
    SyncAPIClient,
    AsyncAPIClient,
)

__all__ = [
    "Timeout",
    "Transport",
    "ProxiesTypes",
    "RequestOptions",
    "resources",
    "Anthropic",
    "AsyncAnthropic",
    "Client",
    "AsyncClient",
]


class Anthropic(SyncAPIClient):
    completions: resources.Completions

    # client options
    api_key: str | None
    auth_token: str | None

    def __init__(
        self,
        *,
        auth_token: str | None = None,
        base_url: Optional[str] = None,
        api_key: Optional[str] = None,
        timeout: Union[float, Timeout, None] = DEFAULT_TIMEOUT,
        max_retries: int = DEFAULT_MAX_RETRIES,
        default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        # See httpx documentation for [custom transports](https://www.python-httpx.org/advanced/#custom-transports)
        transport: Optional[Transport] = None,
        # See httpx documentation for [proxies](https://www.python-httpx.org/advanced/#http-proxying)
        proxies: Optional[ProxiesTypes] = None,
        # See httpx documentation for [limits](https://www.python-httpx.org/advanced/#pool-limit-configuration)
        connection_pool_limits: httpx.Limits | None = DEFAULT_LIMITS,
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
        """Construct a new synchronous anthropic client instance.

        This automatically infers the following arguments from their corresponding environment variables if they are not provided:
        - `auth_token` from `ANTHROPIC_AUTH_TOKEN`
        - `api_key` from `ANTHROPIC_API_KEY`
        """
        api_key = api_key or os.environ.get("ANTHROPIC_API_KEY", "")

        if base_url is None:
            base_url = "https://api.anthropic.com"

        super().__init__(
            version=__version__,
            base_url=base_url,
            max_retries=max_retries,
            timeout=timeout,
            transport=transport,
            proxies=proxies,
            limits=connection_pool_limits,
            custom_headers=default_headers,
            custom_query=default_query,
            _strict_response_validation=_strict_response_validation,
        )

        self.api_key = api_key

        auth_token_envvar = os.environ.get("ANTHROPIC_AUTH_TOKEN", None)
        self.auth_token = auth_token or auth_token_envvar or None

        self._default_stream_cls = Stream

        self.completions = resources.Completions(self)

    @property
    def qs(self) -> Querystring:
        return Querystring(array_format="comma")

    @property
    def auth_headers(self) -> dict[str, str]:
        if self._api_key_header:
            return self._api_key_header
        if self._auth_token_bearer:
            return self._auth_token_bearer
        return {}

    @property
    def _api_key_header(self) -> dict[str, str]:
        api_key = self.api_key
        if api_key is None:
            return {}
        return {"X-Api-Key": api_key}

    @property
    def _auth_token_bearer(self) -> dict[str, str]:
        auth_token = self.auth_token
        if auth_token is None:
            return {}
        return {"Authorization": f"Bearer {auth_token}"}

    @property
    def default_headers(self) -> dict[str, str | Omit]:
        return {
            **super().default_headers,
            "anthropic-version": "2023-06-01",
            **self._custom_headers,
        }

    def _validate_headers(self, headers: Headers, custom_headers: Headers) -> None:
        if self.api_key and headers.get("X-Api-Key"):
            return
        if isinstance(custom_headers.get("X-Api-Key"), Omit):
            return

        if self.auth_token and headers.get("Authorization"):
            return
        if isinstance(custom_headers.get("Authorization"), Omit):
            return

        raise TypeError(
            '"Could not resolve authentication method. Expected either api_key or auth_token to be set. Or for one of the `X-Api-Key` or `Authorization` headers to be explicitly omitted"'
        )

    def copy(
        self,
        *,
        auth_token: str | None = None,
        api_key: str | None = None,
        base_url: str | None = None,
        timeout: float | Timeout | None | NotGiven = NOT_GIVEN,
        connection_pool_limits: httpx.Limits | NotGiven = NOT_GIVEN,
        max_retries: int | NotGiven = NOT_GIVEN,
        default_headers: Mapping[str, str] | None = None,
        set_default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        set_default_query: Mapping[str, object] | None = None,
    ) -> Anthropic:
        """
        Create a new client instance re-using the same options given to the current client with optional overriding.

        It should be noted that this does not share the underlying httpx client class which may lead
        to performance issues.
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

        # TODO: share the same httpx client between instances
        return self.__class__(
            auth_token=auth_token or self.auth_token,
            base_url=base_url or str(self.base_url),
            api_key=api_key or self.api_key,
            timeout=self.timeout if isinstance(timeout, NotGiven) else timeout,
            connection_pool_limits=self._limits
            if isinstance(connection_pool_limits, NotGiven)
            else connection_pool_limits,
            max_retries=self.max_retries if isinstance(max_retries, NotGiven) else max_retries,
            default_headers=headers,
            default_query=params,
        )

    # Alias for `copy` for nicer inline usage, e.g.
    # client.with_options(timeout=10).foo.create(...)
    with_options = copy

    def count_tokens(
        self,
        text: str,
    ) -> int:
        """Count the number of tokens in a given string"""
        # Note: tokenizer is untyped
        tokenizer = self.get_tokenizer()
        encoded_text = tokenizer.encode(text)  # type: ignore
        return len(encoded_text.ids)  # type: ignore

    def get_tokenizer(self) -> Tokenizer:
        return sync_get_tokenizer()


class AsyncAnthropic(AsyncAPIClient):
    completions: resources.AsyncCompletions

    # client options
    api_key: str | None
    auth_token: str | None

    def __init__(
        self,
        *,
        auth_token: str | None = None,
        base_url: Optional[str] = None,
        api_key: Optional[str] = None,
        timeout: Union[float, Timeout, None] = DEFAULT_TIMEOUT,
        max_retries: int = DEFAULT_MAX_RETRIES,
        default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        # See httpx documentation for [custom transports](https://www.python-httpx.org/advanced/#custom-transports)
        transport: Optional[Transport] = None,
        # See httpx documentation for [proxies](https://www.python-httpx.org/advanced/#http-proxying)
        proxies: Optional[ProxiesTypes] = None,
        # See httpx documentation for [limits](https://www.python-httpx.org/advanced/#pool-limit-configuration)
        connection_pool_limits: httpx.Limits | None = DEFAULT_LIMITS,
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
        """Construct a new async anthropic client instance.

        This automatically infers the following arguments from their corresponding environment variables if they are not provided:
        - `auth_token` from `ANTHROPIC_AUTH_TOKEN`
        - `api_key` from `ANTHROPIC_API_KEY`
        """
        api_key = api_key or os.environ.get("ANTHROPIC_API_KEY", "")

        if base_url is None:
            base_url = "https://api.anthropic.com"

        super().__init__(
            version=__version__,
            base_url=base_url,
            max_retries=max_retries,
            timeout=timeout,
            transport=transport,
            proxies=proxies,
            limits=connection_pool_limits,
            custom_headers=default_headers,
            custom_query=default_query,
            _strict_response_validation=_strict_response_validation,
        )

        self.api_key = api_key

        auth_token_envvar = os.environ.get("ANTHROPIC_AUTH_TOKEN", None)
        self.auth_token = auth_token or auth_token_envvar or None

        self._default_stream_cls = AsyncStream

        self.completions = resources.AsyncCompletions(self)

    @property
    def qs(self) -> Querystring:
        return Querystring(array_format="comma")

    @property
    def auth_headers(self) -> dict[str, str]:
        if self._api_key_header:
            return self._api_key_header
        if self._auth_token_bearer:
            return self._auth_token_bearer
        return {}

    @property
    def _api_key_header(self) -> dict[str, str]:
        api_key = self.api_key
        if api_key is None:
            return {}
        return {"X-Api-Key": api_key}

    @property
    def _auth_token_bearer(self) -> dict[str, str]:
        auth_token = self.auth_token
        if auth_token is None:
            return {}
        return {"Authorization": f"Bearer {auth_token}"}

    @property
    def default_headers(self) -> dict[str, str | Omit]:
        return {
            **super().default_headers,
            "anthropic-version": "2023-06-01",
            **self._custom_headers,
        }

    def _validate_headers(self, headers: Headers, custom_headers: Headers) -> None:
        if self.api_key and headers.get("X-Api-Key"):
            return
        if isinstance(custom_headers.get("X-Api-Key"), Omit):
            return

        if self.auth_token and headers.get("Authorization"):
            return
        if isinstance(custom_headers.get("Authorization"), Omit):
            return

        raise TypeError(
            '"Could not resolve authentication method. Expected either api_key or auth_token to be set. Or for one of the `X-Api-Key` or `Authorization` headers to be explicitly omitted"'
        )

    def copy(
        self,
        *,
        auth_token: str | None = None,
        api_key: str | None = None,
        base_url: str | None = None,
        timeout: float | Timeout | None | NotGiven = NOT_GIVEN,
        connection_pool_limits: httpx.Limits | NotGiven = NOT_GIVEN,
        max_retries: int | NotGiven = NOT_GIVEN,
        default_headers: Mapping[str, str] | None = None,
        set_default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        set_default_query: Mapping[str, object] | None = None,
    ) -> AsyncAnthropic:
        """
        Create a new client instance re-using the same options given to the current client with optional overriding.

        It should be noted that this does not share the underlying httpx client class which may lead
        to performance issues.
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

        # TODO: share the same httpx client between instances
        return self.__class__(
            auth_token=auth_token or self.auth_token,
            base_url=base_url or str(self.base_url),
            api_key=api_key or self.api_key,
            timeout=self.timeout if isinstance(timeout, NotGiven) else timeout,
            connection_pool_limits=self._limits
            if isinstance(connection_pool_limits, NotGiven)
            else connection_pool_limits,
            max_retries=self.max_retries if isinstance(max_retries, NotGiven) else max_retries,
            default_headers=headers,
            default_query=params,
        )

    # Alias for `copy` for nicer inline usage, e.g.
    # client.with_options(timeout=10).foo.create(...)
    with_options = copy

    async def count_tokens(
        self,
        text: str,
    ) -> int:
        """Count the number of tokens in a given string"""
        # Note: tokenizer is untyped
        tokenizer = await self.get_tokenizer()
        encoded_text = tokenizer.encode(text)  # type: ignore
        return len(encoded_text.ids)  # type: ignore

    async def get_tokenizer(self) -> Tokenizer:
        return await async_get_tokenizer()


Client = Anthropic

AsyncClient = AsyncAnthropic
