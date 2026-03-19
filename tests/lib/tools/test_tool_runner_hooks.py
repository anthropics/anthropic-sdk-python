from __future__ import annotations

import json
from typing import Any, List
from unittest.mock import MagicMock, NonCallableMagicMock

import pytest

from anthropic import Anthropic, beta_tool
from anthropic._compat import PYDANTIC_V1
from anthropic.lib.tools._beta_runner import BetaToolRunner
from anthropic.lib.tools._beta_functions import ToolError


def _make_tool_call_msg(tool_name: str, tool_input: dict[str, Any], tool_id: str = "toolu_01") -> Any:
    msg = NonCallableMagicMock()
    msg.role = "assistant"
    msg.stop_reason = "tool_use"
    msg.id = "msg_01"
    msg.model = "claude-haiku-4-5"
    msg.container = None
    msg.context_management = None
    block = NonCallableMagicMock()
    block.type = "tool_use"
    block.name = tool_name
    block.input = tool_input
    block.id = tool_id
    msg.content = [block]
    usage = NonCallableMagicMock()
    usage.input_tokens = 100
    usage.output_tokens = 20
    usage.cache_creation_input_tokens = 0
    usage.cache_read_input_tokens = 0
    msg.usage = usage
    return msg


def _make_text_msg(text: str) -> Any:
    msg = NonCallableMagicMock()
    msg.role = "assistant"
    msg.stop_reason = "end_turn"
    msg.id = "msg_02"
    msg.model = "claude-haiku-4-5"
    msg.container = None
    msg.context_management = None
    block = NonCallableMagicMock()
    block.type = "text"
    block.text = text
    msg.content = [block]
    usage = NonCallableMagicMock()
    usage.input_tokens = 150
    usage.output_tokens = 30
    usage.cache_creation_input_tokens = 0
    usage.cache_read_input_tokens = 0
    msg.usage = usage
    return msg


def _make_runner(tool_fn: Any, responses: list[Any]) -> BetaToolRunner[Any]:
    client = Anthropic.__new__(Anthropic)
    idx: dict[str, int] = {"n": 0}

    def fake_parse(**_kwargs: Any) -> Any:
        r = responses[idx["n"]]
        idx["n"] += 1
        return r

    bm = MagicMock()
    bm.parse.side_effect = fake_parse
    b = MagicMock()
    b.messages = bm
    object.__setattr__(client, "beta", b)

    return BetaToolRunner(
        params={  # type: ignore[arg-type]
            "model": "claude-haiku-4-5",
            "max_tokens": 512,
            "messages": [{"role": "user", "content": "test"}],
            "tools": [tool_fn.to_dict()],
        },
        options={},
        tools=[tool_fn],
        client=client,
    )


@pytest.mark.skipif(PYDANTIC_V1, reason="tool runner not supported with pydantic v1")
class TestObservabilityHooks:
    def test_hooks_default_to_none(self) -> None:
        @beta_tool
        def get_weather(location: str) -> str:  # noqa: ARG001
            """Get weather. Args: location: City name."""
            return json.dumps({"temp": "22C"})

        runner = _make_runner(
            get_weather,
            [_make_tool_call_msg("get_weather", {"location": "Paris"}), _make_text_msg("done")],
        )

        assert runner.on_tool_call is None
        assert runner.on_tool_result is None
        assert runner.on_tool_error is None

    def test_on_tool_call_fires_with_correct_args(self) -> None:
        calls: List[tuple[str, Any]] = []

        @beta_tool
        def get_weather(location: str) -> str:  # noqa: ARG001
            """Get weather. Args: location: City name."""
            return json.dumps({"temp": "22C"})

        runner = _make_runner(
            get_weather,
            [_make_tool_call_msg("get_weather", {"location": "Tokyo"}), _make_text_msg("done")],
        )
        runner.on_tool_call = lambda name, inp: calls.append((name, inp))
        runner.until_done()

        assert len(calls) == 1
        assert calls[0][0] == "get_weather"
        assert calls[0][1] == {"location": "Tokyo"}

    def test_on_tool_result_fires_with_correct_args(self) -> None:
        results: List[tuple[str, Any]] = []

        @beta_tool
        def get_weather(location: str) -> str:  # noqa: ARG001
            """Get weather. Args: location: City name."""
            return json.dumps({"temp": "22C"})

        runner = _make_runner(
            get_weather,
            [_make_tool_call_msg("get_weather", {"location": "London"}), _make_text_msg("done")],
        )
        runner.on_tool_result = lambda _name, _result: results.append((_name, _result))
        runner.until_done()

        assert len(results) == 1
        assert results[0][0] == "get_weather"

    def test_on_tool_call_fires_before_on_tool_result(self) -> None:
        events: List[str] = []

        @beta_tool
        def get_weather(location: str) -> str:  # noqa: ARG001
            """Get weather. Args: location: City name."""
            return json.dumps({"temp": "22C"})

        runner = _make_runner(
            get_weather,
            [_make_tool_call_msg("get_weather", {"location": "Paris"}), _make_text_msg("done")],
        )
        runner.on_tool_call = lambda _name, _inp: events.append("call")
        runner.on_tool_result = lambda _name, _result: events.append("result")
        runner.until_done()

        assert events == ["call", "result"]

    def test_on_tool_error_fires_on_tool_error(self) -> None:
        errors: List[tuple[str, BaseException]] = []

        @beta_tool
        def divide(a: float, b: float) -> str:
            """Divide. Args: a: numerator. b: denominator."""
            if b == 0:
                raise ToolError("Cannot divide by zero")
            return str(a / b)

        runner = _make_runner(
            divide,
            [_make_tool_call_msg("divide", {"a": 10.0, "b": 0.0}), _make_text_msg("done")],
        )
        runner.on_tool_error = lambda name, exc: errors.append((name, exc))
        runner.until_done()

        assert len(errors) == 1
        assert errors[0][0] == "divide"
        assert "zero" in str(errors[0][1]).lower()

    def test_on_tool_error_fires_on_unexpected_exception(self) -> None:
        errors: List[tuple[str, BaseException]] = []

        @beta_tool
        def crash(msg: str) -> str:  # noqa: ARG001
            """Crash. Args: msg: ignored."""
            raise RuntimeError("unexpected crash")

        runner = _make_runner(
            crash,
            [_make_tool_call_msg("crash", {"msg": "hi"}), _make_text_msg("done")],
        )
        runner.on_tool_error = lambda name, exc: errors.append((name, exc))
        runner.until_done()

        assert len(errors) == 1
        assert errors[0][0] == "crash"
        assert isinstance(errors[0][1], RuntimeError)

    def test_on_tool_result_does_not_fire_when_tool_errors(self) -> None:
        results: List[Any] = []
        errors: List[Any] = []

        @beta_tool
        def divide(a: float, b: float) -> str:
            """Divide. Args: a: numerator. b: denominator."""
            if b == 0:
                raise ToolError("Cannot divide by zero")
            return str(a / b)

        runner = _make_runner(
            divide,
            [_make_tool_call_msg("divide", {"a": 5.0, "b": 0.0}), _make_text_msg("done")],
        )
        runner.on_tool_result = lambda _name, v: results.append(v)
        runner.on_tool_error = lambda _name, e: errors.append(e)
        runner.until_done()

        assert results == []
        assert len(errors) == 1

    def test_no_hooks_runner_works_normally(self) -> None:
        @beta_tool
        def get_weather(location: str) -> str:  # noqa: ARG001
            """Get weather. Args: location: City name."""
            return json.dumps({"temp": "22C"})

        runner = _make_runner(
            get_weather,
            [_make_tool_call_msg("get_weather", {"location": "Berlin"}), _make_text_msg("Sunny.")],
        )
        messages = list(runner)
        assert len(messages) == 2
