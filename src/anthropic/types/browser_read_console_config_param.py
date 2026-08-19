# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import TypedDict

__all__ = ["BrowserReadConsoleConfigParam"]


class BrowserReadConsoleConfigParam(TypedDict, total=False):
    """``read_console``'s config overrides."""

    defer_loading: Optional[bool]
    """Defer loading for this member.

    Must resolve to the same value on every enabled member of the toolset.
    """

    enabled: Optional[bool]
    """Whether this member is offered to the model.

    Default is per member, per the toolset's documentation. A member whose enabled
    resolves false is withheld from the served schema.
    """
