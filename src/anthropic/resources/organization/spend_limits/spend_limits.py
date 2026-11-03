from __future__ import annotations

from .effective import (
    Effective,
    AsyncEffective,
    EffectiveWithRawResponse,
    AsyncEffectiveWithRawResponse,
    EffectiveWithStreamingResponse,
    AsyncEffectiveWithStreamingResponse,
)
from ...._compat import cached_property
from ...._resource import SyncAPIResource, AsyncAPIResource
from .increase_requests import (
    IncreaseRequests,
    AsyncIncreaseRequests,
    IncreaseRequestsWithRawResponse,
    AsyncIncreaseRequestsWithRawResponse,
    IncreaseRequestsWithStreamingResponse,
    AsyncIncreaseRequestsWithStreamingResponse,
)

__all__ = ["SpendLimits", "AsyncSpendLimits"]


class SpendLimits(SyncAPIResource):
    @cached_property
    def effective(self) -> Effective:
        return Effective(self._client)

    @cached_property
    def increase_requests(self) -> IncreaseRequests:
        return IncreaseRequests(self._client)

    @cached_property
    def with_raw_response(self) -> SpendLimitsWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://platform.claude.com/docs/en/api/sdks/python
        """
        return SpendLimitsWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> SpendLimitsWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://platform.claude.com/docs/en/api/sdks/python
        """
        return SpendLimitsWithStreamingResponse(self)


class AsyncSpendLimits(AsyncAPIResource):
    @cached_property
    def effective(self) -> AsyncEffective:
        return AsyncEffective(self._client)

    @cached_property
    def increase_requests(self) -> AsyncIncreaseRequests:
        return AsyncIncreaseRequests(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncSpendLimitsWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://platform.claude.com/docs/en/api/sdks/python
        """
        return AsyncSpendLimitsWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncSpendLimitsWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://platform.claude.com/docs/en/api/sdks/python
        """
        return AsyncSpendLimitsWithStreamingResponse(self)


class SpendLimitsWithRawResponse:
    def __init__(self, spend_limits: SpendLimits) -> None:
        self._spend_limits = spend_limits

    @cached_property
    def effective(self) -> EffectiveWithRawResponse:
        return EffectiveWithRawResponse(self._spend_limits.effective)

    @cached_property
    def increase_requests(self) -> IncreaseRequestsWithRawResponse:
        return IncreaseRequestsWithRawResponse(self._spend_limits.increase_requests)


class AsyncSpendLimitsWithRawResponse:
    def __init__(self, spend_limits: AsyncSpendLimits) -> None:
        self._spend_limits = spend_limits

    @cached_property
    def effective(self) -> AsyncEffectiveWithRawResponse:
        return AsyncEffectiveWithRawResponse(self._spend_limits.effective)

    @cached_property
    def increase_requests(self) -> AsyncIncreaseRequestsWithRawResponse:
        return AsyncIncreaseRequestsWithRawResponse(self._spend_limits.increase_requests)


class SpendLimitsWithStreamingResponse:
    def __init__(self, spend_limits: SpendLimits) -> None:
        self._spend_limits = spend_limits

    @cached_property
    def effective(self) -> EffectiveWithStreamingResponse:
        return EffectiveWithStreamingResponse(self._spend_limits.effective)

    @cached_property
    def increase_requests(self) -> IncreaseRequestsWithStreamingResponse:
        return IncreaseRequestsWithStreamingResponse(self._spend_limits.increase_requests)


class AsyncSpendLimitsWithStreamingResponse:
    def __init__(self, spend_limits: AsyncSpendLimits) -> None:
        self._spend_limits = spend_limits

    @cached_property
    def effective(self) -> AsyncEffectiveWithStreamingResponse:
        return AsyncEffectiveWithStreamingResponse(self._spend_limits.effective)

    @cached_property
    def increase_requests(self) -> AsyncIncreaseRequestsWithStreamingResponse:
        return AsyncIncreaseRequestsWithStreamingResponse(self._spend_limits.increase_requests)
