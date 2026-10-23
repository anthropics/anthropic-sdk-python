from typing import Optional
from datetime import datetime
from typing_extensions import Literal

from ....._models import BaseModel

__all__ = ["BetaClaudeTagBundle"]


class BetaClaudeTagBundle(BaseModel):
    """
    A named set of access that Claude can use in a Slack channel or a Slack workspace: connectors, repositories and credentials. Created and edited in claude.ai.
    """

    id: str
    """The Bundle's identifier. Starts with `capp_`."""

    created_at: datetime
    """Time the Bundle was created."""

    description: Optional[str] = None
    """What the Bundle is for. Null when it has none. Read-only."""

    display_name: str
    """The Bundle's name. Always set. Read-only."""

    type: Literal["bundle"]

    updated_at: datetime
    """Time of the last change to the Bundle."""
