# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import Literal, Required, TypedDict

__all__ = ["BetaManagedAgentsUserInterruptEventParams"]


class BetaManagedAgentsUserInterruptEventParams(TypedDict, total=False):
    """Parameters for sending an interrupt to pause the agent."""

    type: Required[Literal["user.interrupt"]]

    session_thread_id: Optional[str]
    """
    If absent, interrupts every non-archived thread in a multiagent session (or the
    primary alone in a single-agent session). If present, interrupts only the named
    thread.
    """
