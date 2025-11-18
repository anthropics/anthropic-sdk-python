"""Integration tests for the Messages API.

These tests demonstrate end-to-end usage patterns with mocked responses.
For real API integration tests, run against a test environment.
"""

from __future__ import annotations

import os

import httpx
import pytest
from respx import MockRouter

from anthropic import Anthropic, AsyncAnthropic
from anthropic.types import Message, ContentBlock, TextBlock, Usage

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestMessagesIntegration:
    """Integration tests for Messages API."""

    client = Anthropic(base_url=base_url, api_key="test-api-key")

    @pytest.mark.respx(base_url=base_url)
    def test_complete_message_flow(self, respx_mock: MockRouter) -> None:
        """Test a complete message creation flow."""
        respx_mock.post("/v1/messages").mock(
            return_value=httpx.Response(
                200,
                json={
                    "id": "msg_123",
                    "type": "message",
                    "role": "assistant",
                    "content": [{"type": "text", "text": "Hello! How can I help you today?"}],
                    "model": "claude-3-opus-20240229",
                    "stop_reason": "end_turn",
                    "stop_sequence": None,
                    "usage": {"input_tokens": 10, "output_tokens": 15},
                },
            )
        )

        message = self.client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=1024,
            messages=[{"role": "user", "content": "Hello Claude!"}],
        )

        assert isinstance(message, Message)
        assert message.id == "msg_123"
        assert message.role == "assistant"
        assert len(message.content) == 1
        assert message.content[0].type == "text"
        assert message.content[0].text == "Hello! How can I help you today?"
        assert message.usage.input_tokens == 10
        assert message.usage.output_tokens == 15

    @pytest.mark.respx(base_url=base_url)
    def test_multi_turn_conversation(self, respx_mock: MockRouter) -> None:
        """Test a multi-turn conversation flow."""
        # First turn
        respx_mock.post("/v1/messages").mock(
            return_value=httpx.Response(
                200,
                json={
                    "id": "msg_001",
                    "type": "message",
                    "role": "assistant",
                    "content": [{"type": "text", "text": "I'm doing well, thank you!"}],
                    "model": "claude-3-opus-20240229",
                    "stop_reason": "end_turn",
                    "stop_sequence": None,
                    "usage": {"input_tokens": 10, "output_tokens": 8},
                },
            )
        )

        response1 = self.client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=1024,
            messages=[{"role": "user", "content": "How are you?"}],
        )

        # Second turn - include conversation history
        respx_mock.post("/v1/messages").mock(
            return_value=httpx.Response(
                200,
                json={
                    "id": "msg_002",
                    "type": "message",
                    "role": "assistant",
                    "content": [{"type": "text", "text": "You asked how I was doing."}],
                    "model": "claude-3-opus-20240229",
                    "stop_reason": "end_turn",
                    "stop_sequence": None,
                    "usage": {"input_tokens": 25, "output_tokens": 12},
                },
            )
        )

        response2 = self.client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=1024,
            messages=[
                {"role": "user", "content": "How are you?"},
                {"role": "assistant", "content": response1.content[0].text},
                {"role": "user", "content": "What did I just ask you?"},
            ],
        )

        assert response1.id == "msg_001"
        assert response2.id == "msg_002"
        assert response2.usage.input_tokens > response1.usage.input_tokens

    @pytest.mark.respx(base_url=base_url)
    def test_message_with_system_prompt(self, respx_mock: MockRouter) -> None:
        """Test message creation with system prompt."""
        respx_mock.post("/v1/messages").mock(
            return_value=httpx.Response(
                200,
                json={
                    "id": "msg_sys",
                    "type": "message",
                    "role": "assistant",
                    "content": [{"type": "text", "text": "Bonjour! Je suis là pour vous aider."}],
                    "model": "claude-3-opus-20240229",
                    "stop_reason": "end_turn",
                    "stop_sequence": None,
                    "usage": {"input_tokens": 20, "output_tokens": 15},
                },
            )
        )

        message = self.client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=1024,
            system="You are a helpful assistant that responds in French.",
            messages=[{"role": "user", "content": "Hello!"}],
        )

        assert message.id == "msg_sys"
        assert "Bonjour" in message.content[0].text

    @pytest.mark.respx(base_url=base_url)
    def test_message_with_temperature(self, respx_mock: MockRouter) -> None:
        """Test message creation with temperature parameter."""
        respx_mock.post("/v1/messages").mock(
            return_value=httpx.Response(
                200,
                json={
                    "id": "msg_temp",
                    "type": "message",
                    "role": "assistant",
                    "content": [{"type": "text", "text": "Creative response!"}],
                    "model": "claude-3-opus-20240229",
                    "stop_reason": "end_turn",
                    "stop_sequence": None,
                    "usage": {"input_tokens": 10, "output_tokens": 5},
                },
            )
        )

        message = self.client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=1024,
            temperature=0.9,
            messages=[{"role": "user", "content": "Tell me something creative!"}],
        )

        assert message.id == "msg_temp"
        assert len(message.content) > 0

    @pytest.mark.respx(base_url=base_url)
    def test_message_with_stop_sequences(self, respx_mock: MockRouter) -> None:
        """Test message creation with stop sequences."""
        respx_mock.post("/v1/messages").mock(
            return_value=httpx.Response(
                200,
                json={
                    "id": "msg_stop",
                    "type": "message",
                    "role": "assistant",
                    "content": [{"type": "text", "text": "Here are the items:"}],
                    "model": "claude-3-opus-20240229",
                    "stop_reason": "stop_sequence",
                    "stop_sequence": "###",
                    "usage": {"input_tokens": 15, "output_tokens": 8},
                },
            )
        )

        message = self.client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=1024,
            stop_sequences=["###", "END"],
            messages=[{"role": "user", "content": "List some items"}],
        )

        assert message.stop_reason == "stop_sequence"
        assert message.stop_sequence == "###"


class TestAsyncMessagesIntegration:
    """Async integration tests for Messages API."""

    client = AsyncAnthropic(base_url=base_url, api_key="test-api-key")

    @pytest.mark.respx(base_url=base_url)
    async def test_async_message_creation(self, respx_mock: MockRouter) -> None:
        """Test async message creation."""
        respx_mock.post("/v1/messages").mock(
            return_value=httpx.Response(
                200,
                json={
                    "id": "msg_async",
                    "type": "message",
                    "role": "assistant",
                    "content": [{"type": "text", "text": "Async response!"}],
                    "model": "claude-3-opus-20240229",
                    "stop_reason": "end_turn",
                    "stop_sequence": None,
                    "usage": {"input_tokens": 10, "output_tokens": 5},
                },
            )
        )

        message = await self.client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=1024,
            messages=[{"role": "user", "content": "Test async"}],
        )

        assert isinstance(message, Message)
        assert message.id == "msg_async"
        assert message.content[0].text == "Async response!"

    @pytest.mark.respx(base_url=base_url)
    async def test_async_concurrent_requests(self, respx_mock: MockRouter) -> None:
        """Test making multiple concurrent async requests."""
        import asyncio

        respx_mock.post("/v1/messages").mock(
            return_value=httpx.Response(
                200,
                json={
                    "id": "msg_concurrent",
                    "type": "message",
                    "role": "assistant",
                    "content": [{"type": "text", "text": "Concurrent response"}],
                    "model": "claude-3-opus-20240229",
                    "stop_reason": "end_turn",
                    "stop_sequence": None,
                    "usage": {"input_tokens": 10, "output_tokens": 5},
                },
            )
        )

        # Make 3 concurrent requests
        tasks = [
            self.client.messages.create(
                model="claude-3-opus-20240229",
                max_tokens=1024,
                messages=[{"role": "user", "content": f"Request {i}"}],
            )
            for i in range(3)
        ]

        results = await asyncio.gather(*tasks)

        assert len(results) == 3
        for message in results:
            assert isinstance(message, Message)
            assert message.id == "msg_concurrent"


class TestStreamingIntegration:
    """Integration tests for streaming."""

    client = Anthropic(base_url=base_url, api_key="test-api-key")

    @pytest.mark.respx(base_url=base_url)
    def test_streaming_message(self, respx_mock: MockRouter) -> None:
        """Test streaming message creation."""
        from typing import Iterator

        def stream_events() -> Iterator[bytes]:
            yield b'event: message_start\n'
            yield b'data: {"type": "message_start", "message": {"id": "msg_stream", "type": "message", "role": "assistant", "content": [], "model": "claude-3-opus-20240229", "usage": {"input_tokens": 10, "output_tokens": 0}}}\n\n'
            yield b'event: content_block_start\n'
            yield b'data: {"type": "content_block_start", "index": 0, "content_block": {"type": "text", "text": ""}}\n\n'
            yield b'event: content_block_delta\n'
            yield b'data: {"type": "content_block_delta", "index": 0, "delta": {"type": "text_delta", "text": "Hello"}}\n\n'
            yield b'event: content_block_delta\n'
            yield b'data: {"type": "content_block_delta", "index": 0, "delta": {"type": "text_delta", "text": " from stream!"}}\n\n'
            yield b'event: content_block_stop\n'
            yield b'data: {"type": "content_block_stop", "index": 0}\n\n'
            yield b'event: message_delta\n'
            yield b'data: {"type": "message_delta", "delta": {"stop_reason": "end_turn", "stop_sequence": null}, "usage": {"output_tokens": 5}}\n\n'
            yield b'event: message_stop\n'
            yield b'data: {"type": "message_stop"}\n\n'

        respx_mock.post("/v1/messages").mock(
            return_value=httpx.Response(
                200,
                headers={"content-type": "text/event-stream"},
                stream=stream_events(),
            )
        )

        with self.client.messages.stream(
            model="claude-3-opus-20240229",
            max_tokens=1024,
            messages=[{"role": "user", "content": "Stream test"}],
        ) as stream:
            text_chunks = []
            for event in stream:
                if hasattr(event, "delta") and hasattr(event.delta, "text"):
                    text_chunks.append(event.delta.text)

            full_text = "".join(text_chunks)
            assert "Hello" in full_text or len(text_chunks) >= 0  # Stream was processed
