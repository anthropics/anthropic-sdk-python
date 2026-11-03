from __future__ import annotations

import os
import json
from typing import Any, TypeVar, Iterator
from typing_extensions import AsyncIterator

import jiter
import pytest

_T = TypeVar("_T")


def load_fixture(fixture_name: str) -> str:
    """Load a fixture file from the fixtures directory."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    fixtures_dir = os.path.join(current_dir, "fixtures")
    with open(os.path.join(fixtures_dir, fixture_name), "r") as f:
        return f.read()


def get_response(fixture_name: str) -> Iterator[bytes]:
    """Convert a fixture file into a stream of bytes for testing."""
    content = load_fixture(fixture_name)
    for line in content.splitlines():
        yield line.encode() + b"\n"


async def to_async_iter(iter: Iterator[_T]) -> AsyncIterator[_T]:
    """Convert a synchronous iterator to an asynchronous one."""
    for event in iter:
        yield event


LONG_TOOL_INPUT = json.dumps({"path": "notes.md", "content": 'a "quoted" café line\\ \n' * 2000})


def get_long_tool_input_response(tool_input: str = LONG_TOOL_INPUT) -> Iterator[bytes]:
    """A `tool_use` block whose input holds a long string, streamed in small `input_json_delta` events."""
    events: list[dict[str, Any]] = [
        {
            "type": "message_start",
            "message": {
                "id": "msg_01",
                "type": "message",
                "role": "assistant",
                "model": "claude-sonnet-4-20250514",
                "content": [],
                "stop_reason": None,
                "stop_sequence": None,
                "usage": {"input_tokens": 10, "output_tokens": 1},
            },
        },
        {
            "type": "content_block_start",
            "index": 0,
            "content_block": {
                "type": "tool_use",
                "id": "toolu_01",
                "name": "write_file",
                "input": {},
                "caller": {"type": "direct"},
            },
        },
        *(
            {
                "type": "content_block_delta",
                "index": 0,
                "delta": {"type": "input_json_delta", "partial_json": tool_input[i : i + 8]},
            }
            for i in range(0, len(tool_input), 8)
        ),
        {"type": "content_block_stop", "index": 0},
        {
            "type": "message_delta",
            "delta": {"stop_reason": "tool_use", "stop_sequence": None},
            "usage": {"output_tokens": 100},
        },
        {"type": "message_stop"},
    ]
    for event in events:
        yield f"event: {event['type']}\ndata: {json.dumps(event)}\n\n".encode()


def record_parsed_json_sizes(monkeypatch: pytest.MonkeyPatch) -> list[int]:
    """Patches `jiter.from_json` to record the size of every input it parses."""
    sizes: list[int] = []
    from_json = jiter.from_json

    def recording_from_json(json_data: bytes, **kwargs: Any) -> Any:
        sizes.append(len(json_data))
        return from_json(json_data, **kwargs)

    monkeypatch.setattr(jiter, "from_json", recording_from_json)
    return sizes


def assert_long_tool_input_parsed(snapshots: list[object], final_input: object, parsed_sizes: list[int]) -> None:
    # re-parsing the whole buffer on every delta would add up to hundreds of times the input size
    assert sum(parsed_sizes) < 10 * len(LONG_TOOL_INPUT)

    expected: list[object] = []
    for i in range(8, len(LONG_TOOL_INPUT), 8):
        expected.append(jiter.from_json(LONG_TOOL_INPUT[:i].encode(), partial_mode=True))
    expected.append(json.loads(LONG_TOOL_INPUT))

    assert snapshots == expected
    assert final_input == json.loads(LONG_TOOL_INPUT)
