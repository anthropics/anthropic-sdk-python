from __future__ import annotations

from typing import Dict, Union

import pytest

from anthropic.types import Message, MessageParam
from anthropic._utils import transform
from anthropic._models import construct_type_unchecked
from anthropic.types.beta import BetaMessage, BetaMessageParam

TEXT_BLOCK: Dict[str, object] = {
    "type": "text",
    "text": "It's sunny.",
    "citations": [
        {
            "type": "char_location",
            "cited_text": "sunny",
            "document_index": 0,
            "document_title": None,
            "start_char_index": 5,
            "end_char_index": 10,
            "file_id": "file_011CNha8iCJcU1wXNR6q4V8w",
        }
    ],
}

TOOL_USE_BLOCK: Dict[str, object] = {
    "type": "tool_use",
    "id": "toolu_01A09q90qw90lq917835lq9",
    "name": "get_weather",
    "input": {"location": "San Francisco, CA"},
}

MESSAGE_BODY: Dict[str, object] = {
    "id": "msg_013Zva2CMHLNnXjNJJKqJ2EF",
    "content": [TEXT_BLOCK, TOOL_USE_BLOCK],
    "model": "claude-sonnet-4-5",
    "role": "assistant",
    "stop_reason": "tool_use",
    "stop_sequence": None,
    "type": "message",
    "usage": {"input_tokens": 10, "output_tokens": 25},
}


def make_message(message_cls: type[Union[Message, BetaMessage]]) -> Union[Message, BetaMessage]:
    return construct_type_unchecked(type_=message_cls, value=MESSAGE_BODY)


parametrize_message_cls = pytest.mark.parametrize(
    "message_cls", [Message, BetaMessage], ids=["message", "beta_message"]
)


@parametrize_message_cls
def test_message_role_and_content(message_cls: type[Union[Message, BetaMessage]]) -> None:
    message = make_message(message_cls)
    param = message.to_param()

    assert param["role"] == "assistant"
    assert param["content"] == message.content


@parametrize_message_cls
def test_message_content_list_is_copied(message_cls: type[Union[Message, BetaMessage]]) -> None:
    message = make_message(message_cls)
    content = message.to_param()["content"]

    assert isinstance(content, list)
    assert content is not message.content
    assert content[0] is message.content[0]


@pytest.mark.parametrize(
    "message_cls,param_type",
    [(Message, MessageParam), (BetaMessage, BetaMessageParam)],
    ids=["message", "beta_message"],
)
def test_message_serializes_as_request_param(
    message_cls: type[Union[Message, BetaMessage]], param_type: object
) -> None:
    param = make_message(message_cls).to_param()

    assert transform(param, param_type) == {"role": "assistant", "content": [TEXT_BLOCK, TOOL_USE_BLOCK]}
