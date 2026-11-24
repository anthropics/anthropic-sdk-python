from __future__ import annotations

from ....._compat import cached_property
from ....._resource import SyncAPIResource, AsyncAPIResource
from .google.google import (
    Google,
    AsyncGoogle,
    GoogleWithRawResponse,
    AsyncGoogleWithRawResponse,
    GoogleWithStreamingResponse,
    AsyncGoogleWithStreamingResponse,
)

__all__ = ["Providers", "AsyncProviders"]


class Providers(SyncAPIResource):
    @cached_property
    def google(self) -> Google:
        return Google(self._client)

    @cached_property
    def with_raw_response(self) -> ProvidersWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://platform.claude.com/docs/en/api/sdks/python
        """
        return ProvidersWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ProvidersWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://platform.claude.com/docs/en/api/sdks/python
        """
        return ProvidersWithStreamingResponse(self)


class AsyncProviders(AsyncAPIResource):
    @cached_property
    def google(self) -> AsyncGoogle:
        return AsyncGoogle(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncProvidersWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://platform.claude.com/docs/en/api/sdks/python
        """
        return AsyncProvidersWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncProvidersWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://platform.claude.com/docs/en/api/sdks/python
        """
        return AsyncProvidersWithStreamingResponse(self)


class ProvidersWithRawResponse:
    def __init__(self, providers: Providers) -> None:
        self._providers = providers

    @cached_property
    def google(self) -> GoogleWithRawResponse:
        return GoogleWithRawResponse(self._providers.google)


class AsyncProvidersWithRawResponse:
    def __init__(self, providers: AsyncProviders) -> None:
        self._providers = providers

    @cached_property
    def google(self) -> AsyncGoogleWithRawResponse:
        return AsyncGoogleWithRawResponse(self._providers.google)


class ProvidersWithStreamingResponse:
    def __init__(self, providers: Providers) -> None:
        self._providers = providers

    @cached_property
    def google(self) -> GoogleWithStreamingResponse:
        return GoogleWithStreamingResponse(self._providers.google)


class AsyncProvidersWithStreamingResponse:
    def __init__(self, providers: AsyncProviders) -> None:
        self._providers = providers

    @cached_property
    def google(self) -> AsyncGoogleWithStreamingResponse:
        return AsyncGoogleWithStreamingResponse(self._providers.google)
