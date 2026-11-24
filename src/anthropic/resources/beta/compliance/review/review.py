from __future__ import annotations

from .cases import (
    Cases,
    AsyncCases,
    CasesWithRawResponse,
    AsyncCasesWithRawResponse,
    CasesWithStreamingResponse,
    AsyncCasesWithStreamingResponse,
)
from .items import (
    Items,
    AsyncItems,
    ItemsWithRawResponse,
    AsyncItemsWithRawResponse,
    ItemsWithStreamingResponse,
    AsyncItemsWithStreamingResponse,
)
from .notices import (
    Notices,
    AsyncNotices,
    NoticesWithRawResponse,
    AsyncNoticesWithRawResponse,
    NoticesWithStreamingResponse,
    AsyncNoticesWithStreamingResponse,
)
from ....._compat import cached_property
from ....._resource import SyncAPIResource, AsyncAPIResource

__all__ = ["Review", "AsyncReview"]


class Review(SyncAPIResource):
    @cached_property
    def cases(self) -> Cases:
        return Cases(self._client)

    @cached_property
    def notices(self) -> Notices:
        return Notices(self._client)

    @cached_property
    def items(self) -> Items:
        return Items(self._client)

    @cached_property
    def with_raw_response(self) -> ReviewWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://platform.claude.com/docs/en/api/sdks/python
        """
        return ReviewWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ReviewWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://platform.claude.com/docs/en/api/sdks/python
        """
        return ReviewWithStreamingResponse(self)


class AsyncReview(AsyncAPIResource):
    @cached_property
    def cases(self) -> AsyncCases:
        return AsyncCases(self._client)

    @cached_property
    def notices(self) -> AsyncNotices:
        return AsyncNotices(self._client)

    @cached_property
    def items(self) -> AsyncItems:
        return AsyncItems(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncReviewWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://platform.claude.com/docs/en/api/sdks/python
        """
        return AsyncReviewWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncReviewWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://platform.claude.com/docs/en/api/sdks/python
        """
        return AsyncReviewWithStreamingResponse(self)


class ReviewWithRawResponse:
    def __init__(self, review: Review) -> None:
        self._review = review

    @cached_property
    def cases(self) -> CasesWithRawResponse:
        return CasesWithRawResponse(self._review.cases)

    @cached_property
    def notices(self) -> NoticesWithRawResponse:
        return NoticesWithRawResponse(self._review.notices)

    @cached_property
    def items(self) -> ItemsWithRawResponse:
        return ItemsWithRawResponse(self._review.items)


class AsyncReviewWithRawResponse:
    def __init__(self, review: AsyncReview) -> None:
        self._review = review

    @cached_property
    def cases(self) -> AsyncCasesWithRawResponse:
        return AsyncCasesWithRawResponse(self._review.cases)

    @cached_property
    def notices(self) -> AsyncNoticesWithRawResponse:
        return AsyncNoticesWithRawResponse(self._review.notices)

    @cached_property
    def items(self) -> AsyncItemsWithRawResponse:
        return AsyncItemsWithRawResponse(self._review.items)


class ReviewWithStreamingResponse:
    def __init__(self, review: Review) -> None:
        self._review = review

    @cached_property
    def cases(self) -> CasesWithStreamingResponse:
        return CasesWithStreamingResponse(self._review.cases)

    @cached_property
    def notices(self) -> NoticesWithStreamingResponse:
        return NoticesWithStreamingResponse(self._review.notices)

    @cached_property
    def items(self) -> ItemsWithStreamingResponse:
        return ItemsWithStreamingResponse(self._review.items)


class AsyncReviewWithStreamingResponse:
    def __init__(self, review: AsyncReview) -> None:
        self._review = review

    @cached_property
    def cases(self) -> AsyncCasesWithStreamingResponse:
        return AsyncCasesWithStreamingResponse(self._review.cases)

    @cached_property
    def notices(self) -> AsyncNoticesWithStreamingResponse:
        return AsyncNoticesWithStreamingResponse(self._review.notices)

    @cached_property
    def items(self) -> AsyncItemsWithStreamingResponse:
        return AsyncItemsWithStreamingResponse(self._review.items)
