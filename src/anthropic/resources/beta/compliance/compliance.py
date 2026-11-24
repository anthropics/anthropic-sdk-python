from __future__ import annotations

from ...._compat import cached_property
from ...._resource import SyncAPIResource, AsyncAPIResource
from .review.review import (
    Review,
    AsyncReview,
    ReviewWithRawResponse,
    AsyncReviewWithRawResponse,
    ReviewWithStreamingResponse,
    AsyncReviewWithStreamingResponse,
)

__all__ = ["Compliance", "AsyncCompliance"]


class Compliance(SyncAPIResource):
    @cached_property
    def review(self) -> Review:
        return Review(self._client)

    @cached_property
    def with_raw_response(self) -> ComplianceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://platform.claude.com/docs/en/api/sdks/python
        """
        return ComplianceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ComplianceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://platform.claude.com/docs/en/api/sdks/python
        """
        return ComplianceWithStreamingResponse(self)


class AsyncCompliance(AsyncAPIResource):
    @cached_property
    def review(self) -> AsyncReview:
        return AsyncReview(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncComplianceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://platform.claude.com/docs/en/api/sdks/python
        """
        return AsyncComplianceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncComplianceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://platform.claude.com/docs/en/api/sdks/python
        """
        return AsyncComplianceWithStreamingResponse(self)


class ComplianceWithRawResponse:
    def __init__(self, compliance: Compliance) -> None:
        self._compliance = compliance

    @cached_property
    def review(self) -> ReviewWithRawResponse:
        return ReviewWithRawResponse(self._compliance.review)


class AsyncComplianceWithRawResponse:
    def __init__(self, compliance: AsyncCompliance) -> None:
        self._compliance = compliance

    @cached_property
    def review(self) -> AsyncReviewWithRawResponse:
        return AsyncReviewWithRawResponse(self._compliance.review)


class ComplianceWithStreamingResponse:
    def __init__(self, compliance: Compliance) -> None:
        self._compliance = compliance

    @cached_property
    def review(self) -> ReviewWithStreamingResponse:
        return ReviewWithStreamingResponse(self._compliance.review)


class AsyncComplianceWithStreamingResponse:
    def __init__(self, compliance: AsyncCompliance) -> None:
        self._compliance = compliance

    @cached_property
    def review(self) -> AsyncReviewWithStreamingResponse:
        return AsyncReviewWithStreamingResponse(self._compliance.review)
