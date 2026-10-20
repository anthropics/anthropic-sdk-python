from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["UserProfileEfsFeature"]


class UserProfileEfsFeature(BaseModel):
    """One feature of Enterprise Frontier Safeguards."""

    status: Literal["active", "inactive"]
    """
    `active` when Anthropic has approved the entity the profile represents to use
    the feature, otherwise `inactive`. `active` does not mean that the feature is
    set up or switched on, which is a separate step.
    """
