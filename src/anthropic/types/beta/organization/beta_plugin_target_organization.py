from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaPluginTargetOrganization"]


class BetaPluginTargetOrganization(BaseModel):
    type: Literal["organization"]
    """Every member of the organization."""
