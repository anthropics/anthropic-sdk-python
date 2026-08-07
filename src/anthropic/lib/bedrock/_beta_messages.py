# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Any, Iterable

from ... import _legacy_response
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import to_streamed_response_wrapper, async_to_streamed_response_wrapper
from ...resources.beta import Messages as FirstPartyMessagesAPI, AsyncMessages as FirstPartyAsyncMessagesAPI

__all__ = ["Messages", "AsyncMessages"]


# Fields that Bedrock's stricter API validation rejects
# - parsed_output: Added by tool_runner SDK to text blocks for structured output tracking
# - caller: Added to tool_use blocks for code execution features
BEDROCK_UNSUPPORTED_FIELDS = {"parsed_output", "caller"}


def _sanitize_for_bedrock(messages: Iterable[Any] | None) -> list[Any] | None:
    """Strip Bedrock-unsupported fields from message content blocks.

    The tool_runner SDK adds internal tracking fields that Bedrock's stricter
    API validation rejects with 400 errors. This function sanitizes messages
    before sending to Bedrock.

    Args:
        messages: Iterable of message objects (dicts or Pydantic models)

    Returns:
        Sanitized list of messages with unsupported fields removed, or None if input is None
    """
    if messages is None:
        return None

    sanitized = []
    for msg in messages:
        if isinstance(msg, dict):
            # Handle dict messages
            sanitized_msg = dict(msg)
            if "content" in sanitized_msg and isinstance(sanitized_msg["content"], list):
                sanitized_content = []
                for block in sanitized_msg["content"]:
                    if isinstance(block, dict):
                        # Remove unsupported fields from dict blocks
                        sanitized_block = {k: v for k, v in block.items() if k not in BEDROCK_UNSUPPORTED_FIELDS}
                        sanitized_content.append(sanitized_block)
                    elif hasattr(block, "model_dump"):
                        # Handle Pydantic models - convert to dict and remove unsupported fields
                        block_dict = block.model_dump()
                        for field in BEDROCK_UNSUPPORTED_FIELDS:
                            block_dict.pop(field, None)
                        sanitized_content.append(block_dict)
                    else:
                        # Keep other types as-is
                        sanitized_content.append(block)
                sanitized_msg["content"] = sanitized_content
            sanitized.append(sanitized_msg)
        elif hasattr(msg, "model_dump"):
            # Handle Pydantic message models
            msg_dict = msg.model_dump()
            if "content" in msg_dict and isinstance(msg_dict["content"], list):
                sanitized_content = []
                for block in msg_dict["content"]:
                    if isinstance(block, dict):
                        sanitized_block = {k: v for k, v in block.items() if k not in BEDROCK_UNSUPPORTED_FIELDS}
                        sanitized_content.append(sanitized_block)
                    else:
                        sanitized_content.append(block)
                msg_dict["content"] = sanitized_content
            sanitized.append(msg_dict)
        else:
            # Keep other message types as-is
            sanitized.append(msg)

    return sanitized


class Messages(SyncAPIResource):
    def create(self, *args, **kwargs):
        """Create a message with sanitization for Bedrock compatibility."""
        if "messages" in kwargs:
            kwargs["messages"] = _sanitize_for_bedrock(kwargs["messages"])
        return FirstPartyMessagesAPI.create(self, *args, **kwargs)

    def parse(self, *args, **kwargs):
        """Parse a message with sanitization for Bedrock compatibility."""
        if "messages" in kwargs:
            kwargs["messages"] = _sanitize_for_bedrock(kwargs["messages"])
        return FirstPartyMessagesAPI.parse(self, *args, **kwargs)

    def stream(self, *args, **kwargs):
        """Stream a message with sanitization for Bedrock compatibility."""
        if "messages" in kwargs:
            kwargs["messages"] = _sanitize_for_bedrock(kwargs["messages"])
        return FirstPartyMessagesAPI.stream(self, *args, **kwargs)

    # tool_runner delegates to create/parse/stream internally, so it benefits
    # from the sanitization automatically through method resolution
    tool_runner = FirstPartyMessagesAPI.tool_runner

    @cached_property
    def with_raw_response(self) -> MessagesWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#accessing-raw-response-data-eg-headers
        """
        return MessagesWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> MessagesWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#with_streaming_response
        """
        return MessagesWithStreamingResponse(self)


class AsyncMessages(AsyncAPIResource):
    async def create(self, *args, **kwargs):
        """Create a message with sanitization for Bedrock compatibility."""
        if "messages" in kwargs:
            kwargs["messages"] = _sanitize_for_bedrock(kwargs["messages"])
        return await FirstPartyAsyncMessagesAPI.create(self, *args, **kwargs)

    async def parse(self, *args, **kwargs):
        """Parse a message with sanitization for Bedrock compatibility."""
        if "messages" in kwargs:
            kwargs["messages"] = _sanitize_for_bedrock(kwargs["messages"])
        return await FirstPartyAsyncMessagesAPI.parse(self, *args, **kwargs)

    async def stream(self, *args, **kwargs):
        """Stream a message with sanitization for Bedrock compatibility."""
        if "messages" in kwargs:
            kwargs["messages"] = _sanitize_for_bedrock(kwargs["messages"])
        return await FirstPartyAsyncMessagesAPI.stream(self, *args, **kwargs)

    # tool_runner delegates to create/parse/stream internally, so it benefits
    # from the sanitization automatically through method resolution
    tool_runner = FirstPartyAsyncMessagesAPI.tool_runner

    @cached_property
    def with_raw_response(self) -> AsyncMessagesWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#accessing-raw-response-data-eg-headers
        """
        return AsyncMessagesWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncMessagesWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#with_streaming_response
        """
        return AsyncMessagesWithStreamingResponse(self)


class MessagesWithRawResponse:
    def __init__(self, messages: Messages) -> None:
        self._messages = messages

        self.create = _legacy_response.to_raw_response_wrapper(
            messages.create,
        )


class AsyncMessagesWithRawResponse:
    def __init__(self, messages: AsyncMessages) -> None:
        self._messages = messages

        self.create = _legacy_response.async_to_raw_response_wrapper(
            messages.create,
        )


class MessagesWithStreamingResponse:
    def __init__(self, messages: Messages) -> None:
        self._messages = messages

        self.create = to_streamed_response_wrapper(
            messages.create,
        )


class AsyncMessagesWithStreamingResponse:
    def __init__(self, messages: AsyncMessages) -> None:
        self._messages = messages

        self.create = async_to_streamed_response_wrapper(
            messages.create,
        )
