from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaPluginOwnerOrganization"]


class BetaPluginOwnerOrganization(BaseModel):
    type: Literal["organization"]
    """The Plugin lives in a plugin marketplace the organization owns."""
