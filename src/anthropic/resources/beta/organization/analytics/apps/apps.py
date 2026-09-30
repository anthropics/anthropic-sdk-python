from __future__ import annotations

from .chat.chat import (
    Chat,
    AsyncChat,
    ChatWithRawResponse,
    AsyncChatWithRawResponse,
    ChatWithStreamingResponse,
    AsyncChatWithStreamingResponse,
)
from ......_compat import cached_property
from ......_resource import SyncAPIResource, AsyncAPIResource

__all__ = ["Apps", "AsyncApps"]


class Apps(SyncAPIResource):
    @cached_property
    def chat(self) -> Chat:
        return Chat(self._client)

    @cached_property
    def with_raw_response(self) -> AppsWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#accessing-raw-response-data-eg-headers
        """
        return AppsWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AppsWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#with_streaming_response
        """
        return AppsWithStreamingResponse(self)


class AsyncApps(AsyncAPIResource):
    @cached_property
    def chat(self) -> AsyncChat:
        return AsyncChat(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncAppsWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#accessing-raw-response-data-eg-headers
        """
        return AsyncAppsWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncAppsWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#with_streaming_response
        """
        return AsyncAppsWithStreamingResponse(self)


class AppsWithRawResponse:
    def __init__(self, apps: Apps) -> None:
        self._apps = apps

    @cached_property
    def chat(self) -> ChatWithRawResponse:
        return ChatWithRawResponse(self._apps.chat)


class AsyncAppsWithRawResponse:
    def __init__(self, apps: AsyncApps) -> None:
        self._apps = apps

    @cached_property
    def chat(self) -> AsyncChatWithRawResponse:
        return AsyncChatWithRawResponse(self._apps.chat)


class AppsWithStreamingResponse:
    def __init__(self, apps: Apps) -> None:
        self._apps = apps

    @cached_property
    def chat(self) -> ChatWithStreamingResponse:
        return ChatWithStreamingResponse(self._apps.chat)


class AsyncAppsWithStreamingResponse:
    def __init__(self, apps: AsyncApps) -> None:
        self._apps = apps

    @cached_property
    def chat(self) -> AsyncChatWithStreamingResponse:
        return AsyncChatWithStreamingResponse(self._apps.chat)
