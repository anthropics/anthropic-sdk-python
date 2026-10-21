from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["BetaManagedAgentsCommitCheckout"]


class BetaManagedAgentsCommitCheckout(BaseModel):
    sha: str
    """Full commit SHA to check out."""

    type: Literal["commit"]
