from __future__ import annotations

import logging
from typing import Any, cast
from typing_extensions import override

import pytest

from anthropic.lib import tools
from anthropic._compat import PYDANTIC_V1
from anthropic.lib.tools import ToolError, BetaFunctionTool, BetaAsyncFunctionTool, beta_tool, beta_async_tool
from anthropic.types.beta import BetaToolUseBlock
from anthropic.lib.tools._toolsets import ToolsetContractError
from anthropic.lib.tools._tool_dispatch import index_runnables, tool_error_content
from anthropic.lib.tools._toolsets._runnable import (
    BetaToolsetContent,
    BetaRunnableToolset,
    BetaToolsetCallContext,
    BetaAsyncRunnableToolset,
)
from anthropic.lib.tools._toolsets._sanitize import FIELD_MAX, error_text

from ._stubs import EchoBrowserToolset, AsyncEchoBrowserToolset


def _member_use(
    name: str, input: dict[str, Any] | None = None, *, toolset_name: str | None = "browser"
) -> BetaToolUseBlock:
    return BetaToolUseBlock(
        type="tool_use", id=f"toolu_{name}", name=name, input=input or {}, toolset_name=toolset_name
    )


pytestmark = pytest.mark.skipif(PYDANTIC_V1, reason="tool functions not supported with pydantic v1")


@pytest.fixture
def navigate() -> BetaFunctionTool[Any]:
    # Built inside the fixture: `beta_tool` raises at decoration time under pydantic v1.
    @beta_tool
    def navigate(url: str) -> str:
        """A custom tool that shares a browser member's name."""
        return f"custom:{url}"

    return navigate


@pytest.fixture
def async_navigate() -> BetaAsyncFunctionTool[Any]:
    @beta_async_tool
    async def async_navigate(url: str) -> str:
        """Async custom tool that shares a browser member's name."""
        return f"custom:{url}"

    return async_navigate


def test_tools_are_indexed_by_name_and_toolsets_by_family(navigate: BetaFunctionTool[Any]) -> None:
    toolset = EchoBrowserToolset()
    by_name, by_family = index_runnables([toolset, navigate])
    assert list(by_name) == ["navigate"] and by_name["navigate"] is navigate
    assert by_family == {"browser": toolset}
    assert index_runnables([navigate]) == ({"navigate": navigate}, {})


def test_tool_result_echoes_toolset_name_and_passes_the_tool_use_as_context() -> None:
    toolset = EchoBrowserToolset()
    use = _member_use("navigate", {"url": "https://example.com"})

    result = toolset.tool_result(use)
    assert result == {
        "type": "tool_result",
        "tool_use_id": "toolu_navigate",
        "toolset_name": "browser",
        "content": 'navigate:{"url": "https://example.com"}',
    }
    assert toolset.calls == [("navigate", {"url": "https://example.com"})]

    # The member learns which model call it is answering through the context, not instance state.
    assert toolset.contexts[0].tool_use is use


def test_an_unexpected_exception_is_logged_with_folded_names_and_answered_with_bounded_text(
    caplog: pytest.LogCaptureFixture,
) -> None:
    # The member name is model output and the exception text may carry page content: the operator's log line gets
    # the names with control characters folded, and the model gets at most FIELD_MAX characters.
    class Failing(EchoBrowserToolset):
        @override
        def call(self, context: BetaToolsetCallContext, name: str, input: object) -> BetaToolsetContent:
            raise RuntimeError("x" * 10_000)

    use = BetaToolUseBlock(type="tool_use", id="toolu_f", name="scr\neenshot\x1b[2J", input={}, toolset_name="browser")

    with caplog.at_level(logging.ERROR):
        result = Failing().tool_result(use)

    assert result.get("is_error") is True
    content = result.get("content")
    text = content if isinstance(content, str) else cast(Any, content)[0]["text"]
    assert len(text) == FIELD_MAX and text.startswith("RuntimeError('xxx")
    (record,) = [r for r in caplog.records if "toolset member" in r.getMessage()]
    assert "\n" not in record.getMessage() and "\x1b" not in record.getMessage()


def test_tool_result_maps_tool_error_to_is_error_text_content() -> None:
    # The API rejects anything but text on an is_error result, so the image the member attached to
    # its ToolError is dropped rather than ending the loop.
    result = EchoBrowserToolset().tool_result(_member_use("boom"))
    assert result == {
        "type": "tool_result",
        "tool_use_id": "toolu_boom",
        "toolset_name": "browser",
        "content": [{"type": "text", "text": "member refused"}],
        "is_error": True,
    }


def test_a_lone_surrogate_in_error_text_becomes_the_replacement_character() -> None:
    # page text a member quotes in its refusal may carry one; it could not be sent
    class RefusesWithText(EchoBrowserToolset):
        @override
        def call(self, context: BetaToolsetCallContext, name: str, input: object) -> BetaToolsetContent:
            raise ToolError("bad\ud800")

    class RefusesWithBlocks(EchoBrowserToolset):
        @override
        def call(self, context: BetaToolsetCallContext, name: str, input: object) -> BetaToolsetContent:
            raise ToolError([{"type": "text", "text": "bad\udc00"}])

    assert RefusesWithText().tool_result(_member_use("x"))["content"] == "bad\ufffd"  # pyright: ignore[reportTypedDictNotRequiredAccess]
    assert RefusesWithBlocks().tool_result(_member_use("x"))["content"] == [{"type": "text", "text": "bad\ufffd"}]  # pyright: ignore[reportTypedDictNotRequiredAccess]


def test_an_empty_text_block_is_dropped_from_error_content_so_the_placeholder_applies() -> None:
    # an is_error result may carry neither non-text nor empty content (the API answers either with a 400)
    result = EchoBrowserToolset().tool_result(_member_use("blank"))
    assert result.get("is_error") is True
    assert result.get("content") == "The tool call failed with an empty error message."


@pytest.mark.parametrize(
    ("exc", "text"),
    [
        (TypeError("boom"), "TypeError('boom')"),
        (RuntimeError("two\nlines"), "RuntimeError('two\\nlines')"),
        (ValueError(), "ValueError()"),  # no message: the type name is still there
        (KeyError("k"), "KeyError('k')"),
    ],
)
def test_a_raised_exception_reads_the_same_on_the_function_tool_and_toolset_paths(exc: Exception, text: str) -> None:
    assert tool_error_content(exc) == text
    assert error_text(exc) == text


def test_the_toolset_path_stays_encodable_and_cuts_to_the_field_limit() -> None:
    assert error_text(RuntimeError("a\ud800b")) == "RuntimeError('a\\ud800b')"  # `repr` escapes a lone surrogate
    assert error_text(RuntimeError("x" * 10_000)) == ("RuntimeError('" + "x" * 10_000)[:FIELD_MAX]


def test_tool_result_reports_any_other_exception_to_the_model() -> None:
    # A driver's own failure is something the model can react to, not a reason to stop the run.
    result = EchoBrowserToolset().tool_result(_member_use("crash"))
    assert result.get("is_error") is True
    assert result.get("content") == "RuntimeError('backend exploded')"


def test_tool_result_propagates_the_developer_error_class_only() -> None:
    # ToolsetUsageError is the one thing that stops the run; a TypeError from a driver is not.
    toolset = EchoBrowserToolset()
    with pytest.raises(ToolsetContractError):
        toolset.tool_result(_member_use("misuse"))

    class _TypeErrorToolset(EchoBrowserToolset):
        @override
        def call(self, context: object, name: str, input: object) -> Any:
            raise TypeError("driver bug")

    result = _TypeErrorToolset().tool_result(_member_use("navigate"))
    assert result.get("is_error") is True and result.get("content") == "TypeError('driver bug')"


@pytest.mark.parametrize("toolset_name", [None, "computer"])
def test_tool_result_rejects_block_of_another_family(toolset_name: str | None) -> None:
    toolset = EchoBrowserToolset()
    with pytest.raises(ToolsetContractError, match="is not a member call of the 'browser' toolset"):
        toolset.tool_result(_member_use("navigate", toolset_name=toolset_name))
    assert toolset.calls == []


def test_context_manager_closes_the_toolset() -> None:
    toolset = EchoBrowserToolset()
    with toolset as entered:
        assert entered is toolset
    assert toolset.closed == 1


async def test_async_tool_result_parity(async_navigate: BetaAsyncFunctionTool[Any]) -> None:
    toolset = AsyncEchoBrowserToolset()
    use = _member_use("navigate", {"url": "u"})

    ok = await toolset.tool_result(use)
    assert ok == {
        "type": "tool_result",
        "tool_use_id": "toolu_navigate",
        "toolset_name": "browser",
        "content": 'navigate:{"url": "u"}',
    }
    assert toolset.contexts[0].tool_use is use

    failed = await toolset.tool_result(_member_use("boom"))
    assert failed.get("is_error") is True and failed.get("toolset_name") == "browser"
    assert failed.get("content") == [{"type": "text", "text": "member refused"}]

    crashed = await toolset.tool_result(_member_use("crash"))
    assert crashed.get("content") == "RuntimeError('backend exploded')"

    with pytest.raises(ToolsetContractError):
        await toolset.tool_result(_member_use("misuse"))
    with pytest.raises(ToolsetContractError):
        await toolset.tool_result(_member_use("navigate", toolset_name=None))

    assert index_runnables([toolset, async_navigate]) == ({"async_navigate": async_navigate}, {"browser": toolset})

    async with toolset:
        pass
    assert toolset.closed == 1


def test_the_runnable_toolset_bases_are_exported_next_to_the_runner() -> None:
    assert (
        tools.BetaRunnableToolset is BetaRunnableToolset and tools.BetaAsyncRunnableToolset is BetaAsyncRunnableToolset
    )
    assert {"BetaRunnableToolset", "BetaAsyncRunnableToolset", "BetaToolRunner"} <= set(tools.__all__)


async def test_an_async_unexpected_exception_is_logged_with_folded_names_and_answered_with_bounded_text(
    caplog: pytest.LogCaptureFixture,
) -> None:
    class Failing(AsyncEchoBrowserToolset):
        @override
        async def call(self, context: BetaToolsetCallContext, name: str, input: object) -> BetaToolsetContent:
            raise RuntimeError("x" * 10_000)

    use = BetaToolUseBlock(type="tool_use", id="toolu_f", name="scr\neenshot\x1b[2J", input={}, toolset_name="browser")

    with caplog.at_level(logging.ERROR):
        result = await Failing().tool_result(use)

    assert result.get("is_error") is True
    content = result.get("content")
    text = content if isinstance(content, str) else cast(Any, content)[0]["text"]
    assert len(text) == FIELD_MAX and text.startswith("RuntimeError('xxx")
    (record,) = [r for r in caplog.records if "toolset member" in r.getMessage()]
    assert "\n" not in record.getMessage() and "\x1b" not in record.getMessage()


@pytest.mark.parametrize("toolset_name", [None, "computer"])
async def test_async_tool_result_rejects_block_of_another_family(toolset_name: str | None) -> None:
    toolset = AsyncEchoBrowserToolset()
    with pytest.raises(ToolsetContractError, match="is not a member call of the 'browser' toolset"):
        await toolset.tool_result(_member_use("navigate", toolset_name=toolset_name))
    assert toolset.calls == []
