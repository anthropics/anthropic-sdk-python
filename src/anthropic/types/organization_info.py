from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["OrganizationInfo"]


class OrganizationInfo(BaseModel):
    id: str
    """ID of the Organization."""

    name: str
    """Name of the Organization."""

    type: Literal["organization"]
    """Object type.

    For Organizations, this is always `"organization"`.
    """
