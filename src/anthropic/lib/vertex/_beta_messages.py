# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import json
from typing import List, Union, Iterable, Optional, cast
from typing_extensions import Literal

import httpx
import pydantic

from ... import _legacy_response
from ..._types import NOT_GIVEN, Body, Omit, Query, Headers, NotGiven, SequenceNotStr, omit
from ..._utils import is_given
from ..._compat import cached_property
from ..._models import TypeAdapter
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import to_streamed_response_wrapper, async_to_streamed_response_wrapper
from ...types.beta import message_create_params
from ...resources.beta import Messages as FirstPartyMessagesAPI, AsyncMessages as FirstPartyAsyncMessagesAPI
from .._parse._response import ResponseFormatT, parse_response
from .._parse._transform import transform_schema
from ...types.model_param import ModelParam
from ...types.anthropic_beta_param import AnthropicBetaParam
from ...types.beta.beta_message_param import BetaMessageParam
from ...types.beta.beta_metadata_param import BetaMetadataParam
from ...types.beta.parsed_beta_message import ParsedBetaMessage
from ...types.beta.beta_text_block_param import BetaTextBlockParam
from ...types.beta.beta_tool_union_param import BetaToolUnionParam
from ...types.beta.beta_tool_choice_param import BetaToolChoiceParam
from ...types.beta.beta_output_config_param import BetaOutputConfigParam
from ...types.beta.beta_thinking_config_param import BetaThinkingConfigParam
from ...types.beta.beta_context_management_config_param import BetaContextManagementConfigParam
from ...types.beta.beta_request_mcp_server_url_definition_param import BetaRequestMCPServerURLDefinitionParam

__all__ = ["Messages", "AsyncMessages"]

# System prompt instruction for JSON output when native structured outputs are not available
_JSON_OUTPUT_INSTRUCTION = """You must respond with valid JSON that conforms to the following JSON schema:

{schema}

Important:
- Output ONLY the JSON object, no additional text or markdown formatting
- Do not wrap the response in ```json``` code blocks
- Ensure all required fields are present
- Follow the exact types specified in the schema"""


class Messages(SyncAPIResource):
    create = FirstPartyMessagesAPI.create
    stream = FirstPartyMessagesAPI.stream
    count_tokens = FirstPartyMessagesAPI.count_tokens

    def parse(
        self,
        *,
        max_tokens: int,
        messages: Iterable[BetaMessageParam],
        model: ModelParam,
        output_format: type[ResponseFormatT],
        container: Optional[message_create_params.Container] | Omit = omit,
        context_management: Optional[BetaContextManagementConfigParam] | Omit = omit,
        mcp_servers: Iterable[BetaRequestMCPServerURLDefinitionParam] | Omit = omit,
        metadata: BetaMetadataParam | Omit = omit,
        output_config: BetaOutputConfigParam | Omit = omit,
        service_tier: Literal["auto", "standard_only"] | Omit = omit,
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
    ) -> ParsedBetaMessage[ResponseFormatT]:
        """
        Parse a message response into a structured output format.

        This method provides structured output support for Vertex AI by using client-side
        JSON parsing. Since Vertex AI does not currently support the native structured
        outputs beta header, this implementation:

        1. Generates a JSON schema from the provided Pydantic model
        2. Injects schema instructions into the system prompt
        3. Parses the response client-side using Pydantic validation

        Note: Unlike the first-party Anthropic API's parse() method, this does not
        guarantee valid JSON output at the API level. However, Claude reliably follows
        JSON schema instructions in practice.

        Args:
            output_format: A Pydantic model class that defines the expected response structure.
                          The model will be used to generate a JSON schema and validate the response.

        Returns:
            ParsedBetaMessage with a `parsed_output` property containing the validated response.

        Example:
            ```python
            from pydantic import BaseModel


            class Person(BaseModel):
                name: str
                age: int


            result = client.beta.messages.parse(
                model="claude-sonnet-4-5@20250929",
                max_tokens=1024,
                messages=[{"role": "user", "content": "Extract: John is 30 years old"}],
                output_format=Person,
            )
            print(result.parsed_output)  # Person(name='John', age=30)
            ```
        """
        # Generate JSON schema from the Pydantic type
        adapted_type: TypeAdapter[ResponseFormatT] = TypeAdapter(output_format)

        try:
            schema = adapted_type.json_schema()
            transformed_schema = transform_schema(schema)
        except pydantic.errors.PydanticSchemaGenerationError as e:
            raise TypeError(
                "Could not generate JSON schema for the given `output_format` type. "
                "Use a type that works with `pydantic.TypeAdapter`"
            ) from e

        # Build the JSON instruction to prepend to the system prompt
        json_instruction = _JSON_OUTPUT_INSTRUCTION.format(schema=json.dumps(transformed_schema, indent=2))

        # Combine with existing system prompt if provided
        combined_system: Union[str, list[BetaTextBlockParam]]
        if is_given(system) and system is not None:
            if isinstance(system, str):
                combined_system = f"{json_instruction}\n\n{system}"
            else:
                # system is Iterable[BetaTextBlockParam]
                system_list: list[BetaTextBlockParam] = list(cast(Iterable[BetaTextBlockParam], system))
                json_block: BetaTextBlockParam = {"type": "text", "text": json_instruction}
                combined_system = [json_block] + system_list
        else:
            combined_system = json_instruction

        # Call create() without the structured outputs beta header
        response = self.create(  # type: ignore[misc]
            max_tokens=max_tokens,
            messages=messages,
            model=model,
            container=container,
            context_management=context_management,
            mcp_servers=mcp_servers,
            metadata=metadata,
            output_config=output_config,
            service_tier=service_tier,
            stop_sequences=stop_sequences,
            system=combined_system,
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

        # Parse the response client-side
        return parse_response(
            response=response,
            output_format=cast(ResponseFormatT, output_format),
        )

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
    create = FirstPartyAsyncMessagesAPI.create
    stream = FirstPartyAsyncMessagesAPI.stream
    count_tokens = FirstPartyAsyncMessagesAPI.count_tokens

    async def parse(
        self,
        *,
        max_tokens: int,
        messages: Iterable[BetaMessageParam],
        model: ModelParam,
        output_format: type[ResponseFormatT],
        container: Optional[message_create_params.Container] | Omit = omit,
        context_management: Optional[BetaContextManagementConfigParam] | Omit = omit,
        mcp_servers: Iterable[BetaRequestMCPServerURLDefinitionParam] | Omit = omit,
        metadata: BetaMetadataParam | Omit = omit,
        output_config: BetaOutputConfigParam | Omit = omit,
        service_tier: Literal["auto", "standard_only"] | Omit = omit,
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
    ) -> ParsedBetaMessage[ResponseFormatT]:
        """
        Parse a message response into a structured output format (async version).

        This method provides structured output support for Vertex AI by using client-side
        JSON parsing. Since Vertex AI does not currently support the native structured
        outputs beta header, this implementation:

        1. Generates a JSON schema from the provided Pydantic model
        2. Injects schema instructions into the system prompt
        3. Parses the response client-side using Pydantic validation

        Note: Unlike the first-party Anthropic API's parse() method, this does not
        guarantee valid JSON output at the API level. However, Claude reliably follows
        JSON schema instructions in practice.

        Args:
            output_format: A Pydantic model class that defines the expected response structure.
                          The model will be used to generate a JSON schema and validate the response.

        Returns:
            ParsedBetaMessage with a `parsed_output` property containing the validated response.

        Example:
            ```python
            from pydantic import BaseModel


            class Person(BaseModel):
                name: str
                age: int


            result = await client.beta.messages.parse(
                model="claude-sonnet-4-5@20250929",
                max_tokens=1024,
                messages=[{"role": "user", "content": "Extract: John is 30 years old"}],
                output_format=Person,
            )
            print(result.parsed_output)  # Person(name='John', age=30)
            ```
        """
        # Generate JSON schema from the Pydantic type
        adapted_type: TypeAdapter[ResponseFormatT] = TypeAdapter(output_format)

        try:
            schema = adapted_type.json_schema()
            transformed_schema = transform_schema(schema)
        except pydantic.errors.PydanticSchemaGenerationError as e:
            raise TypeError(
                "Could not generate JSON schema for the given `output_format` type. "
                "Use a type that works with `pydantic.TypeAdapter`"
            ) from e

        # Build the JSON instruction to prepend to the system prompt
        json_instruction = _JSON_OUTPUT_INSTRUCTION.format(schema=json.dumps(transformed_schema, indent=2))

        # Combine with existing system prompt if provided
        combined_system: Union[str, list[BetaTextBlockParam]]
        if is_given(system) and system is not None:
            if isinstance(system, str):
                combined_system = f"{json_instruction}\n\n{system}"
            else:
                # system is Iterable[BetaTextBlockParam]
                system_list: list[BetaTextBlockParam] = list(cast(Iterable[BetaTextBlockParam], system))
                json_block: BetaTextBlockParam = {"type": "text", "text": json_instruction}
                combined_system = [json_block] + system_list
        else:
            combined_system = json_instruction

        # Call create() without the structured outputs beta header
        response = await self.create(  # type: ignore[misc]
            max_tokens=max_tokens,
            messages=messages,
            model=model,
            container=container,
            context_management=context_management,
            mcp_servers=mcp_servers,
            metadata=metadata,
            output_config=output_config,
            service_tier=service_tier,
            stop_sequences=stop_sequences,
            system=combined_system,
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

        # Parse the response client-side
        return parse_response(
            response=response,
            output_format=cast(ResponseFormatT, output_format),
        )

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
