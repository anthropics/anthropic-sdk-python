from __future__ import annotations

import os
import inspect
from typing import Any, Union, Mapping, TypeVar, Callable, Awaitable, cast, overload
from functools import cached_property
from typing_extensions import Self, override

import httpx

from .._types import NOT_GIVEN, Omit, Headers, Timeout, NotGiven
from .._utils import is_given
from .._client import Anthropic, AsyncAnthropic
from .._compat import model_copy
from .._models import FinalRequestOptions
from .._streaming import Stream, AsyncStream
from .._exceptions import AnthropicError
from .._base_client import DEFAULT_MAX_RETRIES, BaseClient
from ..resources.beta import Beta, AsyncBeta
from ..resources.messages import Messages, AsyncMessages
from ..resources.beta.messages import Messages as BetaMessages, AsyncMessages as AsyncBetaMessages

AzureADTokenProvider = Callable[[], str]
AsyncAzureADTokenProvider = Callable[[], "str | Awaitable[str]"]
_HttpxClientT = TypeVar("_HttpxClientT", bound=Union[httpx.Client, httpx.AsyncClient])
_DefaultStreamT = TypeVar("_DefaultStreamT", bound=Union[Stream[Any], AsyncStream[Any]])


class MutuallyExclusiveAuthError(AnthropicError):
    def __init__(self) -> None:
        super().__init__(
            "The `api_key` and `azure_ad_token_provider` arguments are mutually exclusive; Only one can be passed at a time"
        )


class BaseFoundryClient(BaseClient[_HttpxClientT, _DefaultStreamT]): ...


class MessagesFoundry(Messages):
    @cached_property
    @override
    def batches(self) -> None:  # type: ignore[override]
        """Batches endpoint is not supported for Anthropic Foundry client."""
        return None


class BetaFoundryMessages(BetaMessages):
    @cached_property
    @override
    def batches(self) -> None:  # type: ignore[override]
        """Batches endpoint is not supported for Anthropic Foundry client."""
        return None


class BetaFoundry(Beta):
    @cached_property
    @override
    def messages(self) -> BetaMessages:  # type: ignore[override]
        """Return beta messages resource instance with excluded unsupported endpoints."""
        return BetaFoundryMessages(self._client)


class AsyncMessagesFoundry(AsyncMessages):
    @cached_property
    @override
    def batches(self) -> None:  # type: ignore[override]
        """Batches endpoint is not supported for Anthropic Foundry client."""
        return None


class AsyncBetaFoundryMessages(AsyncBetaMessages):
    @cached_property
    @override
    def batches(self) -> None:  # type: ignore[override]
        """Batches endpoint is not supported for Anthropic Foundry client."""
        return None


class AsyncBetaFoundry(AsyncBeta):
    @cached_property
    @override
    def messages(self) -> AsyncBetaMessages:  # type: ignore[override]
        """Return beta messages resource instance with excluded unsupported endpoints."""
        return AsyncBetaFoundryMessages(self._client)


# ==============================================================================


class AnthropicFoundry(BaseFoundryClient[httpx.Client, Stream[Any]], Anthropic):
    @overload
    def __init__(
        self,
        *,
        resource: str | None = None,
        api_key: str | None = None,
        azure_ad_token_provider: AzureADTokenProvider | None = None,
        webhook_key: str | None = None,
        timeout: float | Timeout | None | NotGiven = NOT_GIVEN,
        max_retries: int = DEFAULT_MAX_RETRIES,
        default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        http_client: httpx.Client | None = None,
        _strict_response_validation: bool = False,
    ) -> None: ...

    @overload
    def __init__(
        self,
        *,
        base_url: str,
        api_key: str | None = None,
        azure_ad_token_provider: AzureADTokenProvider | None = None,
        webhook_key: str | None = None,
        timeout: float | Timeout | None | NotGiven = NOT_GIVEN,
        max_retries: int = DEFAULT_MAX_RETRIES,
        default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        http_client: httpx.Client | None = None,
        _strict_response_validation: bool = False,
    ) -> None: ...

    def __init__(
        self,
        *,
        resource: str | None = None,
        api_key: str | None = None,
        azure_ad_token_provider: AzureADTokenProvider | None = None,
        webhook_key: str | None = None,
        base_url: str | None = None,
        timeout: float | Timeout | None | NotGiven = NOT_GIVEN,
        max_retries: int = DEFAULT_MAX_RETRIES,
        default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        http_client: httpx.Client | None = None,
        _strict_response_validation: bool = False,
    ) -> None:
        """Construct a new synchronous Anthropic Foundry client instance.

        This automatically infers the following arguments from their corresponding environment variables if they are not provided:
        - `api_key` from `ANTHROPIC_FOUNDRY_API_KEY`
        - `resource` from `ANTHROPIC_FOUNDRY_RESOURCE`
        - `base_url` from `ANTHROPIC_FOUNDRY_BASE_URL`

        Args:
            resource: Your Foundry resource name, e.g. `example-resource` for `https://example-resource.services.ai.azure.com/anthropic/`
            azure_ad_token_provider: A function that returns an Azure Active Directory token, will be invoked on every request.
        """
        api_key = api_key if api_key is not None else os.environ.get("ANTHROPIC_FOUNDRY_API_KEY")
        resource = resource if resource is not None else os.environ.get("ANTHROPIC_FOUNDRY_RESOURCE")
        base_url = base_url if base_url is not None else os.environ.get("ANTHROPIC_FOUNDRY_BASE_URL")

        if api_key is None and azure_ad_token_provider is None:
            raise AnthropicError(
                "Missing credentials. Please pass one of `api_key`, `azure_ad_token_provider`, or the `ANTHROPIC_FOUNDRY_API_KEY` environment variable."
            )

        if base_url is None:
            if resource is None:
                raise ValueError(
                    "Must provide one of the `base_url` or `resource` arguments, or the `ANTHROPIC_FOUNDRY_RESOURCE` environment variable"
                )
            base_url = f"https://{resource}.services.ai.azure.com/anthropic/"
        elif resource is not None:
            raise ValueError("base_url and resource are mutually exclusive")

        super().__init__(
            api_key=api_key,
            webhook_key=webhook_key,
            base_url=base_url,
            timeout=timeout,
            max_retries=max_retries,
            default_headers=default_headers,
            default_query=default_query,
            http_client=http_client,
            _strict_response_validation=_strict_response_validation,
        )
        self._azure_ad_token_provider = azure_ad_token_provider

    @cached_property
    @override
    def models(self) -> None:  # type: ignore[override]
        """Models endpoint is not supported for Anthropic Foundry client."""
        return None

    @cached_property
    @override
    def messages(self) -> MessagesFoundry:  # type: ignore[override]
        """Return messages resource instance with excluded unsupported endpoints."""
        return MessagesFoundry(client=self)

    @cached_property
    @override
    def beta(self) -> Beta:  # type: ignore[override]
        """Return beta resource instance with excluded unsupported endpoints."""
        return BetaFoundry(self)

    @override
    def copy(  # type: ignore[override]  # pyright: ignore[reportIncompatibleMethodOverride] — subclass intentionally drops `credentials` & `auth_token`
        self,
        *,
        api_key: str | None = None,
        azure_ad_token_provider: AzureADTokenProvider | None = None,
        webhook_key: str | None = None,
        base_url: str | httpx.URL | None = None,
        timeout: float | Timeout | None | NotGiven = NOT_GIVEN,
        http_client: httpx.Client | None = None,
        max_retries: int | NotGiven = NOT_GIVEN,
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

        return self.__class__(
            api_key=api_key or self.api_key,
            azure_ad_token_provider=azure_ad_token_provider or self._azure_ad_token_provider,
            webhook_key=webhook_key or self.webhook_key,
            base_url=str(base_url or self.base_url),
            timeout=self.timeout if isinstance(timeout, NotGiven) else timeout,
            http_client=http_client or self._client,
            max_retries=max_retries if is_given(max_retries) else self.max_retries,
            default_headers=headers,
            default_query=params,
            **_extra_kwargs,
        )

    with_options = copy  # type: ignore[assignment]

    def _get_azure_ad_token(self) -> str | None:
        provider = self._azure_ad_token_provider
        if provider is not None:
            token = provider()
            if not token or not isinstance(token, str):  # pyright: ignore[reportUnnecessaryIsInstance]
                raise ValueError(
                    f"Expected `azure_ad_token_provider` argument to return a string but it returned {token}",
                )
            return token

        return None

    @override
    def _prepare_options(self, options: FinalRequestOptions) -> FinalRequestOptions:
        headers: dict[str, str | Omit] = {**options.headers} if is_given(options.headers) else {}

        options = model_copy(options)
        options.headers = headers

        azure_ad_token = self._get_azure_ad_token()
        if azure_ad_token is not None:
            if headers.get("Authorization") is None:
                headers["Authorization"] = f"Bearer {azure_ad_token}"
        elif self.api_key is not None:
            # In this branch `self.api_key` is always the Foundry key (explicit or
            # ANTHROPIC_FOUNDRY_API_KEY) — with an Azure AD token provider configured
            # the branch above wins, so an environment `ANTHROPIC_API_KEY` can never
            # be sent here. The endpoint authenticates with `x-api-key`; `api-key` is
            # also sent for backwards compatibility.
            if headers.get("x-api-key") is None:
                headers["x-api-key"] = self.api_key
            if headers.get("api-key") is None:
                headers["api-key"] = self.api_key
        else:
            # should never be hit
            raise ValueError("Unable to handle auth")

        return options

    @property
    @override
    def auth_headers(self) -> dict[str, str]:
        # Auth is attached per-request in `_prepare_options` (`x-api-key`/`api-key`
        # headers for API-key auth, or a bearer `Authorization` header for the Azure AD
        # token provider). Emitting nothing here stops the base client from sending an
        # `X-Api-Key` derived from `self.api_key`: when only an Azure AD token
        # provider is configured, `self.api_key` can be populated from an
        # `ANTHROPIC_API_KEY` in the environment, which must not be sent to the
        # Foundry endpoint.
        return {}

    @override
    def _validate_headers(self, headers: Headers, custom_headers: Headers) -> None:
        # Foundry attaches its own auth header in `_prepare_options`, so the base
        # requirement that `X-Api-Key`/`Authorization` already be present does not apply.
        return


class AsyncAnthropicFoundry(BaseFoundryClient[httpx.AsyncClient, AsyncStream[Any]], AsyncAnthropic):
    @overload
    def __init__(
        self,
        *,
        resource: str | None = None,
        api_key: str | None = None,
        azure_ad_token_provider: AsyncAzureADTokenProvider | None = None,
        webhook_key: str | None = None,
        timeout: float | Timeout | None | NotGiven = NOT_GIVEN,
        max_retries: int = DEFAULT_MAX_RETRIES,
        default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        http_client: httpx.AsyncClient | None = None,
        _strict_response_validation: bool = False,
    ) -> None: ...

    @overload
    def __init__(
        self,
        *,
        base_url: str,
        api_key: str | None = None,
        azure_ad_token_provider: AsyncAzureADTokenProvider | None = None,
        webhook_key: str | None = None,
        timeout: float | Timeout | None | NotGiven = NOT_GIVEN,
        max_retries: int = DEFAULT_MAX_RETRIES,
        default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        http_client: httpx.AsyncClient | None = None,
        _strict_response_validation: bool = False,
    ) -> None: ...

    def __init__(
        self,
        *,
        resource: str | None = None,
        api_key: str | None = None,
        azure_ad_token_provider: AsyncAzureADTokenProvider | None = None,
        webhook_key: str | None = None,
        base_url: str | None = None,
        timeout: float | Timeout | None | NotGiven = NOT_GIVEN,
        max_retries: int = DEFAULT_MAX_RETRIES,
        default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        http_client: httpx.AsyncClient | None = None,
        _strict_response_validation: bool = False,
    ) -> None:
        """Construct a new asynchronous Anthropic Foundry client instance.

        This automatically infers the following arguments from their corresponding environment variables if they are not provided:
        - `api_key` from `ANTHROPIC_FOUNDRY_API_KEY`
        - `resource` from `ANTHROPIC_FOUNDRY_RESOURCE`
        - `base_url` from `ANTHROPIC_FOUNDRY_BASE_URL`

        Args:
            resource: Your Foundry resource name, e.g. `example-resource` for `https://example-resource.services.ai.azure.com/anthropic/`
            azure_ad_token_provider: A function that returns an Azure Active Directory token, will be invoked on every request.
        """
        api_key = api_key if api_key is not None else os.environ.get("ANTHROPIC_FOUNDRY_API_KEY")
        resource = resource if resource is not None else os.environ.get("ANTHROPIC_FOUNDRY_RESOURCE")
        base_url = base_url if base_url is not None else os.environ.get("ANTHROPIC_FOUNDRY_BASE_URL")

        if api_key is None and azure_ad_token_provider is None:
            raise AnthropicError(
                "Missing credentials. Please pass one of `api_key`, `azure_ad_token_provider`, or the `ANTHROPIC_FOUNDRY_API_KEY` environment variable."
            )

        if base_url is None:
            if resource is None:
                raise ValueError(
                    "Must provide one of the `base_url` or `resource` arguments, or the `ANTHROPIC_FOUNDRY_RESOURCE` environment variable"
                )
            base_url = f"https://{resource}.services.ai.azure.com/anthropic/"
        elif resource is not None:
            raise ValueError("base_url and resource are mutually exclusive")

        super().__init__(
            api_key=api_key,
            webhook_key=webhook_key,
            base_url=base_url,
            timeout=timeout,
            max_retries=max_retries,
            default_headers=default_headers,
            default_query=default_query,
            http_client=http_client,
            _strict_response_validation=_strict_response_validation,
        )
        self._azure_ad_token_provider = azure_ad_token_provider

    @cached_property
    @override
    def models(self) -> None:  # type: ignore[override]
        """Models endpoint is not supported for Azure Anthropic client."""
        return None

    @cached_property
    @override
    def messages(self) -> AsyncMessagesFoundry:  # type: ignore[override]
        """Return messages resource instance with excluded unsupported endpoints."""
        return AsyncMessagesFoundry(client=self)

    @cached_property
    @override
    def beta(self) -> AsyncBetaFoundry:  # type: ignore[override]
        """Return beta resource instance with excluded unsupported endpoints."""
        return AsyncBetaFoundry(client=self)

    @override
    def copy(  # type: ignore[override]  # pyright: ignore[reportIncompatibleMethodOverride] — subclass intentionally drops `credentials` & `auth_token`
        self,
        *,
        api_key: str | None = None,
        azure_ad_token_provider: AsyncAzureADTokenProvider | None = None,
        webhook_key: str | None = None,
        base_url: str | httpx.URL | None = None,
        timeout: float | Timeout | None | NotGiven = NOT_GIVEN,
        http_client: httpx.AsyncClient | None = None,
        max_retries: int | NotGiven = NOT_GIVEN,
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

        return self.__class__(
            api_key=api_key or self.api_key,
            azure_ad_token_provider=azure_ad_token_provider or self._azure_ad_token_provider,
            webhook_key=webhook_key or self.webhook_key,
            base_url=str(base_url or self.base_url),
            timeout=self.timeout if isinstance(timeout, NotGiven) else timeout,
            http_client=http_client or self._client,
            max_retries=max_retries if is_given(max_retries) else self.max_retries,
            default_headers=headers,
            default_query=params,
            **_extra_kwargs,
        )

    with_options = copy  # type: ignore[assignment]

    async def _get_azure_ad_token(self) -> str | None:
        provider = self._azure_ad_token_provider
        if provider is not None:
            token = provider()
            if inspect.isawaitable(token):
                token = await token
            if not token or not isinstance(cast(Any, token), str):
                raise ValueError(
                    f"Expected `azure_ad_token_provider` argument to return a string but it returned {token}",
                )
            return str(token)

        return None

    @override
    async def _prepare_options(self, options: FinalRequestOptions) -> FinalRequestOptions:
        headers: dict[str, str | Omit] = {**options.headers} if is_given(options.headers) else {}

        options = model_copy(options)
        options.headers = headers

        azure_ad_token = await self._get_azure_ad_token()
        if azure_ad_token is not None:
            if headers.get("Authorization") is None:
                headers["Authorization"] = f"Bearer {azure_ad_token}"
        elif self.api_key is not None:
            # See AnthropicFoundry._prepare_options: `self.api_key` here is always the
            # Foundry key, never an environment `ANTHROPIC_API_KEY`.
            if headers.get("x-api-key") is None:
                headers["x-api-key"] = self.api_key
            if headers.get("api-key") is None:
                headers["api-key"] = self.api_key
        else:
            # should never be hit
            raise ValueError("Unable to handle auth")

        return options

    @property
    @override
    def auth_headers(self) -> dict[str, str]:
        # See AnthropicFoundry.auth_headers: prevents leaking an environment
        # ANTHROPIC_API_KEY as X-Api-Key to the Foundry endpoint.
        return {}

    @override
    def _validate_headers(self, headers: Headers, custom_headers: Headers) -> None:
        # Foundry attaches its own auth header in `_prepare_options`.
        return
