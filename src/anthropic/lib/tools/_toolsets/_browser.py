"""The browser toolset interface: `BetaAbstractBrowserToolset20260801` and its async twin.

A driver subclasses one of them and overrides the members its backend supports. A member it does
not override is reported to the API as disabled and, if the model calls it anyway, answered with an
`is_error` result. `execute` is the dispatch layer: override it (calling `super().execute`)
for before/after hooks around every member. `call` runs the SDK's pipeline around it.
"""

from __future__ import annotations

import copy
import inspect
from abc import abstractmethod
from typing import Any, cast
from collections.abc import Mapping
from typing_extensions import override

import anyio.to_thread

from ._base import (
    BaseToolset,
    BaseSyncToolset,
    BaseAsyncToolset,
    BaseToolsetOptions,
    BetaScreenshotResult,
    parse_input,
    bounded_error,
    check_sync_hook,
)
from ._hooks import (
    BetaURLPolicy,
    BetaFilePolicy,
    BetaURLContext,
    BetaToolConfigs,
    BetaAsyncURLPolicy,
    BetaConfirmCallable,
    BetaAsyncConfirmCallable,
)
from ._errors import ToolsetUsageError, ToolsetConfigError, ToolsetContractError, UnavailableMemberError
from ._inputs import BROWSER_MEMBER_NAMES, BetaBrowserMemberName
from ._results import BetaBrowserState, BetaBrowserMemberResult, BetaBrowserNavigateResult
from ...._types import NOT_GIVEN, NotGiven
from ...._utils import is_given
from ._pipeline import (
    CallRecord,
    PipelineState,
    url_context,
    navigate_url,
    bounded_result,
    policy_outcome,
    confirm_context,
    resolve_upload_paths,
    with_bounded_tab_urls,
)
from ._registry import FAMILY, BROWSER, TOOLSET_TYPE, CONFIRM_REQUIRED
from ._runnable import BetaToolsetContent, BetaToolsetCallContext, classify
from ....types.beta import (
    BetaBrowserKeyInput,
    BetaBrowserFindInput,
    BetaBrowserTypeInput,
    BetaBrowserWaitInput,
    BetaBrowserZoomInput,
    BetaBrowserHoverInput,
    BetaBrowserMemberInput,
    BetaBrowserNewTabInput,
    BetaBrowserScrollInput,
    BetaBrowserHoldKeyInput,
    BetaBrowserCloseTabInput,
    BetaBrowserListTabsInput,
    BetaBrowserNavigateInput,
    BetaBrowserReadPageInput,
    BetaBrowserScrollToInput,
    BetaBrowserFormInputInput,
    BetaBrowserLeftClickInput,
    BetaBrowserMouseMoveInput,
    BetaBrowserSwitchTabInput,
    BetaBrowserFileUploadInput,
    BetaBrowserRightClickInput,
    BetaBrowserScreenshotInput,
    BetaBrowserDoubleClickInput,
    BetaBrowserGetPageTextInput,
    BetaBrowserLeftMouseUpInput,
    BetaBrowserMiddleClickInput,
    BetaBrowserReadConsoleInput,
    BetaBrowserReadNetworkInput,
    BetaBrowserTripleClickInput,
    BetaBrowserLeftClickDragInput,
    BetaBrowserLeftMouseDownInput,
    BetaBrowserStateTabEntryParam,
    BetaBrowserJavascriptExecInput,
    BetaBrowserToolsetConfigsParam,
    BetaBrowserToolset20260801Param,
)
from .._beta_functions import ToolError

__all__ = ["BetaAbstractBrowserToolset20260801", "BetaAsyncAbstractBrowserToolset20260801"]


class BrowserStateError(ToolsetContractError):
    """`_browser_state` raised or returned something that is not a `BetaBrowserState`: the driver's bug, not the model's."""

    def __init__(self, exc: Exception) -> None:
        super().__init__(
            f"_browser_state raised {exc!r} or returned no BetaBrowserState; return one, and catch failures inside the hook"
        )


class BrowserOptions(
    BaseToolsetOptions[BetaBrowserMemberName, BetaBrowserMemberInput, BetaConfirmCallable | BetaAsyncConfirmCallable]
):
    """The constructor options of browser toolset class `cls`, validated and resolved once at construction. A mistake
    in them raises `ToolsetConfigError` here, and a member or hook written for the other flavour (`async def` on the
    synchronous class, a plain `def` member on the asynchronous one) raises `ToolsetContractError`. Beyond what every
    family has (`BaseToolsetOptions`): `url_policy` is what the caller passed, or `NOT_GIVEN` when `navigate` is
    not checked, and `file_policy` the caller's, if any."""

    def __init__(
        self,
        cls: type[BaseToolset[Any, Any, Any]],
        *,
        configs: BetaBrowserToolsetConfigsParam | None,
        confirm: BetaConfirmCallable | BetaAsyncConfirmCallable | None,
        url_policy: BetaURLPolicy | BetaAsyncURLPolicy | NotGiven,
        file_policy: BetaFilePolicy | None,
        tool_configs: BetaToolConfigs | None,
    ) -> None:
        super().__init__(
            cls,
            registry=BROWSER,
            default_bodies=DEFAULT_BODIES,
            configs=configs,
            confirm=confirm,
            tool_configs=tool_configs,
            family_methods=["_browser_state"],
        )
        self.file_policy = file_policy
        # Kept as passed: an explicit None is called like any other policy, so it refuses navigate rather than reading
        # as "unset" and leaving it unchecked.
        self.url_policy = url_policy

        if is_given(url_policy):
            check_sync_hook(cls, "url_policy", url_policy)

        required = sorted(name for name in CONFIRM_REQUIRED if name in self.served and self.is_enabled(name))
        if required and confirm is None:
            # these members act on page-supplied intent (a script to run, files to send), so they are always gated
            raise ToolsetConfigError(
                f"{required!r} requires a confirm callable: pass confirm=<callable>, or disable it in configs"
            )


class BaseBrowserToolset(
    BaseToolset[BetaBrowserMemberName, BetaBrowserMemberInput, BetaConfirmCallable | BetaAsyncConfirmCallable]
):
    """What the synchronous and asynchronous browser toolsets share: the options resolved at construction, the
    `tools[]` entry built from them, and the per-instance pipeline state. Subclass one of the two public classes,
    not this one."""

    toolset_name = FAMILY

    def __init__(
        self,
        *,
        configs: BetaBrowserToolsetConfigsParam | None,
        confirm: BetaConfirmCallable | BetaAsyncConfirmCallable | None,
        url_policy: BetaURLPolicy | BetaAsyncURLPolicy | NotGiven,
        file_policy: BetaFilePolicy | None,
        tool_configs: BetaToolConfigs | None,
    ) -> None:
        self._toolset_options: BrowserOptions = BrowserOptions(
            type(self),
            configs=configs,
            confirm=confirm,
            url_policy=url_policy,
            file_policy=file_policy,
            tool_configs=tool_configs,
        )
        super().__init__(self._toolset_options)
        self._toolset_pipeline: PipelineState = PipelineState()

    @override
    def to_dict(self) -> BetaBrowserToolset20260801Param:
        options = self._toolset_options

        # fresh copies each call: the runner keeps what to_dict() returns, so a later in-place edit must not reach it
        param = cast(BetaBrowserToolset20260801Param, {**copy.deepcopy(options.tool_configs), "type": TOOLSET_TYPE})
        if options.wire_configs is not None:
            param["configs"] = cast("BetaBrowserToolsetConfigsParam", copy.deepcopy(options.wire_configs))
        return param

    @property
    def configs(self) -> BetaBrowserToolsetConfigsParam | None:
        """The wire `configs` that `to_dict()` sends: yours, plus `enabled: False` for every member this class does
        not serve. A copy: nothing you do to it changes the toolset."""
        return self.to_dict().get("configs")


class BetaAbstractBrowserToolset20260801(
    BaseBrowserToolset,
    BaseSyncToolset[BetaBrowserMemberName, BetaBrowserMemberInput, BetaConfirmCallable | BetaAsyncConfirmCallable],
):
    """The synchronous browser toolset for `browser_toolset_20260801`.

    Subclass it and override the members your backend supports. Each takes `(context, input)`
    and returns the result type in its signature. A pure action (a click, typing, scrolling) returns
    nothing, or a string the model reads in a text block of its own after the SDK's fixed
    acknowledgment (such as `Clicked.`), folded to one line. See the browser use tool
    documentation (https://platform.claude.com/docs/en/agents-and-tools/tool-use/browser-use-tool) and read
    "Running a browser toolset safely" in the SDK guide (`browser-toolset.md`) before deploying one.
    """

    _toolset_twin = "BetaAsyncAbstractBrowserToolset20260801"

    def __init__(
        self,
        *,
        configs: BetaBrowserToolsetConfigsParam | None = None,
        confirm: BetaConfirmCallable | None = None,
        url_policy: BetaURLPolicy | NotGiven = NOT_GIVEN,
        file_policy: BetaFilePolicy | None = None,
        tool_configs: BetaToolConfigs | None = None,
    ) -> None:
        """A browser toolset with the given options. A mistake in them raises `ToolsetConfigError` here.

        Args:
            configs: The `configs` object of the `tools[]` entry, sent as given:
                `{"<member>": {"enabled": bool, "defer_loading": bool}}`. This is how a member is
                switched on or off. The SDK adds `enabled: False` for every member the subclass
                does not implement and never dispatches a disabled member. A subclass that overrides
                `execute` serves every member, so turn off the ones it does not serve here.
            confirm: Optional. `(context) -> bool`, called before every member call the SDK is about
                to run (after the URL policy and the file policy, never for a call already refused). Return
                `True` to run it or `False` to answer the model with a refusal, and decide by
                `context.member` which members prompt a person. `context` also has the
                parsed `input` and the target tab's `tab_url` / `tab_id` as of the last
                `browser_state` report the SDK collected (see `BetaConfirmContext`). Required when `javascript_exec` or
                `file_upload` is enabled.
            url_policy: Optional. `(BetaURLContext, str) -> None`, raising `ToolError` to refuse. Called once
                for each `navigate` that has a URL, with the URL exactly as the model wrote it, before the
                driver receives it (`back`, `forward` and `reload` are not checked). Left unset, `navigate` is
                not checked. This is a hook for your own policy, not a security
                boundary: it does not see redirects, sub-resources or addresses a page reaches on its own.
                Request interception in the driver and egress rules around the browser cover those.
            file_policy: Optional `BetaFilePolicy` (the SDK ships `BetaLocalFilePolicy`): which local paths and
                Files API document ids `file_upload` may use, and whether a download's local path is
                shown to the model. Without one, an upload with a path or document id is refused and
                download paths stay hidden.
            tool_configs: Optional fields set on the `tools[]` entry itself rather than on a member:
                `{"cache_control": {"type": "ephemeral"}}`.
        """
        super().__init__(
            configs=configs, confirm=confirm, url_policy=url_policy, file_policy=file_policy, tool_configs=tool_configs
        )

    @override
    def _toolset_run(
        self, context: BetaToolsetCallContext, name: str, input: Mapping[str, object]
    ) -> BetaToolsetContent:
        record = CallRecord(context=context, name=name, raw_input=input)
        options = self._toolset_options

        try:
            member = options.resolve(record.name)
            record.member = member
            record.input = parse_input(member, record.raw_input, family=FAMILY)

            url = navigate_url(record)
            if url is not None:
                self.__apply_policy(url, url_context(record))
            resolve_upload_paths(record, options.file_policy)
            self._toolset_confirm(member.name, confirm_context(record, self._toolset_pipeline))

            try:
                result = self.execute(record.context, member.name, record.input)
            except Exception as exc:
                # The driver's own error text reaches the model, cut to the field limit.
                record.error = bounded_error(classify(exc))
            else:
                record.result = bounded_result(member, result)
        except ToolError as exc:
            record.error = exc

        state = self.__browser_state(record.context)
        content, is_error = self._toolset_pipeline.finish(record, state, options.file_policy)
        if is_error:
            raise ToolError(content) from record.error
        return content

    def __browser_state(self, context: BetaToolsetCallContext) -> BetaBrowserState:
        # Called after every call, failed and refused ones included, so the driver can report what
        # changed meanwhile. Those changes go out with the next block that reaches the model.
        try:
            return with_bounded_tab_urls(self._browser_state(context))
        except ToolsetUsageError:
            raise
        except Exception as exc:
            raise BrowserStateError(exc) from exc

    def __apply_policy(self, url: str, context: BetaURLContext) -> None:
        """Run the `url_policy` callable on one address, raising the refusal unless it passes or there is no policy."""
        policy = self._toolset_options.url_policy
        if not is_given(policy):
            return

        returned: object = None
        raised: Exception | None = None
        try:
            returned = policy(context, url)
        except Exception as exc:
            raised = exc

        policy_outcome(returned, raised)

    def execute(
        self, context: BetaToolsetCallContext, name: BetaBrowserMemberName, input: BetaBrowserMemberInput
    ) -> BetaBrowserMemberResult:
        """Dispatch one member call to its method.

        Override it, calling `super().execute(context, name, input)`, for before/after hooks around every member
        (telemetry, logging, rewriting the input or the typed result). The pipeline still wraps the override, so the URL
        policy, the file policy and `confirm` run before it. A subclass that forwards every member elsewhere (a remote
        browser, a recording proxy) implements this method and `_browser_state`. A subclass that overrides it serves
        every member: one it implements runs through `super().execute`, one it does not raises `ToolError` from its
        default body there, and `configs` is how it turns off the members it does not serve. A call the SDK refused
        before dispatch never reaches it."""
        return self._toolset_member_method(name)(context, input)

    @abstractmethod
    def _browser_state(self, context: BetaToolsetCallContext) -> BetaBrowserState:
        """The browser after a call: the open tabs (one marked active) and the state changes since the previous
        report. Every driver implements it. The SDK calls it once after every member call, refused and failed ones
        included (not one that raised `ToolsetUsageError` or was interrupted), and attaches the result as the
        `browser_state` block, less the download paths the file policy hides. An async method is a contract error."""
        raise NotImplementedError

    def navigate(self, context: BetaToolsetCallContext, input: BetaBrowserNavigateInput) -> BetaBrowserNavigateResult:
        raise UnavailableMemberError("navigate", family=FAMILY)

    def screenshot(self, context: BetaToolsetCallContext, input: BetaBrowserScreenshotInput) -> BetaScreenshotResult:
        raise UnavailableMemberError("screenshot", family=FAMILY)

    def zoom(self, context: BetaToolsetCallContext, input: BetaBrowserZoomInput) -> BetaScreenshotResult:
        raise UnavailableMemberError("zoom", family=FAMILY)

    def left_click(self, context: BetaToolsetCallContext, input: BetaBrowserLeftClickInput) -> str | None:
        raise UnavailableMemberError("left_click", family=FAMILY)

    def right_click(self, context: BetaToolsetCallContext, input: BetaBrowserRightClickInput) -> str | None:
        raise UnavailableMemberError("right_click", family=FAMILY)

    def middle_click(self, context: BetaToolsetCallContext, input: BetaBrowserMiddleClickInput) -> str | None:
        raise UnavailableMemberError("middle_click", family=FAMILY)

    def double_click(self, context: BetaToolsetCallContext, input: BetaBrowserDoubleClickInput) -> str | None:
        raise UnavailableMemberError("double_click", family=FAMILY)

    def triple_click(self, context: BetaToolsetCallContext, input: BetaBrowserTripleClickInput) -> str | None:
        raise UnavailableMemberError("triple_click", family=FAMILY)

    def hover(self, context: BetaToolsetCallContext, input: BetaBrowserHoverInput) -> str | None:
        raise UnavailableMemberError("hover", family=FAMILY)

    def left_click_drag(self, context: BetaToolsetCallContext, input: BetaBrowserLeftClickDragInput) -> str | None:
        raise UnavailableMemberError("left_click_drag", family=FAMILY)

    def left_mouse_down(self, context: BetaToolsetCallContext, input: BetaBrowserLeftMouseDownInput) -> str | None:
        raise UnavailableMemberError("left_mouse_down", family=FAMILY)

    def left_mouse_up(self, context: BetaToolsetCallContext, input: BetaBrowserLeftMouseUpInput) -> str | None:
        raise UnavailableMemberError("left_mouse_up", family=FAMILY)

    def mouse_move(self, context: BetaToolsetCallContext, input: BetaBrowserMouseMoveInput) -> str | None:
        raise UnavailableMemberError("mouse_move", family=FAMILY)

    def scroll(self, context: BetaToolsetCallContext, input: BetaBrowserScrollInput) -> str | None:
        raise UnavailableMemberError("scroll", family=FAMILY)

    def scroll_to(self, context: BetaToolsetCallContext, input: BetaBrowserScrollToInput) -> str | None:
        raise UnavailableMemberError("scroll_to", family=FAMILY)

    def type(self, context: BetaToolsetCallContext, input: BetaBrowserTypeInput) -> str | None:
        raise UnavailableMemberError("type", family=FAMILY)

    def key(self, context: BetaToolsetCallContext, input: BetaBrowserKeyInput) -> str | None:
        raise UnavailableMemberError("key", family=FAMILY)

    def hold_key(self, context: BetaToolsetCallContext, input: BetaBrowserHoldKeyInput) -> str | None:
        raise UnavailableMemberError("hold_key", family=FAMILY)

    def form_input(self, context: BetaToolsetCallContext, input: BetaBrowserFormInputInput) -> str | None:
        raise UnavailableMemberError("form_input", family=FAMILY)

    def read_page(self, context: BetaToolsetCallContext, input: BetaBrowserReadPageInput) -> str:
        raise UnavailableMemberError("read_page", family=FAMILY)

    def find(self, context: BetaToolsetCallContext, input: BetaBrowserFindInput) -> str:
        raise UnavailableMemberError("find", family=FAMILY)

    def get_page_text(self, context: BetaToolsetCallContext, input: BetaBrowserGetPageTextInput) -> str:
        raise UnavailableMemberError("get_page_text", family=FAMILY)

    def wait(self, context: BetaToolsetCallContext, input: BetaBrowserWaitInput) -> str | None:
        raise UnavailableMemberError("wait", family=FAMILY)

    def file_upload(self, context: BetaToolsetCallContext, input: BetaBrowserFileUploadInput) -> str | None:
        """Default-disabled. Enabling it in `configs` lets a page read files on the machine running
        the browser: pass a `file_policy` confined to one dedicated upload directory. `input.paths`
        arrive already resolved by it."""
        raise UnavailableMemberError("file_upload", family=FAMILY)

    def read_console(self, context: BetaToolsetCallContext, input: BetaBrowserReadConsoleInput) -> str:
        raise UnavailableMemberError("read_console", family=FAMILY)

    def read_network(self, context: BetaToolsetCallContext, input: BetaBrowserReadNetworkInput) -> str:
        raise UnavailableMemberError("read_network", family=FAMILY)

    def javascript_exec(self, context: BetaToolsetCallContext, input: BetaBrowserJavascriptExecInput) -> str:
        """Default-disabled. Page content can steer what the model asks to run, so enabling it takes a
        `confirm` callable, which sees every call first. The script runs with the page's own authority (its
        cookies, storage and signed-in sessions), so the browser profile you drive must not be signed into accounts
        whose data or actions you would not hand the model."""
        raise UnavailableMemberError("javascript_exec", family=FAMILY)

    def new_tab(self, context: BetaToolsetCallContext, input: BetaBrowserNewTabInput) -> BetaBrowserStateTabEntryParam:
        raise UnavailableMemberError("new_tab", family=FAMILY)

    def list_tabs(
        self, context: BetaToolsetCallContext, input: BetaBrowserListTabsInput
    ) -> list[BetaBrowserStateTabEntryParam]:
        raise UnavailableMemberError("list_tabs", family=FAMILY)

    def switch_tab(
        self, context: BetaToolsetCallContext, input: BetaBrowserSwitchTabInput
    ) -> BetaBrowserStateTabEntryParam:
        raise UnavailableMemberError("switch_tab", family=FAMILY)

    def close_tab(self, context: BetaToolsetCallContext, input: BetaBrowserCloseTabInput) -> None:
        raise UnavailableMemberError("close_tab", family=FAMILY)


class BetaAsyncAbstractBrowserToolset20260801(
    BaseBrowserToolset,
    BaseAsyncToolset[BetaBrowserMemberName, BetaBrowserMemberInput, BetaConfirmCallable | BetaAsyncConfirmCallable],
):
    """The asynchronous browser toolset for `browser_toolset_20260801`, for `AsyncAnthropic`.

    Identical to `BetaAbstractBrowserToolset20260801` except that members and `_browser_state` are
    async (a sync one is a contract error), `confirm` and `url_policy` may be either, and `close` (also the
    async context-manager exit) is awaited.
    """

    _toolset_twin = "BetaAbstractBrowserToolset20260801"

    def __init__(
        self,
        *,
        configs: BetaBrowserToolsetConfigsParam | None = None,
        confirm: BetaAsyncConfirmCallable | None = None,
        url_policy: BetaAsyncURLPolicy | NotGiven = NOT_GIVEN,
        file_policy: BetaFilePolicy | None = None,
        tool_configs: BetaToolConfigs | None = None,
    ) -> None:
        """An asynchronous browser toolset with the given options. `confirm` and `url_policy` may be plain or
        `async` callables here. A mistake in the options raises `ToolsetConfigError`.

        Args:
            configs: The `configs` object of the `tools[]` entry, sent as given:
                `{"<member>": {"enabled": bool, "defer_loading": bool}}`. This is how a member is
                switched on or off. The SDK adds `enabled: False` for every member the subclass
                does not implement and never dispatches a disabled member. A subclass that overrides
                `execute` serves every member, so turn off the ones it does not serve here.
            confirm: Optional. `(context) -> bool`, called before every member call the SDK is about
                to run (after the URL policy and the file policy, never for a call already refused). Return
                `True` to run it or `False` to answer the model with a refusal, and decide by
                `context.member` which members prompt a person. `context` also has the
                parsed `input` and the target tab's `tab_url` / `tab_id` as of the last
                `browser_state` report the SDK collected (see `BetaConfirmContext`). Required when `javascript_exec` or
                `file_upload` is enabled.
            url_policy: Optional. `(BetaURLContext, str) -> None`, raising `ToolError` to refuse. Called once
                for each `navigate` that has a URL, with the URL exactly as the model wrote it, before the
                driver receives it (`back`, `forward` and `reload` are not checked). Left unset, `navigate` is
                not checked. This is a hook for your own policy, not a security
                boundary: it does not see redirects, sub-resources or addresses a page reaches on its own.
                Request interception in the driver and egress rules around the browser cover those.
            file_policy: Optional `BetaFilePolicy` (the SDK ships `BetaLocalFilePolicy`): which local paths and
                Files API document ids `file_upload` may use, and whether a download's local path is
                shown to the model. Without one, an upload with a path or document id is refused and
                download paths stay hidden.
            tool_configs: Optional fields set on the `tools[]` entry itself rather than on a member:
                `{"cache_control": {"type": "ephemeral"}}`.
        """
        super().__init__(
            configs=configs, confirm=confirm, url_policy=url_policy, file_policy=file_policy, tool_configs=tool_configs
        )

    @override
    async def _toolset_run(
        self, context: BetaToolsetCallContext, name: str, input: Mapping[str, object]
    ) -> BetaToolsetContent:
        record = CallRecord(context=context, name=name, raw_input=input)
        options = self._toolset_options

        try:
            member = options.resolve(record.name)
            record.member = member
            record.input = parse_input(member, record.raw_input, family=FAMILY)

            url = navigate_url(record)
            if url is not None:
                await self.__apply_policy(url, url_context(record))
            if member.name == "file_upload":
                # the file policy resolves upload paths on disk: kept off the event loop
                await anyio.to_thread.run_sync(resolve_upload_paths, record, options.file_policy)
            await self._toolset_confirm(member.name, confirm_context(record, self._toolset_pipeline))

            try:
                result = await self.execute(record.context, member.name, record.input)
            except Exception as exc:
                record.error = bounded_error(classify(exc))
            else:
                record.result = bounded_result(member, result)
        except ToolError as exc:
            record.error = exc

        state = await self.__browser_state(record.context)

        # `finish` writes the pipeline's bookkeeping, so it works on a copy that becomes the pipeline once the hop is
        # back on the loop: a call cancelled natively mid-hop leaves the thread writing to a copy nothing reads.
        pipeline = copy.copy(self._toolset_pipeline)
        try:
            content, is_error = await anyio.to_thread.run_sync(pipeline.finish, record, state, options.file_policy)
        except Exception:
            self._toolset_pipeline = pipeline  # it raised after draining this report's changes; kept, as on the loop
            raise

        self._toolset_pipeline = pipeline
        if is_error:
            raise ToolError(content) from record.error
        return content

    async def __browser_state(self, context: BetaToolsetCallContext) -> BetaBrowserState:
        try:
            return with_bounded_tab_urls(await self._browser_state(context))
        except ToolsetUsageError:
            raise
        except Exception as exc:
            raise BrowserStateError(exc) from exc

    async def __apply_policy(self, url: str, context: BetaURLContext) -> None:
        policy = self._toolset_options.url_policy
        if not is_given(policy):
            return

        returned: object = None
        raised: Exception | None = None
        try:
            returned = policy(context, url)
            if inspect.isawaitable(returned):
                returned = await returned
        except Exception as exc:
            raised = exc

        policy_outcome(returned, raised)

    async def execute(
        self, context: BetaToolsetCallContext, name: BetaBrowserMemberName, input: BetaBrowserMemberInput
    ) -> BetaBrowserMemberResult:
        """Dispatch one member call to its method. See the synchronous class's `execute`. Members are
        async here, and one written sync is a contract error."""
        return await self._toolset_member_method(name)(context, input)

    @abstractmethod
    async def _browser_state(self, context: BetaToolsetCallContext) -> BetaBrowserState:
        """The browser after a call. See the synchronous class's `_browser_state`. Awaited, so a sync method here
        is a contract error."""
        raise NotImplementedError

    async def navigate(
        self, context: BetaToolsetCallContext, input: BetaBrowserNavigateInput
    ) -> BetaBrowserNavigateResult:
        raise UnavailableMemberError("navigate", family=FAMILY)

    async def screenshot(
        self, context: BetaToolsetCallContext, input: BetaBrowserScreenshotInput
    ) -> BetaScreenshotResult:
        raise UnavailableMemberError("screenshot", family=FAMILY)

    async def zoom(self, context: BetaToolsetCallContext, input: BetaBrowserZoomInput) -> BetaScreenshotResult:
        raise UnavailableMemberError("zoom", family=FAMILY)

    async def left_click(self, context: BetaToolsetCallContext, input: BetaBrowserLeftClickInput) -> str | None:
        raise UnavailableMemberError("left_click", family=FAMILY)

    async def right_click(self, context: BetaToolsetCallContext, input: BetaBrowserRightClickInput) -> str | None:
        raise UnavailableMemberError("right_click", family=FAMILY)

    async def middle_click(self, context: BetaToolsetCallContext, input: BetaBrowserMiddleClickInput) -> str | None:
        raise UnavailableMemberError("middle_click", family=FAMILY)

    async def double_click(self, context: BetaToolsetCallContext, input: BetaBrowserDoubleClickInput) -> str | None:
        raise UnavailableMemberError("double_click", family=FAMILY)

    async def triple_click(self, context: BetaToolsetCallContext, input: BetaBrowserTripleClickInput) -> str | None:
        raise UnavailableMemberError("triple_click", family=FAMILY)

    async def hover(self, context: BetaToolsetCallContext, input: BetaBrowserHoverInput) -> str | None:
        raise UnavailableMemberError("hover", family=FAMILY)

    async def left_click_drag(
        self, context: BetaToolsetCallContext, input: BetaBrowserLeftClickDragInput
    ) -> str | None:
        raise UnavailableMemberError("left_click_drag", family=FAMILY)

    async def left_mouse_down(
        self, context: BetaToolsetCallContext, input: BetaBrowserLeftMouseDownInput
    ) -> str | None:
        raise UnavailableMemberError("left_mouse_down", family=FAMILY)

    async def left_mouse_up(self, context: BetaToolsetCallContext, input: BetaBrowserLeftMouseUpInput) -> str | None:
        raise UnavailableMemberError("left_mouse_up", family=FAMILY)

    async def mouse_move(self, context: BetaToolsetCallContext, input: BetaBrowserMouseMoveInput) -> str | None:
        raise UnavailableMemberError("mouse_move", family=FAMILY)

    async def scroll(self, context: BetaToolsetCallContext, input: BetaBrowserScrollInput) -> str | None:
        raise UnavailableMemberError("scroll", family=FAMILY)

    async def scroll_to(self, context: BetaToolsetCallContext, input: BetaBrowserScrollToInput) -> str | None:
        raise UnavailableMemberError("scroll_to", family=FAMILY)

    async def type(self, context: BetaToolsetCallContext, input: BetaBrowserTypeInput) -> str | None:
        raise UnavailableMemberError("type", family=FAMILY)

    async def key(self, context: BetaToolsetCallContext, input: BetaBrowserKeyInput) -> str | None:
        raise UnavailableMemberError("key", family=FAMILY)

    async def hold_key(self, context: BetaToolsetCallContext, input: BetaBrowserHoldKeyInput) -> str | None:
        raise UnavailableMemberError("hold_key", family=FAMILY)

    async def form_input(self, context: BetaToolsetCallContext, input: BetaBrowserFormInputInput) -> str | None:
        raise UnavailableMemberError("form_input", family=FAMILY)

    async def read_page(self, context: BetaToolsetCallContext, input: BetaBrowserReadPageInput) -> str:
        raise UnavailableMemberError("read_page", family=FAMILY)

    async def find(self, context: BetaToolsetCallContext, input: BetaBrowserFindInput) -> str:
        raise UnavailableMemberError("find", family=FAMILY)

    async def get_page_text(self, context: BetaToolsetCallContext, input: BetaBrowserGetPageTextInput) -> str:
        raise UnavailableMemberError("get_page_text", family=FAMILY)

    async def wait(self, context: BetaToolsetCallContext, input: BetaBrowserWaitInput) -> str | None:
        raise UnavailableMemberError("wait", family=FAMILY)

    async def file_upload(self, context: BetaToolsetCallContext, input: BetaBrowserFileUploadInput) -> str | None:
        """Default-disabled. Enabling it in `configs` lets a page read files on the machine running
        the browser: pass a `file_policy` confined to one dedicated upload directory. `input.paths`
        arrive already resolved by it."""
        raise UnavailableMemberError("file_upload", family=FAMILY)

    async def read_console(self, context: BetaToolsetCallContext, input: BetaBrowserReadConsoleInput) -> str:
        raise UnavailableMemberError("read_console", family=FAMILY)

    async def read_network(self, context: BetaToolsetCallContext, input: BetaBrowserReadNetworkInput) -> str:
        raise UnavailableMemberError("read_network", family=FAMILY)

    async def javascript_exec(self, context: BetaToolsetCallContext, input: BetaBrowserJavascriptExecInput) -> str:
        """Default-disabled. Page content can steer what the model asks to run, so enabling it takes a
        `confirm` callable, which sees every call first. The script runs with the page's own authority (its
        cookies, storage and signed-in sessions), so the browser profile you drive must not be signed into accounts
        whose data or actions you would not hand the model."""
        raise UnavailableMemberError("javascript_exec", family=FAMILY)

    async def new_tab(
        self, context: BetaToolsetCallContext, input: BetaBrowserNewTabInput
    ) -> BetaBrowserStateTabEntryParam:
        raise UnavailableMemberError("new_tab", family=FAMILY)

    async def list_tabs(
        self, context: BetaToolsetCallContext, input: BetaBrowserListTabsInput
    ) -> list[BetaBrowserStateTabEntryParam]:
        raise UnavailableMemberError("list_tabs", family=FAMILY)

    async def switch_tab(
        self, context: BetaToolsetCallContext, input: BetaBrowserSwitchTabInput
    ) -> BetaBrowserStateTabEntryParam:
        raise UnavailableMemberError("switch_tab", family=FAMILY)

    async def close_tab(self, context: BetaToolsetCallContext, input: BetaBrowserCloseTabInput) -> None:
        raise UnavailableMemberError("close_tab", family=FAMILY)


DEFAULT_BODIES: frozenset[object] = frozenset(
    getattr(cls, name)
    for cls in (BetaAbstractBrowserToolset20260801, BetaAsyncAbstractBrowserToolset20260801)
    for name in (*BROWSER_MEMBER_NAMES, "execute")
)
"""The two abstract classes' own member and `execute` bodies: a subclass whose attribute is still one of these did
not override it."""
