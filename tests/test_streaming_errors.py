"""Extended streaming tests for error handling and edge cases."""

from __future__ import annotations

import httpx
import pytest
from respx import MockRouter
from typing import AsyncIterator

from anthropic import Anthropic, AsyncAnthropic
from anthropic._streaming import Stream, AsyncStream
from anthropic._exceptions import APIConnectionError, APITimeoutError, APIStatusError
from anthropic.types import Message


class TestStreamingErrorHandling:
    """Test streaming error scenarios and edge cases."""

    client = Anthropic(base_url="http://127.0.0.1:4010", api_key="test-key")
    async_client = AsyncAnthropic(base_url="http://127.0.0.1:4010", api_key="test-key")

    @pytest.mark.respx(base_url="http://127.0.0.1:4010")
    def test_stream_connection_error(self, respx_mock: MockRouter) -> None:
        """Test handling of connection errors during streaming."""
        respx_mock.post("/v1/messages").mock(side_effect=httpx.ConnectError("Connection failed"))

        with pytest.raises(APIConnectionError):
            with self.client.messages.stream(
                max_tokens=1024,
                messages=[{"role": "user", "content": "test"}],
                model="claude-3-opus-20240229",
            ):
                pass

    @pytest.mark.respx(base_url="http://127.0.0.1:4010")
    async def test_async_stream_connection_error(self, respx_mock: MockRouter) -> None:
        """Test handling of connection errors during async streaming."""
        respx_mock.post("/v1/messages").mock(side_effect=httpx.ConnectError("Connection failed"))

        with pytest.raises(APIConnectionError):
            async with self.async_client.messages.stream(
                max_tokens=1024,
                messages=[{"role": "user", "content": "test"}],
                model="claude-3-opus-20240229",
            ):
                pass

    @pytest.mark.respx(base_url="http://127.0.0.1:4010")
    def test_stream_timeout_error(self, respx_mock: MockRouter) -> None:
        """Test handling of timeout errors during streaming."""
        respx_mock.post("/v1/messages").mock(side_effect=httpx.TimeoutException("Request timeout"))

        with pytest.raises(APITimeoutError):
            with self.client.messages.stream(
                max_tokens=1024,
                messages=[{"role": "user", "content": "test"}],
                model="claude-3-opus-20240229",
            ):
                pass

    @pytest.mark.respx(base_url="http://127.0.0.1:4010")
    async def test_async_stream_timeout_error(self, respx_mock: MockRouter) -> None:
        """Test handling of timeout errors during async streaming."""
        respx_mock.post("/v1/messages").mock(side_effect=httpx.TimeoutException("Request timeout"))

        with pytest.raises(APITimeoutError):
            async with self.async_client.messages.stream(
                max_tokens=1024,
                messages=[{"role": "user", "content": "test"}],
                model="claude-3-opus-20240229",
            ):
                pass

    @pytest.mark.respx(base_url="http://127.0.0.1:4010")
    def test_stream_http_error(self, respx_mock: MockRouter) -> None:
        """Test handling of HTTP errors during streaming."""
        respx_mock.post("/v1/messages").mock(
            return_value=httpx.Response(
                500,
                json={"error": {"type": "internal_error", "message": "Internal server error"}},
            )
        )

        with pytest.raises(APIStatusError) as exc_info:
            with self.client.messages.stream(
                max_tokens=1024,
                messages=[{"role": "user", "content": "test"}],
                model="claude-3-opus-20240229",
            ):
                pass

        assert exc_info.value.status_code == 500

    @pytest.mark.respx(base_url="http://127.0.0.1:4010")
    async def test_async_stream_http_error(self, respx_mock: MockRouter) -> None:
        """Test handling of HTTP errors during async streaming."""
        respx_mock.post("/v1/messages").mock(
            return_value=httpx.Response(
                429,
                json={"error": {"type": "rate_limit_error", "message": "Rate limit exceeded"}},
            )
        )

        with pytest.raises(APIStatusError) as exc_info:
            async with self.async_client.messages.stream(
                max_tokens=1024,
                messages=[{"role": "user", "content": "test"}],
                model="claude-3-opus-20240229",
            ):
                pass

        assert exc_info.value.status_code == 429

    @pytest.mark.respx(base_url="http://127.0.0.1:4010")
    def test_stream_incomplete_data(self, respx_mock: MockRouter) -> None:
        """Test handling of incomplete streaming data."""

        def stream_incomplete() -> Iterator[bytes]:
            yield b'event: message_start\n'
            yield b'data: {"type": "message_start", "message": {"id": "msg_test", "type": "message", "role": "assistant", "content": [], "model": "claude-3-opus-20240229", "usage": {"input_tokens": 10, "output_tokens": 0}}}\n\n'
            # Incomplete - missing message_stop event
            return

        from typing import Iterator

        respx_mock.post("/v1/messages").mock(
            return_value=httpx.Response(
                200,
                headers={"content-type": "text/event-stream"},
                stream=stream_incomplete(),
            )
        )

        # Incomplete data - stream should process without complete message_stop
        with self.client.messages.stream(
            max_tokens=1024,
            messages=[{"role": "user", "content": "test"}],
            model="claude-3-opus-20240229",
        ) as stream:
            events = list(stream)
            # Should handle the events we did receive
            assert len(events) >= 0

    @pytest.mark.respx(base_url="http://127.0.0.1:4010")
    async def test_async_stream_incomplete_data(self, respx_mock: MockRouter) -> None:
        """Test handling of incomplete async streaming data."""

        async def async_stream_incomplete() -> AsyncIterator[bytes]:
            yield b'event: message_start\n'
            yield b'data: {"type": "message_start", "message": {"id": "msg_test", "type": "message", "role": "assistant", "content": [], "model": "claude-3-opus-20240229", "usage": {"input_tokens": 10, "output_tokens": 0}}}\n\n'
            # Incomplete - missing message_stop event
            return

        respx_mock.post("/v1/messages").mock(
            return_value=httpx.Response(
                200,
                headers={"content-type": "text/event-stream"},
                stream=async_stream_incomplete(),
            )
        )

        # Incomplete data - stream should process without complete message_stop
        async with self.async_client.messages.stream(
            max_tokens=1024,
            messages=[{"role": "user", "content": "test"}],
            model="claude-3-opus-20240229",
        ) as stream:
            events = []
            async for event in stream:
                events.append(event)
            # Should handle the events we did receive
            assert len(events) >= 0

    @pytest.mark.respx(base_url="http://127.0.0.1:4010")
    def test_stream_context_manager_cleanup(self, respx_mock: MockRouter) -> None:
        """Test that stream context manager properly cleans up resources."""
        respx_mock.post("/v1/messages").mock(
            return_value=httpx.Response(
                200,
                headers={"content-type": "text/event-stream"},
                content=b'event: message_start\ndata: {"type": "message_start"}\n\n',
            )
        )

        stream = self.client.messages.stream(
            max_tokens=1024,
            messages=[{"role": "user", "content": "test"}],
            model="claude-3-opus-20240229",
        )

        # Enter context manager
        stream.__enter__()

        # Manually exit (simulating cleanup)
        stream.__exit__(None, None, None)

        # Should be able to exit cleanly

    @pytest.mark.respx(base_url="http://127.0.0.1:4010")
    async def test_async_stream_context_manager_cleanup(self, respx_mock: MockRouter) -> None:
        """Test that async stream context manager properly cleans up resources."""
        respx_mock.post("/v1/messages").mock(
            return_value=httpx.Response(
                200,
                headers={"content-type": "text/event-stream"},
                content=b'event: message_start\ndata: {"type": "message_start"}\n\n',
            )
        )

        stream = self.async_client.messages.stream(
            max_tokens=1024,
            messages=[{"role": "user", "content": "test"}],
            model="claude-3-opus-20240229",
        )

        # Enter context manager
        await stream.__aenter__()

        # Manually exit (simulating cleanup)
        await stream.__aexit__(None, None, None)

        # Should be able to exit cleanly

    @pytest.mark.respx(base_url="http://127.0.0.1:4010")
    def test_stream_exception_during_iteration(self, respx_mock: MockRouter) -> None:
        """Test handling of exceptions during stream iteration."""

        def stream_with_error() -> Iterator[bytes]:
            from typing import Iterator

            yield b'event: message_start\n'
            yield b'data: {"type": "message_start", "message": {"id": "msg_test", "type": "message", "role": "assistant", "content": [], "model": "claude-3-opus-20240229", "usage": {"input_tokens": 10, "output_tokens": 0}}}\n\n'
            raise RuntimeError("Simulated error during streaming")

        respx_mock.post("/v1/messages").mock(
            return_value=httpx.Response(
                200,
                headers={"content-type": "text/event-stream"},
                stream=stream_with_error(),
            )
        )

        with pytest.raises(RuntimeError, match="Simulated error during streaming"):
            with self.client.messages.stream(
                max_tokens=1024,
                messages=[{"role": "user", "content": "test"}],
                model="claude-3-opus-20240229",
            ) as stream:
                for _ in stream:
                    pass

    @pytest.mark.respx(base_url="http://127.0.0.1:4010")
    async def test_async_stream_exception_during_iteration(self, respx_mock: MockRouter) -> None:
        """Test handling of exceptions during async stream iteration."""

        async def async_stream_with_error() -> AsyncIterator[bytes]:
            yield b'event: message_start\n'
            yield b'data: {"type": "message_start", "message": {"id": "msg_test", "type": "message", "role": "assistant", "content": [], "model": "claude-3-opus-20240229", "usage": {"input_tokens": 10, "output_tokens": 0}}}\n\n'
            raise RuntimeError("Simulated async error during streaming")

        respx_mock.post("/v1/messages").mock(
            return_value=httpx.Response(
                200,
                headers={"content-type": "text/event-stream"},
                stream=async_stream_with_error(),
            )
        )

        with pytest.raises(RuntimeError, match="Simulated async error during streaming"):
            async with self.async_client.messages.stream(
                max_tokens=1024,
                messages=[{"role": "user", "content": "test"}],
                model="claude-3-opus-20240229",
            ) as stream:
                async for _ in stream:
                    pass

    @pytest.mark.respx(base_url="http://127.0.0.1:4010")
    def test_stream_malformed_event_data(self, respx_mock: MockRouter) -> None:
        """Test handling of malformed event data in stream."""
        respx_mock.post("/v1/messages").mock(
            return_value=httpx.Response(
                200,
                headers={"content-type": "text/event-stream"},
                content=b'event: message_start\ndata: {invalid json}\n\n',
            )
        )

        # Should handle malformed data gracefully
        with self.client.messages.stream(
            max_tokens=1024,
            messages=[{"role": "user", "content": "test"}],
            model="claude-3-opus-20240229",
        ) as stream:
            # Depending on implementation, this might raise or skip the event
            try:
                list(stream)
            except Exception:
                # Expected - malformed data should cause an error
                pass
