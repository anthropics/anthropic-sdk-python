from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["BetaManagedAgentsSystemContentBlock"]


class BetaManagedAgentsSystemContentBlock(BaseModel):
    """Regular text content."""

    text: str
    """The text content."""

    type: Literal["text"]
