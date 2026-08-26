# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from .issuers import (
    Issuers,
    AsyncIssuers,
    IssuersWithRawResponse,
    AsyncIssuersWithRawResponse,
    IssuersWithStreamingResponse,
    AsyncIssuersWithStreamingResponse,
)
from ....._compat import cached_property
from .rules.rules import (
    Rules,
    AsyncRules,
    RulesWithRawResponse,
    AsyncRulesWithRawResponse,
    RulesWithStreamingResponse,
    AsyncRulesWithStreamingResponse,
)
from ....._resource import SyncAPIResource, AsyncAPIResource

__all__ = ["Federation", "AsyncFederation"]


class Federation(SyncAPIResource):
    @cached_property
    def issuers(self) -> Issuers:
        return Issuers(self._client)

    @cached_property
    def rules(self) -> Rules:
        return Rules(self._client)

    @cached_property
    def with_raw_response(self) -> FederationWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#accessing-raw-response-data-eg-headers
        """
        return FederationWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> FederationWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#with_streaming_response
        """
        return FederationWithStreamingResponse(self)


class AsyncFederation(AsyncAPIResource):
    @cached_property
    def issuers(self) -> AsyncIssuers:
        return AsyncIssuers(self._client)

    @cached_property
    def rules(self) -> AsyncRules:
        return AsyncRules(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncFederationWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#accessing-raw-response-data-eg-headers
        """
        return AsyncFederationWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncFederationWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#with_streaming_response
        """
        return AsyncFederationWithStreamingResponse(self)


class FederationWithRawResponse:
    def __init__(self, federation: Federation) -> None:
        self._federation = federation

    @cached_property
    def issuers(self) -> IssuersWithRawResponse:
        return IssuersWithRawResponse(self._federation.issuers)

    @cached_property
    def rules(self) -> RulesWithRawResponse:
        return RulesWithRawResponse(self._federation.rules)


class AsyncFederationWithRawResponse:
    def __init__(self, federation: AsyncFederation) -> None:
        self._federation = federation

    @cached_property
    def issuers(self) -> AsyncIssuersWithRawResponse:
        return AsyncIssuersWithRawResponse(self._federation.issuers)

    @cached_property
    def rules(self) -> AsyncRulesWithRawResponse:
        return AsyncRulesWithRawResponse(self._federation.rules)


class FederationWithStreamingResponse:
    def __init__(self, federation: Federation) -> None:
        self._federation = federation

    @cached_property
    def issuers(self) -> IssuersWithStreamingResponse:
        return IssuersWithStreamingResponse(self._federation.issuers)

    @cached_property
    def rules(self) -> RulesWithStreamingResponse:
        return RulesWithStreamingResponse(self._federation.rules)


class AsyncFederationWithStreamingResponse:
    def __init__(self, federation: AsyncFederation) -> None:
        self._federation = federation

    @cached_property
    def issuers(self) -> AsyncIssuersWithStreamingResponse:
        return AsyncIssuersWithStreamingResponse(self._federation.issuers)

    @cached_property
    def rules(self) -> AsyncRulesWithStreamingResponse:
        return AsyncRulesWithStreamingResponse(self._federation.rules)
