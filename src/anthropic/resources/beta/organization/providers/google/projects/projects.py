from __future__ import annotations

from ......._compat import cached_property
from .data_controls import (
    DataControls,
    AsyncDataControls,
    DataControlsWithRawResponse,
    AsyncDataControlsWithRawResponse,
    DataControlsWithStreamingResponse,
    AsyncDataControlsWithStreamingResponse,
)
from ......._resource import SyncAPIResource, AsyncAPIResource

__all__ = ["Projects", "AsyncProjects"]


class Projects(SyncAPIResource):
    @cached_property
    def data_controls(self) -> DataControls:
        return DataControls(self._client)

    @cached_property
    def with_raw_response(self) -> ProjectsWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://platform.claude.com/docs/en/api/sdks/python
        """
        return ProjectsWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ProjectsWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://platform.claude.com/docs/en/api/sdks/python
        """
        return ProjectsWithStreamingResponse(self)


class AsyncProjects(AsyncAPIResource):
    @cached_property
    def data_controls(self) -> AsyncDataControls:
        return AsyncDataControls(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncProjectsWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://platform.claude.com/docs/en/api/sdks/python
        """
        return AsyncProjectsWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncProjectsWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://platform.claude.com/docs/en/api/sdks/python
        """
        return AsyncProjectsWithStreamingResponse(self)


class ProjectsWithRawResponse:
    def __init__(self, projects: Projects) -> None:
        self._projects = projects

    @cached_property
    def data_controls(self) -> DataControlsWithRawResponse:
        return DataControlsWithRawResponse(self._projects.data_controls)


class AsyncProjectsWithRawResponse:
    def __init__(self, projects: AsyncProjects) -> None:
        self._projects = projects

    @cached_property
    def data_controls(self) -> AsyncDataControlsWithRawResponse:
        return AsyncDataControlsWithRawResponse(self._projects.data_controls)


class ProjectsWithStreamingResponse:
    def __init__(self, projects: Projects) -> None:
        self._projects = projects

    @cached_property
    def data_controls(self) -> DataControlsWithStreamingResponse:
        return DataControlsWithStreamingResponse(self._projects.data_controls)


class AsyncProjectsWithStreamingResponse:
    def __init__(self, projects: AsyncProjects) -> None:
        self._projects = projects

    @cached_property
    def data_controls(self) -> AsyncDataControlsWithStreamingResponse:
        return AsyncDataControlsWithStreamingResponse(self._projects.data_controls)
