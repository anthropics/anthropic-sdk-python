from __future__ import annotations

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
    if is_given(output_format):
        adapted_type: TypeAdapter[ResponseFormatT] = TypeAdapter(output_format)
        return adapted_type.validate_json(text)
    return None


def _parse_text_for_stop_reason(
    text: str,
    output_format: ResponseFormatT | NotGiven,
    stop_reason: str | None,
) -> ResponseFormatT | None:
    # Structured output is not guaranteed to match the requested schema when
    # generation is refused or truncated. Preserve the response and its stop
    # reason instead of masking it with a JSON/schema validation exception.
    if stop_reason == "refusal" or stop_reason == "max_tokens":
        return None
    return parse_text(text, output_format)


def parse_beta_response(
    *,
    output_format: ResponseFormatT | NotGiven,
    response: BetaMessage,
) -> ParsedBetaMessage[ResponseFormatT]:
    content_list: list[ParsedBetaContentBlock[ResponseFormatT]] = []
    for content in response.content:
        if content.type == "text":
            content_list.append(
                construct_type_unchecked(
                    type_=ParsedBetaTextBlock[ResponseFormatT],
                    value={
                        **content.to_dict(),
                        "parsed_output": _parse_text_for_stop_reason(
                            content.text,
                            output_format,
                            response.stop_reason,
                        ),
                    },
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
    for content in response.content:
        if content.type == "text":
            content_list.append(
                construct_type_unchecked(
                    type_=ParsedTextBlock[ResponseFormatT],
                    value={
                        **content.to_dict(),
                        "parsed_output": _parse_text_for_stop_reason(
                            content.text,
                            output_format,
                            response.stop_reason,
                        ),
                    },
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
