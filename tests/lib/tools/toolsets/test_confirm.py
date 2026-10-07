# ruff: noqa: ARG001 -- stub members and hooks ignore their arguments
"""The confirm approval gate."""

from __future__ import annotations

import functools
from typing import Any, cast
from urllib.parse import urlsplit
from typing_extensions import override

import pytest

from anthropic.tools import (
    ToolError,
    ToolsetConfigError,
    ToolsetContractError,
)
from anthropic.types.beta import (
    BetaToolUseBlock,
    BetaBrowserLeftClickInput,
)
from anthropic.tools.browser import (
    BetaConfirmContext,
    BetaLocalFilePolicy,
    BetaToolsetCallContext,
)

from ._fakes import CLICK, World, FakeBrowser, AsyncFakeBrowser, texts, approve, refusal

CTX = BetaToolsetCallContext(
    tool_use=BetaToolUseBlock(type="tool_use", id="toolu_7", name="left_click", input={}, toolset_name="browser")
)
DECLINED = "The user did not grant permission to run 'left_click'. Do not retry it unless the user asks you to."
FAILED = (
    "Permission to run 'left_click' could not be obtained (the confirmation prompt failed). "
    "Do not retry it unless the user asks you to."
)


def _deny(context: BetaConfirmContext) -> bool:
    return False


def test_confirm_sees_every_call_and_a_decline_never_reaches_the_driver() -> None:
    # The callable is asked before every member call that is about to run and decides by name (or anything else)
    # which ones it gates; a False never reaches the driver.
    asked: list[str] = []

    def confirm(context: BetaConfirmContext) -> bool:
        asked.append(context.member)
        return context.member != "left_click" or len(asked) > 2

    browser = FakeBrowser(confirm=confirm)
    assert texts(browser.call(CTX, "get_page_text", {})) == ["Hello"]
    assert refusal(browser, CTX, "left_click", CLICK) == DECLINED
    assert browser.world.calls == ["get_page_text"]
    assert texts(browser.call(CTX, "left_click", CLICK)) == ["Clicked."]
    assert browser.world.calls == ["get_page_text", "left_click"] and asked == [
        "get_page_text",
        "left_click",
        "left_click",
    ]

    # a call refused before dispatch (unknown member, disabled member) is never asked about
    with pytest.raises(ToolError):
        browser.call(CTX, "teleport", {})
    assert asked == ["get_page_text", "left_click", "left_click"]
    gated = FakeBrowser(confirm=confirm, configs={"left_click": {"enabled": False}})
    with pytest.raises(ToolError):
        gated.call(CTX, "left_click", CLICK)
    assert asked == ["get_page_text", "left_click", "left_click"] and gated.world.calls == []


def test_enabling_file_upload_or_javascript_exec_requires_confirm() -> None:
    class AnyPath(BetaLocalFilePolicy):
        @override
        def resolve_upload_paths(self, context: Any, paths: Any) -> list[str]:
            return list(paths)

    upload: dict[str, Any] = {"target": {"type": "ref", "ref": "e1"}, "paths": ["/f"]}
    options: dict[str, Any] = {"configs": {"file_upload": {"enabled": True}}, "file_policy": AnyPath()}

    with pytest.raises(ToolsetConfigError, match="file_upload.*confirm"):
        FakeBrowser(**options)

    asked: list[str] = []

    def gate_uploads(context: BetaConfirmContext) -> bool:
        asked.append(context.member)
        return context.member != "file_upload"

    browser = FakeBrowser(**options, confirm=gate_uploads)
    assert refusal(browser, CTX, "file_upload", upload) == DECLINED.replace("left_click", "file_upload")
    assert asked == ["file_upload"] and browser.world.calls == []

    FakeBrowser(**options, confirm=approve).call(CTX, "file_upload", upload)  # approving everything is the opt-out


def test_confirm_context_describes_the_target_tab_as_of_the_last_block_and_costs_nothing_unread() -> None:
    seen: list[Any] = []

    def by_name(context: BetaConfirmContext) -> bool:
        seen.append((context.member, context.tool_use, context.input))
        return True

    browser = FakeBrowser(confirm=by_name)
    use = BetaToolsetCallContext(
        tool_use=BetaToolUseBlock(type="tool_use", id="toolu_c", name="left_click", input=CLICK, toolset_name="browser")
    )

    browser.call(use, "left_click", CLICK)
    assert seen[-1] == ("left_click", use.tool_use, browser.world.inputs[-1])

    # the context carries the very objects the call was given — the parsed input a gate narrows with isinstance, and
    # the tool_use block — not validated copies (pydantic v1 would otherwise retype the input as a sibling model)
    assert seen[-1][1] is use.tool_use and seen[-1][2] is browser.world.inputs[-1]
    assert type(seen[-1][2]) is BetaBrowserLeftClickInput

    # the prompt costs no state read: one per call, as without confirm
    assert len(browser.world.state_contexts) == 1

    def by_tab(context: BetaConfirmContext) -> bool:
        seen.append((context.tab_url, context.tab_id))
        return True

    browser = FakeBrowser(confirm=by_tab)
    browser.call(CTX, "left_click", CLICK)  # before any report there is no tab to describe
    assert seen[-1] == (None, None)

    browser.call(CTX, "navigate", {"url": "https://shop.example.com/cart?x=1"})
    browser.call(CTX, "left_click", CLICK)
    assert seen[-1] == ("https://shop.example.com/cart?x=1", "tab_1")

    # reading the tab costs nothing either: it is described from the last report, with no page read
    assert len(browser.world.state_contexts) == 1 + 1 + 1

    # A call that names a tab is described by that tab, not the active one.
    browser.world.tabs["tab_2"] = {"title": "docs", "url": "https://docs.example.com/"}
    browser.call(CTX, "list_tabs", {})
    browser.call(CTX, "left_click", {**CLICK, "tab_id": "tab_2"})
    assert seen[-1] == ("https://docs.example.com/", "tab_2")

    # tab_url is the URL as the driver reported it and the model read it — no rewriting — folded to one line and held
    # to 4,096 characters. A longer one is cut and starts with `…`.
    browser.call(CTX, "navigate", {"url": "HTTPS://trusted.example@Example.COM:443/cart"})
    browser.call(CTX, "left_click", CLICK)
    assert seen[-1][0] == "HTTPS://trusted.example@Example.COM:443/cart"

    browser.world.tabs["tab_1"] = {"title": "t", "url": "https://example.com/a\u202e)b \u2028" + "c" * 5000}
    browser.call(CTX, "list_tabs", {})
    browser.call(CTX, "left_click", CLICK)
    tab_url, _ = seen[-1]
    assert tab_url.startswith("\u2026https://example.com/a )b  c") and len(tab_url) == 4096 and "\u202e" not in tab_url

    # A page can pad its URL so that its first 4,096 characters alone parse to another host. The leading `…` leaves
    # no host to parse.
    browser.world.tabs["tab_1"] = {"title": "t", "url": "https://trusted.bank.com:" + "0" * 4100 + "@evil.example/"}
    browser.call(CTX, "list_tabs", {})
    browser.call(CTX, "left_click", CLICK)
    cut_url: str = seen[-1][0]
    assert cut_url.startswith("\u2026") and urlsplit(cut_url).hostname is None


def test_an_approval_covers_the_last_report_and_the_page_is_not_read_again() -> None:
    # confirm describes the tab as of the last block the model saw; the page can move after that report, and the
    # approved call runs wherever the tab is by then.
    world = World()
    looked: list[Any] = []

    def confirm(context: BetaConfirmContext) -> bool:
        looked.append(context.tab_url)
        return True

    browser = FakeBrowser(world, confirm=confirm)
    browser.call(CTX, "navigate", {"url": "https://shop.example.com/cart"})

    world.tabs["tab_1"]["url"] = "https://elsewhere.example.net/next"
    assert texts(browser.call(CTX, "left_click", CLICK)) == ["Clicked."]
    assert looked[-1] == "https://shop.example.com/cart" and browser.world.calls == ["navigate", "left_click"]
    assert len(browser.world.state_contexts) == 2  # one report per call, none for the prompt

    # The block that click produced showed the new page, so the next prompt describes it.
    browser.call(CTX, "left_click", CLICK)
    assert looked[-1] == "https://elsewhere.example.net/next"


def test_a_confirm_that_raises_refuses_the_call_and_a_tool_error_is_relayed() -> None:
    def broken(context: BetaConfirmContext) -> bool:
        raise RuntimeError("tty closed")

    assert refusal(FakeBrowser(confirm=broken), CTX, "left_click", CLICK) == FAILED

    def refusing(context: BetaConfirmContext) -> bool:
        raise ToolError("clicks are disabled after 5pm")

    assert refusal(FakeBrowser(confirm=refusing), CTX, "left_click", CLICK) == "clicks are disabled after 5pm"


def test_a_confirm_answer_other_than_true_declines_the_call() -> None:
    def vague(context: BetaConfirmContext) -> Any:
        return "yes"

    browser = FakeBrowser(confirm=vague)
    assert refusal(browser, CTX, "left_click", CLICK) == DECLINED and browser.world.calls == []

    async def coroutine(context: BetaConfirmContext) -> bool:
        return True

    class Prompt:
        async def __call__(self, context: BetaConfirmContext) -> bool:
            return context.member == "left_click"

    # an `async def`, an object whose `__call__` is one, and a partial of either are all seen when the toolset is built
    for confirm in (coroutine, Prompt(), functools.partial(coroutine)):
        with pytest.raises(ToolsetContractError, match="confirm is async on the synchronous toolset"):
            FakeBrowser(confirm=cast(Any, confirm))


def test_the_gate_runs_before_an_execute_override() -> None:
    reached: list[str] = []

    class Hooked(FakeBrowser):
        @override
        def execute(self, context: BetaToolsetCallContext, name: Any, input: Any) -> Any:
            reached.append(name)
            return super().execute(context, name, input)

    with pytest.raises(ToolError):
        Hooked(confirm=_deny).call(CTX, "left_click", CLICK)
    assert reached == []


def test_the_url_policy_runs_before_confirm() -> None:
    asked: list[str] = []

    def no_internal(context: Any, url: str) -> None:
        if "internal" in url:
            raise ToolError("blocked: internal")

    def confirm(context: BetaConfirmContext) -> bool:
        asked.append(context.member)
        return True

    browser = FakeBrowser(url_policy=no_internal, confirm=confirm)
    with pytest.raises(ToolError, match="blocked"):
        browser.call(CTX, "navigate", {"url": "https://wiki.internal/"})
    assert asked == []


async def test_async_confirm_may_be_a_coroutine_or_a_plain_function() -> None:
    async def deny(context: BetaConfirmContext) -> bool:
        return False

    browser = AsyncFakeBrowser(confirm=deny)
    with pytest.raises(ToolError) as caught:
        await browser.call(CTX, "left_click", CLICK)
    assert texts(caught.value.content) == [DECLINED]
    assert browser.world.calls == []

    allow = AsyncFakeBrowser(confirm=approve)
    assert texts(await allow.call(CTX, "left_click", CLICK)) == ["Clicked."]

    # the tab description works the same way on the async class
    seen: list[Any] = []

    async def by_tab(context: BetaConfirmContext) -> bool:
        seen.append((context.tab_url, context.tab_id))
        return True

    looking = AsyncFakeBrowser(confirm=by_tab)
    await looking.call(CTX, "navigate", {"url": "https://shop.example.com/"})
    await looking.call(CTX, "left_click", CLICK)
    assert seen[-1] == ("https://shop.example.com/", "tab_1")

    def vague(context: BetaConfirmContext) -> Any:
        return None

    with pytest.raises(ToolError) as caught:
        await AsyncFakeBrowser(confirm=vague).call(CTX, "left_click", CLICK)
    assert texts(caught.value.content) == [DECLINED]


async def test_an_async_confirm_that_raises_refuses_the_call_and_a_tool_error_is_relayed() -> None:
    async def broken(context: BetaConfirmContext) -> bool:
        raise RuntimeError("tty closed")

    with pytest.raises(ToolError) as failed:
        await AsyncFakeBrowser(confirm=broken).call(CTX, "left_click", CLICK)
    assert texts(failed.value.content) == [FAILED]

    async def refusing(context: BetaConfirmContext) -> bool:
        raise ToolError("clicks are disabled after 5pm")

    with pytest.raises(ToolError) as relayed:
        await AsyncFakeBrowser(confirm=refusing).call(CTX, "left_click", CLICK)
    assert texts(relayed.value.content) == ["clicks are disabled after 5pm"]


async def test_the_async_gate_runs_before_an_execute_override() -> None:
    reached: list[str] = []

    class Hooked(AsyncFakeBrowser):
        @override
        async def execute(self, context: BetaToolsetCallContext, name: Any, input: Any) -> Any:
            reached.append(name)
            return await super().execute(context, name, input)

    with pytest.raises(ToolError):
        await Hooked(confirm=_deny).call(CTX, "left_click", CLICK)
    assert reached == []


async def test_the_async_url_policy_runs_before_confirm() -> None:
    asked: list[str] = []

    async def no_internal(context: Any, url: str) -> None:
        if "internal" in url:
            raise ToolError("blocked: internal")

    async def confirm(context: BetaConfirmContext) -> bool:
        asked.append(context.member)
        return True

    browser = AsyncFakeBrowser(url_policy=no_internal, confirm=confirm)
    with pytest.raises(ToolError, match="blocked"):
        await browser.call(CTX, "navigate", {"url": "https://wiki.internal/"})
    assert asked == []
