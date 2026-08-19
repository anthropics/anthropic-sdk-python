# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["BetaBrowserStateTabEntryParam"]


class BetaBrowserStateTabEntryParam(TypedDict, total=False):
    """One open browser tab reported in a `browser_state` block's `tabs`
    inventory.

    `tab_id` is the caller-assigned identifier for the tab; `title` and
    `url` describe the page the tab is currently showing and may be empty
    strings (a blank tab legitimately has both empty). `active` marks the
    tab that is active after this call; whenever `tabs` is non-empty,
    exactly one entry is marked.
    """

    tab_id: Required[str]
    """The caller-assigned identifier for this tab, unique within the inventory."""

    title: Required[str]
    """The title of the page the tab is showing. May be empty."""

    url: Required[str]
    """The URL of the page the tab is showing. May be empty."""

    active: bool
    """Whether this tab is the active tab after this call.

    Whenever `tabs` is non-empty, exactly one entry is marked `active: true`.
    """
