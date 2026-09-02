from __future__ import annotations

from collections.abc import Iterator

from anthropic.lib.tools import ToolError
from anthropic.lib.tools._tool_dispatch import tool_error_content
from anthropic.types.beta.beta_tool_result_block_param import Content as BetaContent


def _error_blocks() -> Iterator[BetaContent]:
    yield {"type": "text", "text": "first detail"}
    yield {"type": "text", "text": "second detail"}


def test_tool_error_preserves_generator_content_for_runner() -> None:
    error = ToolError(_error_blocks())

    assert str(error) == "first detail second detail"
    assert list(tool_error_content(error)) == [
        {"type": "text", "text": "first detail"},
        {"type": "text", "text": "second detail"},
    ]


def test_tool_error_content_remains_reusable_after_message_rendering() -> None:
    error = ToolError(_error_blocks())

    first_read = list(error.content)
    second_read = list(error.content)

    assert first_read == second_read
    assert first_read == [
        {"type": "text", "text": "first detail"},
        {"type": "text", "text": "second detail"},
    ]


def test_tool_error_string_content_is_unchanged() -> None:
    error = ToolError("plain failure")

    assert str(error) == "plain failure"
    assert error.content == "plain failure"
