from __future__ import annotations

from pydantic import ValidationError
from typing_extensions import TypeVar

from ..._types import NotGiven
from ..._models import TypeAdapter, construct_type_unchecked
from ..._utils._utils import is_given
from ...types.message import Message
from ...types.parsed_message import ParsedMessage, ParsedTextBlock, ParsedContentBlock
from ...types.beta.beta_message import BetaMessage
from ...types.beta.parsed_beta_message import ParsedBetaMessage, ParsedBetaTextBlock, ParsedBetaContentBlock

ResponseFormatT = TypeVar("ResponseFormatT", default=None)


def parse_text(text: str, output_format: ResponseFormatT | NotGiven) -> ResponseFormatT | None:
    if not is_given(output_format):
        return None

    # Empty or whitespace-only text blocks (e.g. from thinking+tool_use turns) should
    # not be parsed — the model emits an empty text block as a placeholder.
    if not text or not text.strip():
        return None

    adapted_type: TypeAdapter[ResponseFormatT] = TypeAdapter(output_format)

    try:
        return adapted_type.validate_json(text)
    except ValidationError as original_error:
        # Bug 2 recovery: the model sometimes prefixes the JSON payload with
        # reasoning text or a partial generation artifact.  Try to salvage the
        # last complete JSON object (or array) from the text before giving up.
        recovered = _extract_last_json(text)
        if recovered is not None:
            try:
                return adapted_type.validate_json(recovered)
            except ValidationError:
                pass

        raise original_error


def _extract_last_json(text: str) -> str | None:
    """Return the last JSON object or array found in *text*, or None."""
    stripped = text.strip()

    # Walk backwards looking for a closing brace/bracket then match open.
    for close_char, open_char in (("}", "{"), ("]", "[")):
        last_close = stripped.rfind(close_char)
        if last_close == -1:
            continue

        # Scan backwards through all candidate open-bracket positions so that a
        # malformed/partial JSON object appearing *before* the final valid payload
        # does not shadow it.  We try each position from the end towards the start
        # and return the first (i.e. rightmost) substring that has balanced
        # braces/brackets, which corresponds to the last valid JSON in the text.
        candidate = stripped[: last_close + 1]

        for start in range(last_close, -1, -1):
            if candidate[start] != open_char:
                continue

            json_candidate = candidate[start : last_close + 1]
            # Quick sanity check: balanced braces/brackets.
            depth = 0
            in_string = False
            escape_next = False
            for ch in json_candidate:
                if escape_next:
                    escape_next = False
                    continue
                if ch == "\\" and in_string:
                    escape_next = True
                    continue
                if ch == '"':
                    in_string = not in_string
                    continue
                if in_string:
                    continue
                if ch == open_char:
                    depth += 1
                elif ch == close_char:
                    depth -= 1

            if depth == 0:
                return json_candidate

    return None


def parse_beta_response(
    *,
    output_format: ResponseFormatT | NotGiven,
    response: BetaMessage,
) -> ParsedBetaMessage[ResponseFormatT]:
    content_list: list[ParsedBetaContentBlock[ResponseFormatT]] = []

    # Intermediate tool-calling turns (stop_reason == "tool_use") contain tool_use
    # blocks as the primary output; any text blocks in that turn are not structured
    # output and must not be parsed against the schema.
    is_tool_use_turn = response.stop_reason == "tool_use"

    for content in response.content:
        if content.type == "text":
            parsed: ResponseFormatT | None = None
            if not is_tool_use_turn:
                parsed = parse_text(content.text, output_format)
            content_list.append(
                construct_type_unchecked(
                    type_=ParsedBetaTextBlock[ResponseFormatT],
                    value={**content.to_dict(), "parsed_output": parsed},
                )
            )
        else:
            content_list.append(content)  # type: ignore

    return construct_type_unchecked(
        type_=ParsedBetaMessage[ResponseFormatT],
        value={
            **response.to_dict(),
            "content": content_list,
        },
    )


def parse_response(
    *,
    output_format: ResponseFormatT | NotGiven,
    response: Message,
) -> ParsedMessage[ResponseFormatT]:
    content_list: list[ParsedContentBlock[ResponseFormatT]] = []

    # Intermediate tool-calling turns (stop_reason == "tool_use") contain tool_use
    # blocks as the primary output; any text blocks in that turn are not structured
    # output and must not be parsed against the schema.
    is_tool_use_turn = response.stop_reason == "tool_use"

    for content in response.content:
        if content.type == "text":
            parsed = None
            if not is_tool_use_turn:
                parsed = parse_text(content.text, output_format)
            content_list.append(
                construct_type_unchecked(
                    type_=ParsedTextBlock[ResponseFormatT],
                    value={**content.to_dict(), "parsed_output": parsed},
                )
            )
        else:
            content_list.append(content)  # type: ignore

    return construct_type_unchecked(
        type_=ParsedMessage[ResponseFormatT],
        value={
            **response.to_dict(),
            "content": content_list,
        },
    )
