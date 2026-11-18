from __future__ import annotations

import os
import json
from typing import cast
from collections.abc import Iterable, Iterator

import httpx2
import pytest
from respx import MockRouter
from respx.models import Call

from anthropic import Anthropic, AsyncAnthropic, beta_tool, beta_async_tool
from anthropic._compat import PYDANTIC_V1
from anthropic.lib.streaming import BetaMessageStream, BetaAsyncMessageStream

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")
pytestmark = pytest.mark.skipif(PYDANTIC_V1, reason="tool functions require Pydantic v2")


def response(*, final: bool, stream: bool) -> httpx2.Response:
    block: dict[str, object] = (
        {"type": "text", "text": "Done."}
        if final
        else {"type": "tool_use", "id": "toolu_example", "name": "lookup", "input": {"city": "Kraków"}}
    )
    message = {
        "id": "msg_final" if final else "msg_tool",
        "type": "message",
        "role": "assistant",
        "model": "claude-haiku-4-5",
        "content": [block],
        "stop_reason": "end_turn" if final else "tool_use",
        "stop_sequence": None,
        "usage": {"input_tokens": 1, "output_tokens": 1},
    }
    if not stream:
        return httpx2.Response(200, json=message)
    events = [
        {"type": "message_start", "message": {**message, "content": [], "stop_reason": None}},
        {"type": "content_block_start", "index": 0, "content_block": block},
        {"type": "content_block_stop", "index": 0},
        {
            "type": "message_delta",
            "delta": {"stop_reason": message["stop_reason"], "stop_sequence": None},
            "usage": {"output_tokens": 1},
        },
        {"type": "message_stop"},
    ]
    data = "".join(f"event: {event['type']}\ndata: {json.dumps(event)}\n\n" for event in events)
    return httpx2.Response(200, headers={"content-type": "text/event-stream"}, text=data)


@pytest.mark.parametrize("sync", [True, False], ids=["sync", "async"])
@pytest.mark.parametrize("stream", [False, True], ids=["json", "stream"])
@pytest.mark.parametrize("source", ["generator", "iterator", "list", "tuple", "empty", "omitted"])
@pytest.mark.respx(base_url=base_url)
async def test_input_examples_survive_followup_requests(
    sync: bool,
    stream: bool,
    source: str,
    client: Anthropic,
    async_client: AsyncAnthropic,
    respx_mock: MockRouter,
) -> None:
    examples: list[dict[str, object]] = [{"city": "Kraków"}, {"city": "London"}]
    original = json.dumps(examples)
    visited: list[dict[str, object]] = []

    def generate() -> Iterator[dict[str, object]]:
        for example in examples:
            visited.append(example)
            yield example

    input_examples: Iterable[dict[str, object]] | None
    if source == "generator":
        input_examples = generate()
    elif source == "iterator":
        input_examples = iter(examples)
    elif source == "list":
        input_examples = examples
    elif source == "tuple":
        input_examples = tuple(examples)
    elif source == "empty":
        input_examples = iter(())
    else:
        input_examples = None

    respx_mock.post("/v1/messages").mock(
        side_effect=[response(final=False, stream=stream), response(final=True, stream=stream)]
    )
    calls: list[str] = []

    def lookup(city: str) -> str:
        calls.append(city)
        return city

    async def async_lookup(city: str) -> str:
        calls.append(city)
        return city

    received: list[str] = []
    if sync:
        tool = beta_tool(lookup, name="lookup", input_examples=input_examples)
        runner = client.beta.messages.tool_runner(
            model="claude-haiku-4-5",
            max_tokens=1024,
            messages=[{"role": "user", "content": "Look up the city."}],
            tools=[tool],
            stream=stream,
        )
        for item in runner:
            message = item.get_final_message() if isinstance(item, BetaMessageStream) else item
            received.append(message.id)
    else:
        async_tool = beta_async_tool(async_lookup, name="lookup", input_examples=input_examples)
        async_runner = async_client.beta.messages.tool_runner(
            model="claude-haiku-4-5",
            max_tokens=1024,
            messages=[{"role": "user", "content": "Look up the city."}],
            tools=[async_tool],
            stream=stream,
        )
        async for async_item in async_runner:
            async_message = (
                await async_item.get_final_message() if isinstance(async_item, BetaAsyncMessageStream) else async_item
            )
            received.append(async_message.id)

    bodies = [json.loads(call.request.content) for call in cast("list[Call]", respx_mock.calls)]
    assert len(bodies) == 2
    for body in bodies:
        assert len(body["tools"]) == 1
        if source == "omitted":
            assert "input_examples" not in body["tools"][0]
        else:
            assert body["tools"][0]["input_examples"] == ([] if source == "empty" else examples)
    assert bodies[0]["tools"] == bodies[1]["tools"]
    assert bodies[1]["messages"][-1]["content"] == [
        {"type": "tool_result", "tool_use_id": "toolu_example", "content": "Kraków"}
    ]
    assert received == ["msg_tool", "msg_final"]
    assert calls == ["Kraków"]
    assert json.dumps(examples) == original
    if source == "generator":
        assert visited == examples
