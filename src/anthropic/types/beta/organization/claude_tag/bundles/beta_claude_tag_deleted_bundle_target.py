from typing_extensions import Literal

from ......_models import BaseModel

__all__ = ["BetaClaudeTagDeletedBundleTarget"]


class BetaClaudeTagDeletedBundleTarget(BaseModel):
    """Confirms that a Bundle was detached."""

    id: str
    """The identifier the Bundle Target had."""

    type: Literal["bundle_target_deleted"]
