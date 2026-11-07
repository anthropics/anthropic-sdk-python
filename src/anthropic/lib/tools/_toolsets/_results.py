"""What a browser toolset member returns.

Tabs and state changes are the generated wire types (`BetaBrowserStateTabEntryParam`,
`BetaBrowserStateChange*Param`) returned as they are. Only the shapes with no wire twin are
declared here.
"""

from __future__ import annotations

from typing_extensions import Literal, Annotated, TypeAlias

from pydantic import Field

from ._base import BetaScreenshotResult
from ...._models import BaseModel, UnionDiscriminator
from ....types.beta import BetaBrowserStateChangeParam, BetaBrowserStateTabEntryParam

__all__ = [
    "BetaBrowserNavigateResult",
    "BetaNavigationRefused",
    "BetaDialogDismissed",
    "StateChange",
    "BetaBrowserState",
    "BetaBrowserMemberResult",
]


def no_changes() -> list[StateChange]:
    return []


class BetaBrowserNavigateResult(BaseModel):
    """Where a navigation ended up. Rendered as `Navigated to {url} — {title} (HTTP {status})`, each value made safe
    for one line of text (control, line-separator and bidi characters replaced, length bounded)."""

    url: str
    """The final URL after redirects."""

    status: int | None = None

    title: str | None = None


class BetaNavigationRefused(BaseModel):
    """A navigation the driver refused, for example a page-started navigation its request interception stopped.

    Its `type` is the SDK's own and is never sent: the SDK reports it to the model as one fixed line of text rather
    than in the `browser_state` block.
    """

    type: Literal["navigation_refused"] = "navigation_refused"


class BetaDialogDismissed(BaseModel):
    """A native dialog (`alert`, `confirm`, `prompt`) the page opened and the driver dismissed.

    Its `type` is the SDK's own and is never sent: the SDK reports it to the model as a line of text with the next
    block (`A confirm dialog "Delete everything?" was dismissed.`), which tells the model the page asked and what the
    answer was. `message` is page-supplied text, capped when rendered.
    """

    type: Literal["dialog_dismissed"] = "dialog_dismissed"

    kind: str
    """`"alert"`, `"confirm"`, `"prompt"` (or whatever the browser called it)."""

    message: str = ""


StateChange: TypeAlias = Annotated[
    BetaBrowserStateChangeParam | BetaNavigationRefused | BetaDialogDismissed,
    Field(discriminator="type"),
    UnionDiscriminator("type"),
]
"""One `state_changes` entry, told apart by `type`: a generated `BetaBrowserStateChange*Param`, or one of the
SDK's own kinds (`BetaNavigationRefused`, `BetaDialogDismissed`) that reach the model as text."""


class BetaBrowserState(BaseModel):
    """The browser after a call: what `_browser_state` returns. Forwarded to the API with download paths the file
    policy does not expose removed and each reported URL, title and error folded to one bounded line.

    `tabs` is the full inventory (the generated `BetaBrowserStateTabEntryParam`, with the active
    tab marked by its own `active` flag), `state_changes` what changed since the last report. The API's
    rules apply unchanged:

    - `tab_id` values are unique;
    - exactly one tab is `active` when any tab is open;
    - at most 100 tabs.

    Of the state changes, the SDK keeps the latest per `download_id` and one `tab_opened` per tab still open, so
    the list need not be deduplicated.
    """

    tabs: list[BetaBrowserStateTabEntryParam]
    state_changes: list[StateChange] = Field(default_factory=no_changes)


BetaBrowserMemberResult: TypeAlias = (
    BetaBrowserNavigateResult
    | BetaScreenshotResult
    | BetaBrowserStateTabEntryParam
    | list[BetaBrowserStateTabEntryParam]
    | str
    | None
)
"""Anything a browser member may return: `execute`'s un-narrowed result type."""
