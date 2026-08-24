# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["BetaBrowserStateChangeTabOpenedParam"]


class BetaBrowserStateChangeTabOpenedParam(TypedDict, total=False):
    """
    A tab this call's execution opened that remains open at its end —
    the creation delta of the `tabs` inventory, not an event log.

    Carries only the `tab_id`; the tab's `title` and `url` live on its
    `tabs` entry, which must include the same `tab_id`. A tab opened
    during a failed call gets no deferred `tab_opened`; it simply appears
    in the next result's `tabs` inventory.
    """

    tab_id: Required[str]
    """The `tab_id` of the opened tab, present in `tabs`."""

    type: Required[Literal["tab_opened"]]
