from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaManagedAgentsTextBlock"]


class BetaManagedAgentsTextBlock(BaseModel):
    """Regular text content."""

    text: str
    """The text content."""

    type: Literal["text"]
