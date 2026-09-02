from __future__ import annotations

from typing import Any

import pytest

from anthropic.types.parsed_message import ParsedMessage, ParsedTextBlock
from anthropic.types.beta.parsed_beta_message import ParsedBetaMessage, ParsedBetaTextBlock


@pytest.mark.parametrize("value", [False, 0, "", [], {}])
def test_parsed_message_returns_falsy_output(value: Any) -> None:
    message = ParsedMessage.construct(
        content=[
            ParsedTextBlock.construct(type="text", text="unparsed", parsed_output=None),
            ParsedTextBlock.construct(type="text", text="parsed", parsed_output=value),
        ]
    )

    assert type(message.parsed_output) is type(value)
    assert message.parsed_output == value


@pytest.mark.parametrize("value", [False, 0, "", [], {}])
def test_parsed_beta_message_returns_falsy_output(value: Any) -> None:
    message = ParsedBetaMessage.construct(
        content=[
            ParsedBetaTextBlock.construct(type="text", text="unparsed", parsed_output=None),
            ParsedBetaTextBlock.construct(type="text", text="parsed", parsed_output=value),
        ]
    )

    assert type(message.parsed_output) is type(value)
    assert message.parsed_output == value


def test_parsed_output_remains_none_when_absent() -> None:
    message = ParsedMessage.construct(
        content=[ParsedTextBlock.construct(type="text", text="unparsed", parsed_output=None)]
    )
    beta_message = ParsedBetaMessage.construct(
        content=[ParsedBetaTextBlock.construct(type="text", text="unparsed", parsed_output=None)]
    )

    assert message.parsed_output is None
    assert beta_message.parsed_output is None
