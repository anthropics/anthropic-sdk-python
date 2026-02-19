# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import TYPE_CHECKING, List, Union, Iterable, Optional
from functools import partial
from typing_extensions import Literal

import httpx

from ... import _legacy_response
from ..._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import to_streamed_response_wrapper, async_to_streamed_response_wrapper
from ..._streaming import Stream, AsyncStream
from ...types.beta import BetaMessage, BetaRawMessageStreamEvent
from ...lib.streaming import (
    BetaMessageStream,
    BetaAsyncMessageStream,
    BetaMessageStreamManager,
    BetaAsyncMessageStreamManager,
)
from ...resources.beta import Messages as FirstPartyMessagesAPI, AsyncMessages as FirstPartyAsyncMessagesAPI
from ...types.model_param import ModelParam
from ...types.anthropic_beta_param import AnthropicBetaParam
from ...types.beta.beta_message_param import BetaMessageParam
from ...types.beta.beta_metadata_param import BetaMetadataParam
from ...types.beta.beta_text_block_param import BetaTextBlockParam
from ...types.beta.beta_tool_union_param import BetaToolUnionParam
from ...types.beta.beta_tool_choice_param import BetaToolChoiceParam
from ...types.beta.beta_thinking_config_param import BetaThinkingConfigParam
from ...types.beta.beta_request_mcp_server_url_definition_param import BetaRequestMCPServerURLDefinitionParam

if TYPE_CHECKING:
    pass

__all__ = ["Messages", "AsyncMessages"]


class Messages(SyncAPIResource):
    # Delegate count_tokens to the first-party implementation
    count_tokens = FirstPartyMessagesAPI.count_tokens

    def create(
        self,
        *,
        max_tokens: int,
        messages: Iterable[BetaMessageParam],
        model: ModelParam,
        container: Optional[str] | NotGiven = NOT_GIVEN,
        mcp_servers: Iterable[BetaRequestMCPServerURLDefinitionParam] | NotGiven = NOT_GIVEN,
        metadata: BetaMetadataParam | NotGiven = NOT_GIVEN,
        service_tier: Literal["auto", "standard_only"] | NotGiven = NOT_GIVEN,
        stop_sequences: List[str] | NotGiven = NOT_GIVEN,
        stream: Literal[False] | Literal[True] | NotGiven = NOT_GIVEN,
        system: Union[str, Iterable[BetaTextBlockParam]] | NotGiven = NOT_GIVEN,
        temperature: float | NotGiven = NOT_GIVEN,
        thinking: BetaThinkingConfigParam | NotGiven = NOT_GIVEN,
        tool_choice: BetaToolChoiceParam | NotGiven = NOT_GIVEN,
        tools: Iterable[BetaToolUnionParam] | NotGiven = NOT_GIVEN,
        top_k: int | NotGiven = NOT_GIVEN,
        top_p: float | NotGiven = NOT_GIVEN,
        betas: List[AnthropicBetaParam] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> BetaMessage | Stream[BetaRawMessageStreamEvent]:
        """
        Create a message using the Vertex AI endpoint.

        When streaming is enabled, this wraps the response in BetaMessageStream
        for proper event accumulation, particularly for tool_use inputs.
        """
        # If streaming is enabled, wrap the response in BetaMessageStream for accumulation
        if stream is True:
            # Get the raw stream from the first-party API
            raw_stream = FirstPartyMessagesAPI.create(
                self,
                max_tokens=max_tokens,
                messages=messages,
                model=model,
                container=container,
                mcp_servers=mcp_servers,
                metadata=metadata,
                service_tier=service_tier,
                stop_sequences=stop_sequences,
                stream=True,
                system=system,
                temperature=temperature,
                thinking=thinking,
                tool_choice=tool_choice,
                tools=tools,
                top_k=top_k,
                top_p=top_p,
                betas=betas,
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
            )
            # Wrap in BetaMessageStream which has the accumulation logic
            # This ensures tool inputs are properly accumulated from delta events
            return BetaMessageStream(raw_stream)

        # For non-streaming, delegate normally
        return FirstPartyMessagesAPI.create(
            self,
            max_tokens=max_tokens,
            messages=messages,
            model=model,
            container=container,
            mcp_servers=mcp_servers,
            metadata=metadata,
            service_tier=service_tier,
            stop_sequences=stop_sequences,
            stream=stream,
            system=system,
            temperature=temperature,
            thinking=thinking,
            tool_choice=tool_choice,
            tools=tools,
            top_k=top_k,
            top_p=top_p,
            betas=betas,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )

    def stream(
        self,
        *,
        max_tokens: int,
        messages: Iterable[BetaMessageParam],
        model: ModelParam,
        container: Optional[str] | NotGiven = NOT_GIVEN,
        mcp_servers: Iterable[BetaRequestMCPServerURLDefinitionParam] | NotGiven = NOT_GIVEN,
        metadata: BetaMetadataParam | NotGiven = NOT_GIVEN,
        service_tier: Literal["auto", "standard_only"] | NotGiven = NOT_GIVEN,
        stop_sequences: List[str] | NotGiven = NOT_GIVEN,
        system: Union[str, Iterable[BetaTextBlockParam]] | NotGiven = NOT_GIVEN,
        temperature: float | NotGiven = NOT_GIVEN,
        thinking: BetaThinkingConfigParam | NotGiven = NOT_GIVEN,
        tool_choice: BetaToolChoiceParam | NotGiven = NOT_GIVEN,
        tools: Iterable[BetaToolUnionParam] | NotGiven = NOT_GIVEN,
        top_k: int | NotGiven = NOT_GIVEN,
        top_p: float | NotGiven = NOT_GIVEN,
        betas: List[AnthropicBetaParam] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> BetaMessageStreamManager:
        """
        Create a streaming message using the Vertex AI endpoint.

        This method ensures that the response is properly wrapped in a BetaMessageStreamManager
        for correct event accumulation, particularly for tool_use inputs.
        """
        # Create a function that makes the streaming request
        make_request = partial(
            self.create,
            max_tokens=max_tokens,
            messages=messages,
            model=model,
            container=container,
            mcp_servers=mcp_servers,
            metadata=metadata,
            service_tier=service_tier,
            stop_sequences=stop_sequences,
            stream=True,  # Force streaming
            system=system,
            temperature=temperature,
            thinking=thinking,
            tool_choice=tool_choice,
            tools=tools,
            top_k=top_k,
            top_p=top_p,
            betas=betas,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )

        # Return the proper stream manager wrapper
        return BetaMessageStreamManager(make_request)

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
    # Delegate count_tokens to the first-party implementation
    count_tokens = FirstPartyAsyncMessagesAPI.count_tokens

    async def create(
        self,
        *,
        max_tokens: int,
        messages: Iterable[BetaMessageParam],
        model: ModelParam,
        container: Optional[str] | NotGiven = NOT_GIVEN,
        mcp_servers: Iterable[BetaRequestMCPServerURLDefinitionParam] | NotGiven = NOT_GIVEN,
        metadata: BetaMetadataParam | NotGiven = NOT_GIVEN,
        service_tier: Literal["auto", "standard_only"] | NotGiven = NOT_GIVEN,
        stop_sequences: List[str] | NotGiven = NOT_GIVEN,
        stream: Literal[False] | Literal[True] | NotGiven = NOT_GIVEN,
        system: Union[str, Iterable[BetaTextBlockParam]] | NotGiven = NOT_GIVEN,
        temperature: float | NotGiven = NOT_GIVEN,
        thinking: BetaThinkingConfigParam | NotGiven = NOT_GIVEN,
        tool_choice: BetaToolChoiceParam | NotGiven = NOT_GIVEN,
        tools: Iterable[BetaToolUnionParam] | NotGiven = NOT_GIVEN,
        top_k: int | NotGiven = NOT_GIVEN,
        top_p: float | NotGiven = NOT_GIVEN,
        betas: List[AnthropicBetaParam] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> BetaMessage | AsyncStream[BetaRawMessageStreamEvent]:
        """
        Create a message using the Vertex AI endpoint.

        When streaming is enabled, this properly wraps the response in BetaAsyncMessageStream
        for proper event accumulation, particularly for tool_use inputs.
        """
        # If streaming is enabled, wrap the response in BetaAsyncMessageStream for accumulation
        if stream is True:
            # Get the raw stream from the first-party API
            raw_stream = await FirstPartyAsyncMessagesAPI.create(
                self,
                max_tokens=max_tokens,
                messages=messages,
                model=model,
                container=container,
                mcp_servers=mcp_servers,
                metadata=metadata,
                service_tier=service_tier,
                stop_sequences=stop_sequences,
                stream=True,
                system=system,
                temperature=temperature,
                thinking=thinking,
                tool_choice=tool_choice,
                tools=tools,
                top_k=top_k,
                top_p=top_p,
                betas=betas,
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
            )
            # Wrap in BetaAsyncMessageStream which has the accumulation logic
            # This ensures tool inputs are properly accumulated from delta events
            return BetaAsyncMessageStream(raw_stream)

        # For non-streaming, delegate normally
        return await FirstPartyAsyncMessagesAPI.create(
            self,
            max_tokens=max_tokens,
            messages=messages,
            model=model,
            container=container,
            mcp_servers=mcp_servers,
            metadata=metadata,
            service_tier=service_tier,
            stop_sequences=stop_sequences,
            stream=stream,
            system=system,
            temperature=temperature,
            thinking=thinking,
            tool_choice=tool_choice,
            tools=tools,
            top_k=top_k,
            top_p=top_p,
            betas=betas,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )

    def stream(
        self,
        *,
        max_tokens: int,
        messages: Iterable[BetaMessageParam],
        model: ModelParam,
        container: Optional[str] | NotGiven = NOT_GIVEN,
        mcp_servers: Iterable[BetaRequestMCPServerURLDefinitionParam] | NotGiven = NOT_GIVEN,
        metadata: BetaMetadataParam | NotGiven = NOT_GIVEN,
        service_tier: Literal["auto", "standard_only"] | NotGiven = NOT_GIVEN,
        stop_sequences: List[str] | NotGiven = NOT_GIVEN,
        system: Union[str, Iterable[BetaTextBlockParam]] | NotGiven = NOT_GIVEN,
        temperature: float | NotGiven = NOT_GIVEN,
        thinking: BetaThinkingConfigParam | NotGiven = NOT_GIVEN,
        tool_choice: BetaToolChoiceParam | NotGiven = NOT_GIVEN,
        tools: Iterable[BetaToolUnionParam] | NotGiven = NOT_GIVEN,
        top_k: int | NotGiven = NOT_GIVEN,
        top_p: float | NotGiven = NOT_GIVEN,
        betas: List[AnthropicBetaParam] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> BetaAsyncMessageStreamManager:
        """
        Create a streaming message using the Vertex AI endpoint.

        This method ensures that the response is properly wrapped in a BetaAsyncMessageStreamManager
        for correct event accumulation, particularly for tool_use inputs.
        """

        # Create an async function that makes the streaming request
        async def make_request():
            return await self.create(
                max_tokens=max_tokens,
                messages=messages,
                model=model,
                container=container,
                mcp_servers=mcp_servers,
                metadata=metadata,
                service_tier=service_tier,
                stop_sequences=stop_sequences,
                stream=True,  # Force streaming
                system=system,
                temperature=temperature,
                thinking=thinking,
                tool_choice=tool_choice,
                tools=tools,
                top_k=top_k,
                top_p=top_p,
                betas=betas,
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
            )

        # Return the proper async stream manager wrapper
        return BetaAsyncMessageStreamManager(make_request())

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
