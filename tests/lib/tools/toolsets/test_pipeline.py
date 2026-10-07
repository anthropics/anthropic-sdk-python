# ruff: noqa: ARG002 -- stub members and hooks ignore their arguments
"""The call pipeline: resolve → parse → execute → browser_state → render, on both classes."""

from __future__ import annotations

import re
import json
import inspect
import threading
from typing import Any, cast
from pathlib import Path
from collections.abc import Sequence
from typing_extensions import override

import anyio
import pytest
import pydantic

from anthropic.tools import (
    ToolError,
    ToolsetClosedError,
    ToolsetConfigError,
    ToolsetContractError,
)
from anthropic._compat import PYDANTIC_V1
from anthropic.types.beta import (
    BetaToolUseBlock,
    BetaBrowserNavigateInput,
    BetaBrowserJavascriptExecInput,
    BetaBrowserStateChangeDownloadCompletedParam,
)
from anthropic.tools.browser import (
    BetaURLContext,
    BetaBrowserState,
    BetaConfirmContext,
    BetaDialogDismissed,
    BetaLocalFilePolicy,
    BetaScreenshotResult,
    BetaNavigationRefused,
    BetaToolsetCallContext,
    BetaBrowserNavigateResult,
    BetaAbstractBrowserToolset20260801,
)
from anthropic.lib.tools._toolsets._runnable import unvalidated
from anthropic.lib.tools._toolsets._sanitize import one_line, quoted_name, bounded_tab_url

from ._fakes import CLICK, World, FakeBrowser, AsyncFakeBrowser, texts, approve, refusal, state_block

CTX = BetaToolsetCallContext()


def _use(name: str, input: dict[str, Any], id: str = "toolu_1") -> BetaToolUseBlock:
    return BetaToolUseBlock(type="tool_use", id=id, name=name, input=input, toolset_name="browser")


# --- rendering ------------------------------------------------------------------------------------


def test_navigate_renders_one_line_and_attaches_the_browser_state_block() -> None:
    browser = FakeBrowser()
    content = browser.call(CTX, "navigate", {"url": "https://example.com/"})
    assert content == [
        {"type": "text", "text": "Navigated to https://example.com/ — Title of https://example.com/ (HTTP 200)"},
        {
            "type": "browser_state",
            "tabs": [
                {
                    "tab_id": "tab_1",
                    "title": "Title of https://example.com/",
                    "url": "https://example.com/",
                    "active": True,
                }
            ],
        },
    ]


def test_navigate_line_folds_control_characters_and_omits_absent_fields() -> None:
    class Bare(FakeBrowser):
        @override
        def navigate(
            self, context: BetaToolsetCallContext, input: BetaBrowserNavigateInput
        ) -> BetaBrowserNavigateResult:
            return BetaBrowserNavigateResult(url=input.url, title="A\nB\u202eC")

    (line,) = texts(Bare().call(CTX, "navigate", {"url": "https://x.test/"}))
    assert line == "Navigated to https://x.test/ — A B C"

    # the landed address is the page's choice through redirects: it reaches the line as the driver reported it, held
    # to the field limit
    class Redirecting(FakeBrowser):
        @override
        def navigate(
            self, context: BetaToolsetCallContext, input: BetaBrowserNavigateInput
        ) -> BetaBrowserNavigateResult:
            return BetaBrowserNavigateResult(url="https://accounts.example.com/" + "a" * 5000)

    (line,) = texts(Redirecting().call(CTX, "navigate", {"url": "https://x.test/"}))
    assert line == "Navigated to \u2026" + ("https://accounts.example.com/" + "a" * 5000)[:4095]


def test_pure_actions_render_their_confirmation_from_the_input() -> None:
    browser = FakeBrowser()
    assert texts(browser.call(CTX, "left_click", {"target": {"type": "coordinate", "x": 1, "y": 2}})) == ["Clicked."]
    assert texts(
        browser.call(CTX, "scroll", {"scroll_direction": "down", "target": {"type": "coordinate", "x": 0, "y": 0}})
    ) == ["Scrolled down."]
    assert texts(browser.call(CTX, "scroll_to", {"target": {"type": "ref", "ref": "e12"}})) == ["Scrolled to e12."]
    assert texts(browser.call(CTX, "key", {"text": "ctrl+a"})) == ["Pressed ctrl+a."]
    assert texts(browser.call(CTX, "wait", {"duration": 1.5})) == ["Waited 1.5s."]
    assert texts(browser.call(CTX, "wait", {"duration": 2})) == ["Waited 2s."]

    # A model-supplied value that looks like a placeholder stays data.
    assert texts(browser.call(CTX, "key", {"text": "{duration}"})) == ["Pressed {duration}."]


def test_a_pure_action_may_return_one_line_the_model_reads_after_the_acknowledgment() -> None:
    # The line is page-shaped, so it is folded to one line as a title is. It is its own text block, after the
    # acknowledgment's.
    browser = FakeBrowser()
    browser.world.results["left_click"] = "Opened menu\nwith 3 items from /var/task/menu.json"
    content = browser.call(CTX, "left_click", CLICK)
    assert texts(content) == ["Clicked.", "Opened menu with 3 items from /var/task/menu.json"]
    assert [block["type"] for block in content] == ["text", "text", "browser_state"]

    # an address stays as the driver wrote it
    browser.world.results["left_click"] = "Opened https://u:p@example.com/menu"
    assert texts(browser.call(CTX, "left_click", CLICK)) == ["Clicked.", "Opened https://u:p@example.com/menu"]

    # nothing returned, or anything but a non-empty string, is the acknowledgment alone
    for returned in (None, "", " \n ", 3, ["Opened"]):
        browser.world.results["left_click"] = returned
        assert texts(browser.call(CTX, "left_click", CLICK)) == ["Clicked."]

    # the line is bounded like every other page-supplied value the SDK writes into its own text
    browser.world.results["left_click"] = "x" * 10_000
    assert texts(browser.call(CTX, "left_click", CLICK)) == ["Clicked.", "x" * 4096]


async def test_an_async_pure_action_may_return_one_line_too() -> None:
    browser = AsyncFakeBrowser()
    browser.world.results["left_click"] = "Opened menu\u2028at /var/task/menu.json"
    assert texts(await browser.call(CTX, "left_click", CLICK)) == ["Clicked.", "Opened menu at /var/task/menu.json"]

    browser.world.results["left_click"] = None
    assert texts(await browser.call(CTX, "left_click", CLICK)) == ["Clicked."]

    # bounded as on the sync path
    browser.world.results["left_click"] = "x" * 10_000
    assert texts(await browser.call(CTX, "left_click", CLICK)) == ["Clicked.", "x" * 4096]


def test_a_duration_is_not_bounded_by_the_sdk() -> None:
    # as in TypeScript: the value reaches the driver as sent, and a driver's refusal is what the model reads
    browser = FakeBrowser()
    assert texts(browser.call(CTX, "wait", {"duration": 60})) == ["Waited 60s."]
    assert texts(browser.call(CTX, "hold_key", {"text": "a", "duration": -1})) == ["Held a for -1s."]
    assert browser.world.calls == ["wait", "hold_key"]

    browser.world.fail["wait"] = ToolError("duration: must be between 0 and 30 seconds")
    assert refusal(browser, CTX, "wait", {"duration": 60}) == "duration: must be between 0 and 30 seconds"


def test_screenshot_renders_one_image_block_as_returned() -> None:
    content = FakeBrowser().call(CTX, "screenshot", {})
    assert content[0] == {
        "type": "image",
        "source": {"type": "base64", "media_type": "image/png", "data": "iVBORw0KGgo="},
    }
    assert content[1]["type"] == "browser_state"


def test_text_members_render_verbatim_and_empty_text_gets_a_placeholder() -> None:
    browser = FakeBrowser()
    assert texts(browser.call(CTX, "get_page_text", {})) == ["Hello"]
    browser.world.page_text = ""
    assert texts(browser.call(CTX, "get_page_text", {})) == ["(empty)"]

    # page text can carry an unpaired surrogate (legal in the DOM); it could not be sent, so it becomes U+FFFD
    browser.world.page_text = "a\ud83dz"
    assert texts(browser.call(CTX, "get_page_text", {})) == ["a\ufffdz"]


def test_tab_members_render_the_browser_state_block_alone() -> None:
    browser = FakeBrowser()
    content = browser.call(CTX, "new_tab", {})
    assert content == [
        {
            "type": "browser_state",
            "tabs": [
                {"tab_id": "tab_1", "title": "Blank", "url": "about:blank", "active": False},
                {"tab_id": "tab_2", "title": "", "url": "about:blank", "active": True},
            ],
            "state_changes": [{"type": "tab_opened", "tab_id": "tab_2"}],
        }
    ]

    assert [b["type"] for b in browser.call(CTX, "list_tabs", {})] == ["browser_state"]
    assert [b["type"] for b in browser.call(CTX, "switch_tab", {"tab_id": "tab_1"})] == ["browser_state"]
    assert [b["type"] for b in browser.call(CTX, "close_tab", {"tab_id": "tab_2"})] == ["browser_state"]
    assert [t["tab_id"] for t in state_block(browser.call(CTX, "list_tabs", {}))["tabs"]] == ["tab_1"]


def test_state_changes_pass_through_and_download_paths_stay_hidden_without_a_file_policy() -> None:
    browser = FakeBrowser()
    browser.world.changes = [  # pyright: ignore[reportAttributeAccessIssue]
        {"type": "download_started", "download_id": "dl_1", "url": "https://example.com/a.pdf", "path": "/tmp/a"},
        {
            "type": "download_completed",
            "download_id": "dl_2",
            "url": "https://example.com/b.pdf",
            "path": "/tmp/b",
            "size_bytes": 3,
        },
        {"type": "download_failed", "download_id": "dl_3", "url": "https://example.com/c.pdf", "path": "/tmp/c"},
    ]

    block = state_block(browser.call(CTX, "get_page_text", {}))
    # a path is dropped from whichever download change carries it, not only the completed one
    assert block["state_changes"] == [
        {"type": "download_started", "download_id": "dl_1", "url": "https://example.com/a.pdf"},
        {"type": "download_completed", "download_id": "dl_2", "url": "https://example.com/b.pdf", "size_bytes": 3},
        {"type": "download_failed", "download_id": "dl_3", "url": "https://example.com/c.pdf"},
    ]

    # Nothing to report is an absent field, never an empty list.
    assert "state_changes" not in state_block(browser.call(CTX, "get_page_text", {}))


def test_a_download_path_is_exposed_only_when_the_file_policy_answers_true() -> None:
    change: BetaBrowserStateChangeDownloadCompletedParam = {
        "type": "download_completed",
        "download_id": "dl_1",
        "url": "https://example.com/a",
        "size_bytes": 1,
    }

    class Answering:
        def __init__(self, answer: object) -> None:
            self.answer = answer

        def resolve_upload_paths(self, context: object, paths: object) -> list[str]:
            return []

        def resolve_upload_documents(self, context: object, document_ids: object) -> list[str]:
            return []

        def is_path_visible(self, path: str) -> bool:
            return self.answer  # pyright: ignore[reportReturnType]

    class Truthy:
        def __bool__(self) -> bool:
            return True

    for answer, exposed in [(True, True), (False, False)]:
        browser = FakeBrowser(file_policy=Answering(answer))
        browser.world.changes = [{**change, "path": "/tmp/a"}]
        (reported,) = state_block(browser.call(CTX, "get_page_text", {}))["state_changes"]
        assert ("path" in reported) is exposed

    # any other answer hides it, even a truthy one
    for answer in (Truthy(), 1, None):
        browser = FakeBrowser(file_policy=Answering(answer))
        browser.world.changes = [{**change, "path": "/tmp/a"}]
        assert state_block(browser.call(CTX, "get_page_text", {}))["state_changes"] == [change]

    # so does what a policy written `async def is_path_visible` returns, and the coroutine is closed, so no "never
    # awaited" warning is left behind
    async def predicate() -> bool:
        return True

    coroutine = predicate()
    browser = FakeBrowser(file_policy=Answering(coroutine))
    browser.world.changes = [{**change, "path": "/tmp/a"}]
    assert state_block(browser.call(CTX, "get_page_text", {}))["state_changes"] == [change]
    assert inspect.getcoroutinestate(coroutine) == "CORO_CLOSED"

    # a policy that raises on a path fails closed: the path is hidden and the change still reaches the model
    class Raising(Answering):
        @override
        def is_path_visible(self, path: str) -> bool:
            raise RuntimeError(path)

    browser = FakeBrowser(file_policy=Raising(True))
    browser.world.changes = [{**change, "path": "/tmp/a"}]
    assert state_block(browser.call(CTX, "get_page_text", {}))["state_changes"] == [change]

    # A server picks a download's file name (its Content-Disposition). If folding the path to one line or cutting it
    # would change it, the path is hidden, since the changed text could name a file the policy never checked.
    browser = FakeBrowser(file_policy=Answering(True))
    browser.world.changes = [{**change, "path": "/tmp/evil\n- tab_9 x\u202e" + "p" * 5000}]
    (reported,) = state_block(browser.call(CTX, "get_page_text", {}))["state_changes"]
    assert "path" not in reported


async def test_an_async_file_policy_hides_the_path_on_the_async_class_too() -> None:
    class AsyncPolicy(BetaLocalFilePolicy):
        @override
        async def is_path_visible(self, path: str) -> bool:  # pyright: ignore[reportIncompatibleMethodOverride]
            return True

    browser = AsyncFakeBrowser(file_policy=AsyncPolicy(download_dir="/dl", expose_download_paths=True))
    browser.world.changes = [  # pyright: ignore[reportAttributeAccessIssue]
        {"type": "download_completed", "download_id": "dl_1", "url": "https://example.com/a", "path": "/dl/a"}
    ]
    (reported,) = state_block(await browser.call(CTX, "get_page_text", {}))["state_changes"]
    assert "path" not in reported


# --- refusals -------------------------------------------------------------------------------------


def test_refusals_before_dispatch_read_as_tool_errors_and_never_reach_the_driver() -> None:
    browser = FakeBrowser(configs={"navigate": {"enabled": False}})
    assert refusal(browser, CTX, "teleport", {}) == "Error: unknown browser toolset member 'teleport'"
    assert (
        refusal(browser, CTX, "navigate", {"url": "https://example.com/"})
        == "The 'navigate' action is not permitted by this application's permissions and cannot be used in this session."
    )

    # Not implemented by the fake and not configured: not available, rather than not permitted.
    assert (
        refusal(browser, CTX, "javascript_exec", {"text": "1"})
        == "The browser toolset member 'javascript_exec' is not available in this environment."
    )
    assert (
        refusal(browser, CTX, "find", {"query": "q"})
        == "The browser toolset member 'find' is not available in this environment."
    )

    # pydantic v1 and v2 word the detail differently ("field required" / "Field required").
    assert (
        refusal(browser, CTX, "wait", {}).lower() == "invalid input for browser member 'wait': duration: field required"
    )
    assert refusal(browser, CTX, "wait", {"duration": "long"}).startswith(
        "invalid input for browser member 'wait': duration:"
    )

    # every bad field is reported, not just the first
    both = refusal(browser, CTX, "scroll", {"scroll_direction": "diagonal", "target": {"type": "ref"}})
    assert "scroll_direction" in both and "target" in both
    assert browser.world.calls == []


async def _call(browser: FakeBrowser | AsyncFakeBrowser, name: str, input: dict[str, Any]) -> Any:
    result: Any = browser.call(CTX, name, input)
    return await result if inspect.isawaitable(result) else result


BOTH_CLASSES = pytest.mark.parametrize("flavour", [FakeBrowser, AsyncFakeBrowser], ids=["sync", "async"])


@BOTH_CLASSES
async def test_a_key_the_schema_does_not_declare_reaches_the_driver_and_confirm(
    flavour: type[FakeBrowser] | type[AsyncFakeBrowser],
) -> None:
    asked: list[BetaConfirmContext] = []

    def confirm(context: BetaConfirmContext) -> bool:
        asked.append(context)
        return True

    browser = flavour(confirm=confirm)
    await _call(browser, "wait", {"duration": 1, "also_run": "rm -rf /", "url": "http://10.0.0.5/"})

    received = browser.world.inputs[-1]
    assert received.duration == 1 and received.also_run == "rm -rf /" and received.url == "http://10.0.0.5/"
    assert received.to_dict()["also_run"] == "rm -rf /"

    (context,) = asked
    assert context.input is received


@pytest.mark.skipif(not PYDANTIC_V1, reason="on pydantic v2 an undeclared key cannot replace a model attribute")
@BOTH_CLASSES
async def test_an_undeclared_key_named_after_a_model_attribute_is_dropped(
    flavour: type[FakeBrowser] | type[AsyncFakeBrowser],
) -> None:
    # On pydantic v1 an undeclared key becomes an instance attribute, so `to_dict` or `copy` sent by the model would
    # replace the method on the parsed input. Those keys are dropped, and the declared field and any other key pass.
    browser = flavour()
    await _call(browser, "navigate", {"url": "https://example.com/", "to_dict": 1, "copy": 2, "note": "x"})

    received = browser.world.inputs[-1]
    assert received.url == "https://example.com/" and received.note == "x"
    assert received.to_dict()["note"] == "x" and callable(received.copy)  # both methods still work


@BOTH_CLASSES
async def test_a_tab_id_on_a_member_that_declares_none_names_no_tab(
    flavour: type[FakeBrowser] | type[AsyncFakeBrowser],
) -> None:
    asked: list[BetaConfirmContext] = []

    def confirm(context: BetaConfirmContext) -> bool:
        asked.append(context)
        return True

    browser = flavour(confirm=confirm)
    await _call(browser, "list_tabs", {})  # a report is on hand now

    for name in ("new_tab", "list_tabs"):
        active = browser.world.active
        await _call(browser, name, {"tab_id": "tab_gone"})

        # the key still reaches the driver, but it is not a tab: confirm is shown the tab the call really targets
        assert browser.world.inputs[-1].tab_id == "tab_gone"
        assert asked[-1].tab_id == active
        assert asked[-1].tab_url == browser.world.tabs[cast(str, active)]["url"]

    # a member that does declare `tab_id` names its tab, even one the report does not list
    await _call(browser, "get_page_text", {"tab_id": "tab_gone"})
    assert asked[-1].tab_id == "tab_gone" and asked[-1].tab_url is None


@BOTH_CLASSES
async def test_a_url_or_paths_on_another_member_is_not_policy_checked(
    flavour: type[FakeBrowser] | type[AsyncFakeBrowser],
) -> None:
    checked: list[str] = []

    def url_policy(_context: BetaURLContext, url: str) -> None:
        checked.append(url)
        raise ToolError("refused by the test's URL policy")

    class Recording(BetaLocalFilePolicy):
        @override
        def resolve_upload_paths(self, context: BetaURLContext, paths: Sequence[str]) -> list[str]:
            checked.extend(paths)
            raise ToolError("refused by the test's file policy")

    browser = flavour(url_policy=url_policy, file_policy=Recording())
    plain = await _call(browser, "wait", {"duration": 1})
    with_url = await _call(browser, "wait", {"duration": 1, "url": "http://10.0.0.5/"})
    await _call(browser, "new_tab", {"url": "http://10.0.0.5/"})
    await _call(browser, "left_click", {**CLICK, "paths": ["/etc/passwd"]})

    # neither policy is asked, and the extra key does not change what the model reads
    assert checked == [] and with_url == plain

    # each key reaches the driver
    _, wait_url, new_tab, click = browser.world.inputs
    assert wait_url.url == "http://10.0.0.5/" and new_tab.url == "http://10.0.0.5/"
    assert click.paths == ["/etc/passwd"]


def test_an_enabled_the_types_do_not_allow_fails_closed_if_it_gets_past_them() -> None:
    # {"enabled": "yes"} is the type checker's to catch; construction does not re-check it, and the dispatch gate
    # reads anything but True or None as off, so it can never turn a member on.
    browser = FakeBrowser(configs=cast(Any, {"screenshot": {"enabled": "yes"}}))
    assert "not permitted" in refusal(browser, CTX, "screenshot", {})

    FakeBrowser(configs={"screenshot": {"enabled": None}})  # None = the member's default
    FakeBrowser(configs={"screenshot": {}})

    # an entry that is not a mapping at all cannot be copied into the wire configs: construction raises
    with pytest.raises(TypeError):
        FakeBrowser(configs=cast(Any, {"screenshot": False}))


def test_enabling_an_unimplemented_member_is_a_configuration_error() -> None:
    # The model would be offered a member that can only ever answer "not available".
    with pytest.raises(ToolsetConfigError, match="does not implement.*javascript_exec"):
        FakeBrowser(configs={"javascript_exec": {"enabled": True}})


def test_an_execute_only_subclass_serves_every_member_and_turns_members_off_with_configs() -> None:
    # A driver that forwards every call elsewhere overrides execute and no member method: it serves them all, and
    # switches off what it does not serve through configs like any other member.
    class Forwarder(BetaAbstractBrowserToolset20260801):
        @override
        def _browser_state(self, context: BetaToolsetCallContext) -> BetaBrowserState:
            return BetaBrowserState(tabs=[])

        @override
        def execute(self, context: BetaToolsetCallContext, name: Any, input: Any) -> Any:
            return f"forwarded {name}"

    forwarder = Forwarder(
        configs={"screenshot": {"enabled": False}, "javascript_exec": {"enabled": True}}, confirm=approve
    )
    assert texts(forwarder.call(CTX, "get_page_text", {})) == ["forwarded get_page_text"]
    assert texts(forwarder.call(CTX, "javascript_exec", {"text": "1"})) == ["forwarded javascript_exec"]
    assert "not permitted" in refusal(cast(Any, forwarder), CTX, "screenshot", {})


def test_enabling_javascript_exec_or_file_upload_requires_a_confirm_callable() -> None:
    # file_upload is implemented by the fake; enabling it without a confirm callable to see its calls is refused up
    # front. A confirm that approves everything is the explicit way to run it unattended; disabled, it needs none.
    with pytest.raises(ToolsetConfigError, match="file_upload.*confirm callable"):
        FakeBrowser(configs={"file_upload": {"enabled": True}})

    FakeBrowser(configs={"file_upload": {"enabled": True}}, confirm=approve)
    FakeBrowser()

    # the fake does not serve javascript_exec, and enabling a member the driver does not serve is a different error
    class Scripted(FakeBrowser):
        @override
        def javascript_exec(self, context: BetaToolsetCallContext, input: BetaBrowserJavascriptExecInput) -> str:
            return ""

    with pytest.raises(ToolsetConfigError, match="javascript_exec.*confirm callable"):
        Scripted(configs={"javascript_exec": {"enabled": True}})
    Scripted(configs={"javascript_exec": {"enabled": True}}, confirm=approve)


def test_a_member_without_fields_takes_an_empty_object() -> None:
    assert [b["type"] for b in FakeBrowser().call(CTX, "new_tab", {})] == ["browser_state"]


# --- errors out of the driver ---------------------------------------------------------------------


def test_driver_tool_error_is_the_error_text_and_any_other_exception_is_reported_too() -> None:
    browser = FakeBrowser()
    browser.world.fail["left_click"] = ToolError("element is covered")
    assert refusal(browser, CTX, "left_click", {"target": {"type": "ref", "ref": "e1"}}) == "element is covered"
    browser.world.fail["left_click"] = TypeError("driver bug")
    assert refusal(browser, CTX, "left_click", {"target": {"type": "ref", "ref": "e1"}}) == "TypeError: driver bug"


def test_the_developer_error_class_propagates_out_of_call() -> None:
    browser = FakeBrowser()
    browser.world.fail["left_click"] = ToolsetContractError("misuse")
    with pytest.raises(ToolsetContractError):
        browser.call(CTX, "left_click", {"target": {"type": "ref", "ref": "e1"}})


def test_a_browser_state_hook_that_raises_is_a_developer_error() -> None:
    browser = FakeBrowser()
    browser.world.state_error = RuntimeError("page crashed")

    with pytest.raises(ToolsetContractError, match="browser_state raised RuntimeError"):
        browser.call(CTX, "get_page_text", {})

    # a hook that returns nothing, or a plain dict, is the same developer error, never a result for the model
    bad: list[Any] = [None, {"tabs": [], "state_changes": []}]
    for returned in bad:

        class BadState(FakeBrowser):
            @override
            def _browser_state(self, context: BetaToolsetCallContext, returned: Any = returned) -> Any:
                return returned

        with pytest.raises(ToolsetContractError, match="browser_state raised"):
            BadState().tool_result(_use("get_page_text", {}))


MALFORMED_REPORTS: list[dict[str, Any]] = [
    # built unvalidated, as pydantic v1 or `model_construct` would let them through
    {"tabs": [{"tab_id": "t", "url": "https://a.test/", "title": None, "active": True}]},
    {"tabs": [], "state_changes": ["download_started"]},
    {"tabs": [], "state_changes": [{"type": "tab_opened"}]},
]


@pytest.mark.parametrize("fields", MALFORMED_REPORTS, ids=range(len(MALFORMED_REPORTS)))
def test_a_report_missing_a_field_the_sdk_reads_is_the_drivers_contract_error_not_the_models(
    fields: dict[str, Any],
) -> None:
    browser = FakeBrowser()
    browser.world.state_override = unvalidated(BetaBrowserState, **{"state_changes": [], **fields})
    with pytest.raises(ToolsetContractError, match="browser_state"):
        browser.call(CTX, "left_click", CLICK)
    with pytest.raises(ToolsetContractError):
        browser.tool_result(_use("left_click", CLICK))
    if fields.get("state_changes"):
        # a failed call holds the state changes back for the next block, so it reads them too
        browser.world.fail["left_click"] = ToolError("element gone")
        with pytest.raises(ToolsetContractError, match="browser_state"):
            browser.call(CTX, "left_click", CLICK)


async def test_a_malformed_report_is_a_contract_error_on_the_async_class_too() -> None:
    for fields in MALFORMED_REPORTS:
        browser = AsyncFakeBrowser()
        browser.world.state_override = unvalidated(BetaBrowserState, **{"state_changes": [], **fields})
        with pytest.raises(ToolsetContractError, match="browser_state"):
            await browser.call(CTX, "get_page_text", {})

        if fields.get("state_changes"):
            # a failed call holds the state changes back for the next block, so it reads them too
            browser.world.fail["left_click"] = ToolError("element gone")
            with pytest.raises(ToolsetContractError, match="browser_state"):
                await browser.call(CTX, "left_click", CLICK)


def test_a_new_tab_result_that_is_not_a_tab_entry_still_renders_the_block() -> None:
    for returned in (None, "tab_2"):
        browser = FakeBrowser()
        browser.world.results["new_tab"] = returned
        browser.world.tabs["tab_2"] = {"title": "", "url": "about:blank"}
        browser.world.changes = [{"type": "tab_opened", "tab_id": "tab_2"}]
        (block,) = browser.call(CTX, "new_tab", {})
        assert block["type"] == "browser_state"
        assert [c["tab_id"] for c in cast(Any, block)["state_changes"]] == ["tab_2"]


def test_tool_result_maps_the_pipeline_onto_a_result_block_and_passes_the_tool_use_along() -> None:
    browser = FakeBrowser()
    use = _use("get_page_text", {})

    result = browser.tool_result(use)
    assert result["content"][0] == {"type": "text", "text": "Hello"}  # pyright: ignore[reportTypedDictNotRequiredAccess, reportIndexIssue]
    assert "is_error" not in result
    assert browser.world.contexts[-1].tool_use is use
    assert browser.world.state_contexts[-1].tool_use is use

    failed = browser.tool_result(_use("teleport", {}))
    assert failed.get("is_error") is True
    assert failed["content"] == [{"type": "text", "text": "Error: unknown browser toolset member 'teleport'"}]  # pyright: ignore[reportTypedDictNotRequiredAccess]


# --- state changes across failed calls ------------------------------------------------------------


def test_changes_drained_by_a_failed_call_ride_the_next_block_that_reaches_the_model() -> None:
    browser = FakeBrowser()
    browser.world.changes = [
        {"type": "tab_opened", "tab_id": "tab_9"},  # its tab is not in the inventory by the next call
        {"type": "download_started", "download_id": "dl_1", "url": "https://example.com/a"},
        {"type": "download_started", "download_id": "dl_2", "url": "https://example.com/b"},
    ]
    browser.world.fail["left_click"] = ToolError("nope")

    with pytest.raises(ToolError):
        browser.call(CTX, "left_click", {"target": {"type": "ref", "ref": "e1"}})

    # The failed call still consulted browser_state, so the driver's queue was drained.
    assert browser.world.changes == []

    browser.world.changes = [
        {"type": "download_completed", "download_id": "dl_2", "url": "https://example.com/b", "size_bytes": 1},
    ]

    block = state_block(browser.call(CTX, "get_page_text", {}))
    assert block["state_changes"] == [
        {"type": "download_started", "download_id": "dl_1", "url": "https://example.com/a"},
        # dl_2's held-back "started" is superseded by this report's "completed"; tab_9 is gone.
        {"type": "download_completed", "download_id": "dl_2", "url": "https://example.com/b", "size_bytes": 1},
    ]

    assert "state_changes" not in state_block(browser.call(CTX, "get_page_text", {}))


def test_of_the_changes_held_for_one_download_the_newest_is_the_one_carried_forward() -> None:
    # One failed call drains both the start and the completion of dl_1; a second failed call holds them
    # again. The block that finally reaches the model carries the completion, not the stale start.
    browser = FakeBrowser()
    browser.world.changes = [
        {"type": "download_started", "download_id": "dl_1", "url": "https://example.com/a"},
        {"type": "download_completed", "download_id": "dl_1", "url": "https://example.com/a", "size_bytes": 7},
    ]
    browser.world.fail["left_click"] = ToolError("nope")

    for _ in range(2):
        with pytest.raises(ToolError):
            browser.call(CTX, "left_click", {"target": {"type": "ref", "ref": "e1"}})

    browser.world.fail = {}
    assert state_block(browser.call(CTX, "get_page_text", {}))["state_changes"] == [
        {"type": "download_completed", "download_id": "dl_1", "url": "https://example.com/a", "size_bytes": 7},
    ]


def test_of_one_reports_changes_for_a_download_only_the_latest_reaches_the_model() -> None:
    # A driver that reports every event need not deduplicate: the block carries one change per download, the latest,
    # where that one stood.
    browser = FakeBrowser()
    browser.world.changes = [
        {"type": "download_started", "download_id": "dl_1", "url": "https://example.com/a"},
        {"type": "download_started", "download_id": "dl_2", "url": "https://example.com/b"},
        {"type": "download_completed", "download_id": "dl_1", "url": "https://example.com/a", "size_bytes": 7},
    ]
    assert state_block(browser.call(CTX, "get_page_text", {}))["state_changes"] == [
        {"type": "download_started", "download_id": "dl_2", "url": "https://example.com/b"},
        {"type": "download_completed", "download_id": "dl_1", "url": "https://example.com/a", "size_bytes": 7},
    ]


def test_a_tab_opened_for_a_tab_the_report_does_not_list_is_dropped_and_a_repeated_one_sent_once() -> None:
    browser = FakeBrowser()
    browser.world.tabs["tab_2"] = {"title": "popup", "url": "https://example.com/popup"}
    browser.world.changes = [
        {"type": "tab_opened", "tab_id": "tab_9"},  # opened and closed again within the call: not in `tabs`
        {"type": "tab_opened", "tab_id": "tab_2"},
        {"type": "tab_opened", "tab_id": "tab_2"},  # reported twice
    ]

    assert state_block(browser.call(CTX, "get_page_text", {}))["state_changes"] == [
        {"type": "tab_opened", "tab_id": "tab_2"},
    ]

    browser.world.changes = [{"type": "tab_opened", "tab_id": "tab_8"}]
    assert "state_changes" not in state_block(browser.call(CTX, "get_page_text", {}))


def test_a_held_change_and_a_replayed_one_give_way_to_the_newest_for_that_download() -> None:
    # The start of dl_1 is drained by a failed call and held; a driver that replays what the model never saw reports
    # it again next to the completion. One change for dl_1 reaches the model: the completion.
    browser = FakeBrowser()
    browser.call(CTX, "list_tabs", {})
    browser.world.changes = [{"type": "download_started", "download_id": "dl_1", "url": "https://example.com/a"}]

    browser.world.fail["get_page_text"] = ToolError("page gone")
    with pytest.raises(ToolError):
        browser.call(CTX, "get_page_text", {})  # failed; the report is still read
    del browser.world.fail["get_page_text"]

    browser.world.changes = [
        {"type": "download_started", "download_id": "dl_1", "url": "https://example.com/a"},
        {"type": "download_completed", "download_id": "dl_1", "url": "https://example.com/a", "size_bytes": 7},
    ]

    assert state_block(browser.call(CTX, "get_page_text", {}))["state_changes"] == [
        {"type": "download_completed", "download_id": "dl_1", "url": "https://example.com/a", "size_bytes": 7},
    ]


def test_a_new_tab_result_carries_only_its_own_tab_opened_and_holds_a_popups_for_the_next_block() -> None:
    # A page opened a popup (tab_2) just before the model asked for a new tab (tab_3): the API accepts
    # exactly one tab_opened on a new_tab result, so the popup's waits for the next block.
    browser = FakeBrowser()
    browser.world.tabs["tab_2"] = {"title": "popup", "url": "https://example.com/popup"}
    browser.world.changes = [{"type": "tab_opened", "tab_id": "tab_2"}]
    browser.world.next_tab = 3

    block = state_block(browser.call(CTX, "new_tab", {}))
    assert block["state_changes"] == [{"type": "tab_opened", "tab_id": "tab_3"}]
    nxt = state_block(browser.call(CTX, "get_page_text", {}))
    assert nxt["state_changes"] == [{"type": "tab_opened", "tab_id": "tab_2"}]

    # The same when the popup's tab_opened was held back from a failed call and merged into the new_tab block.
    browser.world.tabs["tab_4"] = {"title": "popup 2", "url": "https://example.com/p2"}
    browser.world.changes = [{"type": "tab_opened", "tab_id": "tab_4"}]
    browser.world.fail["left_click"] = ToolError("nope")

    with pytest.raises(ToolError):
        browser.call(CTX, "left_click", {"target": {"type": "ref", "ref": "e1"}})

    browser.world.fail.clear()
    browser.world.next_tab = 5
    block = state_block(browser.call(CTX, "new_tab", {}))
    assert block["state_changes"] == [{"type": "tab_opened", "tab_id": "tab_5"}]
    assert state_block(browser.call(CTX, "get_page_text", {}))["state_changes"] == [
        {"type": "tab_opened", "tab_id": "tab_4"}
    ]


NEW_TAB_NOT_ACTIVE = (
    "new_tab opened a tab, but the browser does not report it as the only active tab. Call list_tabs to see the tabs."
)


def test_a_new_tab_result_gets_a_tab_opened_when_the_driver_reported_none() -> None:
    browser = FakeBrowser()
    browser.world.results["new_tab"] = {"tab_id": "tab_2", "title": "", "url": "about:blank", "active": True}
    browser.world.tabs["tab_2"] = {"title": "", "url": "about:blank"}
    browser.world.active = "tab_2"
    block = state_block(browser.call(CTX, "new_tab", {}))
    assert block["state_changes"] == [{"type": "tab_opened", "tab_id": "tab_2"}]


def test_a_new_tab_whose_tab_is_not_the_active_one_fails_and_its_tab_opened_waits_for_the_next_block() -> None:
    # the driver opened tab_2 in the background, or a popup took focus before the report
    browser = FakeBrowser()
    browser.world.results["new_tab"] = {"tab_id": "tab_2", "title": "", "url": "about:blank", "active": False}
    browser.world.tabs["tab_2"] = {"title": "", "url": "about:blank"}
    browser.world.changes = [{"type": "tab_opened", "tab_id": "tab_2"}]
    assert refusal(browser, CTX, "new_tab", {}) == NEW_TAB_NOT_ACTIVE
    assert state_block(browser.call(CTX, "get_page_text", {}))["state_changes"] == [
        {"type": "tab_opened", "tab_id": "tab_2"}
    ]


async def test_an_async_new_tab_whose_tab_is_not_the_active_one_fails_too() -> None:
    browser = AsyncFakeBrowser()
    browser.world.results["new_tab"] = {"tab_id": "tab_2", "title": "", "url": "about:blank", "active": False}
    browser.world.tabs["tab_2"] = {"title": "", "url": "about:blank"}
    with pytest.raises(ToolError) as caught:
        await browser.call(CTX, "new_tab", {})
    assert texts(caught.value.content) == [NEW_TAB_NOT_ACTIVE]


def test_navigate_and_screenshot_results_render_from_their_models() -> None:
    browser = FakeBrowser()

    browser.world.results["navigate"] = BetaBrowserNavigateResult(url="https://example.com/a", title="A", status=200)
    assert texts(browser.call(CTX, "navigate", {"url": "https://example.com"}))[0] == (
        "Navigated to https://example.com/a — A (HTTP 200)"
    )

    browser.world.results["screenshot"] = BetaScreenshotResult(data="QUJD")
    image = cast(dict[str, Any], browser.call(CTX, "screenshot", {})[0])
    assert image["type"] == "image" and image["source"] == {"type": "base64", "media_type": "image/png", "data": "QUJD"}


@BOTH_CLASSES
@pytest.mark.parametrize(("tool", "given"), [("navigate", {"url": "https://example.com"}), ("screenshot", {})])
async def test_a_bare_string_from_navigate_or_screenshot_reaches_the_model_as_an_error_naming_its_type(
    flavour: type[FakeBrowser] | type[AsyncFakeBrowser], tool: str, given: dict[str, Any]
) -> None:
    # a bare string is not a result model: the call fails, and the model reads an error that names what the driver
    # returned, not one that blames the browser_state report
    browser = flavour()
    browser.world.results[tool] = "https://example.com/c" if tool == "navigate" else "QUJD"
    failed: Any = browser.tool_result(_use(tool, given))
    if inspect.isawaitable(failed):
        failed = await failed
    assert failed.get("is_error") is True
    assert failed.get("content") == f"ValueError('{tool} returned str, not its result model')"


def test_a_dismissed_dialog_is_a_line_of_text_with_its_message_capped() -> None:
    # A driver reports a native dialog it dismissed as a BetaDialogDismissed change; the model reads one line per dialog
    # with the next result that can carry text (a click's, an error's, or after a tab member the one after), the
    # page-supplied message capped, and never in the browser_state block.
    browser = FakeBrowser()
    browser.world.changes = [BetaDialogDismissed(kind="confirm", message="Delete\neverything?")]
    content = browser.call(CTX, "left_click", CLICK)
    assert texts(content) == ["Clicked.", 'A confirm dialog "Delete everything?" was dismissed.']
    assert "state_changes" not in state_block(content)

    browser.world.changes = [BetaDialogDismissed(kind="alert", message="x" * 500), BetaDialogDismissed(kind="prompt")]
    browser.world.fail["left_click"] = ToolError("element gone")
    lines = texts(pytest.raises(ToolError, browser.call, CTX, "left_click", CLICK).value.content)
    assert lines == ["element gone", f'An alert dialog "{"x" * 200}…" was dismissed.', "A prompt dialog was dismissed."]
    browser.world.fail.clear()

    # a blank or control-only kind reads as none; a long one is capped at a word's length (it lands unquoted)
    browser.world.changes = [BetaDialogDismissed(kind="\n"), BetaDialogDismissed(kind="y" * 50)]
    assert texts(browser.call(CTX, "left_click", CLICK))[1:] == [
        "A dialog was dismissed.",
        f"A {'y' * 20} dialog was dismissed.",
    ]

    # A tab member cannot carry text, so the dialogs are held; the cap applies when the lines are finally written.
    browser.world.changes = [BetaDialogDismissed(kind="confirm", message=str(i)) for i in range(2)]
    assert [b["type"] for b in browser.call(CTX, "list_tabs", {})] == ["browser_state"]
    browser.world.changes = [BetaDialogDismissed(kind="confirm", message=str(i)) for i in range(2, 5)]
    assert texts(browser.call(CTX, "get_page_text", {}))[1:] == [
        'A confirm dialog "0" was dismissed.',
        'A confirm dialog "1" was dismissed.',
        'A confirm dialog "2" was dismissed.',
        "2 more dialogs were dismissed.",
    ]

    browser.world.changes = [BetaDialogDismissed(kind="confirm", message="Löschen?")]
    assert texts(browser.call(CTX, "get_page_text", {}))[1:] == ['A confirm dialog "Löschen?" was dismissed.']


def _text_cases() -> list[tuple[str, str, str]]:
    """`text_cases.json`, the table both SDKs' tests read for the text folds: `{c*N}` stands for N copies of the
    character c, and where the SDKs differ on purpose a row gives `{"py", "ts"}`."""
    rows: list[dict[str, Any]] = json.loads((Path(__file__).parent / "text_cases.json").read_text())

    def expand(text: str) -> str:
        return re.sub(r"\{(.)\*(\d+)\}", lambda m: m.group(1) * int(m.group(2)), text)

    return [
        (r["fn"], expand(r["input"]), expand(r["shown"] if isinstance(r["shown"], str) else r["shown"]["py"]))
        for r in rows
    ]


TEXT_CASES = _text_cases()


@pytest.mark.parametrize("fn, raw, shown", TEXT_CASES, ids=range(len(TEXT_CASES)))
def test_page_and_model_text_is_folded_the_same_in_both_sdks(fn: str, raw: str, shown: str) -> None:
    assert {"one_line": one_line, "quoted_name": quoted_name}[fn](raw) == shown


def test_a_reported_url_is_folded_to_one_line_and_cut_to_the_field_limit_and_nothing_else() -> None:
    # A tab's or download's address is page-supplied: line breaks, controls and bidi characters are folded to a space,
    # the ends trimmed and the whole held to 4,096 characters. Nothing else is parsed or re-encoded.
    long_url = "https://evil.test/" + "(" * 5000
    assert bounded_tab_url(long_url) == "\u2026" + long_url[:4095]
    fits = "https://x.test/" + "a" * (4096 - len("https://x.test/"))
    assert bounded_tab_url(fits) == fits  # exactly at the limit: untouched
    assert bounded_tab_url(fits + "b") == "\u2026" + fits[:4095]
    assert bounded_tab_url("https://exa\nmple.test/a b)\x0bc\u202e\u2028d\t") == "https://exa mple.test/a b) c d"
    assert (
        bounded_tab_url("https://user:secret@example.com:8443/p?to=a@b#c")
        == "https://user:secret@example.com:8443/p?to=a@b#c"
    )
    assert (
        bounded_tab_url("https://evil.test/h\udc00") == "https://evil.test/h\ufffd"
    )  # a lone surrogate could not be sent

    browser = FakeBrowser()
    browser.world.tabs["tab_1"] = {"title": "x", "url": long_url}
    browser.world.tabs["tab_2"] = {"title": "ok", "url": "https://example.com/p-a_th~!$&'*+,;=:@%20x?q=1&r[]=2#frag"}
    browser.world.tabs["tab_3"] = {"title": "raw", "url": " https://example.com/pfad-\u00fc?q=\u00e9 \nnext"}
    browser.world.changes = [
        {"type": "download_started", "download_id": "dl_1", "url": "https://example.com/" + "a" * 5000},
        {"type": "download_started", "download_id": "dl_2", "url": "data:text/csv,a b\x0bc\n"},
    ]

    block = state_block(browser.call(CTX, "get_page_text", {}))
    tabs = {t["tab_id"]: t["url"] for t in block["tabs"]}
    assert tabs == {
        "tab_1": "\u2026" + long_url[:4095],
        "tab_2": "https://example.com/p-a_th~!$&'*+,;=:@%20x?q=1&r[]=2#frag",
        "tab_3": "https://example.com/pfad-\u00fc?q=\u00e9  next",
    }
    assert [c["url"] for c in block["state_changes"]] == [
        "\u2026" + ("https://example.com/" + "a" * 5000)[:4095],
        "data:text/csv,a b c",
    ]

    # a failed download's error and a tab's title are page-chosen too: folded and bounded like the URL beside them
    error = "net::ERR\nX\u202e" + "e" * 5000
    browser.world.changes = [
        {"type": "download_failed", "download_id": "dl_3", "url": "https://example.com/f", "error": error}
    ]
    browser.world.tabs = {
        "tab_1": {
            "title": "Inbox\n- tab_9 Admin (https://evil.test/)\u2029" + "t" * 5000,
            "url": "https://example.com/",
        }
    }

    block = state_block(browser.call(CTX, "get_page_text", {}))
    [change] = block["state_changes"]
    assert change["error"] == ("net::ERR X " + "e" * 5000)[:4096]
    assert block["tabs"][0]["title"] == ("Inbox - tab_9 Admin (https://evil.test/) " + "t" * 5000)[:4096]


def test_a_refused_navigation_is_one_line_of_text_never_the_url() -> None:
    browser = FakeBrowser()
    browser.world.changes = [BetaNavigationRefused()]
    content = browser.call(CTX, "get_page_text", {})
    assert texts(content) == ["Hello", "A navigation was refused."]
    assert "state_changes" not in state_block(content)

    # On a failed call it is appended to the error, since it is often why the member failed.
    browser.world.changes = [BetaNavigationRefused(), BetaNavigationRefused()]
    browser.world.fail["left_click"] = ToolError("navigation aborted")
    assert texts(
        pytest.raises(ToolError, browser.call, CTX, "left_click", {"target": {"type": "ref", "ref": "e"}}).value.content
    ) == ["navigation aborted", "A navigation was refused."]

    # A tab member cannot carry text, so the line waits for the next result that can.
    browser.world.fail.clear()
    browser.world.changes = [BetaNavigationRefused()]
    assert [b["type"] for b in browser.call(CTX, "list_tabs", {})] == ["browser_state"]
    assert texts(browser.call(CTX, "get_page_text", {})) == ["Hello", "A navigation was refused."]
    assert texts(browser.call(CTX, "get_page_text", {})) == ["Hello"]


# --- hooks ----------------------------------------------------------------------------------------


def test_an_async_browser_state_on_the_sync_class_is_a_contract_error() -> None:
    class AsyncState(FakeBrowser):
        @override
        async def _browser_state(self, context: BetaToolsetCallContext) -> BetaBrowserState:  # pyright: ignore[reportIncompatibleMethodOverride]
            return self.world.state(context)

    with pytest.raises(ToolsetContractError, match="_browser_state is async on the synchronous toolset"):
        AsyncState()


# --- execute as the before/after hook -------------------------------------------------------------


def test_an_execute_override_wraps_dispatch_and_the_pipeline_wraps_the_override() -> None:
    seen: list[Any] = []

    class Hooked(FakeBrowser):
        @override
        def execute(self, context: BetaToolsetCallContext, name: Any, input: Any) -> Any:
            seen.append((name, type(input).__name__))
            result = super().execute(context, name, input)
            if name == "get_page_text":
                return cast(str, result).upper()
            return result

    browser = Hooked()
    assert texts(browser.call(CTX, "get_page_text", {})) == ["HELLO"]
    assert seen == [("get_page_text", "BetaBrowserGetPageTextInput")]

    # A call refused before dispatch never reaches the override.
    with pytest.raises(ToolError):
        browser.call(CTX, "teleport", {})
    assert len(seen) == 1


def test_an_async_execute_override_on_the_sync_class_is_a_contract_error() -> None:
    # reported when the toolset is built: never a coroutine rendered as a result, nor an is_error the model reads
    class AsyncExecute(FakeBrowser):
        @override
        async def execute(self, context: BetaToolsetCallContext, name: Any, input: Any) -> Any:  # pyright: ignore[reportIncompatibleMethodOverride]
            return "never awaited"

    with pytest.raises(ToolsetContractError, match="execute is async on the synchronous toolset"):
        AsyncExecute()


async def test_a_plain_execute_override_on_the_async_class_is_a_contract_error() -> None:
    class SyncExecute(AsyncFakeBrowser):
        @override
        def execute(self, context: BetaToolsetCallContext, name: Any, input: Any) -> Any:
            return "plain"

    with pytest.raises(ToolsetContractError, match="execute is sync on the asynchronous toolset"):
        SyncExecute()


# --- serialization --------------------------------------------------------------------------------


def test_calls_run_one_at_a_time() -> None:
    def max_overlap(browser: FakeBrowser) -> int:
        inside = 0
        peak = 0
        gate = threading.Lock()

        class Slow(World):
            @override
            def get_page_text(self, context: BetaToolsetCallContext, input: Any) -> str:
                nonlocal inside, peak
                with gate:
                    inside += 1
                    peak = max(peak, inside)
                threading.Event().wait(0.05)
                with gate:
                    inside -= 1
                return "t"

        browser.world.__class__ = Slow
        threads = [threading.Thread(target=browser.call, args=(CTX, "get_page_text", {})) for _ in range(4)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        return peak

    assert max_overlap(FakeBrowser()) == 1


def test_call_from_inside_a_member_is_a_contract_error_not_a_deadlock() -> None:
    # call() is the tool runner's entry point; a member that composes other members calls their methods directly.
    class Nested(FakeBrowser):
        @override
        def get_page_text(self, context: BetaToolsetCallContext, input: Any) -> str:
            self.call(context, "list_tabs", {})
            return "unreachable"

    with pytest.raises(ToolsetContractError, match="from inside a member"):
        Nested().call(CTX, "get_page_text", {})


# --- async parity ---------------------------------------------------------------------------------


async def test_async_pipeline_parity() -> None:
    browser = AsyncFakeBrowser()
    content = await browser.call(CTX, "navigate", {"url": "https://example.com/"})
    assert texts(content) == ["Navigated to https://example.com/ — Title of https://example.com/ (HTTP 200)"]
    assert state_block(content)["tabs"][0]["url"] == "https://example.com/"

    # the async class reads the report through the same bound
    browser.world.tabs["tab_1"]["url"] = "https://u:p@example.com/\n" + "a" * 5000
    bounded = state_block(await browser.call(CTX, "get_page_text", {}))["tabs"][0]["url"]
    assert bounded == "\u2026" + ("https://u:p@example.com/ " + "a" * 5000)[:4095]

    assert [b["type"] for b in await browser.call(CTX, "new_tab", {})] == ["browser_state"]

    with pytest.raises(ToolError, match="not available"):
        await browser.call(CTX, "javascript_exec", {"text": "1"})

    browser.world.fail["left_click"] = ValueError("bad")
    result = await browser.tool_result(_use("left_click", {"target": {"type": "ref", "ref": "e"}}))
    assert result.get("is_error") is True and result["content"] == [{"type": "text", "text": "ValueError: bad"}]  # pyright: ignore[reportTypedDictNotRequiredAccess]

    browser.world.state_error = RuntimeError("gone")
    with pytest.raises(ToolsetContractError):
        await browser.call(CTX, "get_page_text", {})

    bad: list[Any] = [None, {"tabs": [], "state_changes": []}]
    for returned in bad:

        class BadState(AsyncFakeBrowser):
            @override
            async def _browser_state(self, context: BetaToolsetCallContext, returned: Any = returned) -> Any:
                return returned

        with pytest.raises(ToolsetContractError, match="browser_state raised"):
            await BadState().tool_result(_use("get_page_text", {}))


async def test_a_sync_member_or_browser_state_on_the_async_class_is_a_contract_error() -> None:
    # The async class awaits its members and _browser_state; a plain def would run blocking browser I/O on the event
    # loop, so it is refused as the wiring mistake it is, as an async member is on the sync class.
    class SyncMember(AsyncFakeBrowser):
        @override
        def get_page_text(self, context: BetaToolsetCallContext, input: Any) -> str:  # pyright: ignore[reportIncompatibleMethodOverride]
            return "sync body"

    with pytest.raises(ToolsetContractError, match="'get_page_text' is sync on the asynchronous toolset"):
        SyncMember()

    class SyncState(AsyncFakeBrowser):
        @override
        def _browser_state(self, context: BetaToolsetCallContext) -> BetaBrowserState:  # pyright: ignore[reportIncompatibleMethodOverride]
            return self.world.state(context)

    with pytest.raises(ToolsetContractError, match="_browser_state is sync on the asynchronous toolset"):
        SyncState()


async def test_async_call_from_inside_a_member_is_a_contract_error_and_cancellation_releases_the_lock() -> None:
    class Nested(AsyncFakeBrowser):
        @override
        async def get_page_text(self, context: BetaToolsetCallContext, input: Any) -> str:
            await self.call(context, "list_tabs", {})
            return "unreachable"

        @override
        async def wait(self, context: BetaToolsetCallContext, input: Any) -> None:
            await anyio.sleep(10)

    browser = Nested()
    with pytest.raises(ToolsetContractError, match="from inside a member"):
        await browser.call(CTX, "get_page_text", {})

    with anyio.move_on_after(0.05) as scope:
        await browser.call(CTX, "wait", {"duration": 10})
    assert scope.cancelled_caught
    # The lock was released by the cancelled call, so the next one runs.
    with anyio.fail_after(1):
        assert [b["type"] for b in await browser.call(CTX, "list_tabs", {})] == ["browser_state"]


def test_driver_values_are_validated_where_the_driver_builds_them_and_forwarded_as_built() -> None:
    # BetaBrowserState and the result models are real pydantic models: a report that breaks their field types fails in
    # the driver, where it is built. What a driver did build reaches the block as it is — keys the SDK does not know
    # included — because the SDK's own copies (the judged state, the contexts) are made without re-validating.
    with pytest.raises(pydantic.ValidationError):
        BetaBrowserState(tabs=cast(Any, "tab_1"))

    browser = FakeBrowser()
    tab: Any = {"tab_id": "tab_1", "title": "T", "url": "https://example.com/", "active": True, "surprise": ["x"]}
    change: Any = {
        "type": "download_completed",
        "download_id": "d1",
        "url": "https://example.com/f",
        "filename": "f",
        "sha256": "abc",
    }

    browser.world.state_override = BetaBrowserState(tabs=[tab], state_changes=[change])
    block = state_block(browser.call(CTX, "get_page_text", {}))
    assert block["tabs"] == [tab] and block["state_changes"] == [change]


def test_a_closed_toolset_answers_no_member_call() -> None:
    browser = FakeBrowser()
    browser.call(CTX, "get_page_text", {})
    browser.close()
    with pytest.raises(ToolsetClosedError):
        browser.call(CTX, "get_page_text", {})
    assert browser.world.calls == ["get_page_text"]


async def test_a_closed_async_toolset_answers_no_member_call() -> None:
    browser = AsyncFakeBrowser()
    await browser.close()
    with pytest.raises(ToolsetClosedError):
        await browser.call(CTX, "get_page_text", {})
    assert browser.world.calls == []


def test_close_waits_for_accepted_calls_to_settle() -> None:
    # close() marks the toolset closed at once (a call that arrives later is refused) and then waits for the calls
    # already accepted — the one in flight and the one queued behind it — so an override that calls super().close()
    # first tears the browser down with nothing still using it.
    entered, release = threading.Event(), threading.Event()
    events: list[str] = []

    class Slow(FakeBrowser):
        @override
        def get_page_text(self, context: BetaToolsetCallContext, input: Any) -> str:
            entered.set()
            release.wait(5)
            return "text"

    browser = Slow()

    first = threading.Thread(target=lambda: (browser.call(CTX, "get_page_text", {}), events.append("first done")))
    first.start()
    assert entered.wait(5)

    queued = threading.Thread(target=lambda: (browser.call(CTX, "get_page_text", {}), events.append("queued done")))
    queued.start()

    closer = threading.Thread(target=lambda: (browser.close(), events.append("closed")))
    closer.start()
    closer.join(0.2)
    assert closer.is_alive()  # still waiting: a call is in flight and another is queued

    with pytest.raises(ToolsetClosedError):
        browser.call(CTX, "get_page_text", {})  # arrives after close(): refused, never queued

    release.set()
    for thread in (first, queued, closer):
        thread.join(5)
    assert sorted(events[:2]) == ["first done", "queued done"] and events[2] == "closed"


def test_close_from_inside_a_member_does_not_wait_for_itself() -> None:
    class ClosesItself(FakeBrowser):
        @override
        def get_page_text(self, context: BetaToolsetCallContext, input: Any) -> str:
            self.close()
            return "closing"

    browser = ClosesItself()
    assert "closing" in texts(browser.call(CTX, "get_page_text", {}))[0]
    with pytest.raises(ToolsetClosedError):
        browser.call(CTX, "get_page_text", {})


async def test_async_close_waits_for_accepted_calls_to_settle() -> None:
    entered, release = anyio.Event(), anyio.Event()
    events: list[str] = []

    class Slow(AsyncFakeBrowser):
        @override
        async def get_page_text(self, context: BetaToolsetCallContext, input: Any) -> str:
            entered.set()
            await release.wait()
            return "text"

    browser = Slow()

    async def member(label: str) -> None:
        await browser.call(CTX, "get_page_text", {})
        events.append(label)

    async def closer() -> None:
        await browser.close()
        events.append("closed")

    async with anyio.create_task_group() as tasks:
        tasks.start_soon(member, "first done")
        await entered.wait()

        tasks.start_soon(member, "queued done")
        await anyio.wait_all_tasks_blocked()

        tasks.start_soon(closer)
        await anyio.wait_all_tasks_blocked()
        assert "closed" not in events  # still waiting

        with pytest.raises(ToolsetClosedError):
            await browser.call(CTX, "get_page_text", {})

        release.set()

    assert sorted(events[:2]) == ["first done", "queued done"] and events[2] == "closed"


async def test_async_close_from_inside_a_member_does_not_wait_for_itself() -> None:
    class ClosesItself(AsyncFakeBrowser):
        @override
        async def get_page_text(self, context: BetaToolsetCallContext, input: Any) -> str:
            await self.close()
            return "closing"

    browser = ClosesItself()
    assert "closing" in texts(await browser.call(CTX, "get_page_text", {}))[0]
    with pytest.raises(ToolsetClosedError):
        await browser.call(CTX, "get_page_text", {})


# --- the same behaviours on the async class ---------------------------------------------------------


async def test_changes_drained_by_a_failed_call_ride_the_next_block_on_the_async_class() -> None:
    browser = AsyncFakeBrowser()
    browser.world.changes = [
        {"type": "tab_opened", "tab_id": "tab_9"},  # its tab is not in the inventory by the next call
        {"type": "download_started", "download_id": "dl_1", "url": "https://example.com/a"},
        {"type": "download_started", "download_id": "dl_2", "url": "https://example.com/b"},
    ]
    browser.world.fail["left_click"] = ToolError("nope")

    with pytest.raises(ToolError):
        await browser.call(CTX, "left_click", {"target": {"type": "ref", "ref": "e1"}})

    # The failed call still consulted browser_state, so the driver's queue was drained.
    assert browser.world.changes == []
    browser.world.changes = [
        {"type": "download_completed", "download_id": "dl_2", "url": "https://example.com/b", "size_bytes": 1},
    ]

    block = state_block(await browser.call(CTX, "get_page_text", {}))
    assert block["state_changes"] == [
        {"type": "download_started", "download_id": "dl_1", "url": "https://example.com/a"},
        # dl_2's held-back "started" is superseded by this report's "completed"; tab_9 is gone.
        {"type": "download_completed", "download_id": "dl_2", "url": "https://example.com/b", "size_bytes": 1},
    ]
    assert "state_changes" not in state_block(await browser.call(CTX, "get_page_text", {}))


async def test_an_execute_override_wraps_dispatch_on_the_async_class() -> None:
    seen: list[Any] = []

    class Hooked(AsyncFakeBrowser):
        @override
        async def execute(self, context: BetaToolsetCallContext, name: Any, input: Any) -> Any:
            seen.append((name, type(input).__name__))
            result = await super().execute(context, name, input)
            if name == "get_page_text":
                return cast(str, result).upper()
            return result

    browser = Hooked()
    assert texts(await browser.call(CTX, "get_page_text", {})) == ["HELLO"]
    assert seen == [("get_page_text", "BetaBrowserGetPageTextInput")]

    # A call refused before dispatch never reaches the override.
    with pytest.raises(ToolError):
        await browser.call(CTX, "teleport", {})
    assert len(seen) == 1


async def test_async_calls_run_one_at_a_time() -> None:
    inside = 0
    peak = 0

    class Slow(AsyncFakeBrowser):
        @override
        async def get_page_text(self, context: BetaToolsetCallContext, input: Any) -> str:
            nonlocal inside, peak
            inside += 1
            peak = max(peak, inside)
            await anyio.sleep(0.05)
            inside -= 1
            return "t"

    browser = Slow()

    async def read_page() -> None:
        await browser.call(CTX, "get_page_text", {})

    async with anyio.create_task_group() as tasks:
        for _ in range(4):
            tasks.start_soon(read_page)

    assert peak == 1


async def test_download_paths_stay_hidden_on_the_async_class_without_a_file_policy() -> None:
    browser = AsyncFakeBrowser()
    browser.world.changes = [  # pyright: ignore[reportAttributeAccessIssue]
        {"type": "download_started", "download_id": "dl_1", "url": "https://example.com/a.pdf", "path": "/tmp/a"},
        {
            "type": "download_completed",
            "download_id": "dl_2",
            "url": "https://example.com/b.pdf",
            "path": "/tmp/b",
            "size_bytes": 3,
        },
        {"type": "download_failed", "download_id": "dl_3", "url": "https://example.com/c.pdf", "path": "/tmp/c"},
    ]

    block = state_block(await browser.call(CTX, "get_page_text", {}))
    # a path is dropped from whichever download change carries it, not only the completed one
    assert block["state_changes"] == [
        {"type": "download_started", "download_id": "dl_1", "url": "https://example.com/a.pdf"},
        {"type": "download_completed", "download_id": "dl_2", "url": "https://example.com/b.pdf", "size_bytes": 3},
        {"type": "download_failed", "download_id": "dl_3", "url": "https://example.com/c.pdf"},
    ]

    # Nothing to report is an absent field, never an empty list.
    assert "state_changes" not in state_block(await browser.call(CTX, "get_page_text", {}))


async def test_a_download_path_is_exposed_on_the_async_class_only_when_the_file_policy_answers_true() -> None:
    change: BetaBrowserStateChangeDownloadCompletedParam = {
        "type": "download_completed",
        "download_id": "dl_1",
        "url": "https://example.com/a",
        "size_bytes": 1,
    }

    class Answering:
        def __init__(self, answer: object) -> None:
            self.answer = answer

        def resolve_upload_paths(self, context: object, paths: object) -> list[str]:
            return []

        def resolve_upload_documents(self, context: object, document_ids: object) -> list[str]:
            return []

        def is_path_visible(self, path: str) -> bool:
            return self.answer  # pyright: ignore[reportReturnType]

    class Truthy:
        def __bool__(self) -> bool:
            return True

    for answer, exposed in [(True, True), (False, False)]:
        browser = AsyncFakeBrowser(file_policy=Answering(answer))
        browser.world.changes = [{**change, "path": "/tmp/a"}]
        (reported,) = state_block(await browser.call(CTX, "get_page_text", {}))["state_changes"]
        assert ("path" in reported) is exposed

    # any other answer hides it, even a truthy one
    for answer in (Truthy(), 1, None):
        browser = AsyncFakeBrowser(file_policy=Answering(answer))
        browser.world.changes = [{**change, "path": "/tmp/a"}]
        assert state_block(await browser.call(CTX, "get_page_text", {}))["state_changes"] == [change]

    # a policy that raises on a path fails closed: the path is hidden and the change still reaches the model
    class Raising(Answering):
        @override
        def is_path_visible(self, path: str) -> bool:
            raise RuntimeError(path)

    browser = AsyncFakeBrowser(file_policy=Raising(True))
    browser.world.changes = [{**change, "path": "/tmp/a"}]
    assert state_block(await browser.call(CTX, "get_page_text", {}))["state_changes"] == [change]

    # A server picks a download's file name (its Content-Disposition). If folding the path to one line or cutting it
    # would change it, the path is hidden, since the changed text could name a file the policy never checked.
    browser = AsyncFakeBrowser(file_policy=Answering(True))
    browser.world.changes = [{**change, "path": "/tmp/evil\n- tab_9 x\u202e" + "p" * 5000}]
    (reported,) = state_block(await browser.call(CTX, "get_page_text", {}))["state_changes"]
    assert "path" not in reported


async def test_a_dismissed_dialog_is_a_line_of_text_on_the_async_class() -> None:
    browser = AsyncFakeBrowser()
    browser.world.changes = [BetaDialogDismissed(kind="confirm", message="Delete\neverything?")]
    content = await browser.call(CTX, "left_click", CLICK)
    assert texts(content) == ["Clicked.", 'A confirm dialog "Delete everything?" was dismissed.']
    assert "state_changes" not in state_block(content)

    browser.world.changes = [BetaDialogDismissed(kind="alert", message="x" * 500), BetaDialogDismissed(kind="prompt")]
    browser.world.fail["left_click"] = ToolError("element gone")
    with pytest.raises(ToolError) as caught:
        await browser.call(CTX, "left_click", CLICK)
    assert texts(caught.value.content) == [
        "element gone",
        f'An alert dialog "{"x" * 200}…" was dismissed.',
        "A prompt dialog was dismissed.",
    ]
    browser.world.fail.clear()

    # A tab member cannot carry text, so the dialogs are held; the cap applies when the lines are finally written.
    browser.world.changes = [BetaDialogDismissed(kind="confirm", message=str(i)) for i in range(2)]
    assert [b["type"] for b in await browser.call(CTX, "list_tabs", {})] == ["browser_state"]
    browser.world.changes = [BetaDialogDismissed(kind="confirm", message=str(i)) for i in range(2, 5)]
    assert texts(await browser.call(CTX, "get_page_text", {}))[1:] == [
        'A confirm dialog "0" was dismissed.',
        'A confirm dialog "1" was dismissed.',
        'A confirm dialog "2" was dismissed.',
        "2 more dialogs were dismissed.",
    ]


async def test_a_refused_navigation_is_one_line_of_text_on_the_async_class() -> None:
    browser = AsyncFakeBrowser()
    browser.world.changes = [BetaNavigationRefused()]
    content = await browser.call(CTX, "get_page_text", {})
    assert texts(content) == ["Hello", "A navigation was refused."]
    assert "state_changes" not in state_block(content)

    # On a failed call it is appended to the error, since it is often why the member failed.
    browser.world.changes = [BetaNavigationRefused(), BetaNavigationRefused()]
    browser.world.fail["left_click"] = ToolError("navigation aborted")
    with pytest.raises(ToolError) as caught:
        await browser.call(CTX, "left_click", {"target": {"type": "ref", "ref": "e"}})
    assert texts(caught.value.content) == ["navigation aborted", "A navigation was refused."]

    # A tab member cannot carry text, so the line waits for the next result that can.
    browser.world.fail.clear()
    browser.world.changes = [BetaNavigationRefused()]
    assert [b["type"] for b in await browser.call(CTX, "list_tabs", {})] == ["browser_state"]
    assert texts(await browser.call(CTX, "get_page_text", {})) == ["Hello", "A navigation was refused."]
    assert texts(await browser.call(CTX, "get_page_text", {})) == ["Hello"]


async def test_driver_values_reach_the_block_as_built_on_the_async_class() -> None:
    browser = AsyncFakeBrowser()
    tab: Any = {"tab_id": "tab_1", "title": "T", "url": "https://example.com/", "active": True, "surprise": ["x"]}
    change: Any = {
        "type": "download_completed",
        "download_id": "d1",
        "url": "https://example.com/f",
        "filename": "f",
        "sha256": "abc",
    }

    browser.world.state_override = BetaBrowserState(tabs=[tab], state_changes=[change])
    block = state_block(await browser.call(CTX, "get_page_text", {}))
    assert block["tabs"] == [tab] and block["state_changes"] == [change]
