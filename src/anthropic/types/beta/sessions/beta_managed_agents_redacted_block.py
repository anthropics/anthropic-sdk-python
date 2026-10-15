from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaManagedAgentsRedactedBlock"]


class BetaManagedAgentsRedactedBlock(BaseModel):
    """Placeholder for content withheld by Anthropic model policy."""

    type: Literal["redacted"]
