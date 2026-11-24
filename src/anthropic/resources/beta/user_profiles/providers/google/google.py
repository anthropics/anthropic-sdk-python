from __future__ import annotations

from ......_compat import cached_property
from .data_controls import (
    DataControls,
    AsyncDataControls,
    DataControlsWithRawResponse,
    AsyncDataControlsWithRawResponse,
    DataControlsWithStreamingResponse,
    AsyncDataControlsWithStreamingResponse,
)
from ......_resource import SyncAPIResource, AsyncAPIResource

__all__ = ["Google", "AsyncGoogle"]


class Google(SyncAPIResource):
    @cached_property
    def data_controls(self) -> DataControls:
        return DataControls(self._client)

    @cached_property
    def with_raw_response(self) -> GoogleWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://platform.claude.com/docs/en/api/sdks/python
        """
        return GoogleWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> GoogleWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://platform.claude.com/docs/en/api/sdks/python
        """
        return GoogleWithStreamingResponse(self)


class AsyncGoogle(AsyncAPIResource):
    @cached_property
    def data_controls(self) -> AsyncDataControls:
        return AsyncDataControls(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncGoogleWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://platform.claude.com/docs/en/api/sdks/python
        """
        return AsyncGoogleWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncGoogleWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://platform.claude.com/docs/en/api/sdks/python
        """
        return AsyncGoogleWithStreamingResponse(self)


class GoogleWithRawResponse:
    def __init__(self, google: Google) -> None:
        self._google = google

    @cached_property
    def data_controls(self) -> DataControlsWithRawResponse:
        return DataControlsWithRawResponse(self._google.data_controls)


class AsyncGoogleWithRawResponse:
    def __init__(self, google: AsyncGoogle) -> None:
        self._google = google

    @cached_property
    def data_controls(self) -> AsyncDataControlsWithRawResponse:
        return AsyncDataControlsWithRawResponse(self._google.data_controls)


class GoogleWithStreamingResponse:
    def __init__(self, google: Google) -> None:
        self._google = google

    @cached_property
    def data_controls(self) -> DataControlsWithStreamingResponse:
        return DataControlsWithStreamingResponse(self._google.data_controls)


class AsyncGoogleWithStreamingResponse:
    def __init__(self, google: AsyncGoogle) -> None:
        self._google = google

    @cached_property
    def data_controls(self) -> AsyncDataControlsWithStreamingResponse:
        return AsyncDataControlsWithStreamingResponse(self._google.data_controls)
