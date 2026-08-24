# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable, Optional
from typing_extensions import Literal, Required, TypedDict

from .browser_state_change_param import BrowserStateChangeParam
from .browser_state_tab_entry_param import BrowserStateTabEntryParam
from .cache_control_ephemeral_param import CacheControlEphemeralParam

__all__ = ["BrowserStateBlockParam"]


class BrowserStateBlockParam(TypedDict, total=False):
    """
    The caller's browser state after a browser toolset member call —
    the full inventory of open tabs, which tab is active, and any side
    effects (tabs opened, download state changes) the call produced.

    At most one per `tool_result`, only on a non-error result answering a
    browser toolset member `tool_use`. The server renders the
    model-visible text from it; the model never sees the raw fields.
    """

    tabs: Required[Iterable[BrowserStateTabEntryParam]]
    """All tabs open in the browser after this call — the full inventory, not a delta.

    May be empty. Whenever non-empty, exactly one entry carries `active: true`.
    """

    type: Required[Literal["browser_state"]]

    cache_control: Optional[CacheControlEphemeralParam]
    """Create a cache control breakpoint at this content block."""

    state_changes: Optional[Iterable[BrowserStateChangeParam]]
    """Tabs opened and download state changes during this call.

    "Nothing to report" is expressed by omitting the field, never by an empty list.
    """
