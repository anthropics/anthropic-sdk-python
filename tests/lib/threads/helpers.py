from __future__ import annotations

import os
import json
from typing import Any, Callable, Iterable, Iterator, NamedTuple, cast, overload
from typing_extensions import Literal, Protocol

import httpx2
import pytest
import pydantic
from respx import Route, MockRouter

from anthropic import Anthropic, AsyncAnthropic
from anthropic._compat import PYDANTIC_V1
from anthropic.lib.tools import (
    BetaToolRunner,
    BetaAsyncToolRunner,
    BetaStreamingToolRunner,
    BetaAsyncStreamingToolRunner,
    beta_tool,
    beta_async_tool,
)
from anthropic.types.beta import (
    BetaMessage,
    BetaToolParam,
    BetaMessageParam,
    BetaTextBlockParam,
    BetaToolUnionParam,
)
from anthropic.lib.threads import BetaMessageThread, BetaAsyncMessageThread

from ..streaming.helpers import to_async_iter

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")
api_key = "my-anthropic-api-key"

MODEL = "claude-sonnet-5"
MAX_TOKENS = 1024
THREADS_BETA = "message-threads-2026-08-12"
STRUCTURED_OUTPUTS_BETA = "structured-outputs-2025-12-15"
CONTEXT_MANAGEMENT_BETA = "context-management-2025-06-27"
INLINE_TOOLS_BETA = "inline-tools-2026-09-15"
CREATE = {"type": "create"}
FALLBACK_MODEL = "claude-haiku-4-5"
FALLBACKS: list[Any] = [{"model": FALLBACK_MODEL}]
FALLBACK_BETA = "server-side-fallback-2026-07-01"
THREADS_LOGGER = "anthropic.lib.threads"


class Forecast(pydantic.BaseModel):
    forecast: str


def make_client() -> Anthropic:
    return Anthropic(base_url=base_url, api_key=api_key, _strict_response_validation=True, max_retries=0)


def make_async_client() -> AsyncAnthropic:
    return AsyncAnthropic(base_url=base_url, api_key=api_key, _strict_response_validation=True, max_retries=0)


CLIENT_KINDS = pytest.mark.parametrize("make_client", [make_client, make_async_client], ids=["sync", "async"])

InPlaceEdit = Callable[[list[BetaTextBlockParam], BetaToolParam], object]
_in_place_edits: list[tuple[str, InPlaceEdit]] = [
    ("system", lambda system, _tool: system.append({"type": "text", "text": "Be kind."})),
    ("system", lambda system, _tool: system[0].update({"text": "Be verbose."})),
    ("tools", lambda _system, tool: tool.update({"description": "Does something."})),
]
IN_PLACE_EDITS = pytest.mark.parametrize(
    ("field", "edit"), _in_place_edits, ids=["system_block_added", "system_block_edited", "tool_definition_edited"]
)


def make_thread(**fields: Any) -> BetaMessageThread[Any]:
    """A thread on the sync client; `model` and `max_tokens` default to values no test depends on."""
    return make_client().beta.messages.thread(**_thread_fields(fields))


def make_async_thread(**fields: Any) -> BetaAsyncMessageThread[Any]:
    """A thread on the async client; `model` and `max_tokens` default to values no test depends on."""
    return make_async_client().beta.messages.thread(**_thread_fields(fields))


def _thread_fields(fields: dict[str, Any]) -> dict[str, Any]:
    return {"model": MODEL, "max_tokens": MAX_TOKENS, **fields}


@overload
def make_runner(*, stream: Literal[False] = False, **fields: Any) -> BetaToolRunner[Any]: ...


@overload
def make_runner(*, stream: bool, **fields: Any) -> BetaToolRunner[Any] | BetaStreamingToolRunner[Any]: ...


def make_runner(*, stream: bool = False, **fields: Any) -> BetaToolRunner[Any] | BetaStreamingToolRunner[Any]:
    """`client.beta.messages.tool_runner(...)` on the sync client, with the `get_weather` tool and the weather
    question unless `fields` replaces them."""
    return make_client().beta.messages.tool_runner(**_runner_fields(beta_tool(get_weather), fields), stream=stream)


@overload
def make_async_runner(*, stream: Literal[False] = False, **fields: Any) -> BetaAsyncToolRunner[Any]: ...


@overload
def make_async_runner(
    *, stream: bool, **fields: Any
) -> BetaAsyncToolRunner[Any] | BetaAsyncStreamingToolRunner[Any]: ...


def make_async_runner(
    *, stream: bool = False, **fields: Any
) -> BetaAsyncToolRunner[Any] | BetaAsyncStreamingToolRunner[Any]:
    """`client.beta.messages.tool_runner(...)` on the async client, with the `get_weather` tool and the weather
    question unless `fields` replaces them."""
    tool = beta_async_tool(async_get_weather, name="get_weather")
    return make_async_client().beta.messages.tool_runner(**_runner_fields(tool, fields), stream=stream)


def _runner_fields(tool: object, fields: dict[str, Any]) -> dict[str, Any]:
    return _thread_fields({"tools": [tool], "messages": [WEATHER_QUESTION], **fields})


def get_weather(location: str) -> str:
    """Lookup the weather for a given city.

    Args:
        location: The city, e.g. San Francisco
    """
    return f"Sunny in {location}"


async def async_get_weather(location: str) -> str:
    """Lookup the weather for a given city.

    Args:
        location: The city, e.g. San Francisco
    """
    return get_weather(location)


def lookup(location: str) -> str:
    """Lookup the population of a given city.

    Args:
        location: The city, e.g. San Francisco
    """
    return f"800,000 people live in {location}"


async def async_lookup(location: str) -> str:
    """Lookup the population of a given city.

    Args:
        location: The city, e.g. San Francisco
    """
    return lookup(location)


WEATHER_QUESTION: BetaMessageParam = {"role": "user", "content": "What is the weather in SF?"}


def user(text: str) -> BetaMessageParam:
    return {"role": "user", "content": text}


def marked(text: str) -> BetaMessageParam:
    """A user message whose only block has a `cache_control` marker."""
    return {"role": "user", "content": [{"type": "text", "text": text, "cache_control": {"type": "ephemeral"}}]}


def marked_twice(text: str) -> BetaMessageParam:
    """A user message with two blocks, each with a `cache_control` marker."""
    block: BetaTextBlockParam = {"type": "text", "text": text, "cache_control": {"type": "ephemeral"}}
    return {"role": "user", "content": [block, block]}


def unmarked(text: str) -> BetaMessageParam:
    """`marked(text)` without the marker."""
    return {"role": "user", "content": [{"type": "text", "text": text}]}


def assistant(text: str = "Hi!") -> BetaMessageParam:
    return {"role": "assistant", "content": [{"type": "text", "text": text}]}


def tool_use(tool_use_id: str, name: str = "get_weather") -> BetaMessageParam:
    return {
        "role": "assistant",
        "content": [{"type": "tool_use", "id": tool_use_id, "name": name, "input": {"location": "San Francisco"}}],
    }


def tool_result(tool_use_id: str, content: str = "Sunny in San Francisco") -> BetaMessageParam:
    return {"role": "user", "content": [{"type": "tool_result", "tool_use_id": tool_use_id, "content": content}]}


def tool_addition(definition: BetaToolUnionParam) -> BetaMessageParam:
    return {
        "role": "system",
        "content": [{"type": "tool_addition", "tool": {"type": "tool_definition", "definition": definition}}],
    }


def tool_removal(name: str) -> BetaMessageParam:
    return {"role": "system", "content": [{"type": "tool_removal", "tool": {"type": "tool_reference", "name": name}}]}


def history_with_nested_blocks(marker: dict[str, Any]) -> list[Any]:
    """A history with `marker` in every block, nested ones included. Its free-form data has `cache_control` keys of its
    own, and so do the `tool_changes` of its compaction block, whatever `marker` is."""

    def added_tool(marker: dict[str, Any]) -> dict[str, Any]:
        definition: dict[str, Any] = {
            "name": "fetch",
            "input_schema": {"type": "object", "properties": {"cache_control": {}}},
            "input_examples": [{"cache_control": "no-store"}],
            **marker,
        }
        return {"type": "tool_addition", "tool": {"type": "tool_definition", "definition": definition}, **marker}

    return [
        {"role": "user", "content": "Hello"},
        {
            "role": "assistant",
            "content": [
                {
                    "type": "compaction",
                    "content": "Said hello.",
                    "tool_changes": [added_tool({"cache_control": {"type": "ephemeral"}})],
                    **marker,
                }
            ],
        },
        {"role": "system", "content": [added_tool(marker)]},
        {"role": "user", "content": "Fetch it."},
        {
            "role": "assistant",
            "content": [
                {
                    "type": "tool_search_tool_result",
                    "tool_use_id": "srvtoolu_a",
                    "content": {
                        "type": "tool_search_tool_search_result",
                        "tool_references": [{"type": "tool_reference", "tool_name": "fetch", **marker}],
                    },
                    **marker,
                },
                {
                    "type": "tool_use",
                    "id": "toolu_a",
                    "name": "fetch",
                    "input": {"cache_control": "no-store", "headers": [{"cache_control": "no-store"}]},
                    **marker,
                },
            ],
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "tool_result",
                    "tool_use_id": "toolu_a",
                    "content": [{"type": "text", "text": "Fetched.", **marker}],
                    **marker,
                },
                {
                    "type": "document",
                    "source": {"type": "content", "content": [{"type": "text", "text": "Notes.", **marker}]},
                    **marker,
                },
            ],
        },
    ]


def continue_from(previous_message_id: str) -> dict[str, Any]:
    return {"type": "continue", "previous_message_id": previous_message_id}


def roles(messages: Iterable[BetaMessageParam | dict[str, Any]]) -> list[str]:
    return [message["role"] for message in messages]


def queue_responses(respx_mock: MockRouter, *responses: httpx2.Response | Exception) -> Route:
    """Answer the next `len(responses)` Messages API requests with `responses`, in order. An exception is raised in
    place of a response."""
    return respx_mock.post("/v1/messages").mock(side_effect=list(responses))


def message_response(
    id: str,
    text: str = "Hi!",
    *,
    tool_use_id: str | None = None,
    tool_name: str = "get_weather",
    container: str | None = None,
    stop_reason: str | None = None,
    iterations: list[Any] | None = None,
    headers: dict[str, str] | None = None,
) -> httpx2.Response:
    content = (assistant(text) if tool_use_id is None else tool_use(tool_use_id, tool_name)).get("content")
    return httpx2.Response(
        200,
        headers=headers,
        json={
            "id": id,
            "type": "message",
            "role": "assistant",
            "model": MODEL,
            "content": content,
            "container": {"id": container, "expires_at": "2026-08-19T00:00:00Z"} if container is not None else None,
            "stop_reason": stop_reason or ("tool_use" if tool_use_id is not None else "end_turn"),
            "stop_sequence": None,
            "usage": {"input_tokens": 10, "output_tokens": 5, **({"iterations": iterations} if iterations else {})},
        },
    )


def id_headers(request_id: str, workspace_id: str) -> dict[str, str]:
    """The response headers that a reply's `_request_id` and `_workspace_id` come from."""
    return {"request-id": request_id, "anthropic-workspace-id": workspace_id}


def response_ids(*replies: BetaMessage) -> list[tuple[str | None, str | None]]:
    return [(reply._request_id, reply._workspace_id) for reply in replies]


def _iteration(type: str, model: str) -> dict[str, Any]:
    return {
        "type": type,
        "model": model,
        "input_tokens": 10,
        "output_tokens": 5,
        "cache_creation_input_tokens": 0,
        "cache_read_input_tokens": 0,
    }


FALLBACK_ITERATIONS = [
    _iteration("message", MODEL),
    _iteration("fallback_message", FALLBACK_MODEL),
    _iteration("advisor_message", "claude-opus-4-8"),
]
"""The `usage.iterations` of a reply that `FALLBACK_MODEL` wrote after `MODEL` declined."""


def fallback_reply(text: str = "Hi!") -> BetaMessageParam:
    """The reply of `fallback_response()`."""
    return {
        "role": "assistant",
        "content": [
            {
                "type": "fallback",
                "from": {"model": MODEL},
                "to": {"model": FALLBACK_MODEL},
                "trigger": {"type": "refusal", "category": "cyber"},
            },
            {"type": "text", "text": text},
        ],
    }


def fallback_response(id: str) -> httpx2.Response:
    """A reply that `FALLBACK_MODEL` wrote after `MODEL` declined, with the block that marks the hand-over."""
    body = message_response(id, iterations=FALLBACK_ITERATIONS).json()
    return httpx2.Response(200, json={**body, "model": FALLBACK_MODEL, "content": fallback_reply().get("content")})


def tool_change_replies() -> list[httpx2.Response]:
    """The replies of a run that calls `get_weather`, then `lookup`, then `get_weather` again, and then ends."""
    return [
        message_response("msg_a", tool_use_id="toolu_a"),
        message_response("msg_b", tool_use_id="toolu_b", tool_name="lookup"),
        message_response("msg_c", tool_use_id="toolu_c"),
        message_response("msg_d", "Sunny."),
    ]


def tool_change_turns(lookup_definition: BetaToolUnionParam) -> list[list[BetaMessageParam]]:
    """What answers each of the first three `tool_change_replies()` when `lookup` is added while the first one is
    handled and `get_weather` is removed while the second one is."""
    return [
        [tool_result("toolu_a"), tool_addition(lookup_definition)],
        [tool_result("toolu_b", "800,000 people live in San Francisco"), tool_removal("get_weather")],
        [
            {
                "role": "user",
                "content": [
                    {
                        "type": "tool_result",
                        "tool_use_id": "toolu_c",
                        "content": "Error: Tool 'get_weather' not found",
                        "is_error": True,
                    }
                ],
            }
        ],
    ]


COMPACTED: BetaMessageParam = {
    "role": "assistant",
    "content": [{"type": "compaction", "content": "Asked about SF; it is sunny."}],
}


def compaction_response(id: str) -> httpx2.Response:
    body = message_response(id, stop_reason="compaction").json()
    return httpx2.Response(200, json={**body, "content": COMPACTED.get("content")})


def stream_response(
    id: str,
    text: str = "Hello there!",
    *,
    tool_use_id: str | None = None,
    container: str | None = None,
    stop_reason: str | None = None,
    iterations: list[Any] | None = None,
    message_stop: bool = True,
) -> httpx2.Response:
    """A streamed reply. With `message_stop=False` the body ends after `message_delta`, as when the connection drops
    just before the last event."""
    body = list(
        _sse_body(
            id, text, tool_use_id=tool_use_id, container=container, stop_reason=stop_reason, iterations=iterations
        )
    )
    if not message_stop:
        del body[-3:]  # the `message_stop` event's three lines
    return httpx2.Response(200, headers={"content-type": "text/event-stream"}, content=iter(body))


def async_stream_response(
    id: str,
    text: str = "Hello there!",
    *,
    tool_use_id: str | None = None,
    container: str | None = None,
    stop_reason: str | None = None,
    iterations: list[Any] | None = None,
) -> httpx2.Response:
    return httpx2.Response(
        200,
        headers={"content-type": "text/event-stream"},
        content=to_async_iter(
            _sse_body(
                id, text, tool_use_id=tool_use_id, container=container, stop_reason=stop_reason, iterations=iterations
            )
        ),
    )


def partial_tool_use_stream_response(id: str, text: str, *, tool_use_id: str) -> httpx2.Response:
    """A streamed reply with a finished text block followed by a `tool_use` block whose input is cut off before
    `content_block_stop`, as a client that stops reading mid-call sees it."""
    content_events: list[Any] = [
        (
            "content_block_start",
            {"type": "content_block_start", "index": 0, "content_block": {"type": "text", "text": ""}},
        ),
        (
            "content_block_delta",
            {"type": "content_block_delta", "index": 0, "delta": {"type": "text_delta", "text": text}},
        ),
        ("content_block_stop", {"type": "content_block_stop", "index": 0}),
        (
            "content_block_start",
            {
                "type": "content_block_start",
                "index": 1,
                "content_block": {"type": "tool_use", "id": tool_use_id, "name": "get_weather", "input": {}},
            },
        ),
        (
            "content_block_delta",
            {
                "type": "content_block_delta",
                "index": 1,
                "delta": {"type": "input_json_delta", "partial_json": '{"location": "San'},
            },
        ),
    ]
    return httpx2.Response(
        200, headers={"content-type": "text/event-stream"}, content=_sse_body(id, content_events=content_events)
    )


def interrupted_stream_response(
    id: str, text: str, *, error: type[httpx2.TransportError] | None = None
) -> httpx2.Response:
    """A streamed reply cut off in its text block, once `text` has arrived: the body ends there, or reading on raises
    `error`."""
    return httpx2.Response(
        200, headers={"content-type": "text/event-stream"}, content=_interrupted_sse_body(id, text, error)
    )


def async_interrupted_stream_response(
    id: str, text: str, *, error: type[httpx2.TransportError] | None = None
) -> httpx2.Response:
    return httpx2.Response(
        200,
        headers={"content-type": "text/event-stream"},
        content=to_async_iter(_interrupted_sse_body(id, text, error)),
    )


def _interrupted_sse_body(id: str, text: str, error: type[httpx2.TransportError] | None) -> Iterator[bytes]:
    # All but `content_block_stop`, `message_delta` and `message_stop`, at three lines an event.
    yield from list(_sse_body(id, text))[:-9]
    if error is not None:
        raise error("The connection dropped")


RESPONSE_KINDS = pytest.mark.parametrize(
    ("respond", "stream"),
    [(message_response, False), (stream_response, True)],
    ids=["non_streaming", "streaming"],
)
ASYNC_RESPONSE_KINDS = pytest.mark.parametrize(
    ("respond", "stream"),
    [(message_response, False), (async_stream_response, True)],
    ids=["non_streaming", "streaming"],
)

RUNNER_MODES = pytest.mark.parametrize("mode", [{}, {"thread": False}], ids=["default", "opt_out"])

FOGGY = tool_result("toolu_a", "Foggy")
CACHED_RESULT: BetaMessageParam = {
    "role": "user",
    "content": [
        {
            "type": "tool_result",
            "tool_use_id": "toolu_a",
            "content": "Sunny in San Francisco",
            "cache_control": {"type": "ephemeral"},
        }
    ],
}
EDITED_TOOL_USE: BetaMessageParam = {
    "role": "assistant",
    "content": [{"type": "tool_use", "id": "toolu_a", "name": "get_weather", "input": {"location": "Oakland"}}],
}


Change = Callable[[Any, Any, Any], None]
"""Called with the runner, the reply and the tool response."""


class LoopBody(NamedTuple):
    """What a loop body does with the `toolu_a` reply to the weather question, and what the runner does next."""

    reads: Literal["nothing", "reply", "tool_response"]
    """What the body reads first. A streamed reply is still unread when the body reads nothing."""

    change: Change

    conversation: list[BetaMessageParam]
    """The conversation the model sees with the next request."""

    tool_runs: int


def _append(*messages: BetaMessageParam) -> Change:
    def change(runner: Any, _reply: Any, _tool_response: Any) -> None:
        runner.append_messages(*messages)

    return change


def _append_reply_and_own_result(runner: Any, reply: Any, _tool_response: Any) -> None:
    runner.append_messages(reply, FOGGY)


def _append_reply_tool_response_and_text(runner: Any, reply: Any, tool_response: Any) -> None:
    runner.append_messages(reply, tool_response, user("Be concise."))


def _append_reply_and_changed_tool_response(runner: Any, reply: Any, tool_response: Any) -> None:
    for block in tool_response["content"]:
        block["cache_control"] = {"type": "ephemeral"}
    runner.append_messages(reply, tool_response)


def _set_messages(*added: BetaMessageParam) -> Change:
    def add(params: dict[str, Any]) -> dict[str, Any]:
        return {**params, "messages": [*params["messages"], *added]}

    def change(runner: Any, _reply: Any, _tool_response: Any) -> None:
        runner.set_messages_params(add)

    return change


def _rewrite_then_append(runner: Any, _reply: Any, _tool_response: Any) -> None:
    def rewrite(params: dict[str, Any]) -> dict[str, Any]:
        return {**params, "messages": [user("Start over: Oakland?")]}

    runner.set_messages_params(rewrite)
    runner.append_messages(user("Also Berkeley."))


_loop_bodies = {
    "reply_tool_response_and_text_appended": LoopBody(
        "tool_response",
        _append_reply_tool_response_and_text,
        [WEATHER_QUESTION, tool_use("toolu_a"), tool_result("toolu_a"), user("Be concise.")],
        tool_runs=2,
    ),
    "reply_and_changed_tool_response_appended": LoopBody(
        "tool_response",
        _append_reply_and_changed_tool_response,
        [WEATHER_QUESTION, tool_use("toolu_a"), CACHED_RESULT],
        tool_runs=2,
    ),
    "reply_and_own_result_appended": LoopBody(
        "reply", _append_reply_and_own_result, [WEATHER_QUESTION, tool_use("toolu_a"), FOGGY], tool_runs=1
    ),
    "own_result_appended": LoopBody("nothing", _append(FOGGY), [WEATHER_QUESTION, FOGGY], tool_runs=1),
    "text_appended": LoopBody(
        "nothing", _append(user("In one word.")), [WEATHER_QUESTION, user("In one word.")], tool_runs=1
    ),
    "edited_reply_and_own_result_appended": LoopBody(
        "nothing", _append(EDITED_TOOL_USE, FOGGY), [WEATHER_QUESTION, EDITED_TOOL_USE, FOGGY], tool_runs=1
    ),
    "history_rewritten_then_text_appended": LoopBody(
        "nothing", _rewrite_then_append, [user("Start over: Oakland?"), user("Also Berkeley.")], tool_runs=1
    ),
    "text_set": LoopBody(
        "nothing",
        _set_messages(user("In one word.")),
        [WEATHER_QUESTION, user("In one word."), tool_use("toolu_a"), tool_result("toolu_a")],
        tool_runs=1,
    ),
    "reply_and_text_set": LoopBody(
        "nothing",
        _set_messages(tool_use("toolu_a"), user("In one word.")),
        [WEATHER_QUESTION, tool_use("toolu_a"), user("In one word."), tool_use("toolu_a"), tool_result("toolu_a")],
        tool_runs=1,
    ),
    "same_history_set": LoopBody(
        "nothing", _set_messages(), [WEATHER_QUESTION, tool_use("toolu_a"), tool_result("toolu_a")], tool_runs=1
    ),
}
LOOP_BODIES = pytest.mark.parametrize("body", list(_loop_bodies.values()), ids=list(_loop_bodies))


def assert_sends_conversation(
    request: dict[str, Any], mode: dict[str, Any], conversation: list[BetaMessageParam]
) -> None:
    """Assert that `request`, which follows the `toolu_a` reply `msg_a` to the weather question, shows the model
    `conversation`. With default settings it leaves out the question and the reply when `conversation` starts with
    them, and sends all of any other."""
    if mode:
        assert "thread" not in request
        assert request["messages"] == conversation
    elif conversation[:2] == [WEATHER_QUESTION, tool_use("toolu_a")]:
        assert request["thread"] == continue_from("msg_a")
        assert request["messages"] == conversation[2:]
    else:
        assert request["thread"] == CREATE
        assert request["messages"] == conversation


def two_tool_uses_response(id: str) -> httpx2.Response:
    reply = message_response(id, tool_use_id="toolu_a").json()
    reply["content"] += message_response(id, tool_use_id="toolu_b").json()["content"]
    return httpx2.Response(200, json=reply)


def _sse_body(
    id: str,
    text: str = "Hello there!",
    *,
    tool_use_id: str | None = None,
    container: str | None = None,
    stop_reason: str | None = None,
    iterations: list[Any] | None = None,
    content_events: list[Any] | None = None,
) -> Iterator[bytes]:
    content_events = content_events or (
        [
            (
                "content_block_start",
                {"type": "content_block_start", "index": 0, "content_block": {"type": "text", "text": ""}},
            ),
            *[
                (
                    "content_block_delta",
                    {"type": "content_block_delta", "index": 0, "delta": {"type": "text_delta", "text": chunk}},
                )
                for chunk in _text_deltas(text)
            ],
            ("content_block_stop", {"type": "content_block_stop", "index": 0}),
        ]
        if tool_use_id is None
        else [
            (
                "content_block_start",
                {
                    "type": "content_block_start",
                    "index": 0,
                    "content_block": {"type": "tool_use", "id": tool_use_id, "name": "get_weather", "input": {}},
                },
            ),
            (
                "content_block_delta",
                {
                    "type": "content_block_delta",
                    "index": 0,
                    "delta": {"type": "input_json_delta", "partial_json": json.dumps({"location": "San Francisco"})},
                },
            ),
            ("content_block_stop", {"type": "content_block_stop", "index": 0}),
        ]
    )
    events: list[Any] = [
        (
            "message_start",
            {
                "type": "message_start",
                "message": {
                    "id": id,
                    "type": "message",
                    "role": "assistant",
                    "model": MODEL,
                    "content": [],
                    "container": None,
                    "stop_reason": None,
                    "stop_sequence": None,
                    "usage": {"input_tokens": 10, "output_tokens": 5},
                },
            },
        ),
        *content_events,
        (
            "message_delta",
            {
                "type": "message_delta",
                "delta": {
                    "stop_reason": stop_reason or ("tool_use" if tool_use_id is not None else "end_turn"),
                    "stop_sequence": None,
                    "container": {"id": container, "expires_at": "2026-08-19T00:00:00Z"} if container else None,
                },
                "usage": {"output_tokens": 5, **({"iterations": iterations} if iterations else {})},
            },
        ),
        ("message_stop", {"type": "message_stop"}),
    ]
    for name, data in events:
        yield f"event: {name}\n".encode()
        yield f"data: {json.dumps(data)}\n".encode()
        yield b"\n"


def _text_deltas(text: str) -> list[str]:
    """`text` split into one delta per word, which concatenate back to `text`."""
    words = text.split(" ")
    return [words[0], *(f" {word}" for word in words[1:])]


def api_error_response(
    status: int, error_type: str, message: str, *, error_code: str | None = None, **details: Any
) -> httpx2.Response:
    error: dict[str, Any] = {"type": error_type, "message": message}
    if error_code is not None:
        error["details"] = {"error_code": error_code, **details}
    return httpx2.Response(status, json={"type": "error", "error": error}, headers={"x-should-retry": "false"})


def server_error() -> httpx2.Response:
    return api_error_response(500, "api_error", "Internal server error")


def stream_error_response() -> httpx2.Response:
    """A stream whose first event is an error."""
    error = {"type": "error", "error": {"type": "overloaded_error", "message": "Overloaded"}}
    return httpx2.Response(
        200, headers={"content-type": "text/event-stream"}, content=f"event: error\ndata: {json.dumps(error)}\n\n"
    )


TURN_METHODS = pytest.mark.parametrize("method", ["send", "parse", "stream"])
ANSWERED_TURN_METHODS = pytest.mark.parametrize(
    "method",
    [
        "send",
        pytest.param(
            "parse", marks=pytest.mark.skipif(PYDANTIC_V1, reason="structured outputs not supported with pydantic v1")
        ),
        "stream",
    ],
)
FAILURES_BEFORE_A_REPLY = pytest.mark.parametrize(
    "failure",
    [
        api_error_response(400, "invalid_request_error", "messages.0.content: too long"),
        api_error_response(529, "overloaded_error", "Overloaded"),
        httpx2.ConnectError("Connection refused"),
        httpx2.ReadTimeout("Timed out"),
    ],
    ids=["bad_request", "overloaded", "connection_error", "timeout"],
)
_one_turn_create_only_fields: list[dict[str, Any]] = [
    {"system": "Be brief."},
    {"tools": [{"name": "noop", "input_schema": {"type": "object", "properties": {}}}]},
]
ONE_TURN_CREATE_ONLY_FIELDS = pytest.mark.parametrize("override", _one_turn_create_only_fields, ids=["system", "tools"])


def _update_system(thread: BetaMessageThread[Any] | BetaAsyncMessageThread[Any]) -> None:
    thread.update(system="Be verbose.")


def _update_tools(thread: BetaMessageThread[Any] | BetaAsyncMessageThread[Any]) -> None:
    thread.update(tools=[])


def _set_messages_params(thread: BetaMessageThread[Any] | BetaAsyncMessageThread[Any]) -> None:
    thread.tool_runner().set_messages_params(lambda params: {**params, "system": "Be verbose."})


def _update_max_tokens(thread: BetaMessageThread[Any] | BetaAsyncMessageThread[Any]) -> None:
    thread.update(max_tokens=12)


def _set_messages_params_max_tokens(thread: BetaMessageThread[Any] | BetaAsyncMessageThread[Any]) -> None:
    thread.tool_runner().set_messages_params(lambda params: {**params, "max_tokens": 12})


_changes_during_the_turn: list[Any] = [
    ({"system": "Be brief."}, _update_system),
    ({"tools": [{"name": "noop", "input_schema": {"type": "object"}}]}, _update_tools),
    pytest.param(
        {"system": "Be brief."},
        _set_messages_params,
        marks=pytest.mark.skipif(PYDANTIC_V1, reason="tool runner not supported with pydantic v1"),
    ),
]
CHANGES_DURING_THE_TURN = pytest.mark.parametrize(
    ("override", "change"), _changes_during_the_turn, ids=["update_system", "update_tools", "set_messages_params"]
)
_own_create_only_fields: list[dict[str, Any]] = [
    {},
    {"system": "Be kind.", "tools": [{"name": "other", "input_schema": {"type": "object", "properties": {}}}]},
]
OWN_CREATE_ONLY_FIELDS = pytest.mark.parametrize(
    "own", _own_create_only_fields, ids=["no_system_or_tools_of_its_own", "system_and_tools_of_its_own"]
)
CHANGES_OF_ANOTHER_FIELD_DURING_THE_TURN = pytest.mark.parametrize(
    "change",
    [
        _update_max_tokens,
        pytest.param(
            _set_messages_params_max_tokens,
            marks=pytest.mark.skipif(PYDANTIC_V1, reason="tool runner not supported with pydantic v1"),
        ),
    ],
    ids=["update", "set_messages_params"],
)


def _new_system(params: dict[str, Any]) -> dict[str, Any]:
    return {**params, "system": "Be very brief."}


def _new_system_without_the_reply(runner: Any) -> None:
    runner.append_messages(user("Never mind."))
    runner.set_messages_params(_new_system)


def _new_system_with_a_rewritten_history(runner: Any) -> None:
    def rewrite(params: dict[str, Any]) -> dict[str, Any]:
        return {**_new_system(params), "messages": [user("Start over.")]}

    runner.set_messages_params(rewrite)


NEW_SYSTEM_WITH_ANOTHER_HISTORY = pytest.mark.parametrize(
    "change",
    [_new_system_without_the_reply, _new_system_with_a_rewritten_history],
    ids=["without_the_reply", "rewritten_history"],
)


THREAD_NOT_FOUND = api_error_response(
    404,
    "not_found_error",
    "No thread state was found for the requested `previous_message_id`.",
    error_code="thread_not_found",
)
FINGERPRINT_MISMATCH = api_error_response(
    400,
    "invalid_request_error",
    "`tools` differs from the request that created this Thread.",
    error_code="thread_fingerprint_mismatch",
)
ALREADY_CONTINUED_MESSAGE = (
    "The requested `previous_message_id` has already been continued. Each response `id` may be continued at most "
    "once; continue from the Thread's most recent response `id`."
)
ALREADY_CONTINUED = api_error_response(
    400, "invalid_request_error", ALREADY_CONTINUED_MESSAGE, error_code="thread_already_continued"
)
CONTINUE_IN_FLIGHT = api_error_response(
    400,
    "invalid_request_error",
    "Another request is already continuing the requested `previous_message_id`.",
    error_code="thread_continue_in_flight",
)


def unsupported_response(*unsupported: str) -> httpx2.Response:
    return api_error_response(
        400,
        "invalid_request_error",
        "This request cannot be used with `thread`.",
        error_code="thread_unsupported_request",
        unsupported=list(unsupported),
    )


class MockRequestCall(Protocol):
    request: httpx2.Request


def sent_requests(respx_mock: MockRouter) -> list[httpx2.Request]:
    return [call.request for call in cast("list[MockRequestCall]", respx_mock.calls)]


def request_bodies(respx_mock: MockRouter) -> list[dict[str, Any]]:
    return [json.loads(request.content) for request in sent_requests(respx_mock)]


def request_threads(respx_mock: MockRouter) -> list[dict[str, Any] | None]:
    """The `thread` param of each request, or `None` for a request sent without one."""
    return [body.get("thread") for body in request_bodies(respx_mock)]


def request_betas(respx_mock: MockRouter) -> list[list[str]]:
    headers = [cast(str, request.headers.get("anthropic-beta", "")) for request in sent_requests(respx_mock)]
    return [[beta.strip() for beta in header.split(",") if beta.strip()] for header in headers]


def request_helper_tags(respx_mock: MockRouter) -> list[list[str]]:
    """The lines of the helper telemetry header on each request."""
    return [request.headers.get_list("x-stainless-helper") for request in sent_requests(respx_mock)]


def thread_logs(caplog: pytest.LogCaptureFixture) -> list[tuple[int, str]]:
    """The (level, message) pairs logged under the `anthropic.lib.threads` logger or its children."""
    return [(level, message) for name, level, message in caplog.record_tuples if name.startswith(THREADS_LOGGER)]
