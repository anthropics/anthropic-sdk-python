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

__all__ = ["PromptCaching", "AsyncPromptCaching"]


class PromptCaching(SyncAPIResource):
    @cached_property
    def messages(self) -> Messages:
        return Messages(self._client)

    @cached_property
    def with_raw_response(self) -> PromptCachingWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#accessing-raw-response-data-eg-headers
        """
        return PromptCachingWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> PromptCachingWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#with_streaming_response
        """
        return PromptCachingWithStreamingResponse(self)


class AsyncPromptCaching(AsyncAPIResource):
    @cached_property
    def messages(self) -> AsyncMessages:
        return AsyncMessages(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncPromptCachingWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#accessing-raw-response-data-eg-headers
        """
        return AsyncPromptCachingWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncPromptCachingWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#with_streaming_response
        """
        return AsyncPromptCachingWithStreamingResponse(self)


class PromptCachingWithRawResponse:
    def __init__(self, prompt_caching: PromptCaching) -> None:
        self._prompt_caching = prompt_caching

    @cached_property
    def messages(self) -> MessagesWithRawResponse:
        return MessagesWithRawResponse(self._prompt_caching.messages)


class AsyncPromptCachingWithRawResponse:
    def __init__(self, prompt_caching: AsyncPromptCaching) -> None:
        self._prompt_caching = prompt_caching

    @cached_property
    def messages(self) -> AsyncMessagesWithRawResponse:
        return AsyncMessagesWithRawResponse(self._prompt_caching.messages)


class PromptCachingWithStreamingResponse:
    def __init__(self, prompt_caching: PromptCaching) -> None:
        self._prompt_caching = prompt_caching

    @cached_property
    def messages(self) -> MessagesWithStreamingResponse:
        return MessagesWithStreamingResponse(self._prompt_caching.messages)


class AsyncPromptCachingWithStreamingResponse:
    def __init__(self, prompt_caching: AsyncPromptCaching) -> None:
        self._prompt_caching = prompt_caching

    @cached_property
    def messages(self) -> AsyncMessagesWithStreamingResponse:
        return AsyncMessagesWithStreamingResponse(self._prompt_caching.messages)
