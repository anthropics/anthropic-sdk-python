from __future__ import annotations

from .projects import (
    Projects,
    AsyncProjects,
    ProjectsWithRawResponse,
    AsyncProjectsWithRawResponse,
    ProjectsWithStreamingResponse,
    AsyncProjectsWithStreamingResponse,
)
from ......._compat import cached_property
from ......._resource import SyncAPIResource, AsyncAPIResource

__all__ = ["Chat", "AsyncChat"]


class Chat(SyncAPIResource):
    @cached_property
    def projects(self) -> Projects:
        return Projects(self._client)

    @cached_property
    def with_raw_response(self) -> ChatWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#accessing-raw-response-data-eg-headers
        """
        return ChatWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ChatWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#with_streaming_response
        """
        return ChatWithStreamingResponse(self)


class AsyncChat(AsyncAPIResource):
    @cached_property
    def projects(self) -> AsyncProjects:
        return AsyncProjects(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncChatWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#accessing-raw-response-data-eg-headers
        """
        return AsyncChatWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncChatWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#with_streaming_response
        """
        return AsyncChatWithStreamingResponse(self)


class ChatWithRawResponse:
    def __init__(self, chat: Chat) -> None:
        self._chat = chat

    @cached_property
    def projects(self) -> ProjectsWithRawResponse:
        return ProjectsWithRawResponse(self._chat.projects)


class AsyncChatWithRawResponse:
    def __init__(self, chat: AsyncChat) -> None:
        self._chat = chat

    @cached_property
    def projects(self) -> AsyncProjectsWithRawResponse:
        return AsyncProjectsWithRawResponse(self._chat.projects)


class ChatWithStreamingResponse:
    def __init__(self, chat: Chat) -> None:
        self._chat = chat

    @cached_property
    def projects(self) -> ProjectsWithStreamingResponse:
        return ProjectsWithStreamingResponse(self._chat.projects)


class AsyncChatWithStreamingResponse:
    def __init__(self, chat: AsyncChat) -> None:
        self._chat = chat

    @cached_property
    def projects(self) -> AsyncProjectsWithStreamingResponse:
        return AsyncProjectsWithStreamingResponse(self._chat.projects)
