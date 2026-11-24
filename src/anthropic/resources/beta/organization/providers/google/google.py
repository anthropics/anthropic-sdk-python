from __future__ import annotations

from ......_compat import cached_property
from ......_resource import SyncAPIResource, AsyncAPIResource
from .projects.projects import (
    Projects,
    AsyncProjects,
    ProjectsWithRawResponse,
    AsyncProjectsWithRawResponse,
    ProjectsWithStreamingResponse,
    AsyncProjectsWithStreamingResponse,
)

__all__ = ["Google", "AsyncGoogle"]


class Google(SyncAPIResource):
    @cached_property
    def projects(self) -> Projects:
        return Projects(self._client)

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
    def projects(self) -> AsyncProjects:
        return AsyncProjects(self._client)

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
    def projects(self) -> ProjectsWithRawResponse:
        return ProjectsWithRawResponse(self._google.projects)


class AsyncGoogleWithRawResponse:
    def __init__(self, google: AsyncGoogle) -> None:
        self._google = google

    @cached_property
    def projects(self) -> AsyncProjectsWithRawResponse:
        return AsyncProjectsWithRawResponse(self._google.projects)


class GoogleWithStreamingResponse:
    def __init__(self, google: Google) -> None:
        self._google = google

    @cached_property
    def projects(self) -> ProjectsWithStreamingResponse:
        return ProjectsWithStreamingResponse(self._google.projects)


class AsyncGoogleWithStreamingResponse:
    def __init__(self, google: AsyncGoogle) -> None:
        self._google = google

    @cached_property
    def projects(self) -> AsyncProjectsWithStreamingResponse:
        return AsyncProjectsWithStreamingResponse(self._google.projects)
