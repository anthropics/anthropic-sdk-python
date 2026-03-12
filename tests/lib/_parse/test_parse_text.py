"""Unit tests for parse_text() and parse_response() edge-cases.

Covers issue #1204: structured output + thinking + tool use crashes.

Bug 1 – empty text block: when the model returns stop_reason="end_turn" with a
         thinking block and an empty text block, parse_text("") used to crash
         because validate_json("") raises ValidationError.

Bug 2 – malformed JSON prefix: when the model prefixes the JSON payload with
         reasoning text, validate_json() raises ValidationError on the full
         string.  parse_text() now tries to salvage the last JSON object from
         the text before re-raising.
"""

from __future__ import annotations

from typing import Optional
from unittest.mock import MagicMock

import pytest
from pydantic import BaseModel, ValidationError

from anthropic import _compat
from anthropic.lib._parse._response import _extract_last_json, parse_text
from anthropic.lib._parse._response import parse_response, parse_beta_response
from anthropic._models import construct_type_unchecked
from anthropic.types.message import Message
from anthropic.types.beta.beta_message import BetaMessage


# ---------------------------------------------------------------------------
# Shared model used across tests
# ---------------------------------------------------------------------------

class Location(BaseModel):
    city: str
    country: str


# ---------------------------------------------------------------------------
# parse_text() — unit tests
# ---------------------------------------------------------------------------

@pytest.mark.skipif(_compat.PYDANTIC_V1, reason="structured outputs not supported with pydantic v1")
class TestParseText:
    def test_returns_none_when_no_output_format(self) -> None:
        from anthropic._types import NOT_GIVEN
        result = parse_text("anything", NOT_GIVEN)
        assert result is None

    def test_empty_string_returns_none(self) -> None:
        result = parse_text("", Location)
        assert result is None

    def test_whitespace_only_returns_none(self) -> None:
        result = parse_text("   \n\t  ", Location)
        assert result is None

    def test_valid_json_parses_correctly(self) -> None:
        result = parse_text('{"city": "Paris", "country": "France"}', Location)
        assert isinstance(result, Location)
        assert result.city == "Paris"
        assert result.country == "France"

    def test_malformed_prefix_recovers_last_json(self) -> None:
        """Model prefixed the JSON with thinking text — recovery should work."""
        text = 'partial garbage\n\n{"city": "Tokyo", "country": "Japan"}'
        result = parse_text(text, Location)
        assert isinstance(result, Location)
        assert result.city == "Tokyo"
        assert result.country == "Japan"

    def test_completely_invalid_text_raises_validation_error(self) -> None:
        with pytest.raises(ValidationError):
            parse_text("this is not json at all", Location)

    def test_recovery_fails_gracefully_on_bad_json(self) -> None:
        """Even if we find a JSON-like fragment it must still validate against the schema."""
        text = 'prefix text {"wrong_field": 123}'
        with pytest.raises(ValidationError):
            parse_text(text, Location)


# ---------------------------------------------------------------------------
# _extract_last_json() — unit tests
# ---------------------------------------------------------------------------

class TestExtractLastJson:
    def test_plain_json_object(self) -> None:
        assert _extract_last_json('{"a": 1}') == '{"a": 1}'

    def test_json_with_prefix(self) -> None:
        assert _extract_last_json('some prefix {"a": 1}') == '{"a": 1}'

    def test_json_array(self) -> None:
        assert _extract_last_json('[1, 2, 3]') == '[1, 2, 3]'

    def test_no_json_returns_none(self) -> None:
        assert _extract_last_json("no json here") is None

    def test_nested_objects(self) -> None:
        text = 'noise {"outer": {"inner": 42}}'
        result = _extract_last_json(text)
        assert result == '{"outer": {"inner": 42}}'

    def test_string_containing_braces(self) -> None:
        text = 'noise {"key": "value with } brace"}'
        result = _extract_last_json(text)
        assert result == '{"key": "value with } brace"}'


# ---------------------------------------------------------------------------
# parse_response() — integration-style tests using constructed Message objects
# ---------------------------------------------------------------------------

def _make_message(stop_reason: str, content_dicts: list) -> Message:
    """Build a minimal Message object via construct_type_unchecked."""
    return construct_type_unchecked(
        type_=Message,
        value={
            "id": "msg_test",
            "type": "message",
            "role": "assistant",
            "model": "claude-test",
            "stop_reason": stop_reason,
            "stop_sequence": None,
            "usage": {"input_tokens": 10, "output_tokens": 20},
            "content": content_dicts,
        },
    )


def _make_beta_message(stop_reason: str, content_dicts: list) -> BetaMessage:
    return construct_type_unchecked(
        type_=BetaMessage,
        value={
            "id": "msg_test",
            "type": "message",
            "role": "assistant",
            "model": "claude-test",
            "stop_reason": stop_reason,
            "stop_sequence": None,
            "usage": {"input_tokens": 10, "output_tokens": 20},
            "content": content_dicts,
        },
    )


@pytest.mark.skipif(_compat.PYDANTIC_V1, reason="structured outputs not supported with pydantic v1")
class TestParseResponse:
    def test_end_turn_with_valid_json_parses(self) -> None:
        msg = _make_message(
            stop_reason="end_turn",
            content_dicts=[
                {"type": "text", "text": '{"city": "Berlin", "country": "Germany"}'},
            ],
        )
        parsed = parse_response(output_format=Location, response=msg)
        assert parsed.stop_reason == "end_turn"
        text_block = parsed.content[0]
        assert text_block.type == "text"
        assert isinstance(text_block.parsed_output, Location)
        assert text_block.parsed_output.city == "Berlin"

    def test_tool_use_turn_does_not_parse_text(self) -> None:
        """stop_reason=tool_use: text blocks must not be parsed as structured output."""
        msg = _make_message(
            stop_reason="tool_use",
            content_dicts=[
                {"type": "thinking", "thinking": "I need to call a tool.", "signature": "sig123"},
                {"type": "text", "text": ""},
                {
                    "type": "tool_use",
                    "id": "tool_abc",
                    "name": "get_weather",
                    "input": {"location": "London"},
                },
            ],
        )
        # Must not raise even though empty text block is present
        parsed = parse_response(output_format=Location, response=msg)
        assert parsed.stop_reason == "tool_use"
        text_block = next(b for b in parsed.content if b.type == "text")
        assert text_block.parsed_output is None

    def test_end_turn_with_empty_text_block_does_not_crash(self) -> None:
        """stop_reason=end_turn with thinking block + empty text: no crash."""
        msg = _make_message(
            stop_reason="end_turn",
            content_dicts=[
                {"type": "thinking", "thinking": "Hmm.", "signature": "sig456"},
                {"type": "text", "text": ""},
            ],
        )
        parsed = parse_response(output_format=Location, response=msg)
        text_block = next(b for b in parsed.content if b.type == "text")
        assert text_block.parsed_output is None

    def test_tool_use_turn_no_output_format(self) -> None:
        """Without output_format everything should still work fine."""
        from anthropic._types import NOT_GIVEN
        msg = _make_message(
            stop_reason="tool_use",
            content_dicts=[
                {"type": "text", "text": ""},
                {
                    "type": "tool_use",
                    "id": "tool_xyz",
                    "name": "search",
                    "input": {},
                },
            ],
        )
        parsed = parse_response(output_format=NOT_GIVEN, response=msg)
        assert parsed.stop_reason == "tool_use"


@pytest.mark.skipif(_compat.PYDANTIC_V1, reason="structured outputs not supported with pydantic v1")
class TestParseBetaResponse:
    def test_end_turn_with_valid_json_parses(self) -> None:
        msg = _make_beta_message(
            stop_reason="end_turn",
            content_dicts=[
                {"type": "text", "text": '{"city": "Rome", "country": "Italy"}'},
            ],
        )
        parsed = parse_beta_response(output_format=Location, response=msg)
        text_block = parsed.content[0]
        assert text_block.type == "text"
        assert isinstance(text_block.parsed_output, Location)
        assert text_block.parsed_output.city == "Rome"

    def test_tool_use_turn_does_not_parse_text(self) -> None:
        msg = _make_beta_message(
            stop_reason="tool_use",
            content_dicts=[
                {"type": "thinking", "thinking": "Calling a tool.", "signature": "sig789"},
                {"type": "text", "text": ""},
                {
                    "type": "tool_use",
                    "id": "tool_def",
                    "name": "lookup",
                    "input": {},
                },
            ],
        )
        parsed = parse_beta_response(output_format=Location, response=msg)
        text_block = next(b for b in parsed.content if b.type == "text")
        assert text_block.parsed_output is None
