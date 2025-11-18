"""Tests for Bedrock streaming functionality."""

from __future__ import annotations

from unittest import mock
from typing import Iterator, AsyncIterator

import pytest

# Only run these tests if botocore is available
botocore = pytest.importorskip("botocore")

from anthropic.lib.bedrock._stream_decoder import AWSEventStreamDecoder, get_response_stream_shape
from anthropic._streaming import ServerSentEvent


class TestAWSEventStreamDecoder:
    """Test AWS EventStream decoder functionality."""

    def test_decoder_initialization(self) -> None:
        """Test that decoder initializes correctly."""
        decoder = AWSEventStreamDecoder()
        assert decoder is not None
        assert decoder.parser is not None

    def test_get_response_stream_shape(self) -> None:
        """Test getting the response stream shape from botocore."""
        shape = get_response_stream_shape()
        assert shape is not None
        # Shape should be cached
        shape2 = get_response_stream_shape()
        assert shape is shape2

    def test_iter_bytes_with_valid_event(self) -> None:
        """Test iterating over bytes with a valid AWS event."""
        from botocore.eventstream import EventStreamMessage

        decoder = AWSEventStreamDecoder()

        # Create a mock event
        mock_event = mock.Mock(spec=EventStreamMessage)
        mock_event.to_response_dict.return_value = {
            "status_code": 200,
            "headers": {},
            "body": b'{"bytes": "test data"}',
        }

        with mock.patch("anthropic.lib.bedrock._stream_decoder.EventStreamBuffer") as MockBuffer:
            mock_buffer_instance = MockBuffer.return_value
            # Make the buffer return our mock event when iterated
            mock_buffer_instance.__iter__.return_value = iter([mock_event])

            with mock.patch.object(decoder, "_parse_message_from_event", return_value="test message"):
                # Create a simple bytes iterator
                byte_iterator: Iterator[bytes] = iter([b"test chunk"])

                events = list(decoder.iter_bytes(byte_iterator))

                assert len(events) == 1
                assert isinstance(events[0], ServerSentEvent)
                assert events[0].data == "test message"
                assert events[0].event == "completion"

    async def test_aiter_bytes_with_valid_event(self) -> None:
        """Test async iteration over bytes with a valid AWS event."""
        from botocore.eventstream import EventStreamMessage

        decoder = AWSEventStreamDecoder()

        # Create a mock event
        mock_event = mock.Mock(spec=EventStreamMessage)
        mock_event.to_response_dict.return_value = {
            "status_code": 200,
            "headers": {},
            "body": b'{"bytes": "test async data"}',
        }

        async def async_byte_iterator() -> AsyncIterator[bytes]:
            yield b"test chunk"

        with mock.patch("anthropic.lib.bedrock._stream_decoder.EventStreamBuffer") as MockBuffer:
            mock_buffer_instance = MockBuffer.return_value
            mock_buffer_instance.__iter__.return_value = iter([mock_event])

            with mock.patch.object(decoder, "_parse_message_from_event", return_value="test async message"):
                events = []
                async for event in decoder.aiter_bytes(async_byte_iterator()):
                    events.append(event)

                assert len(events) == 1
                assert isinstance(events[0], ServerSentEvent)
                assert events[0].data == "test async message"
                assert events[0].event == "completion"

    def test_iter_bytes_with_multiple_chunks(self) -> None:
        """Test processing multiple chunks of data."""
        from botocore.eventstream import EventStreamMessage

        decoder = AWSEventStreamDecoder()

        # Create mock events
        mock_event1 = mock.Mock(spec=EventStreamMessage)
        mock_event1.to_response_dict.return_value = {
            "status_code": 200,
            "headers": {},
            "body": b'{"bytes": "chunk1"}',
        }

        mock_event2 = mock.Mock(spec=EventStreamMessage)
        mock_event2.to_response_dict.return_value = {
            "status_code": 200,
            "headers": {},
            "body": b'{"bytes": "chunk2"}',
        }

        with mock.patch("anthropic.lib.bedrock._stream_decoder.EventStreamBuffer") as MockBuffer:
            # First chunk adds event1, second chunk adds event2
            mock_buffer1 = mock.Mock()
            mock_buffer1.__iter__.return_value = iter([mock_event1])
            mock_buffer2 = mock.Mock()
            mock_buffer2.__iter__.return_value = iter([mock_event2])

            MockBuffer.return_value = mock_buffer1

            with mock.patch.object(
                decoder, "_parse_message_from_event", side_effect=["message1", "message2"]
            ):
                byte_iterator: Iterator[bytes] = iter([b"chunk1", b"chunk2"])

                events = list(decoder.iter_bytes(byte_iterator))

                # Should process both chunks
                assert len(events) >= 1

    def test_iter_bytes_skips_none_messages(self) -> None:
        """Test that None messages are skipped."""
        from botocore.eventstream import EventStreamMessage

        decoder = AWSEventStreamDecoder()

        mock_event = mock.Mock(spec=EventStreamMessage)
        mock_event.to_response_dict.return_value = {
            "status_code": 200,
            "headers": {},
            "body": b"{}",
        }

        with mock.patch("anthropic.lib.bedrock._stream_decoder.EventStreamBuffer") as MockBuffer:
            mock_buffer_instance = MockBuffer.return_value
            mock_buffer_instance.__iter__.return_value = iter([mock_event])

            # _parse_message_from_event returns None
            with mock.patch.object(decoder, "_parse_message_from_event", return_value=None):
                byte_iterator: Iterator[bytes] = iter([b"test chunk"])

                events = list(decoder.iter_bytes(byte_iterator))

                # Should skip the None message
                assert len(events) == 0

    def test_parse_message_from_event_success(self) -> None:
        """Test parsing a successful message from an event."""
        from botocore.eventstream import EventStreamMessage

        decoder = AWSEventStreamDecoder()

        mock_event = mock.Mock(spec=EventStreamMessage)
        mock_event.to_response_dict.return_value = {
            "status_code": 200,
            "headers": {},
            "body": b'test body',
        }

        with mock.patch.object(decoder.parser, "parse") as mock_parse:
            mock_parse.return_value = {
                "chunk": {"bytes": b"test message"}
            }

            message = decoder._parse_message_from_event(mock_event)

            assert message == "test message"
            mock_parse.assert_called_once()

    def test_parse_message_from_event_no_chunk(self) -> None:
        """Test parsing when response has no chunk."""
        from botocore.eventstream import EventStreamMessage

        decoder = AWSEventStreamDecoder()

        mock_event = mock.Mock(spec=EventStreamMessage)
        mock_event.to_response_dict.return_value = {
            "status_code": 200,
            "headers": {},
            "body": b'test body',
        }

        with mock.patch.object(decoder.parser, "parse") as mock_parse:
            # No chunk in response
            mock_parse.return_value = {}

            message = decoder._parse_message_from_event(mock_event)

            assert message is None

    def test_parse_message_from_event_bad_status_code(self) -> None:
        """Test parsing fails with bad status code."""
        from botocore.eventstream import EventStreamMessage

        decoder = AWSEventStreamDecoder()

        mock_event = mock.Mock(spec=EventStreamMessage)
        mock_event.to_response_dict.return_value = {
            "status_code": 500,
            "headers": {},
            "body": b'error',
        }

        with mock.patch.object(decoder.parser, "parse") as mock_parse:
            mock_parse.return_value = {"chunk": {"bytes": b"data"}}

            with pytest.raises(ValueError, match="Bad response code, expected 200"):
                decoder._parse_message_from_event(mock_event)

    async def test_aiter_bytes_empty_iterator(self) -> None:
        """Test async iteration with empty iterator."""
        decoder = AWSEventStreamDecoder()

        async def empty_iterator() -> AsyncIterator[bytes]:
            return
            yield  # Make it async generator # pragma: no cover

        with mock.patch("anthropic.lib.bedrock._stream_decoder.EventStreamBuffer") as MockBuffer:
            mock_buffer_instance = MockBuffer.return_value
            mock_buffer_instance.__iter__.return_value = iter([])

            events = []
            async for event in decoder.aiter_bytes(empty_iterator()):
                events.append(event)

            assert len(events) == 0

    def test_iter_bytes_empty_iterator(self) -> None:
        """Test iteration with empty iterator."""
        decoder = AWSEventStreamDecoder()

        byte_iterator: Iterator[bytes] = iter([])

        with mock.patch("anthropic.lib.bedrock._stream_decoder.EventStreamBuffer") as MockBuffer:
            mock_buffer_instance = MockBuffer.return_value
            mock_buffer_instance.__iter__.return_value = iter([])

            events = list(decoder.iter_bytes(byte_iterator))

            assert len(events) == 0
