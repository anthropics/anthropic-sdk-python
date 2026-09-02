from __future__ import annotations

from typing import Literal

import pytest
from pydantic import BaseModel, ValidationError

from anthropic import _compat
from anthropic.lib._parse._response import parse_beta_response, parse_response
from anthropic.types import Message, TextBlock, Usage
from anthropic.types.beta import BetaMessage, BetaTextBlock, BetaUsage


pytestmark = pytest.mark.skipif(_compat.PYDANTIC_V1, reason="structured outputs not supported with pydantic v1")


class ParsedValue(BaseModel):
    value: int


def _message(stop_reason: Literal["refusal", "max_tokens", "end_turn"], text: str) -> Message:
    return Message.construct(
        id="msg_test",
        type="message",
        role="assistant",
        content=[TextBlock.construct(type="text", text=text, citations=None)],
        model="claude-test",
        stop_reason=stop_reason,
        stop_sequence=None,
        usage=Usage.construct(input_tokens=1, output_tokens=1),
    )


def _beta_message(stop_reason: Literal["refusal", "max_tokens", "end_turn"], text: str) -> BetaMessage:
    return BetaMessage.construct(
        id="msg_test",
        type="message",
        role="assistant",
        content=[BetaTextBlock.construct(type="text", text=text, citations=None)],
        model="claude-test",
        stop_reason=stop_reason,
        stop_sequence=None,
        usage=BetaUsage.construct(input_tokens=1, output_tokens=1),
    )


@pytest.mark.parametrize(
    ("stop_reason", "text"),
    [
        ("refusal", "I cannot provide that."),
        ("max_tokens", '{"value":'),
    ],
)
def test_parse_response_preserves_non_schema_terminal_output(
    stop_reason: Literal["refusal", "max_tokens"],
    text: str,
) -> None:
    response = parse_response(output_format=ParsedValue, response=_message(stop_reason, text))

    assert response.stop_reason == stop_reason
    assert response.parsed_output is None


@pytest.mark.parametrize(
    ("stop_reason", "text"),
    [
        ("refusal", "I cannot provide that."),
        ("max_tokens", '{"value":'),
    ],
)
def test_parse_beta_response_preserves_non_schema_terminal_output(
    stop_reason: Literal["refusal", "max_tokens"],
    text: str,
) -> None:
    response = parse_beta_response(output_format=ParsedValue, response=_beta_message(stop_reason, text))

    assert response.stop_reason == stop_reason
    assert response.parsed_output is None


def test_completed_response_still_validates_structured_output() -> None:
    with pytest.raises(ValidationError):
        parse_response(output_format=ParsedValue, response=_message("end_turn", "not json"))

    with pytest.raises(ValidationError):
        parse_beta_response(output_format=ParsedValue, response=_beta_message("end_turn", "not json"))
