"""Toolset member routing through `client.beta.messages.tool_runner`: the
Messages responses are mocked so the runner sees `tool_use` blocks carrying
`toolset_name` exactly as the API stamps them."""

from __future__ import annotations

import os
import json
from typing import Any, cast

import httpx2
import pytest
from respx import MockRouter

from anthropic import Anthropic, AsyncAnthropic, beta_tool, beta_async_tool
from anthropic._compat import PYDANTIC_V1
from anthropic.lib.tools import BetaFunctionTool, BetaAsyncFunctionTool
from anthropic.types.beta import BetaMessageParam, BetaToolUseBlock, BetaContentBlockParam
from anthropic.lib.tools._toolsets import ToolsetClosedError, ToolsetContractError
from anthropic.lib._stainless_helpers import tag_helper

from ._stubs import BROWSER_ENTRY, EchoBrowserToolset, AsyncEchoBrowserToolset

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")

pytestmark = [
    pytest.mark.skipif(PYDANTIC_V1, reason="tool runner not supported with pydantic v1"),
    pytest.mark.respx(base_url=base_url),
]


def _tool_use(name: str, id: str, input: dict[str, Any], *, toolset_name: str | None = None) -> dict[str, Any]:
    block: dict[str, Any] = {"type": "tool_use", "id": id, "name": name, "input": input}
    if toolset_name is not None:
        block["toolset_name"] = toolset_name
    return block


def _response(*blocks: dict[str, Any]) -> httpx2.Response:
    return httpx2.Response(
        200,
        json={
            "id": "msg_tool_use",
            "type": "message",
            "role": "assistant",
            "model": "claude-haiku-4-5",
            "content": list(blocks),
            "stop_reason": "tool_use",
            "stop_sequence": None,
            "usage": {"input_tokens": 1, "output_tokens": 1},
        },
    )


def _end_turn() -> httpx2.Response:
    return httpx2.Response(
        200,
        json={
            "id": "msg_end_turn",
            "type": "message",
            "role": "assistant",
            "model": "claude-haiku-4-5",
            "content": [{"type": "text", "text": "Done."}],
            "stop_reason": "end_turn",
            "stop_sequence": None,
            "usage": {"input_tokens": 1, "output_tokens": 1},
        },
    )


def _sse(message: dict[str, Any]) -> httpx2.Response:
    """`message` as the server-sent event stream a streaming request receives (one event per content block)."""
    events: list[str] = []

    def event(name: str, data: dict[str, Any]) -> None:
        events.append(f"event: {name}\ndata: {json.dumps(data)}\n\n")

    event("message_start", {"type": "message_start", "message": {**message, "content": [], "stop_reason": None}})
    for index, block in enumerate(message["content"]):
        if block["type"] == "tool_use":
            event(
                "content_block_start",
                {"type": "content_block_start", "index": index, "content_block": {**block, "input": {}}},
            )
            delta = {"type": "input_json_delta", "partial_json": json.dumps(block["input"])}
        else:
            event(
                "content_block_start",
                {"type": "content_block_start", "index": index, "content_block": {**block, "text": ""}},
            )
            delta = {"type": "text_delta", "text": block["text"]}
        event("content_block_delta", {"type": "content_block_delta", "index": index, "delta": delta})
        event("content_block_stop", {"type": "content_block_stop", "index": index})
    usage = {"output_tokens": 1}
    event("message_delta", {"type": "message_delta", "delta": {"stop_reason": message["stop_reason"]}, "usage": usage})
    event("message_stop", {"type": "message_stop"})
    return httpx2.Response(200, content="".join(events).encode(), headers={"content-type": "text/event-stream"})


def _tool_removal(name: str) -> BetaContentBlockParam:
    return {"type": "tool_removal", "tool": {"type": "tool_reference", "name": name}}


@pytest.fixture
def client(client: Anthropic) -> Anthropic:  # the shared client (tests/conftest.py), without retries
    return client.with_options(max_retries=0)


@pytest.fixture
def async_client(async_client: AsyncAnthropic) -> AsyncAnthropic:
    return async_client.with_options(max_retries=0)


def _run_sync(client: Anthropic, *, tools: list[Any], messages: list[BetaMessageParam]) -> list[BetaMessageParam]:
    runner = client.beta.messages.tool_runner(max_tokens=1024, model="claude-haiku-4-5", tools=tools, messages=messages)
    responses: list[BetaMessageParam] = []
    for _ in runner:
        response = runner.generate_tool_call_response()
        if response is not None:
            responses.append(response)
    return responses


async def _run_async(
    client: AsyncAnthropic, *, tools: list[Any], messages: list[BetaMessageParam]
) -> list[BetaMessageParam]:
    runner = client.beta.messages.tool_runner(max_tokens=1024, model="claude-haiku-4-5", tools=tools, messages=messages)
    responses: list[BetaMessageParam] = []
    async for _ in runner:
        response = await runner.generate_tool_call_response()
        if response is not None:
            responses.append(response)
    return responses


def _sent_tools(respx_mock: MockRouter) -> list[dict[str, Any]]:
    """The `tools` array of the first request the runner sent."""
    call = cast(Any, respx_mock.calls[0])
    body = cast(dict[str, Any], json.loads(call.request.content))
    return cast(list[dict[str, Any]], body["tools"])


USER_MESSAGE: BetaMessageParam = {"role": "user", "content": "Open example.com"}


@pytest.fixture
def navigate() -> BetaFunctionTool[Any]:
    # Built inside the fixture: `beta_tool` raises at decoration time under pydantic v1.
    @beta_tool
    def navigate(url: str) -> str:
        """Custom tool that shares a browser member's name."""
        return f"custom:{url}"

    return navigate


@pytest.fixture
def async_navigate() -> BetaAsyncFunctionTool[Any]:
    async def _async_navigate(url: str) -> str:
        """Custom tool that shares a browser member's name."""
        return f"custom:{url}"

    return beta_async_tool(_async_navigate, name="navigate")


def test_member_call_routes_by_family_not_name_sync(
    client: Anthropic, respx_mock: MockRouter, navigate: BetaFunctionTool[Any]
) -> None:
    # Two `navigate` calls in one turn: the member one (toolset_name set) goes
    # to the toolset, the bare one to the same-named custom tool.
    respx_mock.post("/v1/messages").mock(
        side_effect=[
            _response(
                _tool_use("navigate", "toolu_member", {"url": "https://example.com"}, toolset_name="browser"),
                _tool_use("navigate", "toolu_custom", {"url": "https://custom.test"}),
            ),
            _end_turn(),
        ]
    )
    toolset = EchoBrowserToolset()

    results = _run_sync(client, tools=[toolset, navigate], messages=[USER_MESSAGE])

    assert toolset.calls == [("navigate", {"url": "https://example.com"})]
    assert results == [
        {
            "role": "user",
            "content": [
                {
                    "type": "tool_result",
                    "tool_use_id": "toolu_member",
                    "toolset_name": "browser",
                    "content": 'navigate:{"url": "https://example.com"}',
                },
                {"type": "tool_result", "tool_use_id": "toolu_custom", "content": "custom:https://custom.test"},
            ],
        }
    ]

    # Wire golden: the toolset goes out as its nameless entry, nothing SDK-side leaks.
    sent_tools = _sent_tools(respx_mock)
    assert sent_tools[0] == BROWSER_ENTRY
    assert sent_tools[1]["name"] == "navigate"
    assert len(sent_tools) == 2


@pytest.mark.parametrize("flavour", ["sync", "async"])
async def test_a_streamed_member_call_is_routed_to_the_toolset(
    client: Anthropic,
    async_client: AsyncAnthropic,
    respx_mock: MockRouter,
    navigate: BetaFunctionTool[Any],
    async_navigate: BetaAsyncFunctionTool[Any],
    flavour: str,
) -> None:
    # The streaming runner accumulates the tool_use from events; `toolset_name` must survive that and route the
    # block to the toolset, and a same-named plain tool in the same turn still goes to the function tool.
    turn = json.loads(
        _response(
            _tool_use("navigate", "toolu_member", {"url": "u"}, toolset_name="browser"),
            _tool_use("navigate", "toolu_custom", {"url": "v"}),
        ).content
    )

    respx_mock.post("/v1/messages").mock(side_effect=[_sse(turn), _sse(json.loads(_end_turn().content))])

    toolset: Any = EchoBrowserToolset() if flavour == "sync" else AsyncEchoBrowserToolset()
    make: Any = (client if flavour == "sync" else async_client).beta.messages.tool_runner
    runner = make(
        max_tokens=1024,
        model="claude-haiku-4-5",
        tools=[toolset, navigate if flavour == "sync" else async_navigate],
        messages=[USER_MESSAGE],
        stream=True,
    )

    results: list[Any] = []
    if flavour == "sync":
        for stream in runner:
            stream.until_done()
            response = runner.generate_tool_call_response()
            if response is not None:
                results.extend(response["content"])
    else:
        async for astream in runner:
            await astream.until_done()
            aresponse = await runner.generate_tool_call_response()
            if aresponse is not None:
                results.extend(aresponse["content"])

    assert toolset.calls == [("navigate", {"url": "u"})]
    assert [(r["tool_use_id"], r.get("toolset_name"), r["content"]) for r in results] == [
        ("toolu_member", "browser", 'navigate:{"url": "u"}'),
        ("toolu_custom", None, "custom:v"),
    ]


def test_unregistered_family_is_error_result_with_toolset_name_sync(client: Anthropic, respx_mock: MockRouter) -> None:
    # A computer member call with only the browser toolset (and a custom tool
    # that happens to be called `screenshot`) registered: nothing runs, and
    # the error result still carries `toolset_name`, which the API requires on every member result.
    respx_mock.post("/v1/messages").mock(
        side_effect=[_response(_tool_use("screenshot", "toolu_cu", {}, toolset_name="computer")), _end_turn()]
    )
    toolset = EchoBrowserToolset()
    screenshot_called = False

    @beta_tool
    def screenshot() -> str:
        """Custom tool sharing a computer member's name."""
        nonlocal screenshot_called
        screenshot_called = True
        return "custom"

    with pytest.warns(UserWarning, match="Toolset 'computer' \\(member 'screenshot'\\) not found in tool runner"):
        results = _run_sync(client, tools=[toolset, screenshot], messages=[USER_MESSAGE])

    assert toolset.calls == []
    assert screenshot_called is False
    assert results == [
        {
            "role": "user",
            "content": [
                {
                    "type": "tool_result",
                    "tool_use_id": "toolu_cu",
                    "toolset_name": "computer",
                    "content": "Error: Toolset 'computer' member 'screenshot' not found",
                    "is_error": True,
                }
            ],
        }
    ]


@pytest.mark.parametrize("flavour", ["sync", "async"])
async def test_unregistered_family_names_are_folded_before_they_reach_a_log_or_the_result(
    client: Anthropic, async_client: AsyncAnthropic, respx_mock: MockRouter, flavour: str
) -> None:
    # Both names are model output: a line break, escape or bidi override in one must not forge the warning record or
    # the error text, and neither may run to any length.
    weird_family = "comp\nuter\x1b[2J" + "x" * 500

    respx_mock.post("/v1/messages").mock(
        side_effect=[_response(_tool_use("scr\u202eeen", "toolu_cu", {}, toolset_name=weird_family)), _end_turn()]
    )

    with pytest.warns(UserWarning) as caught:
        if flavour == "sync":
            results = _run_sync(client, tools=[EchoBrowserToolset()], messages=[USER_MESSAGE])
        else:
            results = await _run_async(async_client, tools=[AsyncEchoBrowserToolset()], messages=[USER_MESSAGE])

    warned = next(str(w.message) for w in caught if "not found in tool runner" in str(w.message))
    content = str(cast(Any, results[0])["content"][0]["content"])

    for text in (warned.split(". Registered")[0], content):
        assert "\n" not in text and "\x1b" not in text and "\u202e" not in text and len(text) < 500
    assert content.startswith("Error: Toolset 'comp uter [2J" + "x" * 20)


@pytest.mark.parametrize("flavour", ["sync", "async"])
async def test_family_or_type_named_block_without_toolset_name_is_not_a_member_call(
    client: Anthropic, async_client: AsyncAnthropic, respx_mock: MockRouter, flavour: str
) -> None:
    # Only `toolset_name` marks a member call. None of these blocks has one, so none reaches the toolset and no
    # result carries `toolset_name`. The block named after the family gets an error that says what is wrong with it.
    # The block named after the type is an unknown tool, and so is the one named after a toolset not in the run.
    # The sync and async runners each have their own dispatch loop, so both are exercised.
    respx_mock.post("/v1/messages").mock(
        side_effect=[
            _response(
                _tool_use("browser", "toolu_family", {}),
                _tool_use("browser_toolset_20260801", "toolu_type", {}),
                _tool_use("computer", "toolu_other", {}),
            ),
            _end_turn(),
        ]
    )

    toolset: Any = EchoBrowserToolset() if flavour == "sync" else AsyncEchoBrowserToolset()

    with pytest.warns(UserWarning) as warned:
        if flavour == "sync":
            results = _run_sync(client, tools=[toolset], messages=[USER_MESSAGE])
        else:
            results = await _run_async(async_client, tools=[toolset], messages=[USER_MESSAGE])

    assert [str(w.message).split(".")[0] for w in warned] == [
        "Tool 'browser_toolset_20260801' not found in tool runner",
        "Tool 'computer' not found in tool runner",
    ]
    assert toolset.calls == []
    assert results == [
        {
            "role": "user",
            "content": [
                {
                    "type": "tool_result",
                    "tool_use_id": "toolu_family",
                    "content": "Error: the 'browser' toolset could not run this call: the call has no 'actions' list; "
                    "nothing in the batch was executed",
                    "is_error": True,
                },
                {
                    "type": "tool_result",
                    "tool_use_id": "toolu_type",
                    "content": "Error: Tool 'browser_toolset_20260801' not found",
                    "is_error": True,
                },
                {
                    "type": "tool_result",
                    "tool_use_id": "toolu_other",
                    "content": "Error: Tool 'computer' not found",
                    "is_error": True,
                },
            ],
        }
    ]


@pytest.mark.parametrize("flavour", ["sync", "async"])
async def test_member_errors_carry_toolset_name(
    client: Anthropic, async_client: AsyncAnthropic, respx_mock: MockRouter, flavour: str
) -> None:
    respx_mock.post("/v1/messages").mock(
        side_effect=[
            _response(_tool_use("boom", "toolu_boom", {}, toolset_name="browser")),
            _response(_tool_use("crash", "toolu_crash", {}, toolset_name="browser")),
            _end_turn(),
        ]
    )
    if flavour == "sync":
        results = _run_sync(client, tools=[EchoBrowserToolset()], messages=[USER_MESSAGE])
    else:
        results = await _run_async(async_client, tools=[AsyncEchoBrowserToolset()], messages=[USER_MESSAGE])

    assert [message["content"] for message in results] == [
        [
            {
                "type": "tool_result",
                "tool_use_id": "toolu_boom",
                "toolset_name": "browser",
                "content": [{"type": "text", "text": "member refused"}],
                "is_error": True,
            }
        ],
        [
            {
                "type": "tool_result",
                "tool_use_id": "toolu_crash",
                "toolset_name": "browser",
                "content": "RuntimeError('backend exploded')",
                "is_error": True,
            }
        ],
    ]


def test_a_failed_member_stops_the_rest_of_the_turns_members_but_not_function_tools_sync(
    client: Anthropic, respx_mock: MockRouter, navigate: BetaFunctionTool[Any]
) -> None:
    # Three browser actions in one turn, the second fails: the third is not run and says so. A function tool in the
    # same turn runs regardless, before or after the failure, and a failed function tool stops nothing.
    respx_mock.post("/v1/messages").mock(
        side_effect=[
            _response(
                _tool_use("navigate", "toolu_1", {"url": "a"}, toolset_name="browser"),
                _tool_use("navigate", "toolu_fn1", {"url": "f1"}),
                _tool_use("boom", "toolu_2", {}, toolset_name="browser"),
                _tool_use("navigate", "toolu_3", {"url": "c"}, toolset_name="browser"),
                _tool_use("navigate", "toolu_fn2", {"url": "f2"}),
            ),
            _response(
                _tool_use("nope", "toolu_fn3", {}),  # an unknown function tool fails...
                _tool_use("navigate", "toolu_4", {"url": "d"}, toolset_name="browser"),  # ...and stops nothing
            ),
            _end_turn(),
        ]
    )

    toolset = EchoBrowserToolset()

    with pytest.warns(UserWarning, match="not found"):
        results = _run_sync(client, tools=[toolset, navigate], messages=[USER_MESSAGE])

    first = {r["tool_use_id"]: (r.get("is_error", False), r["content"]) for r in cast(Any, results[0]["content"])}
    assert first["toolu_1"] == (False, 'navigate:{"url": "a"}')
    assert first["toolu_2"][0] is True and first["toolu_2"][1] == [{"type": "text", "text": "member refused"}]
    assert first["toolu_3"] == (True, "Not executed: an earlier action in this turn failed.")
    assert first["toolu_fn1"] == (False, "custom:f1") and first["toolu_fn2"] == (False, "custom:f2")
    assert [c[1] for c in toolset.calls] == [{"url": "a"}, {}, {"url": "d"}]  # toolu_3 never reached the toolset

    second = {r["tool_use_id"]: r.get("is_error", False) for r in cast(Any, results[1]["content"])}
    assert second == {"toolu_fn3": True, "toolu_4": False}


@pytest.mark.parametrize("flavour", ["sync", "async"])
async def test_tool_removal_of_member_name_does_not_withdraw_toolset(
    client: Anthropic,
    async_client: AsyncAnthropic,
    respx_mock: MockRouter,
    navigate: BetaFunctionTool[Any],
    async_navigate: BetaAsyncFunctionTool[Any],
    flavour: str,
) -> None:
    # `tool_reference` names plain tools; a member name is not reserved, so
    # removing `navigate` withdraws the custom tool but not the toolset member.
    respx_mock.post("/v1/messages").mock(
        side_effect=[
            _response(
                _tool_use("navigate", "toolu_member", {"url": "u"}, toolset_name="browser"),
                _tool_use("navigate", "toolu_custom", {"url": "u"}),
            ),
            _end_turn(),
        ]
    )

    toolset: Any = EchoBrowserToolset() if flavour == "sync" else AsyncEchoBrowserToolset()
    messages: list[BetaMessageParam] = [USER_MESSAGE, {"role": "system", "content": [_tool_removal("navigate")]}]

    with pytest.warns(UserWarning, match="Tool 'navigate' not found in tool runner"):
        if flavour == "sync":
            results = _run_sync(client, tools=[toolset, navigate], messages=messages)
        else:
            results = await _run_async(async_client, tools=[toolset, async_navigate], messages=messages)

    assert toolset.calls == [("navigate", {"url": "u"})]
    assert results == [
        {
            "role": "user",
            "content": [
                {
                    "type": "tool_result",
                    "tool_use_id": "toolu_member",
                    "toolset_name": "browser",
                    "content": 'navigate:{"url": "u"}',
                },
                {
                    "type": "tool_result",
                    "tool_use_id": "toolu_custom",
                    "content": "Error: Tool 'navigate' not found",
                    "is_error": True,
                },
            ],
        }
    ]


async def test_member_call_roundtrip_async(
    async_client: AsyncAnthropic, respx_mock: MockRouter, async_navigate: BetaAsyncFunctionTool[Any]
) -> None:
    respx_mock.post("/v1/messages").mock(
        side_effect=[
            _response(
                _tool_use("navigate", "toolu_member", {"url": "https://example.com"}, toolset_name="browser"),
                _tool_use("navigate", "toolu_custom", {"url": "https://custom.test"}),
                _tool_use("boom", "toolu_boom", {}, toolset_name="browser"),
            ),
            _end_turn(),
        ]
    )

    toolset = AsyncEchoBrowserToolset()
    results = await _run_async(async_client, tools=[toolset, async_navigate], messages=[USER_MESSAGE])

    assert toolset.calls == [("navigate", {"url": "https://example.com"}), ("boom", {})]
    assert results == [
        {
            "role": "user",
            "content": [
                {
                    "type": "tool_result",
                    "tool_use_id": "toolu_member",
                    "toolset_name": "browser",
                    "content": 'navigate:{"url": "https://example.com"}',
                },
                {"type": "tool_result", "tool_use_id": "toolu_custom", "content": "custom:https://custom.test"},
                {
                    "type": "tool_result",
                    "tool_use_id": "toolu_boom",
                    "toolset_name": "browser",
                    "content": [{"type": "text", "text": "member refused"}],
                    "is_error": True,
                },
            ],
        }
    ]
    assert _sent_tools(respx_mock)[0] == BROWSER_ENTRY


async def test_a_failed_member_stops_the_rest_of_the_turns_members_but_not_function_tools_async(
    async_client: AsyncAnthropic, respx_mock: MockRouter, async_navigate: BetaAsyncFunctionTool[Any]
) -> None:
    # Three browser actions in one turn, the second fails: the third is not run and says so. A function tool in the
    # same turn runs regardless, before or after the failure, and a failed function tool stops nothing.
    respx_mock.post("/v1/messages").mock(
        side_effect=[
            _response(
                _tool_use("navigate", "toolu_1", {"url": "a"}, toolset_name="browser"),
                _tool_use("navigate", "toolu_fn1", {"url": "f1"}),
                _tool_use("boom", "toolu_2", {}, toolset_name="browser"),
                _tool_use("navigate", "toolu_3", {"url": "c"}, toolset_name="browser"),
                _tool_use("navigate", "toolu_fn2", {"url": "f2"}),
            ),
            _response(
                _tool_use("nope", "toolu_fn3", {}),  # an unknown function tool fails...
                _tool_use("navigate", "toolu_4", {"url": "d"}, toolset_name="browser"),  # ...and stops nothing
            ),
            _end_turn(),
        ]
    )

    toolset = AsyncEchoBrowserToolset()
    with pytest.warns(UserWarning, match="not found"):
        results = await _run_async(async_client, tools=[toolset, async_navigate], messages=[USER_MESSAGE])

    first = {r["tool_use_id"]: (r.get("is_error", False), r["content"]) for r in cast(Any, results[0]["content"])}
    assert first["toolu_1"] == (False, 'navigate:{"url": "a"}')
    assert first["toolu_2"][0] is True and first["toolu_2"][1] == [{"type": "text", "text": "member refused"}]
    assert first["toolu_3"] == (True, "Not executed: an earlier action in this turn failed.")
    assert first["toolu_fn1"] == (False, "custom:f1") and first["toolu_fn2"] == (False, "custom:f2")
    assert [c[1] for c in toolset.calls] == [{"url": "a"}, {}, {"url": "d"}]  # toolu_3 never reached the toolset

    second = {r["tool_use_id"]: r.get("is_error", False) for r in cast(Any, results[1]["content"])}
    assert second == {"toolu_fn3": True, "toolu_4": False}


async def test_unregistered_family_is_error_result_with_toolset_name_async(
    async_client: AsyncAnthropic, respx_mock: MockRouter
) -> None:
    respx_mock.post("/v1/messages").mock(
        side_effect=[_response(_tool_use("screenshot", "toolu_cu", {}, toolset_name="computer")), _end_turn()]
    )
    with pytest.warns(UserWarning, match="Toolset 'computer' \\(member 'screenshot'\\) not found"):
        results = await _run_async(async_client, tools=[AsyncEchoBrowserToolset()], messages=[USER_MESSAGE])

    assert results == [
        {
            "role": "user",
            "content": [
                {
                    "type": "tool_result",
                    "tool_use_id": "toolu_cu",
                    "toolset_name": "computer",
                    "content": "Error: Toolset 'computer' member 'screenshot' not found",
                    "is_error": True,
                }
            ],
        }
    ]


@pytest.mark.parametrize("flavour", ["sync", "async"])
async def test_every_call_to_an_unregistered_family_in_a_turn_says_not_found(
    client: Anthropic, async_client: AsyncAnthropic, respx_mock: MockRouter, flavour: str
) -> None:
    # The family is not registered, so no call ran, and each call reports "not found" on its own.
    uses = [_tool_use(name, f"toolu_{name}", {}, toolset_name="computer") for name in ("screenshot", "left_click")]
    respx_mock.post("/v1/messages").mock(side_effect=[_response(*uses), _end_turn()])

    with pytest.warns(UserWarning, match="not found in tool runner"):
        if flavour == "sync":
            results = _run_sync(client, tools=[EchoBrowserToolset()], messages=[USER_MESSAGE])
        else:
            results = await _run_async(async_client, tools=[AsyncEchoBrowserToolset()], messages=[USER_MESSAGE])

    assert [block["content"] for block in cast(Any, results[0])["content"]] == [
        "Error: Toolset 'computer' member 'screenshot' not found",
        "Error: Toolset 'computer' member 'left_click' not found",
    ]


def test_runner_passes_the_tool_use_as_context_and_leaves_the_toolset_open_sync(
    client: Anthropic, respx_mock: MockRouter
) -> None:
    # The runner never closes a toolset: whoever created the browser closes it, and one instance can serve a second
    # run. A usage error stops the run and still leaves the toolset open.
    respx_mock.post("/v1/messages").mock(
        side_effect=[
            _response(_tool_use("navigate", "toolu_member", {"url": "u"}, toolset_name="browser")),
            _end_turn(),
            _response(_tool_use("misuse", "toolu_misuse", {}, toolset_name="browser")),
            _response(_tool_use("navigate", "toolu_again", {"url": "v"}, toolset_name="browser")),
            _end_turn(),
        ]
    )

    toolset = EchoBrowserToolset()
    _run_sync(client, tools=[toolset], messages=[USER_MESSAGE])
    assert toolset.contexts[0].tool_use is not None and toolset.contexts[0].tool_use.id == "toolu_member"
    assert toolset.closed == 0

    runner = client.beta.messages.tool_runner(
        max_tokens=1024, model="claude-haiku-4-5", tools=[toolset], messages=[USER_MESSAGE]
    )
    with pytest.raises(ToolsetContractError):
        runner.until_done()
    assert toolset.closed == 0

    _run_sync(client, tools=[toolset], messages=[USER_MESSAGE])  # the same instance serves another run
    assert [c[1] for c in toolset.calls if c[0] == "navigate"] == [{"url": "u"}, {"url": "v"}] and toolset.closed == 0


async def test_runner_passes_context_and_leaves_the_toolset_open_async(
    async_client: AsyncAnthropic, respx_mock: MockRouter
) -> None:
    # The runner never closes a toolset: whoever created the browser closes it, and one instance can serve a second
    # run. A usage error stops the run and still leaves the toolset open.
    respx_mock.post("/v1/messages").mock(
        side_effect=[
            _response(_tool_use("navigate", "toolu_member", {"url": "u"}, toolset_name="browser")),
            _end_turn(),
            _response(_tool_use("misuse", "toolu_misuse", {}, toolset_name="browser")),
            _response(_tool_use("navigate", "toolu_again", {"url": "v"}, toolset_name="browser")),
            _end_turn(),
        ]
    )

    toolset = AsyncEchoBrowserToolset()
    await _run_async(async_client, tools=[toolset], messages=[USER_MESSAGE])
    assert toolset.contexts[0].tool_use is not None and toolset.contexts[0].tool_use.id == "toolu_member"
    assert toolset.closed == 0

    runner = async_client.beta.messages.tool_runner(
        max_tokens=1024, model="claude-haiku-4-5", tools=[toolset], messages=[USER_MESSAGE]
    )
    with pytest.raises(ToolsetContractError):
        await runner.until_done()
    assert toolset.contexts[1].tool_use is not None and toolset.contexts[1].tool_use.id == "toolu_misuse"
    assert toolset.closed == 0

    await _run_async(async_client, tools=[toolset], messages=[USER_MESSAGE])  # the same instance serves another run
    assert [c[1] for c in toolset.calls if c[0] == "navigate"] == [{"url": "u"}, {"url": "v"}] and toolset.closed == 0


_LATE_USE = BetaToolUseBlock(
    type="tool_use", id="toolu_late", name="navigate", input={"url": "u"}, toolset_name="browser"
)


def test_close_and_with_mark_the_toolset_closed_sync() -> None:
    # close() — directly or through `with` — marks the toolset closed once; a member call afterwards raises at
    # your code instead of answering the model.
    toolset = EchoBrowserToolset()

    with toolset:
        toolset.tool_result(_LATE_USE)
    assert toolset.closed == 1

    with pytest.raises(ToolsetClosedError, match="is closed"):
        toolset.tool_result(_LATE_USE)
    with pytest.raises(ToolsetClosedError):
        with toolset:
            pass

    twice = EchoBrowserToolset()
    with twice:
        twice.close()
    assert twice.closed == 1  # closed inside the block: the block does not close again


async def test_async_close_and_async_with_mark_the_toolset_closed_async() -> None:
    toolset = AsyncEchoBrowserToolset()
    async with toolset:
        await toolset.tool_result(_LATE_USE)
    assert toolset.closed == 1
    with pytest.raises(ToolsetClosedError):
        await toolset.tool_result(_LATE_USE)

    with pytest.raises(ToolsetClosedError):
        async with toolset:
            pass

    twice = AsyncEchoBrowserToolset()
    async with twice:
        await twice.close()
    assert twice.closed == 1  # closed inside the block: the block does not close again


def test_sync_tool_runner_rejects_an_async_toolset(client: Anthropic) -> None:
    # Reported at the tool_runner() call rather than failing deep in JSON encoding.
    with pytest.raises(ToolsetContractError, match="async"):
        client.beta.messages.tool_runner(
            max_tokens=1024,
            model="claude-haiku-4-5",
            messages=[USER_MESSAGE],
            tools=[AsyncEchoBrowserToolset()],  # pyright: ignore[reportArgumentType]
        )


async def test_async_tool_runner_rejects_a_sync_toolset(async_client: AsyncAnthropic) -> None:
    with pytest.raises(ToolsetContractError, match="synchronous"):
        async_client.beta.messages.tool_runner(
            max_tokens=1024,
            model="claude-haiku-4-5",
            messages=[USER_MESSAGE],
            tools=[EchoBrowserToolset()],  # pyright: ignore[reportArgumentType]
        )


async def test_tool_runner_rejects_a_function_tool_of_the_other_flavour(
    client: Anthropic, async_client: AsyncAnthropic
) -> None:
    @beta_tool
    def sync_tool(x: str) -> str:
        """A sync tool."""
        return x

    async def _async_tool(x: str) -> str:
        """An async tool."""
        return x

    async_tool = beta_async_tool(_async_tool)
    with pytest.raises(TypeError, match="async tool"):
        client.beta.messages.tool_runner(
            max_tokens=1024,
            model="claude-haiku-4-5",
            messages=[USER_MESSAGE],
            tools=[async_tool],  # pyright: ignore[reportArgumentType]
        )
    with pytest.raises(TypeError, match="synchronous tool"):
        async_client.beta.messages.tool_runner(
            max_tokens=1024,
            model="claude-haiku-4-5",
            messages=[USER_MESSAGE],
            tools=[sync_tool],  # pyright: ignore[reportArgumentType]
        )


@pytest.mark.parametrize("flavour", ["sync", "async"])
async def test_tool_runner_accepts_a_generator_of_tools(
    respx_mock: MockRouter, client: Anthropic, async_client: AsyncAnthropic, flavour: str
) -> None:
    # A one-shot generator of tools behaves like a list: it is materialized before registration, so the runner sends
    # the toolset's entry (not tools: []) and can still dispatch to it.
    respx_mock.post("/v1/messages").mock(return_value=_end_turn())
    toolset: Any = EchoBrowserToolset() if flavour == "sync" else AsyncEchoBrowserToolset()
    make: Any = (client if flavour == "sync" else async_client).beta.messages.tool_runner
    runner = make(max_tokens=1024, model="claude-haiku-4-5", messages=[USER_MESSAGE], tools=(t for t in [toolset]))

    done = runner.until_done()
    if flavour == "async":
        await done
    assert _sent_tools(respx_mock) == [BROWSER_ENTRY]


# --- helper header --------------------------------------------------------------------------------


def test_the_helper_header_names_the_toolset_the_runner_was_created_with_sync(
    client: Anthropic, respx_mock: MockRouter, navigate: BetaFunctionTool[Any]
) -> None:
    def helper_tags(index: int) -> list[str]:
        header = cast(Any, respx_mock.calls[index]).request.headers.get("x-stainless-helper", "")
        return [tag for tag in header.split(", ") if tag]

    respx_mock.post("/v1/messages").mock(side_effect=[_end_turn(), _end_turn()])
    browser = EchoBrowserToolset()
    tag_helper(browser, cast(Any, "browser-toolset"))  # what the browser base class does for itself

    _run_sync(client, tools=[browser], messages=[USER_MESSAGE])
    _run_sync(client, tools=[navigate], messages=[USER_MESSAGE])

    assert "browser-toolset" in helper_tags(0) and "BetaToolRunner" in helper_tags(0)
    assert "browser-toolset" not in helper_tags(1)


async def test_the_helper_header_names_the_toolset_the_runner_was_created_with_async(
    async_client: AsyncAnthropic, respx_mock: MockRouter, async_navigate: BetaAsyncFunctionTool[Any]
) -> None:
    def helper_tags(index: int) -> list[str]:
        header = cast(Any, respx_mock.calls[index]).request.headers.get("x-stainless-helper", "")
        return [tag for tag in header.split(", ") if tag]

    respx_mock.post("/v1/messages").mock(side_effect=[_end_turn(), _end_turn()])
    browser = AsyncEchoBrowserToolset()
    tag_helper(browser, cast(Any, "browser-toolset"))  # what the browser base class does for itself

    await _run_async(async_client, tools=[browser], messages=[USER_MESSAGE])
    await _run_async(async_client, tools=[async_navigate], messages=[USER_MESSAGE])

    assert "browser-toolset" in helper_tags(0) and "BetaToolRunner" in helper_tags(0)
    assert "browser-toolset" not in helper_tags(1)
