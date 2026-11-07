"""In-memory browser toolsets for the pipeline tests: a handful of members over a scripted tab list,
with a queue of state changes the test can load before a call. The sync and async fakes drive the
same `World`. The inputs and helpers the tests share when reading a call's result sit at the bottom."""

from __future__ import annotations

from typing import Any, cast
from typing_extensions import override

import pytest

from anthropic.tools import (
    ToolError,
)
from anthropic.types.beta import (
    BetaBrowserKeyInput,
    BetaBrowserWaitInput,
    BetaBrowserNewTabInput,
    BetaBrowserScrollInput,
    BetaBrowserHoldKeyInput,
    BetaBrowserCloseTabInput,
    BetaBrowserListTabsInput,
    BetaBrowserNavigateInput,
    BetaBrowserScrollToInput,
    BetaBrowserLeftClickInput,
    BetaBrowserSwitchTabInput,
    BetaBrowserFileUploadInput,
    BetaBrowserScreenshotInput,
    BetaBrowserGetPageTextInput,
    BetaBrowserStateTabEntryParam,
)
from anthropic.tools.browser import (
    BetaBrowserState,
    BetaConfirmContext,
    BetaScreenshotResult,
    BetaToolsetCallContext,
    BetaBrowserNavigateResult,
    BetaAbstractBrowserToolset20260801,
    BetaAsyncAbstractBrowserToolset20260801,
)
from anthropic.lib.tools._toolsets._results import StateChange


class World:
    """The browser both fakes drive: tabs, the active tab, queued state changes and a call log."""

    def __init__(self) -> None:
        self.tabs: dict[str, dict[str, str]] = {"tab_1": {"title": "Blank", "url": "about:blank"}}
        self.active: str | None = "tab_1"
        self.changes: list[StateChange] = []
        self.calls: list[str] = []
        self.inputs: list[Any] = []
        self.contexts: list[BetaToolsetCallContext] = []
        self.state_contexts: list[BetaToolsetCallContext] = []
        self.page_text = "Hello"
        self.fail: dict[str, BaseException] = {}
        self.state_error: BaseException | None = None
        self.state_override: BetaBrowserState | None = None

        # a member name -> the result to hand back instead of the usual one; tests stash off-type values on purpose
        self.results: dict[str, Any] = {}
        self.next_tab = 2

    def state(self, context: BetaToolsetCallContext) -> BetaBrowserState:
        self.state_contexts.append(context)

        if self.state_error is not None:
            raise self.state_error
        if self.state_override is not None:
            return self.state_override

        changes, self.changes = self.changes, []
        tabs: list[BetaBrowserStateTabEntryParam] = [
            {"tab_id": tab_id, "title": tab["title"], "url": tab["url"], "active": tab_id == self.active}
            for tab_id, tab in self.tabs.items()
        ]
        return BetaBrowserState(tabs=tabs, state_changes=changes)

    def do(self, name: str, context: BetaToolsetCallContext, input: Any) -> None:
        self.calls.append(name)
        self.inputs.append(input)
        self.contexts.append(context)
        if name in self.fail:
            raise self.fail[name]

    def tab(self, tab_id: str | None) -> str:
        key = tab_id or self.active
        if key is None or key not in self.tabs:
            raise ToolError(f"No open tab with tab_id {tab_id!r}.")
        return key

    # member bodies -------------------------------------------------------------------------

    def navigate(self, context: BetaToolsetCallContext, input: BetaBrowserNavigateInput) -> BetaBrowserNavigateResult:
        self.do("navigate", context, input)
        key = self.tab(input.tab_id)

        # a history word moves within the tab's history; like a real browser the fake then reports the page it is on
        url = self.tabs.get(key, {}).get("url", "about:blank") if input.url in ("back", "forward") else input.url
        self.tabs[key] = {"title": f"Title of {url}", "url": url}

        if "navigate" in self.results:
            return self.results["navigate"]
        return BetaBrowserNavigateResult(url=url, status=200, title=self.tabs[key]["title"])

    def screenshot(self, context: BetaToolsetCallContext, input: BetaBrowserScreenshotInput) -> BetaScreenshotResult:
        self.do("screenshot", context, input)
        if "screenshot" in self.results:
            return self.results["screenshot"]
        return BetaScreenshotResult(data="iVBORw0KGgo=")

    def action(self, name: str, context: BetaToolsetCallContext, input: Any) -> Any:
        self.do(name, context, input)
        return self.results.get(name)  # a pure action may hand back one line of text

    def get_page_text(self, context: BetaToolsetCallContext, input: BetaBrowserGetPageTextInput) -> str:
        self.do("get_page_text", context, input)
        return self.page_text

    def new_tab(self, context: BetaToolsetCallContext, input: BetaBrowserNewTabInput) -> BetaBrowserStateTabEntryParam:
        self.do("new_tab", context, input)

        if "new_tab" in self.results:
            return self.results["new_tab"]

        tab_id = f"tab_{self.next_tab}"
        self.next_tab += 1
        self.tabs[tab_id] = {"title": "", "url": "about:blank"}
        self.active = tab_id
        self.changes.append({"type": "tab_opened", "tab_id": tab_id})
        return {"tab_id": tab_id, "title": "", "url": "about:blank", "active": True}

    def list_tabs(
        self, context: BetaToolsetCallContext, input: BetaBrowserListTabsInput
    ) -> list[BetaBrowserStateTabEntryParam]:
        self.do("list_tabs", context, input)
        return [
            {"tab_id": tab_id, "title": tab["title"], "url": tab["url"], "active": tab_id == self.active}
            for tab_id, tab in self.tabs.items()
        ]

    def switch_tab(
        self, context: BetaToolsetCallContext, input: BetaBrowserSwitchTabInput
    ) -> BetaBrowserStateTabEntryParam:
        self.do("switch_tab", context, input)
        key = self.tab(input.tab_id)
        self.active = key
        return {"tab_id": key, "title": self.tabs[key]["title"], "url": self.tabs[key]["url"], "active": True}

    def close_tab(self, context: BetaToolsetCallContext, input: BetaBrowserCloseTabInput) -> None:
        self.do("close_tab", context, input)
        key = self.tab(input.tab_id)
        del self.tabs[key]
        if self.active == key:
            self.active = next(iter(self.tabs), None)


class FakeBrowser(BetaAbstractBrowserToolset20260801):
    def __init__(self, world: World | None = None, **options: Any) -> None:
        self.world = world or World()
        super().__init__(**options)

    @override
    def _browser_state(self, context: BetaToolsetCallContext) -> BetaBrowserState:
        return self.world.state(context)

    @override
    def navigate(self, context: BetaToolsetCallContext, input: BetaBrowserNavigateInput) -> BetaBrowserNavigateResult:
        return self.world.navigate(context, input)

    @override
    def screenshot(self, context: BetaToolsetCallContext, input: BetaBrowserScreenshotInput) -> BetaScreenshotResult:
        return self.world.screenshot(context, input)

    @override
    def left_click(self, context: BetaToolsetCallContext, input: BetaBrowserLeftClickInput) -> str | None:
        return self.world.action("left_click", context, input)

    @override
    def scroll(self, context: BetaToolsetCallContext, input: BetaBrowserScrollInput) -> None:
        self.world.action("scroll", context, input)

    @override
    def scroll_to(self, context: BetaToolsetCallContext, input: BetaBrowserScrollToInput) -> None:
        self.world.action("scroll_to", context, input)

    @override
    def key(self, context: BetaToolsetCallContext, input: BetaBrowserKeyInput) -> None:
        self.world.action("key", context, input)

    @override
    def hold_key(self, context: BetaToolsetCallContext, input: BetaBrowserHoldKeyInput) -> None:
        self.world.action("hold_key", context, input)

    @override
    def wait(self, context: BetaToolsetCallContext, input: BetaBrowserWaitInput) -> None:
        self.world.action("wait", context, input)

    @override
    def file_upload(self, context: BetaToolsetCallContext, input: BetaBrowserFileUploadInput) -> None:
        self.world.action("file_upload", context, input)

    @override
    def get_page_text(self, context: BetaToolsetCallContext, input: BetaBrowserGetPageTextInput) -> str:
        return self.world.get_page_text(context, input)

    @override
    def new_tab(self, context: BetaToolsetCallContext, input: BetaBrowserNewTabInput) -> BetaBrowserStateTabEntryParam:
        return self.world.new_tab(context, input)

    @override
    def list_tabs(
        self, context: BetaToolsetCallContext, input: BetaBrowserListTabsInput
    ) -> list[BetaBrowserStateTabEntryParam]:
        return self.world.list_tabs(context, input)

    @override
    def switch_tab(
        self, context: BetaToolsetCallContext, input: BetaBrowserSwitchTabInput
    ) -> BetaBrowserStateTabEntryParam:
        return self.world.switch_tab(context, input)

    @override
    def close_tab(self, context: BetaToolsetCallContext, input: BetaBrowserCloseTabInput) -> None:
        self.world.close_tab(context, input)


class AsyncFakeBrowser(BetaAsyncAbstractBrowserToolset20260801):
    def __init__(self, world: World | None = None, **options: Any) -> None:
        self.world = world or World()
        super().__init__(**options)

    @override
    async def _browser_state(self, context: BetaToolsetCallContext) -> BetaBrowserState:
        return self.world.state(context)

    @override
    async def navigate(
        self, context: BetaToolsetCallContext, input: BetaBrowserNavigateInput
    ) -> BetaBrowserNavigateResult:
        return self.world.navigate(context, input)

    @override
    async def screenshot(
        self, context: BetaToolsetCallContext, input: BetaBrowserScreenshotInput
    ) -> BetaScreenshotResult:
        return self.world.screenshot(context, input)

    @override
    async def left_click(self, context: BetaToolsetCallContext, input: BetaBrowserLeftClickInput) -> str | None:
        return self.world.action("left_click", context, input)

    @override
    async def scroll(self, context: BetaToolsetCallContext, input: BetaBrowserScrollInput) -> None:
        self.world.action("scroll", context, input)

    @override
    async def scroll_to(self, context: BetaToolsetCallContext, input: BetaBrowserScrollToInput) -> None:
        self.world.action("scroll_to", context, input)

    @override
    async def key(self, context: BetaToolsetCallContext, input: BetaBrowserKeyInput) -> None:
        self.world.action("key", context, input)

    @override
    async def hold_key(self, context: BetaToolsetCallContext, input: BetaBrowserHoldKeyInput) -> None:
        self.world.action("hold_key", context, input)

    @override
    async def wait(self, context: BetaToolsetCallContext, input: BetaBrowserWaitInput) -> None:
        self.world.action("wait", context, input)

    @override
    async def file_upload(self, context: BetaToolsetCallContext, input: BetaBrowserFileUploadInput) -> None:
        self.world.action("file_upload", context, input)

    @override
    async def get_page_text(self, context: BetaToolsetCallContext, input: BetaBrowserGetPageTextInput) -> str:
        return self.world.get_page_text(context, input)

    @override
    async def new_tab(
        self, context: BetaToolsetCallContext, input: BetaBrowserNewTabInput
    ) -> BetaBrowserStateTabEntryParam:
        return self.world.new_tab(context, input)

    @override
    async def list_tabs(
        self, context: BetaToolsetCallContext, input: BetaBrowserListTabsInput
    ) -> list[BetaBrowserStateTabEntryParam]:
        return self.world.list_tabs(context, input)

    @override
    async def switch_tab(
        self, context: BetaToolsetCallContext, input: BetaBrowserSwitchTabInput
    ) -> BetaBrowserStateTabEntryParam:
        return self.world.switch_tab(context, input)

    @override
    async def close_tab(self, context: BetaToolsetCallContext, input: BetaBrowserCloseTabInput) -> None:
        self.world.close_tab(context, input)


# shared inputs and result readers ----------------------------------------------------------------

CLICK: dict[str, Any] = {"target": {"type": "coordinate", "x": 1, "y": 1}}
UPLOAD: dict[str, Any] = {"target": {"type": "ref", "ref": "e1"}}
TAB_GONE = "The tab this call was addressed to is not open; nothing was returned. Use list_tabs to see what is open."


def approve(_context: BetaConfirmContext) -> bool:
    return True


def texts(content: Any) -> list[str]:
    return [block["text"] for block in content if block.get("type") == "text"]


def state_block(content: Any) -> dict[str, Any]:
    (block,) = [b for b in content if b.get("type") == "browser_state"]
    return cast(dict[str, Any], block)


def refusal(browser: FakeBrowser, context: BetaToolsetCallContext, name: str, input: Any) -> str:
    with pytest.raises(ToolError) as caught:
        browser.call(context, name, input)
    (text,) = texts(caught.value.content)
    return text
