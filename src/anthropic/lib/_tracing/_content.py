from __future__ import annotations

import re
from typing import cast
from collections.abc import Mapping, Callable, Sequence
from typing_extensions import Literal, TypedDict, NotRequired

from ._utils import MessageCreateBody, get, as_dict, to_json
from ...types import TextBlockParam, SearchResultBlockParam
from ..._utils import is_list
from ..._tracing import DEFAULT_MAX_CONTENT_BYTES
from ._attributes import AnthropicSpan, AttributeName
from ...types.beta import BetaTextBlockParam, BetaSearchResultBlockParam
from ...types.beta.sessions import BetaManagedAgentsTextBlockParam, BetaManagedAgentsSearchResultBlockParam

__all__ = [
    "CONTENT_LIMIT",
    "Part",
    "TextPart",
    "ReasoningPart",
    "ToolCallRequestPart",
    "ToolCallResponsePart",
    "GenericPart",
    "ChatMessage",
    "OutputMessage",
    "InputMessages",
    "OutputMessages",
    "SystemInstructions",
    "ToolResultContent",
    "ResultBlockContent",
    "content_parts",
    "tool_result_content",
    "result_block_content",
    "set_content_attributes",
    "fit_content",
    "truncate_tool_result_content",
    "set_message_content",
]


# The values of the content attributes before they are serialized to JSON. Their shapes follow the JSON schemas of
# the OpenTelemetry generative-AI conventions.


class TextPart(TypedDict):
    type: Literal["text"]
    content: str


class ReasoningPart(TypedDict):
    type: Literal["reasoning"]
    content: str


class ToolCallRequestPart(TypedDict):
    type: Literal["tool_call"]
    id: str
    name: str
    arguments: dict[str, object]
    anthropic_mcp_server_name: NotRequired[str]
    anthropic_toolset_name: NotRequired[str]


class ToolCallResponsePart(TypedDict):
    type: Literal["tool_call_response"]
    id: str
    response: ToolResultContent | ResultBlockContent


class GenericPart(TypedDict):
    """All that is kept of any other block: its `type`, after `anthropic_` when the block is in a message."""

    type: str


Part = TextPart | ReasoningPart | ToolCallRequestPart | ToolCallResponsePart | GenericPart


class ChatMessage(TypedDict):
    role: str
    parts: list[Part]


class OutputMessage(TypedDict):
    role: Literal["assistant"]
    parts: list[Part]


InputMessages = list[ChatMessage]
OutputMessages = list[OutputMessage]
SystemInstructions = list[Part]

ToolResultContent = list[
    TextBlockParam
    | BetaTextBlockParam
    | BetaManagedAgentsTextBlockParam
    | SearchResultBlockParam
    | BetaSearchResultBlockParam
    | BetaManagedAgentsSearchResultBlockParam
    | GenericPart
]
"""The `content` of a tool result, as content blocks. Only `text` and `search_result` blocks keep more than their `type`."""

ResultBlockContent = list[dict[str, object]] | dict[str, object]
"""The `content` of a result block other than `tool_result`: a list of content blocks, or the one object it holds."""

# The default `max_content_bytes`. In bytes of UTF-8. What is kept of an emptied attribute can exceed it by itself.
CONTENT_LIMIT = DEFAULT_MAX_CONTENT_BYTES

# In the order in which they lose their parts to the limit.
PART_ATTRIBUTES: tuple[AttributeName, ...] = (
    "gen_ai.system_instructions",
    "gen_ai.input.messages",
    "gen_ai.output.messages",
)


def set_content_attributes(
    span: AnthropicSpan,
    attributes: Mapping[AttributeName, object],
    *,
    limit: int,
    stop_sequences: Sequence[str] = (),
) -> None:
    """Sets the content attributes of `span` within `limit`, the client's `max_content_bytes`.

    `limit` is in bytes of UTF-8. Each of `attributes` is set as one JSON string, and `stop_sequences` as an array of
    strings, whose size is the total of its strings. Stop sequences that exceed `limit` by themselves are left out
    whole, before anything else is reduced. Those that stay count toward the limit. A span that lost any content has
    `anthropic.content.truncated`.
    """
    stops_size = sum(map(utf8_size, stop_sequences))
    stops_removed = bool(stop_sequences) and stops_size > limit
    if stop_sequences and not stops_removed:
        span.set_attribute("gen_ai.request.stop_sequences", stop_sequences)

    # What fits at the most that it can be stays whole, and none of it is encoded to be measured.
    room = limit if stops_removed else limit - stops_size
    values, truncated = fit_content(attributes, room, most_utf8_size)
    if truncated:
        values, truncated = fit_content(attributes, room)
    for key, value in values.items():
        span.set_attribute(key, value)
    if truncated or stops_removed:
        span.set_attribute("anthropic.content.truncated", True)


def utf8_size(text: str) -> int:
    """The size of `text` in bytes of UTF-8. An ASCII string says that it is one without being read, and has as many
    bytes as characters.
    """
    return len(text) if text.isascii() else len(text.encode("utf-8", "surrogatepass"))


def most_utf8_size(text: str) -> int:
    """The most that `utf8_size` can be, without reading `text`: no character is more than four bytes."""
    return len(text) if text.isascii() else 4 * len(text)


def fit_content(
    attributes: Mapping[AttributeName, object], limit: int, size: Callable[[str], int] = utf8_size
) -> tuple[dict[AttributeName, str], bool]:
    """Serializes each content attribute that is not `None` to JSON, within `limit` bytes of UTF-8 in total.

    `size` gives the bytes of a string, and never fewer than it has. Returns the JSON of each that stays, and whether
    any content was removed. First, `gen_ai.tool.call.arguments` that exceed `limit` by themselves are left out
    whole. Then the parts of the system instructions, then of the input messages, then of the output messages make
    one list, which loses whole parts from its start until the values fit or one part is left. That part keeps the
    start of its `content` that fits and ends with a whole character when it is a `text` part, and is removed
    otherwise. On the span of a tool run, `anthropic.tool_result.content` loses whole content blocks instead, last
    first. What is kept of an attribute that lost everything, such as an emptied list or a message without parts,
    can still total more than `limit`.
    """
    values: dict[AttributeName, str] = {
        key: to_json(value) for key, value in attributes.items() if value is not None and key not in PART_ATTRIBUTES
    }
    arguments = values.get("gen_ai.tool.call.arguments")
    arguments_removed = arguments is not None and size(arguments) > limit
    if arguments_removed:
        del values["gen_ai.tool.call.arguments"]

    # The lists of parts in the order of the one list that they make, and for each attribute that has some, its JSON
    # split where the parts of each list go: one more string than it has lists.
    lists: list[list[Part]] = []
    around: dict[AttributeName, list[str]] = {}
    for key in PART_ATTRIBUTES:
        value = attributes.get(key)
        if value is None:
            continue
        if key == "gen_ai.system_instructions":
            lists.append(cast(SystemInstructions, value))
            around[key] = ["[", "]"]
            continue
        # A message is its `role` and its `parts`, in this order. Its JSON without parts ends with `[]}`.
        starts: dict[str, str] = {}
        texts = ["["]
        for message in cast(InputMessages, value):
            role = message["role"]
            if role not in starts:
                starts[role] = to_json({"role": role, "parts": []})[:-2]
            lists.append(message["parts"])
            texts[-1] += ("," if len(texts) > 1 else "") + starts[role]
            texts.append("]}")
        texts[-1] += "]"
        around[key] = texts
    total = sum(map(size, values.values())) + sum(size(text) for texts in around.values() for text in texts)

    result = attributes.get("anthropic.tool_result.content")
    if total > limit and is_list(result):
        others = total - size(values["anthropic.tool_result.content"])
        values["anthropic.tool_result.content"], truncated = truncate_tool_result_content(
            cast(ToolResultContent, result), limit - others, size
        )
        return values, truncated or arguments_removed

    # Newest first, stopping at the first part that does not fit, so that content far over `limit` costs no more than
    # content at it. The JSON of a list is its brackets, its items, and a comma between each two.
    kept: list[list[str]] = [[] for _ in lists]
    left = [(part, items) for parts, items in zip(lists, kept, strict=True) for part in parts]
    truncated = False
    while left:
        part, items = left.pop()
        item = to_json(part)
        item_size = size(item) + (1 if items else 0)
        if total + item_size <= limit:
            items.append(item)
            total += item_size
            continue
        content = part.get("content")
        if not any(kept) and part["type"] == "text" and isinstance(content, str):
            # The last part of all. What is left for the JSON of `content` without its quotes is what `item` has not.
            start = cut_text(content, limit - total - size(item) + size(to_json(content)) - 2)
            items.append(to_json({**part, "content": start}))
            truncated = bool(left) or start != content
        else:
            truncated = True
        break

    items_of = iter(kept)
    for key, texts in around.items():
        pieces = [texts[0]]
        for text in texts[1:]:
            pieces += [",".join(reversed(next(items_of))), text]
        values[key] = "".join(pieces)
    return values, truncated or arguments_removed


# The characters whose JSON is longer than they are: two bytes, or six for a control character without a short form.
ESCAPED_CHARACTER = re.compile(rb'["\\\x00-\x1f]')
SHORT_ESCAPES = b'"\\\b\f\n\r\t'


def cut_text(content: str, room: int) -> str:
    """The longest start of `content` whose JSON, without its quotes, is within `room` bytes of UTF-8."""
    room = max(room, 0)
    # No character is less than a byte, so no more than `room` of them fit.
    data = content[:room].encode("utf-8", "surrogatepass")
    for match in ESCAPED_CHARACTER.finditer(data, 0, room):
        extra = 1 if match.group() in SHORT_ESCAPES else 5
        if match.end() + extra > room:
            room = min(room, match.start())
            break
        room -= extra
    # The bytes of a character after its first are `10xxxxxx`. A cut before one of them would be inside the character.
    while 0 < room < len(data) and data[room] & 0xC0 == 0x80:
        room -= 1
    return data[:room].decode("utf-8", "surrogatepass")


def truncate_tool_result_content(
    blocks: ToolResultContent, limit: int, size: Callable[[str], int] = utf8_size
) -> tuple[str, bool]:
    """Serializes `blocks` to JSON within `limit` bytes of UTF-8, dropping the last blocks first.

    `size` gives the bytes of a string, and never fewer than it has. Returns the JSON, and whether any block was
    dropped.
    """
    kept: list[str] = []
    total = 2
    for block in blocks:
        item = to_json(block)
        total += size(item) + (1 if kept else 0)
        if total > limit:
            break
        kept.append(item)
    return "[" + ",".join(kept) + "]", len(kept) < len(blocks)


def content_parts(content: object) -> list[Part]:
    """The parts of `content`, a string or a list of content blocks."""
    if isinstance(content, str):
        return [{"type": "text", "content": content}]
    if isinstance(content, (list, tuple)):
        return [block_part(block) for block in cast("list[object]", content)]
    return []


def block_part(block: object) -> Part:
    block_type = get(block, "type")
    if block_type == "text":
        return {"type": "text", "content": get(block, "text")}
    if block_type == "thinking":
        return {"type": "reasoning", "content": get(block, "thinking")}
    if block_type in ("tool_use", "server_tool_use"):
        tool_call: ToolCallRequestPart = {
            "type": "tool_call",
            "id": get(block, "id"),
            "name": get(block, "name"),
            "arguments": get(block, "input"),
        }
        toolset_name = get(block, "toolset_name")
        if block_type == "tool_use" and isinstance(toolset_name, str):
            tool_call["anthropic_toolset_name"] = toolset_name
        return tool_call
    if block_type == "mcp_tool_use":
        return {
            "type": "tool_call",
            "id": get(block, "id"),
            "name": get(block, "name"),
            "arguments": get(block, "input"),
            "anthropic_mcp_server_name": get(block, "server_name"),
        }
    if block_type == "tool_result":
        return {
            "type": "tool_call_response",
            "id": get(block, "tool_use_id"),
            "response": tool_result_content(get(block, "content")),
        }
    # The result block of an MCP tool or of a server tool, such as `web_search_tool_result`.
    if isinstance(block_type, str) and block_type.endswith("_tool_result"):
        return {
            "type": "tool_call_response",
            "id": get(block, "tool_use_id"),
            "response": result_block_content(get(block, "content")),
        }
    return {"type": f"anthropic_{block_type}" if isinstance(block_type, str) else "anthropic_unknown"}


def tool_result_content(content: object) -> ToolResultContent:
    if isinstance(content, str):
        return [{"type": "text", "text": content}]
    if not isinstance(content, (list, tuple)):
        return []
    blocks: ToolResultContent = []
    for block in cast("list[object]", content):
        block_type = get(block, "type")
        if block_type in ("text", "search_result"):
            blocks.append(cast("TextBlockParam | SearchResultBlockParam", without_data(block)))
            continue
        blocks.append({"type": block_type if isinstance(block_type, str) else "unknown"})
    return blocks


def result_block_content(content: object) -> ResultBlockContent:
    if isinstance(content, str):
        return [{"type": "text", "text": content}]
    if isinstance(content, (list, tuple)):
        blocks: list[dict[str, object]] = []
        for block in cast("list[object]", content):
            block_type = get(block, "type")
            if block_type in ("text", "search_result", "web_search_result"):
                blocks.append(cast("dict[str, object]", without_data(block)))
                continue
            blocks.append({"type": block_type if isinstance(block_type, str) else "unknown"})
        return blocks
    if as_dict(content) is None:
        return []
    return cast("dict[str, object]", without_data(content))


def without_data(value: object) -> object:
    """`value` without its `encrypted_` fields, which are opaque, and without image and document data, which is
    large and binary, at any depth.
    """
    if isinstance(value, (list, tuple)):
        return [without_data(item) for item in cast("list[object]", value)]
    fields = as_dict(value)
    if fields is None:
        return value
    if fields.get("type") in ("image", "document"):
        return {"type": fields["type"]}
    is_file_data = fields.get("type") == "text_editor_code_execution_view_result" and fields.get("file_type") in (
        "image",
        "pdf",
    )
    return {
        key: without_data(item)
        for key, item in fields.items()
        if not key.startswith("encrypted_") and not (key == "content" and is_file_data)
    }


def set_message_content(span: AnthropicSpan, body: MessageCreateBody, output: object, *, limit: int) -> None:
    """Sets the content attributes of a Messages create call, within `limit`, the client's `max_content_bytes`.

    `output` is the response's content, if it has one.
    """
    messages = body.get("messages")
    inputs: InputMessages = [
        {"role": str(get(message, "role") or "user"), "parts": content_parts(get(message, "content"))}
        for message in (cast("list[object]", messages) if isinstance(messages, (list, tuple)) else [])
    ]
    system = body.get("system")
    instructions: SystemInstructions | None = None if system is None else content_parts(system)
    outputs: OutputMessages | None = None if output is None else [{"role": "assistant", "parts": content_parts(output)}]

    # An array of strings, not JSON, as the conventions type it.
    stop_sequences = body.get("stop_sequences")
    stops: list[str] = list(stop_sequences) if isinstance(stop_sequences, (list, tuple)) else []

    set_content_attributes(
        span,
        {
            "gen_ai.system_instructions": instructions,
            "gen_ai.input.messages": inputs,
            "gen_ai.output.messages": outputs,
        },
        limit=limit,
        stop_sequences=stops,
    )
