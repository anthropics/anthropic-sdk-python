from __future__ import annotations

import copy
import json
from typing import Any, Set, cast
from typing_extensions import get_args, get_origin

import httpx2
import pytest

from anthropic._compat import model_copy
from anthropic._models import construct_type_unchecked
from anthropic.types.beta import BetaFallbackBlock
from anthropic.types.content_block import ContentBlock
from anthropic.types.parsed_message import ParsedTextBlock, ParsedContentBlock
from anthropic.types.beta.beta_usage import BetaUsage
from anthropic.lib.streaming._beta_messages import accumulate_event
from anthropic.types.beta.beta_content_block import BetaContentBlock
from anthropic.types.beta.parsed_beta_message import ParsedBetaMessage, ParsedBetaTextBlock, ParsedBetaContentBlock


def _union_members(union: Any) -> Set[type]:
    """Return the runtime classes in an `Annotated[Union[...], ...]` type alias."""
    annotated_args = get_args(union)
    assert annotated_args, f"expected an Annotated union, got {union!r}"
    members: Set[type] = set()
    for member in get_args(annotated_args[0]):
        # unwrap generic subscriptions, e.g. ParsedBetaTextBlock[ResponseFormatT]
        members.add(get_origin(member) or member)
    return members


def _to_generated(member: type) -> type:
    """Map a Parsed* wrapper to the generated block class it stands in for."""
    if member.__name__.startswith("Parsed"):
        return member.__bases__[0]
    return member


@pytest.mark.parametrize(
    ("parsed_union", "generated_union", "parsed_file"),
    [
        (ParsedBetaContentBlock, BetaContentBlock, "src/anthropic/types/beta/parsed_beta_message.py"),
        (ParsedContentBlock, ContentBlock, "src/anthropic/types/parsed_message.py"),
    ],
    ids=["beta", "non-beta"],
)
def test_parsed_union_matches_generated_union(parsed_union: Any, generated_union: Any, parsed_file: str) -> None:
    """The hand-written Parsed*ContentBlock unions must track the generated unions.

    If a block type only exists in the generated union, streaming snapshots
    construct it through the parsed union's permissive fallback and it lands
    as the wrong class at runtime (and the wrong type statically).
    """
    parsed_members = {_to_generated(member) for member in _union_members(parsed_union)}
    generated_members = _union_members(generated_union)

    missing = sorted(member.__name__ for member in generated_members - parsed_members)
    extra = sorted(member.__name__ for member in parsed_members - generated_members)
    assert not missing and not extra, (
        f"the hand-written parsed content block union in {parsed_file} is out of sync "
        f"with the generated union: missing={missing} extra={extra}. "
        f"Update the union in {parsed_file} to match the generated content block union."
    )


def test_streamed_fallback_block_is_constructed_as_fallback_block() -> None:
    snapshot = ParsedBetaMessage(
        id="msg_123",
        type="message",
        role="assistant",
        content=[],
        model="claude-sonnet-4-5",
        stop_reason=None,
        stop_sequence=None,
        usage=BetaUsage(input_tokens=10, output_tokens=10),
    )

    event = {
        "type": "content_block_start",
        "index": 0,
        "content_block": {
            "type": "fallback",
            "from": {"model": "claude-sonnet-4-5"},
            "to": {"model": "claude-haiku-4-5"},
            "trigger": {"type": "refusal", "category": None},
        },
    }
    message = accumulate_event(
        event=cast(Any, event),
        current_snapshot=snapshot,
        json_bufs={},
        request_headers=httpx2.Headers(),
    )

    block = message.content[0]
    assert isinstance(block, BetaFallbackBlock)
    assert block.type == "fallback"
    assert block.from_.model == "claude-sonnet-4-5"
    assert block.to.model == "claude-haiku-4-5"


@pytest.mark.parametrize("block_type", [ParsedTextBlock, ParsedBetaTextBlock], ids=["non-beta", "beta"])
def test_parsed_output_is_readable_but_not_dumped(block_type: Any) -> None:
    block = construct_type_unchecked(value={"type": "text", "text": "{}", "citations": None}, type_=block_type)
    # the stream accumulator sets the parsed value after it builds the block
    block.parsed_output = {"greeting": "hi"}

    # the API rejects `parsed_output`, so a dumped block must not carry it
    assert "parsed_output" not in block.model_dump()
    assert "parsed_output" not in block.to_dict()
    assert "parsed_output" not in json.loads(block.to_json())

    assert block.parsed_output == {"greeting": "hi"}

    # copies keep the parsed value but still dump without it
    for copied in [model_copy(block), model_copy(block, deep=True), copy.copy(block), copy.deepcopy(block)]:
        assert copied.parsed_output == block.parsed_output
        assert "parsed_output" not in copied.model_dump()
        assert "parsed_output" not in copied.to_dict()
        assert "parsed_output" not in json.loads(copied.to_json())
