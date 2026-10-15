"""The stages of a browser member call that do not depend on whether the toolset is sync or async.

The stages every family runs (resolving, parsing, the confirm verdict) are in `_base`.
"""

from __future__ import annotations

import copy
from typing import NamedTuple
from collections.abc import Mapping, Sequence

from ._base import bounded_error, error_content
from ._hooks import BetaFilePolicy, BetaURLContext, BetaConfirmContext
from ._errors import (
    URLRefusedError,
    ToolsetUsageError,
    UploadNoRootsError,
    UploadRefusedError,
    ToolsetContractError,
)
from ._render import (
    NAVIGATION_REFUSED_LINE,
    text_block,
    action_line,
    dialog_lines,
    render_result,
    is_download_change,
    render_browser_state,
)
from ._results import StateChange, BetaBrowserState, BetaDialogDismissed, BetaNavigationRefused, BetaBrowserMemberResult
from ._registry import STATE_ONLY_MEMBERS, BrowserMember
from ._runnable import BetaToolsetContent, BetaToolsetCallContext, unvalidated, hook_refusal
from ._sanitize import FIELD_MAX, folded, bounded_tab_url
from ...._compat import get_model_fields
from ....types.beta import (
    BetaBrowserMemberInput,
    BetaBrowserNavigateInput,
    BetaBrowserFileUploadInput,
    BetaBrowserStateChangeParam,
    BetaBrowserStateTabEntryParam,
)
from .._beta_functions import ToolError

__all__ = ["CallRecord", "Report", "PipelineState", "with_bounded_tab_urls"]


class CallRecord:
    """One member call in flight: what each stage produced, for the stages after it."""

    def __init__(self, *, context: BetaToolsetCallContext, name: str, raw_input: Mapping[str, object]) -> None:
        self.context = context
        self.name = name
        self.raw_input = raw_input

        self.member: BrowserMember | None = None
        self.input: BetaBrowserMemberInput | None = None
        self.result: BetaBrowserMemberResult = None
        self.error: ToolError | None = None

    @property
    def tab_id(self) -> str | None:
        """The tab the call names, or None when it names none (an absent or empty `tab_id` both mean
        the active tab, which is how drivers resolve them). Only a member whose input declares `tab_id`
        names a tab: on any other member a `tab_id` key is an extra field and does not count."""
        if self.member is None or "tab_id" not in get_model_fields(self.member.input):
            return None

        tab_id: str | None = getattr(self.input, "tab_id", None)
        return tab_id or None

    @property
    def tool_use_id(self) -> str | None:
        return self.context.tool_use.id if self.context.tool_use is not None else None

    @property
    def opened_tab_id(self) -> str | None:
        """The `tab_id` of the tab a `new_tab` call opened, from the tab entry it returned, or `None` for any other call
        or result."""
        if self.member is None or self.member.name != "new_tab" or not isinstance(self.result, dict):
            return None
        return self.result.get("tab_id")


class Report(NamedTuple):
    """The driver's report as the pipeline reads it, built once: the tabs and the wire changes with each page-supplied
    URL bounded, and the SDK's own change kinds set apart, since they reach the model as text."""

    tabs: list[BetaBrowserStateTabEntryParam]
    changes: list[BetaBrowserStateChangeParam]
    navigation_refused: bool
    dialogs: list[BetaDialogDismissed]


def report_of(state: BetaBrowserState) -> Report:
    """The checked `BetaBrowserState` as the `Report` that `finish` renders: its tabs and wire changes as they stand, the
    SDK's own change kinds set apart."""
    changes: list[BetaBrowserStateChangeParam] = []
    dialogs: list[BetaDialogDismissed] = []
    navigation_refused = False
    for change in state.state_changes:
        if isinstance(change, BetaNavigationRefused):
            navigation_refused = True
        elif isinstance(change, BetaDialogDismissed):
            dialogs.append(change)
        else:
            changes.append(change)
    return Report(tabs=list(state.tabs), changes=changes, navigation_refused=navigation_refused, dialogs=dialogs)


def with_bounded_tab_urls(state: BetaBrowserState) -> BetaBrowserState:
    """The report with each tab's and each download's page-supplied URL as the model will read it, folded to one line
    and held to the API's limit (see `bounded_tab_url`), before anything else reads or forwards it."""
    tabs: list[BetaBrowserStateTabEntryParam] = []
    touched = False
    for tab in state.tabs:
        bounded = bounded_tab_url(tab["url"])
        if bounded != tab["url"]:
            touched = True
            tab = copy.copy(tab)  # the driver's dict is left as it was
            tab["url"] = bounded
        tabs.append(tab)

    changes: list[StateChange] = []
    for change in state.state_changes:
        if is_download_change(change):
            bounded = bounded_tab_url(change["url"])
            if bounded != change["url"]:
                touched = True
                change = copy.copy(change)
                change["url"] = bounded
        changes.append(change)

    # Rebuilt without validation: the report is the driver's, forwarded for the API to judge.
    return unvalidated(BetaBrowserState, tabs=tabs, state_changes=changes) if touched else state


def target_tab(
    tabs: Sequence[BetaBrowserStateTabEntryParam], tab_id: str | None
) -> BetaBrowserStateTabEntryParam | None:
    """Which tab a call targets: the tab it names by `tab_id`, else the active tab. `None` when the
    named tab is not in the report (or nothing is active)."""
    for tab in tabs:
        if tab_id is not None:
            if tab.get("tab_id") == tab_id:
                return tab
        elif tab.get("active") is True:
            return tab
    return None


class PipelineState:
    """Per-toolset bookkeeping that outlives a single call."""

    def __init__(self) -> None:
        self.pending_changes: list[BetaBrowserStateChangeParam] = []
        """State changes not sent yet: those drained by a failed call, and a popup's `tab_opened` held back from a
        successful `new_tab`. They go out with the next `browser_state` block."""

        self.refusal_pending = False
        """A refused-navigation line that could not be attached yet (the result was state-only)."""

        self.dialogs_pending: list[BetaDialogDismissed] = []
        """Dismissed dialogs whose lines could not be attached yet, for the same reason."""

        self.last_tabs: list[BetaBrowserStateTabEntryParam] = []
        """The tab inventory of the most recent report: what `BetaConfirmContext` is filled from."""

    def finish(
        self, call: CallRecord, state: BetaBrowserState, file_policy: BetaFilePolicy | None
    ) -> tuple[BetaToolsetContent, bool]:
        """Render the call's outcome with the browser state the driver just reported.

        On success the content is the member's rendering plus the `browser_state` block (with
        any changes held back earlier). On failure the changes are held back for the next block,
        because an error result cannot include one, and the content is the error text, plus the
        refused-navigation line when the driver reported one, since that is often why the member
        failed. Returns `(content, is_error)`; a report the SDK cannot read raises `ToolsetContractError` instead."""
        try:
            return self._render(call, state, file_policy)
        except ToolsetUsageError:
            raise
        except (KeyError, TypeError, AttributeError) as exc:
            raise ToolsetContractError(
                f"browser_state returned a report the SDK cannot read ({type(exc).__name__}: {exc}); "
                "report each tab and state change with its documented fields"
            ) from exc

    def _render(
        self, call: CallRecord, state: BetaBrowserState, file_policy: BetaFilePolicy | None
    ) -> tuple[BetaToolsetContent, bool]:
        report = report_of(state)
        self.last_tabs = report.tabs
        refused = report.navigation_refused or self.refusal_pending
        dialogs = [*self.dialogs_pending, *report.dialogs]
        changes = merge_pending_changes(self.pending_changes, report)

        # Held first: should rendering stop the run (a ToolsetUsageError out of the file policy), the
        # drained changes are still on hand rather than lost with this call.
        self.pending_changes = changes
        opened = call.opened_tab_id if call.error is None else None
        if opened is not None and [tab["tab_id"] for tab in report.tabs if tab.get("active") is True] != [opened]:
            # The API rejects a new_tab result unless the opened tab is the only active one, and that ends the run.
            # A tab opened in the background, or a popup that takes focus first, breaks the rule, so the call fails.
            call.error = ToolError(NEW_TAB_NOT_ACTIVE)

        if call.error is None:
            assert call.member is not None and call.input is not None
            content = render_result(call.member, call.input, call.result)
            changes, held = new_tab_changes(opened, changes)
            block = render_browser_state(report.tabs, changes, file_policy)
            self.pending_changes = held

            if call.member.name in STATE_ONLY_MEMBERS:
                # A block-only result has no text, so the lines wait for the next result that can include them.
                self.refusal_pending = refused
                self.dialogs_pending = dialogs
                return [block], False
            return [*content, *self._take_notices(refused, dialogs), block], False

        return [*error_content(bounded_error(call.error)), *self._take_notices(refused, dialogs)], True

    def _take_notices(self, refused: bool, dialogs: Sequence[BetaDialogDismissed]) -> BetaToolsetContent:
        """The refused-navigation line and the dialog lines as text blocks, now that a result can include them."""
        self.refusal_pending = False
        self.dialogs_pending = []
        lines = [NAVIGATION_REFUSED_LINE] if refused else []
        return [text_block(line) for line in [*lines, *dialog_lines(dialogs)]]


def merge_pending_changes(
    pending: Sequence[BetaBrowserStateChangeParam], report: Report
) -> list[BetaBrowserStateChangeParam]:
    """State changes held back from earlier calls (a failed call's, or a popup's `tab_opened` after `new_tab`),
    followed by this report's own, coalesced into what one block may contain: of the changes for one `download_id`
    only the latest, where it stands; of the `tab_opened` entries for one tab only the first, and only while that tab
    is in the report's `tabs`. A driver's list need not be deduplicated, and a held entry cannot make a valid report
    invalid."""
    changes = [*pending, *report.changes]
    live_tabs = {tab["tab_id"] for tab in report.tabs}

    # the last position of each download's changes (pydantic v1 lets a missing key through, hence `.get`)
    latest = {change.get("download_id"): index for index, change in enumerate(changes) if is_download_change(change)}

    kept: list[BetaBrowserStateChangeParam] = []
    opened: set[str] = set()
    for index, change in enumerate(changes):
        if change["type"] == "tab_opened":
            if change["tab_id"] not in live_tabs or change["tab_id"] in opened:
                continue
            opened.add(change["tab_id"])
        elif is_download_change(change) and latest[change.get("download_id")] != index:
            continue
        kept.append(change)
    return kept


NEW_TAB_NOT_ACTIVE = (
    "new_tab opened a tab, but the browser does not report it as the only active tab. Call list_tabs to see the tabs."
)


def new_tab_changes(
    opened: str | None, changes: list[BetaBrowserStateChangeParam]
) -> tuple[list[BetaBrowserStateChangeParam], list[BetaBrowserStateChangeParam]]:
    """The changes for this block and the changes to hold, as `(keep, held)`. On a `new_tab` result (`opened` is the
    tab it opened) the block carries exactly one `tab_opened`, for `opened`, added when the driver reported none. A
    `tab_opened` for any other tab, such as a popup the page opened meanwhile, waits for the next block rather than
    making this one invalid. For any other call (`opened` is `None`) the changes pass through."""
    if opened is None:
        return changes, []

    keep: list[BetaBrowserStateChangeParam] = []
    held: list[BetaBrowserStateChangeParam] = []

    for change in changes:
        if change["type"] == "tab_opened" and change["tab_id"] != opened:
            held.append(change)
        else:
            keep.append(change)
    if not any(change["type"] == "tab_opened" for change in keep):
        keep.append({"type": "tab_opened", "tab_id": opened})
    return keep, held


# --- URL and file policy enforcement ----------------------------------------------------------------


def bounded_result(member: BrowserMember, result: BetaBrowserMemberResult) -> BetaBrowserMemberResult:
    """`result` as the record keeps it: the line a pure action returned is folded to one line and cut. Anything else
    is kept as returned."""
    line = action_line(member, result)
    return result if line is None else folded(line)[:FIELD_MAX]


POLICY_REFUSED = "refused by the URL policy"
"""The refusal for a `url_policy` that raised something other than a ToolError: its own message may
contain the URL it refused, so the model reads this instead and the traceback goes to the log."""
NO_DOCUMENT_POLICY = "file_upload has no configured document allowlist"
UPLOAD_REFUSED = "the file policy could not vet the upload"


def url_context(record: CallRecord) -> BetaURLContext:
    assert record.member is not None
    return unvalidated(BetaURLContext, member=record.member.name, tab_id=record.tab_id, tool_use_id=record.tool_use_id)


HISTORY_NAVIGATION = frozenset(("back", "forward", "reload"))


def navigate_url(record: CallRecord) -> str | None:
    """The `url` of a `navigate` call exactly as the model wrote it, for the URL policy. `None` for the history
    words `back` / `forward` / `reload` (the driver receives the canonical lower-case word) and for other members."""
    if not isinstance(record.input, BetaBrowserNavigateInput):
        return None

    url = record.input.url
    word = url.strip().lower()

    if word in HISTORY_NAVIGATION:
        if word != url:
            object.__setattr__(record.input, "url", word)
        return None
    return url


def policy_outcome(returned: object, raised: Exception | None) -> None:
    """Turn what the `url_policy` callable did into the pipeline's decision: return to proceed, or raise the refusal
    the model reads. A `ToolError` it raised is relayed as-is. Any other exception fails closed with the SDK's own
    text (a `ToolsetUsageError` propagates). A non-`None` return is a contract error."""
    if raised is not None:
        raise hook_refusal(raised, URLRefusedError(POLICY_REFUSED))
    if returned is not None:
        # "return None to allow, raise to refuse": a policy mistakenly written as a predicate
        # returns False to block, and reading that as a pass would fail open silently.
        raise ToolsetContractError(
            f"url_policy must return None to allow or raise ToolError to refuse; got {type(returned).__name__}"
        )


def resolve_upload_paths(record: CallRecord, file_policy: BetaFilePolicy | None) -> None:
    """For `file_upload`: run `input.paths` and `input.document_ids` through the file policy before
    dispatch, so the driver receives what the policy returned and a refused path or document never
    reaches it. Without a file policy, an upload that names either is refused."""
    upload = record.input
    if not isinstance(upload, BetaBrowserFileUploadInput):
        return

    if file_policy is None:
        if upload.paths:
            raise UploadNoRootsError()
        if upload.document_ids:
            raise UploadRefusedError(NO_DOCUMENT_POLICY)
        return

    ctx = url_context(record)
    if upload.paths:
        paths = vetted_upload_entries(file_policy, "resolve_upload_paths", ctx, upload.paths)
        object.__setattr__(upload, "paths", paths)

    if upload.document_ids:
        ids = vetted_upload_entries(file_policy, "resolve_upload_documents", ctx, upload.document_ids)
        object.__setattr__(upload, "document_ids", ids)


def vetted_upload_entries(
    file_policy: BetaFilePolicy, hook: str, ctx: BetaURLContext, given: Sequence[str]
) -> list[str]:
    """One `file_upload` field run through the file policy's `hook`: the entries the driver receives, read once (a
    generator is spent after one pass)."""
    try:
        return list(getattr(file_policy, hook)(ctx, given))  # a generator does its work here, inside the guard
    except Exception as exc:
        # hook_refusal logs it, and the upload never reaches the driver
        raise hook_refusal(exc, UploadRefusedError(UPLOAD_REFUSED)) from None


# --- confirmation ---------------------------------------------------------------------------------


def confirm_context(record: CallRecord, pipeline: PipelineState) -> BetaConfirmContext:
    """What the `confirm` callable receives: the member and its parsed input, and the tab the call
    targets (named, else active) with its URL, as of the last report and with no page read."""
    assert record.member is not None and record.input is not None
    # The URL exactly as the model read it in the last block: folded and bounded when the report was collected.
    tab = target_tab(pipeline.last_tabs, record.tab_id)
    # Built from values the pipeline already holds, so nothing here is user input to validate.
    return unvalidated(
        BetaConfirmContext,
        tool_use=record.context.tool_use,
        member=record.member.name,
        input=record.input,
        tab_id=record.tab_id if tab is None else tab["tab_id"],
        tab_url=None if tab is None else tab["url"],
    )
