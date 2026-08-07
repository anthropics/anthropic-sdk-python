import copy

import httpx
import respx
import pytest

from anthropic import Anthropic, AsyncAnthropic
from anthropic.types.usage import Usage
from anthropic.types.message import Message
from anthropic.types.tool_use_block import ToolUseBlock
from anthropic.types.input_json_delta import InputJSONDelta
from anthropic.lib.streaming._messages import accumulate_event
from anthropic.types.raw_content_block_delta_event import RawContentBlockDeltaEvent

from .helpers import to_async_iter

base_url = "http://127.0.0.1:4010"
api_key = "my-anthropic-api-key"

sync_client = Anthropic(base_url=base_url, api_key=api_key, _strict_response_validation=True)
async_client = AsyncAnthropic(base_url=base_url, api_key=api_key, _strict_response_validation=True)


class TestNonBetaPartialJson:
    """Tests for the non-beta streaming accumulate_event JSON parsing."""

    def _make_snapshot(self) -> Message:
        return Message(
            id="msg_123",
            type="message",
            role="assistant",
            content=[
                ToolUseBlock(
                    type="tool_use",
                    input={},
                    id="tool_123",
                    name="test_tool",
                )
            ],
            model="claude-sonnet-4-5",
            stop_reason=None,
            stop_sequence=None,
            usage=Usage(input_tokens=10, output_tokens=10),
        )

    def test_valid_json_parses_correctly(self) -> None:
        """Valid JSON input should be parsed normally."""
        snapshot = self._make_snapshot()
        event = RawContentBlockDeltaEvent(
            type="content_block_delta",
            index=0,
            delta=InputJSONDelta(type="input_json_delta", partial_json='{"key": "value"}'),
        )

        result = accumulate_event(
            event=event,
            current_snapshot=copy.deepcopy(snapshot),
        )

        assert isinstance(result.content[0], ToolUseBlock)
        assert result.content[0].input == {"key": "value"}

    def test_invalid_json_raises_helpful_error(self) -> None:
        """Invalid JSON should raise ValueError with a helpful message, not a raw parser error."""
        snapshot = self._make_snapshot()
        event = RawContentBlockDeltaEvent(
            type="content_block_delta",
            index=0,
            delta=InputJSONDelta(
                type="input_json_delta",
                partial_json='{"city": INVALID_VALUE}',
            ),
        )

        with pytest.raises(ValueError) as exc_info:
            accumulate_event(
                event=event,
                current_snapshot=copy.deepcopy(snapshot),
            )

        error_msg = str(exc_info.value)
        assert "Unable to parse tool parameter JSON from model" in error_msg
        assert "INVALID_VALUE" in error_msg

    def test_invalid_json_chained_from_original(self) -> None:
        """The error should be chained from the original ValueError."""
        snapshot = self._make_snapshot()
        event = RawContentBlockDeltaEvent(
            type="content_block_delta",
            index=0,
            delta=InputJSONDelta(
                type="input_json_delta",
                partial_json='{"bad": syntax}',
            ),
        )

        with pytest.raises(ValueError) as exc_info:
            accumulate_event(
                event=event,
                current_snapshot=copy.deepcopy(snapshot),
            )

        assert exc_info.value.__cause__ is not None


# Streaming SSE response with malformed JSON in a tool_use content block
MALFORMED_TOOL_USE_SSE = (
    b'event: message_start\r\n'
    b'data: {"type":"message_start","message":{"id":"msg_test","type":"message","role":"assistant",'
    b'"content":[],"model":"claude-sonnet-4-5","stop_reason":null,"stop_sequence":null,'
    b'"usage":{"input_tokens":10,"output_tokens":1}}}\r\n\r\n'
    b'event: content_block_start\r\n'
    b'data: {"type":"content_block_start","index":0,'
    b'"content_block":{"type":"tool_use","id":"toolu_test","name":"get_weather","input":{}}}\r\n\r\n'
    b'event: content_block_delta\r\n'
    b'data: {"type":"content_block_delta","index":0,'
    b'"delta":{"type":"input_json_delta","partial_json":"{\\"city\\": INVALID_VALUE}"}}\r\n\r\n'
)


def _sse_bytes_iter(data: bytes):
    """Yield SSE data as a single chunk for mocking."""
    yield data


class TestNonBetaPartialJsonAsyncStream:
    """Tests for malformed JSON error handling through actual async streaming path."""

    @pytest.mark.asyncio
    @respx.mock(base_url=base_url)
    async def test_async_stream_malformed_json_error(self, respx_mock: respx.MockRouter) -> None:
        """Async streaming should raise helpful ValueError on malformed JSON, not raw parser error."""
        respx_mock.post("/v1/messages").mock(
            return_value=httpx.Response(200, content=to_async_iter(_sse_bytes_iter(MALFORMED_TOOL_USE_SSE)))
        )

        with pytest.raises(ValueError, match="Unable to parse tool parameter JSON from model"):
            async with async_client.messages.stream(
                max_tokens=1024,
                messages=[{"role": "user", "content": "What is the weather?"}],
                model="claude-sonnet-4-5",
                tools=[{
                    "name": "get_weather",
                    "description": "Get weather",
                    "input_schema": {
                        "type": "object",
                        "properties": {"city": {"type": "string"}},
                    },
                }],
            ) as stream:
                async for _ in stream:
                    pass

    @pytest.mark.respx(base_url=base_url)
    def test_sync_stream_malformed_json_error(self, respx_mock: respx.MockRouter) -> None:
        """Sync streaming should raise helpful ValueError on malformed JSON, not raw parser error."""
        respx_mock.post("/v1/messages").mock(
            return_value=httpx.Response(200, content=to_async_iter(_sse_bytes_iter(MALFORMED_TOOL_USE_SSE)))
        )

        with pytest.raises(ValueError, match="Unable to parse tool parameter JSON from model"):
            with sync_client.messages.stream(
                max_tokens=1024,
                messages=[{"role": "user", "content": "What is the weather?"}],
                model="claude-sonnet-4-5",
                tools=[{
                    "name": "get_weather",
                    "description": "Get weather",
                    "input_schema": {
                        "type": "object",
                        "properties": {"city": {"type": "string"}},
                    },
                }],
            ) as stream:
                for _ in stream:
                    pass
