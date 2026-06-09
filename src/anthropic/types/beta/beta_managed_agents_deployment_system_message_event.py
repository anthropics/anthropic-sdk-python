# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List
from typing_extensions import Literal

from ..._models import BaseModel
from .beta_managed_agents_system_content_block import BetaManagedAgentsSystemContentBlock

__all__ = ["BetaManagedAgentsDeploymentSystemMessageEvent"]


class BetaManagedAgentsDeploymentSystemMessageEvent(BaseModel):
    """
    Privileged context for the accompanying turn and all subsequent turns, appended to the session's system context as a `role: "system"` turn rather than replacing the top-level system prompt.
    """

    content: List[BetaManagedAgentsSystemContentBlock]
    """System content blocks to append. Text-only."""

    type: Literal["system.message"]
