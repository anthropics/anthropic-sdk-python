from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["BetaManagedAgentsSystemContentBlock"]


class BetaManagedAgentsSystemContentBlock(BaseModel):
    """Content block in a mid-conversation system message. Text-only."""

    text: str
    """The text content."""

    type: Literal["text"]
