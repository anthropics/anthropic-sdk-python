# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from .messages import (
    Messages,
    AsyncMessages,
    MessagesWithRawResponse,
    AsyncMessagesWithRawResponse,
    MessagesWithStreamingResponse,
    AsyncMessagesWithStreamingResponse,
)
from ...._compat import cached_property
from ...._resource import SyncAPIResource, AsyncAPIResource

__all__ = ["Tools", "AsyncTools"]


class Tools(SyncAPIResource):
    @cached_property
    def messages(self) -> Messages:
        return Messages(self._client)

    @cached_property
    def with_raw_response(self) -> ToolsWithRawResponse:
        return ToolsWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ToolsWithStreamingResponse:
        return ToolsWithStreamingResponse(self)


class AsyncTools(AsyncAPIResource):
    @cached_property
    def messages(self) -> AsyncMessages:
        return AsyncMessages(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncToolsWithRawResponse:
        return AsyncToolsWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncToolsWithStreamingResponse:
        return AsyncToolsWithStreamingResponse(self)


class ToolsWithRawResponse:
    def __init__(self, tools: Tools) -> None:
        self._tools = tools

    @cached_property
    def messages(self) -> MessagesWithRawResponse:
        return MessagesWithRawResponse(self._tools.messages)


class AsyncToolsWithRawResponse:
    def __init__(self, tools: AsyncTools) -> None:
        self._tools = tools

    @cached_property
    def messages(self) -> AsyncMessagesWithRawResponse:
        return AsyncMessagesWithRawResponse(self._tools.messages)


class ToolsWithStreamingResponse:
    def __init__(self, tools: Tools) -> None:
        self._tools = tools

    @cached_property
    def messages(self) -> MessagesWithStreamingResponse:
        return MessagesWithStreamingResponse(self._tools.messages)


class AsyncToolsWithStreamingResponse:
    def __init__(self, tools: AsyncTools) -> None:
        self._tools = tools

    @cached_property
    def messages(self) -> AsyncMessagesWithStreamingResponse:
        return AsyncMessagesWithStreamingResponse(self._tools.messages)
