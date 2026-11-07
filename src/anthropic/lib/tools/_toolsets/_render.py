"""Turns what a member returned into `tool_result` content, and a `BetaBrowserState` into the
`browser_state` block.

The registry row records what kind of result a member returns. The renderer reads the fields it
needs off that result. The tab-management members render no content of their own: the API accepts
the `browser_state` block as their whole result and produces the text the model reads from it.
"""

from __future__ import annotations

import re
import copy
import json
import inspect
from typing import Literal, cast
from collections.abc import Sequence
from typing_extensions import TypeAlias, TypeGuard, assert_never

from ._base import Member, BetaScreenshotResult
from ._hooks import BetaFilePolicy
from ._results import (
    StateChange,
    BetaDialogDismissed,
    BetaBrowserMemberResult,
    BetaBrowserNavigateResult,
)
from ._runnable import BetaToolsetContent, hook_refusal
from ._sanitize import one_line, well_formed, bounded_tab_url
from ...._models import BaseModel
from ....types.beta import (
    BetaImageBlockParam,
    BetaBrowserStateBlockParam,
    BetaBrowserStateChangeParam,
    BetaBrowserStateTabEntryParam,
    BetaBrowserStateChangeDownloadFailedParam,
    BetaBrowserStateChangeDownloadStartedParam,
    BetaBrowserStateChangeDownloadCompletedParam,
)
from .._beta_functions import ToolError
from ._computer_results import BetaScreenshotResult, BetaComputerMemberResult, BetaComputerCursorPositionResult
from ....types.beta.beta_tool_result_block_param import Content

__all__ = [
    "MemberResult",
    "text_block",
    "image_block",
    "NAVIGATION_REFUSED_LINE",
    "action_line",
    "render_result",
    "render_browser_state",
    "path_visible",
    "dialog_lines",
    "is_download_change",
]

MemberResult = BetaBrowserMemberResult | BetaComputerMemberResult
"""What any member of either family may return."""

NAVIGATION_REFUSED_LINE = "A navigation was refused."
"""The single line the model reads for any number of `BetaNavigationRefused` entries in a report."""


def input_field(input: BaseModel, path: str) -> str:
    value: object = input
    for part in path.split("."):
        if value is None:
            return ""
        value = getattr(value, part)
    if value is None:
        return ""
    if isinstance(value, float) and value.is_integer():
        value = int(value)  # a whole number as JSON spells it, so the model reads `Waited 2s.`
    return one_line(str(value))


TEMPLATE_FIELDS = {
    "scroll_direction": "scroll_direction",
    "text": "text",
    "duration": "duration",
    "ref": "target.ref",
}
TEMPLATE_TOKEN_RE = re.compile("|".join(re.escape("{" + key + "}") for key in TEMPLATE_FIELDS))


def confirmation_text(template: str, input: BaseModel) -> str:
    """Fill a pure action's template from its input in a single pass, so a model-supplied value
    such as `"{ref}"` stays data and is never re-read as a placeholder."""
    return TEMPLATE_TOKEN_RE.sub(lambda m: input_field(input, TEMPLATE_FIELDS[m.group(0)[1:-1]]), template)


def text_block(text: str) -> Content:
    return {"type": "text", "text": text}


def image_block(data: str, media_type: Literal["image/png", "image/jpeg", "image/gif", "image/webp"]) -> Content:
    """One image block around the base64 `data` a screenshot or zoom member returned."""
    image: BetaImageBlockParam = {"type": "image", "source": {"type": "base64", "media_type": media_type, "data": data}}
    return image


def action_line(member: Member[str, BaseModel], result: object) -> str | None:
    """The line of text a pure action returned, as written: `render_result` folds it to one line (control,
    line-separator and bidi characters a space) and bounds it, and the browser pipeline checks it as error text first.
    `None` when it returned nothing, or anything but a non-empty string, and for every other member."""
    if member.result != "none" or member.text is None or not isinstance(result, str):
        return None
    return result or None


def render_result(member: Member[str, BaseModel], input: BaseModel, result: MemberResult) -> BetaToolsetContent:
    """The content blocks for a member's result, by the registry's result kind. A pure action renders as its fixed
    acknowledgment, then, in a text block of its own, the line it returned, if any (already bounded when
    it arrives here)."""
    kind = member.result

    if kind == "none":
        if not member.text:
            return []
        lines = [confirmation_text(member.text, input)]
        line = action_line(member, result)
        if line is not None:
            lines.append(one_line(line))
        return [text_block(text) for text in lines]

    if kind == "tab" or kind == "tabs":
        # new_tab / switch_tab / list_tabs: the browser_state block is the whole result.
        return []

    if kind == "navigate":
        nav = result
        if not isinstance(nav, BetaBrowserNavigateResult):
            # Not a TypeError: the browser_state check turns one into ToolsetContractError, which stops the run. A
            # ValueError reaches the model as an error result.
            raise ValueError(f"navigate returned {type(nav).__name__}, not its result model")

        # the final address is page-chosen through redirects: folded to one line and held to the bound, as a tab's is
        line = f"Navigated to {bounded_tab_url(nav.url)}"
        if nav.title is not None:
            line += f" — {one_line(nav.title)}"
        if nav.status is not None:
            line += f" (HTTP {nav.status})"
        return [text_block(line)]

    if kind == "screenshot":
        shot = result
        if not isinstance(shot, BetaScreenshotResult):
            raise ValueError(f"screenshot returned {type(shot).__name__}, not its result model")
        return [image_block(shot.data, shot.media_type)]

    if kind == "point":
        point = result
        if not isinstance(point, BetaComputerCursorPositionResult):
            raise ValueError(f"cursor_position returned {type(point).__name__}, not its result model")
        return [text_block(f"X={point.x},Y={point.y}")]

    if kind == "text":
        text = well_formed(str(result))  # page text: a lone surrogate in it could not be sent
        return [text_block(text if text else "(empty)")]

    assert_never(kind)


# the API's limit for these fields, as for a URL
def bounded_tab(tab: BetaBrowserStateTabEntryParam) -> BetaBrowserStateTabEntryParam:
    bounded = copy.copy(tab)
    bounded["url"], bounded["title"] = bounded_tab_url(tab["url"]), one_line(tab["title"])
    return bounded


DIALOG_MESSAGE_MAX = 200
DIALOG_KIND_MAX = 20  # `kind` is driver-supplied and goes into the line unquoted, and a real one is a single word
DIALOG_LINES_MAX = 3


def dialog_lines(dialogs: Sequence[BetaDialogDismissed]) -> list[str]:
    """One line per dismissed dialog the driver reported (`A confirm dialog "…" was dismissed.`), the message capped
    and at most a few lines, then a count of the rest, because a page can open dialogs in a loop."""
    lines: list[str] = []
    for dialog in dialogs[:DIALOG_LINES_MAX]:
        kind = one_line(dialog.kind)[:DIALOG_KIND_MAX] or "dialog"
        article = "An" if kind[:1].lower() in "aeiou" else "A"
        noun = kind if kind == "dialog" else f"{kind} dialog"
        message = one_line(dialog.message)
        if len(message) > DIALOG_MESSAGE_MAX:
            message = message[:DIALOG_MESSAGE_MAX] + "…"
        quoted = f" {json.dumps(message, ensure_ascii=False)}" if message else ""
        lines.append(f"{article} {noun}{quoted} was dismissed.")
    if len(dialogs) > DIALOG_LINES_MAX:
        lines.append(f"{len(dialogs) - DIALOG_LINES_MAX} more dialogs were dismissed.")
    return lines


DownloadChangeParam: TypeAlias = (
    BetaBrowserStateChangeDownloadStartedParam
    | BetaBrowserStateChangeDownloadCompletedParam
    | BetaBrowserStateChangeDownloadFailedParam
)
"""The wire change kinds that have a page-supplied `url` (and possibly a local `path` or an `error`)."""
DownloadChangeType: TypeAlias = Literal["download_started", "download_completed", "download_failed"]
DOWNLOAD_TYPES: tuple[DownloadChangeType, ...] = ("download_started", "download_completed", "download_failed")


def is_download_change(change: StateChange) -> TypeGuard[DownloadChangeParam]:
    return isinstance(change, dict) and change["type"] in DOWNLOAD_TYPES


def path_visible(file_policy: BetaFilePolicy | None, path: str) -> bool:
    """The file policy's verdict on one download path, hidden without a policy. Only `True` shows it. A
    `ToolsetUsageError` propagates. Any other exception from the predicate fails closed: the path stays hidden and the
    report still goes out."""
    if file_policy is None:
        return False

    try:
        verdict: object = file_policy.is_path_visible(path)
    except Exception as exc:
        hook_refusal(exc, ToolError("path hidden"))  # a ToolsetUsageError propagates; anything else is logged
        return False

    if inspect.iscoroutine(verdict):
        verdict.close()  # from an `async` predicate: hidden, with no "never awaited" warning left behind
    return verdict is True


def render_browser_state(
    tabs: Sequence[BetaBrowserStateTabEntryParam],
    changes: Sequence[BetaBrowserStateChangeParam],
    file_policy: BetaFilePolicy | None,
) -> BetaBrowserStateBlockParam:
    """The `browser_state` block: the driver's tabs as reported with each URL and title folded to one line and held to
    the API's length limit, and `changes` with a download's `url` and a failed download's `error` bounded the same
    way, and its `path` removed from every download change, kept only on a `download_completed` whose path the file
    policy exposes."""
    wire_changes: list[BetaBrowserStateChangeParam] = []
    for change in changes:
        if is_download_change(change):
            change = copy.copy(change)  # the driver's dict is left as it was
            change["url"] = bounded_tab_url(change["url"])
            # taken off whichever kind has it, declared or not: a local path never goes out unchecked
            path = cast("dict[str, str | None]", change).pop("path", None)
            if change["type"] == "download_completed" and path is not None and path_visible(file_policy, path):
                # a page-chosen name that folding or cutting would change could name another file
                if one_line(path) == path:
                    change["path"] = path
            if change["type"] == "download_failed" and (error := change.get("error")) is not None:
                change["error"] = one_line(error)
        wire_changes.append(change)
    block: BetaBrowserStateBlockParam = {"type": "browser_state", "tabs": [bounded_tab(tab) for tab in tabs]}
    if wire_changes:  # "nothing to report" is an absent field, never an empty list
        block["state_changes"] = wire_changes
    return block
