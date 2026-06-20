# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable
from typing_extensions import Literal, Required, TypedDict

from ..beta_managed_agents_system_content_block_param import BetaManagedAgentsSystemContentBlockParam

__all__ = ["BetaManagedAgentsSystemMessageEventParams"]


class BetaManagedAgentsSystemMessageEventParams(TypedDict, total=False):
    """
    Privileged context for the accompanying turn and all subsequent turns, appended to the session's system context as a `role: "system"` turn rather than replacing the top-level system prompt. At most one per request: it must be the final event and immediately follow the `user.message`, `user.tool_result`, or `user.custom_tool_result` it accompanies. Only supported on models that accept mid-conversation system messages.
    """

    content: Required[Iterable[BetaManagedAgentsSystemContentBlockParam]]
    """System content blocks to append. Text-only."""

    type: Required[Literal["system.message"]]
