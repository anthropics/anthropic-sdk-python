# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import warnings
from typing import Any, List, Union, Literal, Iterable, Optional, Awaitable, cast
from typing_extensions import Literal

import httpx
from pydantic import TypeAdapter

from anthropic._streaming import AsyncStream

from ... import _legacy_response
from ..._types import NOT_GIVEN, Body, Omit, Query, Headers, NotGiven, SequenceNotStr, omit
from ..._utils import is_given, maybe_transform, strip_not_given
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import to_streamed_response_wrapper, async_to_streamed_response_wrapper
from ...types.beta import BetaMessage, message_create_params
from ..._exceptions import AnthropicError
from ..._base_client import make_request_options
from ..._utils._utils import is_dict
from ...lib.streaming import BetaAsyncMessageStreamManager
from ...resources.beta import Messages as FirstPartyMessagesAPI, AsyncMessages as FirstPartyAsyncMessagesAPI
from ...types.model_param import ModelParam
from ...lib._parse._response import ResponseFormatT
from ...lib._parse._transform import transform_schema
from ...lib._stainless_helpers import stainless_helper_header as _stainless_helper_header
from ...types.anthropic_beta_param import AnthropicBetaParam
from ...types.beta.beta_message_param import BetaMessageParam
from ...types.beta.beta_metadata_param import BetaMetadataParam
from ...types.beta.beta_text_block_param import BetaTextBlockParam
from ...types.beta.beta_tool_union_param import BetaToolUnionParam
from ...types.beta.beta_tool_choice_param import BetaToolChoiceParam
from ...types.beta.beta_output_config_param import BetaOutputConfigParam
from ...types.beta.beta_thinking_config_param import BetaThinkingConfigParam
from ...types.beta.beta_json_output_format_param import BetaJSONOutputFormatParam
from ...types.beta.beta_raw_message_stream_event import BetaRawMessageStreamEvent
from ...types.beta.beta_cache_control_ephemeral_param import BetaCacheControlEphemeralParam
from ...types.beta.beta_context_management_config_param import BetaContextManagementConfigParam
from ...types.beta.beta_request_mcp_server_url_definition_param import BetaRequestMCPServerURLDefinitionParam

# ---------------------------------------------------------------------------
# Helpers mirrored from first-party resources.beta.messages.messages
# ---------------------------------------------------------------------------


def _validate_output_config_conflict(
    output_config: BetaOutputConfigParam | Omit,
    output_format: object,
) -> None:
    if is_given(output_format) and output_format is not None and is_given(output_config):
        if "format" in output_config and output_config["format"] is not None:
            raise AnthropicError(
                "Both output_format and output_config.format were provided. "
                "Please use only output_config.format (output_format is deprecated).",
            )


def _merge_output_configs(
    output_config: BetaOutputConfigParam | Omit,
    output_format: Optional[BetaJSONOutputFormatParam] | Omit,
) -> BetaOutputConfigParam | Omit:
    if is_given(output_format):
        if is_given(output_config):
            return {**output_config, "format": output_format}
        else:
            return {"format": output_format}
    return output_config


def _warn_output_format_deprecated(output_format: object) -> None:
    if is_given(output_format) and output_format is not None:
        warnings.warn(
            "The 'output_format' parameter is deprecated. Please use 'output_config.format' instead.",
            DeprecationWarning,
            stacklevel=4,
        )


# ---------------------------------------------------------------------------
# Deferred request wrapper for async stream
# ---------------------------------------------------------------------------


class _DeferredAsyncStreamRequest(Awaitable[Any]):
    """Defers the await of an async client method until __await__ is called.

    BetaAsyncMessageStreamManager.__aenter__ awaits self.__api_request, so
    passing a _DeferredAsyncStreamRequest defers the HTTP call to inside
    the async with block -- ensuring respx mocks are active for tests.
    """

    __slots__ = ("_client", "_path", "_kwargs")

    def __init__(
        self,
        client: AsyncAPIResource,
        path: str,
        *,
        body: Any,
        options: Any,
        cast_to: Any,
        stream: bool,
        stream_cls: Any,
    ) -> None:
        self._client = client
        self._path = path
        self._kwargs = {
            "body": body,
            "options": options,
            "cast_to": cast_to,
            "stream": stream,
            "stream_cls": stream_cls,
        }

    def __await__(self) -> Any:
        return self._client._post(self._path, **self._kwargs).__await__()


# ---------------------------------------------------------------------------
# Sync Messages
# ---------------------------------------------------------------------------


class Messages(SyncAPIResource):
    create = FirstPartyMessagesAPI.create
    stream = FirstPartyMessagesAPI.stream

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


# ---------------------------------------------------------------------------
# Async Messages — own implementation (not alias) because AsyncAPIResource._post
# is an async method that must be awaited, unlike the sync path
# ---------------------------------------------------------------------------


class AsyncMessages(AsyncAPIResource):
    create = FirstPartyAsyncMessagesAPI.create

    def stream(
        self,
        *,
        max_tokens: int,
        messages: Iterable[BetaMessageParam],
        model: ModelParam,
        cache_control: Optional[BetaCacheControlEphemeralParam] | Omit = omit,
        metadata: BetaMetadataParam | Omit = omit,
        output_config: BetaOutputConfigParam | Omit = omit,
        output_format: None | type[ResponseFormatT] | BetaJSONOutputFormatParam | Omit = omit,
        container: Optional[message_create_params.Container] | Omit = omit,
        context_management: Optional[BetaContextManagementConfigParam] | Omit = omit,
        inference_geo: Optional[str] | Omit = omit,
        mcp_servers: Iterable[BetaRequestMCPServerURLDefinitionParam] | Omit = omit,
        service_tier: Literal["auto", "standard_only"] | Omit = omit,
        speed: Optional[Literal["standard", "fast"]] | Omit = omit,
        stop_sequences: SequenceNotStr[str] | Omit = omit,
        system: Union[str, Iterable[BetaTextBlockParam]] | Omit = omit,
        temperature: float | Omit = omit,
        thinking: BetaThinkingConfigParam | Omit = omit,
        tool_choice: BetaToolChoiceParam | Omit = omit,
        tools: Iterable[BetaToolUnionParam] | Omit = omit,
        top_k: int | Omit = omit,
        top_p: float | Omit = omit,
        betas: List[AnthropicBetaParam] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> BetaAsyncMessageStreamManager[ResponseFormatT]:
        """
        Create a async stream.

        Sends a POST request to the messages endpoint with the stream parameter set to True.
        Returns a context manager that yields a stream object.
        """
        _validate_output_config_conflict(output_config, output_format)
        _warn_output_format_deprecated(output_format)

        extra_headers = {
            "X-Stainless-Helper-Method": "stream",
            "X-Stainless-Stream-Helper": "beta.messages",
            **strip_not_given({"anthropic-beta": ",".join(str(e) for e in betas) if is_given(betas) else NOT_GIVEN}),
            **_stainless_helper_header(tools, messages),
            **(extra_headers or {}),
        }

        transformed_output_format: BetaJSONOutputFormatParam | Omit = omit

        if is_dict(output_format):
            transformed_output_format = cast(BetaJSONOutputFormatParam, output_format)
        elif is_given(output_format) and output_format is not None:
            adapted_type: TypeAdapter[ResponseFormatT] = TypeAdapter(output_format)
            try:
                schema = adapted_type.json_schema()
                transformed_output_format = BetaJSONOutputFormatParam(
                    schema=transform_schema(schema), type="json_schema"
                )
            except Exception as e:
                raise TypeError(
                    "Could not generate JSON schema for the given `output_format` type. "
                    "Use a type that works with `pydantic.TypeAdapter`"
                ) from e

        merged_output_config = _merge_output_configs(output_config, transformed_output_format)

        return BetaAsyncMessageStreamManager(
            _DeferredAsyncStreamRequest(
                self,
                "/v1/messages?beta=true",
                body=maybe_transform(
                    {
                        "max_tokens": max_tokens,
                        "messages": messages,
                        "model": model,
                        "cache_control": cache_control,
                        "metadata": metadata,
                        "output_config": merged_output_config,
                        "output_format": omit,
                        "container": container,
                        "context_management": context_management,
                        "inference_geo": inference_geo,
                        "mcp_servers": mcp_servers,
                        "service_tier": service_tier,
                        "speed": speed,
                        "stop_sequences": stop_sequences,
                        "system": system,
                        "temperature": temperature,
                        "thinking": thinking,
                        "top_k": top_k,
                        "top_p": top_p,
                        "tools": tools,
                        "tool_choice": tool_choice,
                        "stream": True,
                    },
                    message_create_params.MessageCreateParams,
                ),
                options=make_request_options(
                    extra_headers=extra_headers,
                    extra_query=extra_query,
                    extra_body=extra_body,
                    timeout=timeout,
                ),
                cast_to=BetaMessage,
                stream=True,
                stream_cls=AsyncStream[BetaRawMessageStreamEvent],
            ),
            output_format=NOT_GIVEN if is_dict(output_format) else cast(ResponseFormatT, output_format),
        )

    @cached_property
    def with_raw_response(self) -> AsyncMessagesWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.
        """
        return AsyncMessagesWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncMessagesWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.
        """
        return AsyncMessagesWithStreamingResponse(self)


class MessagesWithRawResponse:
    def __init__(self, messages: Messages) -> None:
        self._messages = messages
        self.create = _legacy_response.to_raw_response_wrapper(messages.create)


class AsyncMessagesWithRawResponse:
    def __init__(self, messages: AsyncMessages) -> None:
        self._messages = messages
        self.create = _legacy_response.async_to_raw_response_wrapper(messages.create)


class MessagesWithStreamingResponse:
    def __init__(self, messages: Messages) -> None:
        self._messages = messages
        self.create = to_streamed_response_wrapper(messages.create)


class AsyncMessagesWithStreamingResponse:
    def __init__(self, messages: AsyncMessages) -> None:
        self._messages = messages
        self.create = async_to_streamed_response_wrapper(messages.create)
