from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaAnthropicHumanReview"]


class BetaAnthropicHumanReview(BaseModel):
    """The Workspace's human review setting."""

    type: Literal["disabled", "enabled"]
