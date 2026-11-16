from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["ParentOrganizationRequiredErrorDetails"]


class ParentOrganizationRequiredErrorDetails(BaseModel):
    """
    The endpoint serves only organizations that belong to a parent organization, and this organization belongs to none.
    """

    error_code: Literal["parent_organization_required"]
