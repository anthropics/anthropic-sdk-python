"""A browser toolset through `client.beta.messages.tool_runner` with the Messages responses mocked."""

from __future__ import annotations

import os
import json
from typing import Any, cast

import httpx2
import pytest
from respx import MockRouter

from anthropic import Anthropic, AsyncAnthropic, beta_tool, beta_async_tool
from anthropic.tools import ToolsetContractError
from anthropic._compat import PYDANTIC_V1

from ._fakes import FakeBrowser, AsyncFakeBrowser

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")

pytestmark = [pytest.mark.respx(base_url=base_url)]
needs_runner = pytest.mark.skipif(PYDANTIC_V1, reason="tool runner not supported with pydantic v1")


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


def _member_use(name: str, id: str, input: dict[str, Any]) -> dict[str, Any]:
    return {"type": "tool_use", "id": id, "name": name, "input": input, "toolset_name": "browser"}


DONE = _message({"type": "text", "text": "Done."}, stop="end_turn")


def _requests(respx_mock: MockRouter) -> list[dict[str, Any]]:
    calls = cast(list[Any], list(respx_mock.calls))
    return [cast(dict[str, Any], json.loads(call.request.content)) for call in calls]


@needs_runner
@pytest.mark.parametrize("flavour", ["sync", "async"])
async def test_member_calls_round_trip_through_the_runner(
    respx_mock: MockRouter, client: Anthropic, async_client: AsyncAnthropic, flavour: str
) -> None:
    respx_mock.post("/v1/messages").mock(
        side_effect=[
            _message(
                _member_use("navigate", "toolu_nav", {"url": "https://example.com/"}),
                _member_use("teleport", "toolu_bad", {}),
            ),
            DONE,
        ]
    )
    make: Any = (client if flavour == "sync" else async_client).beta.messages.tool_runner
    browser = FakeBrowser() if flavour == "sync" else AsyncFakeBrowser()
    runner = make(
        max_tokens=1024, model="claude-haiku-4-5", tools=[browser], messages=[{"role": "user", "content": "go"}]
    )

    done = runner.until_done()
    if flavour == "async":
        await done

    first, second = _requests(respx_mock)
    # The entry on the wire is exactly to_dict(): the type plus enabled:false for unimplemented members.
    assert first["tools"] == [browser.to_dict()]
    assert "browser-toolset" in cast(Any, respx_mock.calls[0]).request.headers["x-stainless-helper"].split(", ")
    results = second["messages"][-1]["content"]
    assert results[0]["tool_use_id"] == "toolu_nav" and results[0]["toolset_name"] == "browser"
    assert [b["type"] for b in results[0]["content"]] == ["text", "browser_state"]
    assert "is_error" not in results[0]
    assert results[1] == {
        "type": "tool_result",
        "tool_use_id": "toolu_bad",
        "toolset_name": "browser",
        "content": [{"type": "text", "text": "Error: unknown browser toolset member 'teleport'"}],
        "is_error": True,
    }
    # The member and the state hook both saw the tool_use they were answering.
    assert browser.world.contexts[0].tool_use is not None and browser.world.contexts[0].tool_use.id == "toolu_nav"


@needs_runner
async def test_member_calls_round_trip_through_the_async_runner(
    respx_mock: MockRouter, async_client: AsyncAnthropic
) -> None:
    respx_mock.post("/v1/messages").mock(side_effect=[_message(_member_use("get_page_text", "toolu_txt", {})), DONE])
    browser = AsyncFakeBrowser()
    runner = async_client.beta.messages.tool_runner(
        max_tokens=1024, model="claude-haiku-4-5", tools=[browser], messages=[{"role": "user", "content": "go"}]
    )
    await runner.until_done()

    results = _requests(respx_mock)[1]["messages"][-1]["content"]
    assert results[0]["content"][0] == {"type": "text", "text": "Hello"}
    assert results[0]["content"][1]["type"] == "browser_state"


@needs_runner
def test_a_toolset_of_the_other_flavour_is_refused_when_the_runner_is_built(
    client: Anthropic, async_client: AsyncAnthropic
) -> None:
    messages: Any = [{"role": "user", "content": "go"}]
    with pytest.raises(
        ToolsetContractError, match=r"Received an async tool or toolset \(AsyncFakeBrowser\) in the synchronous"
    ):
        client.beta.messages.tool_runner(
            max_tokens=1024, model="claude-haiku-4-5", tools=cast(Any, [AsyncFakeBrowser()]), messages=messages
        )

    with pytest.raises(
        ToolsetContractError, match=r"Received a synchronous tool or toolset \(FakeBrowser\) in the asynchronous"
    ):
        async_client.beta.messages.tool_runner(
            max_tokens=1024, model="claude-haiku-4-5", tools=cast(Any, [FakeBrowser()]), messages=messages
        )


@needs_runner
@pytest.mark.parametrize("flavour", ["sync", "async"])
async def test_a_toolset_in_set_messages_params_is_sent_as_its_wire_entry(
    respx_mock: MockRouter, client: Anthropic, async_client: AsyncAnthropic, flavour: str
) -> None:
    respx_mock.post("/v1/messages").mock(return_value=DONE)

    make: Any = (client if flavour == "sync" else async_client).beta.messages.tool_runner
    mine = FakeBrowser() if flavour == "sync" else AsyncFakeBrowser()

    runner = make(model="claude-test", max_tokens=64, messages=[{"role": "user", "content": "hi"}], tools=[mine])
    raw: dict[str, Any] = {"type": "custom", "name": "raw", "input_schema": {"type": "object"}}
    runner.set_messages_params(_with_tools(mine, raw))

    done = runner.until_done()
    if flavour == "async":
        await done
    assert _requests(respx_mock)[0]["tools"] == [mine.to_dict(), raw]


@needs_runner
@pytest.mark.parametrize("flavour", ["sync", "async"])
async def test_add_tools_refuses_a_toolset_and_queues_nothing(
    respx_mock: MockRouter, client: Anthropic, async_client: AsyncAnthropic, flavour: str
) -> None:
    respx_mock.post("/v1/messages").mock(return_value=DONE)
    make: Any = (client if flavour == "sync" else async_client).beta.messages.tool_runner
    runner = make(model="claude-test", max_tokens=64, messages=[{"role": "user", "content": "hi"}], tools=[])
    toolset = FakeBrowser() if flavour == "sync" else AsyncFakeBrowser()

    with pytest.raises(
        ToolsetContractError,
        match=r"^add_tools\(\) can't add the 'browser' toolset: a tool runner's toolsets are fixed",
    ):
        runner.add_tools(_noop_tool(flavour, "get_time"), toolset)
    done = runner.until_done()
    if flavour == "async":
        await done

    assert _requests(respx_mock)[0]["messages"] == [{"role": "user", "content": "hi"}]


@needs_runner
@pytest.mark.parametrize("flavour", ["sync", "async"])
@pytest.mark.parametrize("removed", ["toolset", "its_name", "a_function_tool_named_like_it"])
async def test_remove_tools_refuses_a_toolset_and_queues_nothing(
    respx_mock: MockRouter, client: Anthropic, async_client: AsyncAnthropic, flavour: str, removed: str
) -> None:
    respx_mock.post("/v1/messages").mock(return_value=DONE)
    make: Any = (client if flavour == "sync" else async_client).beta.messages.tool_runner
    browser = FakeBrowser() if flavour == "sync" else AsyncFakeBrowser()
    get_time = _noop_tool(flavour, "get_time")
    runner = make(
        model="claude-test", max_tokens=64, messages=[{"role": "user", "content": "hi"}], tools=[browser, get_time]
    )

    refused = {
        "toolset": browser,
        "its_name": "browser",
        "a_function_tool_named_like_it": _noop_tool(flavour, "browser"),
    }
    with pytest.raises(
        ToolsetContractError,
        match=r"^remove_tools\(\) can't remove the 'browser' toolset: a tool runner's toolsets are fixed when it is created; build a new runner without it$",
    ):
        runner.remove_tools(get_time, refused[removed])
    done = runner.until_done()
    if flavour == "async":
        await done

    assert _requests(respx_mock)[0]["messages"] == [{"role": "user", "content": "hi"}]


@needs_runner
@pytest.mark.parametrize("flavour", ["sync", "async"])
@pytest.mark.parametrize("definition_type", ["browser_toolset_20260801", "browser_toolset_20270101"])
async def test_add_tools_refuses_a_raw_definition_of_the_runners_toolset_and_queues_nothing(
    respx_mock: MockRouter, client: Anthropic, async_client: AsyncAnthropic, flavour: str, definition_type: str
) -> None:
    respx_mock.post("/v1/messages").mock(return_value=DONE)
    make: Any = (client if flavour == "sync" else async_client).beta.messages.tool_runner
    browser = FakeBrowser() if flavour == "sync" else AsyncFakeBrowser()
    runner = make(model="claude-test", max_tokens=64, messages=[{"role": "user", "content": "hi"}], tools=[browser])

    with pytest.raises(ToolsetContractError, match=r"^add_tools\(\) can't replace the 'browser' toolset: "):
        runner.add_tools(_noop_tool(flavour, "get_time"), {"type": definition_type})
    done = runner.until_done()
    if flavour == "async":
        await done

    assert _requests(respx_mock)[0]["messages"] == [{"role": "user", "content": "hi"}]


@needs_runner
@pytest.mark.parametrize("flavour", ["sync", "async"])
@pytest.mark.parametrize("added", ["function_tool", "raw_definition"])
async def test_add_tools_refuses_a_tool_named_like_the_runners_toolset_and_queues_nothing(
    respx_mock: MockRouter, client: Anthropic, async_client: AsyncAnthropic, flavour: str, added: str
) -> None:
    respx_mock.post("/v1/messages").mock(return_value=DONE)
    make: Any = (client if flavour == "sync" else async_client).beta.messages.tool_runner
    browser = FakeBrowser() if flavour == "sync" else AsyncFakeBrowser()
    runner = make(model="claude-test", max_tokens=64, messages=[{"role": "user", "content": "hi"}], tools=[browser])
    named: Any = (
        _noop_tool(flavour, "browser")
        if added == "function_tool"
        else {"name": "browser", "description": "A tool.", "input_schema": {"type": "object"}}
    )

    with pytest.raises(
        ToolsetContractError,
        match=r"^add_tools\(\) can't add a tool named 'browser': the runner's browser toolset has that name; give the tool another name$",
    ):
        runner.add_tools(_noop_tool(flavour, "get_time"), named)
    done = runner.until_done()
    if flavour == "async":
        await done

    assert _requests(respx_mock)[0]["messages"] == [{"role": "user", "content": "hi"}]


@needs_runner
@pytest.mark.parametrize("flavour", ["sync", "async"])
async def test_add_tools_sends_a_raw_toolset_definition_of_another_family(
    respx_mock: MockRouter, client: Anthropic, async_client: AsyncAnthropic, flavour: str
) -> None:
    respx_mock.post("/v1/messages").mock(return_value=DONE)
    make: Any = (client if flavour == "sync" else async_client).beta.messages.tool_runner
    browser = FakeBrowser() if flavour == "sync" else AsyncFakeBrowser()
    runner = make(model="claude-test", max_tokens=64, messages=[{"role": "user", "content": "hi"}], tools=[browser])
    computer: Any = {"type": "computer_toolset_20260801"}

    runner.add_tools(computer)
    done = runner.until_done()
    if flavour == "async":
        await done

    assert _requests(respx_mock)[0]["messages"][-1] == {
        "role": "system",
        "content": [{"type": "tool_addition", "tool": {"type": "tool_definition", "definition": computer}}],
    }


@needs_runner
@pytest.mark.parametrize("flavour", ["sync", "async"])
async def test_remove_tools_removes_a_function_tool_named_like_a_member(
    respx_mock: MockRouter, client: Anthropic, async_client: AsyncAnthropic, flavour: str
) -> None:
    respx_mock.post("/v1/messages").mock(return_value=DONE)
    make: Any = (client if flavour == "sync" else async_client).beta.messages.tool_runner
    browser = FakeBrowser() if flavour == "sync" else AsyncFakeBrowser()
    runner = make(
        model="claude-test",
        max_tokens=64,
        messages=[{"role": "user", "content": "hi"}],
        tools=[browser, _noop_tool(flavour, "navigate")],
    )

    runner.remove_tools("navigate")
    done = runner.until_done()
    if flavour == "async":
        await done

    assert _requests(respx_mock)[0]["messages"][-1] == {
        "role": "system",
        "content": [{"type": "tool_removal", "tool": {"type": "tool_reference", "name": "navigate"}}],
    }


@needs_runner
@pytest.mark.parametrize("flavour", ["sync", "async"])
async def test_remove_tools_with_a_member_name_removes_only_the_function_tool_of_that_name(
    respx_mock: MockRouter, client: Anthropic, async_client: AsyncAnthropic, flavour: str
) -> None:
    respx_mock.post("/v1/messages").mock(
        side_effect=[
            _message(
                _member_use("navigate", "toolu_1", {"url": "https://a.test/"}),
                {"type": "tool_use", "id": "toolu_fn", "name": "navigate", "input": {}},
            ),
            DONE,
        ]
    )
    make: Any = (client if flavour == "sync" else async_client).beta.messages.tool_runner
    browser = FakeBrowser() if flavour == "sync" else AsyncFakeBrowser()

    def navigate() -> str:
        return "custom"

    async def navigate_async() -> str:
        return navigate()

    named_like_a_member: Any = (
        beta_tool(navigate, description="A tool named like a browser member.")
        if flavour == "sync"
        else beta_async_tool(navigate_async, name="navigate", description="A tool named like a browser member.")
    )
    runner = make(
        model="claude-test",
        max_tokens=64,
        messages=[{"role": "user", "content": "hi"}],
        tools=[browser, named_like_a_member],
    )
    runner.remove_tools("navigate")

    with pytest.warns(UserWarning, match="Tool 'navigate' not found in tool runner"):
        done = runner.until_done()
        if flavour == "async":
            await done

    assert browser.world.calls == ["navigate"]
    first, second = _requests(respx_mock)
    assert first["messages"][-1] == {
        "role": "system",
        "content": [{"type": "tool_removal", "tool": {"type": "tool_reference", "name": "navigate"}}],
    }
    member_result, function_result = second["messages"][-1]["content"]
    assert member_result["tool_use_id"] == "toolu_1" and "is_error" not in member_result
    assert function_result == {
        "type": "tool_result",
        "tool_use_id": "toolu_fn",
        "content": "Error: Tool 'navigate' not found",
        "is_error": True,
    }


def _noop_tool(flavour: str, name: str) -> Any:
    def run() -> str:
        return f"{name} ran"

    async def run_async() -> str:
        return run()

    if flavour == "sync":
        return beta_tool(run, name=name, description=f"Run {name}.")
    return beta_async_tool(run_async, name=name, description=f"Run {name}.")


@needs_runner
@pytest.mark.parametrize("flavour", ["sync", "async"])
@pytest.mark.parametrize("with_toolset", [False, True])
async def test_a_tools_list_is_kept_so_editing_it_in_place_reaches_the_next_request(
    respx_mock: MockRouter, client: Anthropic, async_client: AsyncAnthropic, flavour: str, with_toolset: bool
) -> None:
    respx_mock.post("/v1/messages").mock(return_value=DONE)
    make: Any = (client if flavour == "sync" else async_client).beta.messages.tool_runner
    mine = FakeBrowser() if flavour == "sync" else AsyncFakeBrowser()
    toolsets: list[Any] = [mine] if with_toolset else []
    runner = make(model="claude-test", max_tokens=64, messages=[{"role": "user", "content": "hi"}], tools=toolsets)
    raw: dict[str, Any] = {"type": "custom", "name": "raw", "input_schema": {"type": "object"}}
    added: dict[str, Any] = {"type": "custom", "name": "added", "input_schema": {"type": "object"}}
    tools: list[Any] = [*toolsets, raw]

    def update(params: Any) -> Any:
        return {**params, "tools": tools}

    runner.set_messages_params(update)
    tools.append(added)
    done = runner.until_done()
    if flavour == "async":
        await done
    assert _requests(respx_mock)[0]["tools"] == [*(toolset.to_dict() for toolset in toolsets), raw, added]


@needs_runner
@pytest.mark.parametrize("flavour", ["sync", "async"])
async def test_a_function_tool_appended_to_the_list_in_place_is_sent_with_the_next_request(
    respx_mock: MockRouter, client: Anthropic, async_client: AsyncAnthropic, flavour: str
) -> None:
    respx_mock.post("/v1/messages").mock(return_value=DONE)
    make: Any = (client if flavour == "sync" else async_client).beta.messages.tool_runner
    runner = make(model="claude-test", max_tokens=64, messages=[{"role": "user", "content": "hi"}], tools=[])

    def search(query: str) -> str:
        """Search for something."""
        return query

    async def async_search(query: str) -> str:
        """Search for something."""
        return query

    tool = beta_tool(search) if flavour == "sync" else beta_async_tool(async_search)
    raw: dict[str, Any] = {"type": "custom", "name": "raw", "input_schema": {"type": "object"}}
    tools: list[Any] = [raw]

    def update(params: Any) -> Any:
        return {**params, "tools": tools}

    runner.set_messages_params(update)
    tools.append(tool)
    done = runner.until_done()
    if flavour == "async":
        await done
    assert _requests(respx_mock)[0]["tools"] == [raw, tool.to_dict()]


@needs_runner
@pytest.mark.parametrize("flavour", ["sync", "async"])
async def test_a_toolset_taken_out_of_the_list_in_place_is_not_sent_with_the_next_request(
    respx_mock: MockRouter, client: Anthropic, async_client: AsyncAnthropic, flavour: str
) -> None:
    paused = _message({"type": "text", "text": "Working."}, stop="pause_turn")
    respx_mock.post("/v1/messages").mock(side_effect=[paused, DONE])
    make: Any = (client if flavour == "sync" else async_client).beta.messages.tool_runner
    mine = FakeBrowser() if flavour == "sync" else AsyncFakeBrowser()
    runner = make(model="claude-test", max_tokens=64, messages=[{"role": "user", "content": "hi"}], tools=[mine])
    raw: dict[str, Any] = {"type": "custom", "name": "raw", "input_schema": {"type": "object"}}
    tools: list[Any] = [mine, raw]

    def update(params: Any) -> Any:
        return {**params, "tools": tools}

    runner.set_messages_params(update)
    if flavour == "sync":
        for _ in runner:
            if mine in tools:
                tools.remove(mine)
    else:
        async for _ in runner:
            if mine in tools:
                tools.remove(mine)
    assert [request["tools"] for request in _requests(respx_mock)] == [[mine.to_dict(), raw], [raw]]


@needs_runner
@pytest.mark.parametrize("flavour", ["sync", "async"])
async def test_tools_passed_as_a_one_shot_iterable_reach_every_request(
    respx_mock: MockRouter, client: Anthropic, async_client: AsyncAnthropic, flavour: str
) -> None:
    paused = _message({"type": "text", "text": "Working."}, stop="pause_turn")
    respx_mock.post("/v1/messages").mock(side_effect=[paused, DONE])
    make: Any = (client if flavour == "sync" else async_client).beta.messages.tool_runner
    mine = FakeBrowser() if flavour == "sync" else AsyncFakeBrowser()
    runner = make(model="claude-test", max_tokens=64, messages=[{"role": "user", "content": "hi"}], tools=[mine])
    raw: dict[str, Any] = {"type": "custom", "name": "raw", "input_schema": {"type": "object"}}

    def update(params: Any) -> Any:
        return {**params, "tools": (tool for tool in [mine, raw])}

    runner.set_messages_params(update)
    done = runner.until_done()
    if flavour == "async":
        await done
    assert [request["tools"] for request in _requests(respx_mock)] == [[mine.to_dict(), raw]] * 2


@needs_runner
@pytest.mark.parametrize("flavour", ["sync", "async"])
async def test_messages_passed_as_a_one_shot_iterable_reach_every_request(
    respx_mock: MockRouter, client: Anthropic, async_client: AsyncAnthropic, flavour: str
) -> None:
    paused = _message({"type": "text", "text": "Working."}, stop="pause_turn")
    respx_mock.post("/v1/messages").mock(side_effect=[paused, DONE])
    make: Any = (client if flavour == "sync" else async_client).beta.messages.tool_runner
    mine = FakeBrowser() if flavour == "sync" else AsyncFakeBrowser()
    first = {"role": "user", "content": "hi"}
    runner = make(model="claude-test", max_tokens=64, messages=[first], tools=[mine])

    def update(params: Any) -> Any:
        return {**params, "messages": (message for message in params["messages"])}

    runner.set_messages_params(update)
    done = runner.until_done()
    if flavour == "async":
        await done
    assert [request["messages"][:1] for request in _requests(respx_mock)] == [[first]] * 2


def _with_tools(*tools: Any) -> Any:
    def update(params: Any) -> Any:
        return {**params, "tools": list(tools)}

    return update


@pytest.mark.parametrize("flavour", ["sync", "async"])
async def test_a_toolset_instance_stands_in_tools_for_create_and_count_tokens(
    respx_mock: MockRouter, client: Anthropic, async_client: AsyncAnthropic, flavour: str
) -> None:
    # BetaToolLike: messages.create and its siblings take the toolset instance itself and send its wire entry; the
    # sync and async resources are separate methods, so both are exercised.
    respx_mock.post("/v1/messages").mock(return_value=_message({"type": "text", "text": "Done."}, stop="end_turn"))
    respx_mock.post("/v1/messages/count_tokens").mock(return_value=httpx2.Response(200, json={"input_tokens": 3}))

    raw: Any = {"type": "custom", "name": "raw", "input_schema": {"type": "object"}}
    messages: Any = [{"role": "user", "content": "hi"}]

    if flavour == "sync":
        browser: Any = FakeBrowser()
        client.beta.messages.create(model="m", max_tokens=8, messages=messages, tools=[browser, raw])
        client.beta.messages.count_tokens(model="m", messages=messages, tools=[browser])
    else:
        browser = AsyncFakeBrowser()
        await async_client.beta.messages.create(model="m", max_tokens=8, messages=messages, tools=[browser, raw])
        await async_client.beta.messages.count_tokens(model="m", messages=messages, tools=[browser])

    sent = [body["tools"] for body in _requests(respx_mock)]
    assert sent == [[browser.to_dict(), raw], [browser.to_dict()]]
