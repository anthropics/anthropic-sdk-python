"""A computer toolset through `client.beta.messages.tool_runner` with the Messages responses mocked, alone and
beside a browser toolset."""

from __future__ import annotations

import os
import json
from typing import Any, cast

import httpx2
import pytest
from respx import MockRouter

from anthropic import Anthropic, AsyncAnthropic
from anthropic._compat import PYDANTIC_V1

from ._fakes import FakeBrowser
from ._computer_fakes import FakeDesktop, AsyncFakeDesktop

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")

pytestmark = [
    pytest.mark.respx(base_url=base_url),
    pytest.mark.skipif(PYDANTIC_V1, reason="tool runner not supported with pydantic v1"),
]

HALT = "Not executed: an earlier computer action in this turn failed."


@pytest.fixture
def client(client: Anthropic) -> Anthropic:  # the shared client (tests/conftest.py), without retries
    return client.with_options(max_retries=0)


@pytest.fixture
def async_client(async_client: AsyncAnthropic) -> AsyncAnthropic:
    return async_client.with_options(max_retries=0)


def _message(*blocks: dict[str, Any], stop: str = "tool_use") -> httpx2.Response:
    return httpx2.Response(
        200,
        json={
            "id": "msg_1",
            "type": "message",
            "role": "assistant",
            "model": "claude-haiku-4-5",
            "content": list(blocks),
            "stop_reason": stop,
            "stop_sequence": None,
            "usage": {"input_tokens": 1, "output_tokens": 1},
        },
    )


def _member_use(name: str, id: str, input: dict[str, Any], family: str = "computer") -> dict[str, Any]:
    return {"type": "tool_use", "id": id, "name": name, "input": input, "toolset_name": family}


DONE = _message({"type": "text", "text": "Done."}, stop="end_turn")


def _requests(respx_mock: MockRouter) -> list[dict[str, Any]]:
    calls = cast(list[Any], list(respx_mock.calls))
    return [cast(dict[str, Any], json.loads(call.request.content)) for call in calls]


def test_member_calls_round_trip_through_the_runner(respx_mock: MockRouter, client: Anthropic) -> None:
    respx_mock.post("/v1/messages").mock(
        side_effect=[
            _message(
                _member_use("mouse_move", "toolu_move", {"coordinate": [10, 20]}),
                _member_use("cursor_position", "toolu_pos", {}),
                _member_use("teleport", "toolu_bad", {}),
            ),
            DONE,
        ]
    )
    desktop = FakeDesktop()
    runner = client.beta.messages.tool_runner(
        max_tokens=1024, model="claude-haiku-4-5", tools=[desktop], messages=[{"role": "user", "content": "go"}]
    )
    runner.until_done()

    first, second = _requests(respx_mock)
    # The entry on the wire is exactly to_dict(): the type plus enabled:false for unimplemented members.
    assert first["tools"] == [desktop.to_dict()]
    assert "computer-toolset" in cast(Any, respx_mock.calls[0]).request.headers["x-stainless-helper"].split(", ")
    results = second["messages"][-1]["content"]
    assert results[0] == {
        "type": "tool_result",
        "tool_use_id": "toolu_move",
        "toolset_name": "computer",
        "content": [{"type": "text", "text": "Moved the mouse."}],
    }
    assert results[1]["content"] == [{"type": "text", "text": "X=10,Y=20"}]
    assert results[2] == {
        "type": "tool_result",
        "tool_use_id": "toolu_bad",
        "toolset_name": "computer",
        "content": [{"type": "text", "text": "Error: unknown computer toolset member 'teleport'"}],
        "is_error": True,
    }
    assert desktop.desktop.contexts[0].tool_use is not None and desktop.desktop.contexts[0].tool_use.id == "toolu_move"


def test_a_failure_halts_the_later_computer_actions_of_the_turn_with_the_computer_wording(
    respx_mock: MockRouter, client: Anthropic
) -> None:
    respx_mock.post("/v1/messages").mock(
        side_effect=[
            _message(
                _member_use("left_click", "toolu_1", {"coordinate": [1, 1]}),
                _member_use("key", "toolu_2", {"text": "Return"}),
                _member_use("screenshot", "toolu_3", {}),
            ),
            DONE,
        ]
    )
    desktop = FakeDesktop()
    desktop.desktop.fail["key"] = RuntimeError("keyboard unplugged")
    runner = client.beta.messages.tool_runner(
        max_tokens=1024, model="claude-haiku-4-5", tools=[desktop], messages=[{"role": "user", "content": "go"}]
    )
    runner.until_done()

    results = _requests(respx_mock)[1]["messages"][-1]["content"]
    assert [r["tool_use_id"] for r in results] == ["toolu_1", "toolu_2", "toolu_3"]
    assert "is_error" not in results[0]
    assert results[1]["is_error"] is True and results[1]["content"] == [
        {"type": "text", "text": "RuntimeError: keyboard unplugged"}
    ]
    assert results[2] == {
        "type": "tool_result",
        "tool_use_id": "toolu_3",
        "toolset_name": "computer",
        "content": HALT,
        "is_error": True,
    }
    assert desktop.desktop.calls == ["left_click", "key"]  # the screenshot was never taken


def test_a_computer_and_a_browser_toolset_serve_one_request_by_family(
    respx_mock: MockRouter, client: Anthropic
) -> None:
    # The families share member names; each block is routed by its toolset_name, and a failure in one family does
    # not halt the other (each family keeps its own halt wording).
    respx_mock.post("/v1/messages").mock(
        side_effect=[
            _message(
                _member_use("screenshot", "toolu_c1", {}),
                _member_use("screenshot", "toolu_b1", {}, family="browser"),
                _member_use("key", "toolu_c2", {"text": "a"}),
                _member_use("key", "toolu_c3", {"text": "b"}),
                _member_use("navigate", "toolu_b2", {"url": "https://example.com/"}, family="browser"),
                _member_use("navigate", "toolu_b3", {"url": "https://example.com/"}, family="browser"),
            ),
            DONE,
        ]
    )
    desktop, browser = FakeDesktop(), FakeBrowser()
    desktop.desktop.fail["key"] = RuntimeError("stuck")
    browser.world.fail["navigate"] = RuntimeError("offline")
    runner = client.beta.messages.tool_runner(
        max_tokens=1024,
        model="claude-haiku-4-5",
        tools=[desktop, browser],
        messages=[{"role": "user", "content": "go"}],
    )
    runner.until_done()

    first, second = _requests(respx_mock)
    assert first["tools"] == [desktop.to_dict(), browser.to_dict()]
    results = {r["tool_use_id"]: r for r in second["messages"][-1]["content"]}
    assert results["toolu_c1"]["content"][0]["type"] == "image" and results["toolu_c1"]["toolset_name"] == "computer"
    assert [b["type"] for b in results["toolu_b1"]["content"]] == ["image", "browser_state"]
    assert results["toolu_c3"]["content"] == HALT
    assert results["toolu_b3"]["content"] == "Not executed: an earlier action in this turn failed."
    assert desktop.desktop.calls == ["screenshot", "key"] and browser.world.calls == ["screenshot", "navigate"]


def test_a_call_named_after_the_toolset_without_toolset_name_gets_an_error_that_says_what_is_wrong(
    respx_mock: MockRouter, client: Anthropic
) -> None:
    calls: dict[str, dict[str, Any]] = {
        "text": {"actions": '[{"action": "key",}]'},
        "object": {"actions": {"action": "key"}},
        "empty": {"actions": []},
        "no_action": {"actions": [{"action": "screenshot"}, {"text": "a"}]},
        "not_text": {"actions": [{"action": 5}]},
        "not_object": {"actions": ["key"]},
        "flat_number": {"action": 5},
        "null": {"actions": None},
        "odd_name": {"actions": [{"action": "a'b\nc  d"}]},
        "well_formed": {"actions": [{"action": "screenshot"}, {"action": "x"}]},
        "many": {"actions": [{"action": f"a{i}"} for i in range(12)]},
        "flat": {"action": "screenshot"},
        "none": {},
    }
    respx_mock.post("/v1/messages").mock(
        side_effect=[
            _message(
                *({"type": "tool_use", "id": key, "name": "computer", "input": input} for key, input in calls.items()),
                {
                    "type": "tool_use",
                    "id": "null_toolset",
                    "name": "computer",
                    "input": {"actions": []},
                    "toolset_name": None,
                },
                {"type": "tool_use", "id": "calculator", "name": "calculator", "input": {}},
            ),
            DONE,
        ]
    )
    desktop = FakeDesktop()
    runner = client.beta.messages.tool_runner(
        max_tokens=1024, model="claude-haiku-4-5", tools=[desktop], messages=[{"role": "user", "content": "go"}]
    )
    with pytest.warns(UserWarning) as warned:
        runner.until_done()

    results = {result["tool_use_id"]: result for result in _requests(respx_mock)[1]["messages"][-1]["content"]}
    prefix = "Error: the 'computer' toolset could not run this call"
    suffix = "; nothing in the batch was executed"
    many = ", ".join(f"'a{i}'" for i in range(10))
    assert {key: result["content"] for key, result in results.items()} == {
        "text": f"{prefix}: 'actions' is text, not a list of actions{suffix}",
        "object": f"{prefix}: 'actions' is not a list of actions{suffix}",
        "empty": f"{prefix}: the 'actions' list is empty{suffix}",
        "no_action": f"{prefix}: action 1 must be an object with a string 'action' field{suffix}",
        "not_text": f"{prefix}: action 0 must be an object with a string 'action' field{suffix}",
        "not_object": f"{prefix}: action 0 must be an object with a string 'action' field{suffix}",
        "flat_number": f"{prefix}: the call has no 'actions' list{suffix}",
        "null": f"{prefix}: 'actions' is not a list of actions{suffix}",
        "odd_name": f"{prefix}: its actions could not be run as sent (actions: 'a b c d'){suffix}",
        "well_formed": f"{prefix}: its actions could not be run as sent (actions: 'screenshot', 'x'){suffix}",
        "many": f"{prefix}: its actions could not be run as sent (actions: {many}, and 2 more){suffix}",
        "flat": f"{prefix}: the call has no 'actions' list (action: 'screenshot'){suffix}",
        "none": f"{prefix}: the call has no 'actions' list{suffix}",
        "null_toolset": f"{prefix}: the 'actions' list is empty{suffix}",
        # A name that is neither a tool nor a toolset in the run gets the plain not-found reply.
        "calculator": "Error: Tool 'calculator' not found",
    }
    assert all(result["is_error"] is True and "toolset_name" not in result for result in results.values())
    assert [str(w.message).split(".")[0] for w in warned] == ["Tool 'calculator' not found in tool runner"]
    assert desktop.desktop.calls == []


@pytest.mark.parametrize("flavour", ["sync", "async"])
async def test_a_call_named_after_the_toolset_stops_the_toolsets_later_calls_in_the_reply(
    respx_mock: MockRouter, client: Anthropic, async_client: AsyncAnthropic, flavour: str
) -> None:
    respx_mock.post("/v1/messages").mock(
        side_effect=[
            _message(
                _member_use("mouse_move", "toolu_before", {"coordinate": [10, 20]}),
                {"type": "tool_use", "id": "toolu_bad", "name": "computer", "input": {"actions": "["}},
                _member_use("cursor_position", "toolu_after", {}),
            ),
            DONE,
        ]
    )
    if flavour == "sync":
        desktop: Any = FakeDesktop()
        client.beta.messages.tool_runner(
            max_tokens=1024, model="claude-haiku-4-5", tools=[desktop], messages=[{"role": "user", "content": "go"}]
        ).until_done()
    else:
        desktop = AsyncFakeDesktop()
        await async_client.beta.messages.tool_runner(
            max_tokens=1024, model="claude-haiku-4-5", tools=[desktop], messages=[{"role": "user", "content": "go"}]
        ).until_done()

    results = _requests(respx_mock)[1]["messages"][-1]["content"]
    assert [(r["tool_use_id"], r.get("is_error", False)) for r in results] == [
        ("toolu_before", False),
        ("toolu_bad", True),
        ("toolu_after", True),
    ]
    assert results[2]["content"] == HALT
    assert desktop.desktop.calls == ["mouse_move"]


async def test_member_calls_round_trip_through_the_async_runner(
    respx_mock: MockRouter, async_client: AsyncAnthropic
) -> None:
    respx_mock.post("/v1/messages").mock(
        side_effect=[_message(_member_use("zoom", "toolu_z", {"region": [0, 0, 4, 4]})), DONE]
    )
    desktop = AsyncFakeDesktop()
    runner = async_client.beta.messages.tool_runner(
        max_tokens=1024, model="claude-haiku-4-5", tools=[desktop], messages=[{"role": "user", "content": "go"}]
    )
    await runner.until_done()

    results = _requests(respx_mock)[1]["messages"][-1]["content"]
    assert results[0]["content"][0]["source"]["media_type"] == "image/jpeg"


@pytest.mark.parametrize("flavour", ["sync", "async"])
async def test_a_toolset_instance_stands_in_tools_for_create_and_count_tokens(
    respx_mock: MockRouter, client: Anthropic, async_client: AsyncAnthropic, flavour: str
) -> None:
    respx_mock.post("/v1/messages").mock(return_value=DONE)
    respx_mock.post("/v1/messages/count_tokens").mock(return_value=httpx2.Response(200, json={"input_tokens": 3}))
    messages: Any = [{"role": "user", "content": "hi"}]
    if flavour == "sync":
        desktop: Any = FakeDesktop()
        client.beta.messages.create(model="m", max_tokens=8, messages=messages, tools=[desktop])
        client.beta.messages.count_tokens(model="m", messages=messages, tools=[desktop])
    else:
        desktop = AsyncFakeDesktop()
        await async_client.beta.messages.create(model="m", max_tokens=8, messages=messages, tools=[desktop])
        await async_client.beta.messages.count_tokens(model="m", messages=messages, tools=[desktop])
    assert [body["tools"] for body in _requests(respx_mock)] == [[desktop.to_dict()], [desktop.to_dict()]]
