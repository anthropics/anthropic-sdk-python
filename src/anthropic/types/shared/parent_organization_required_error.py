from typing_extensions import Literal

from ..._exceptions import BadRequestError
from .parent_organization_required_error_details import ParentOrganizationRequiredErrorDetails

__all__ = ["ParentOrganizationRequiredError"]


class ParentOrganizationRequiredError(BadRequestError):
    """
    The endpoint serves only organizations that belong to a parent organization, and this organization belongs to none.
    """

    error_code: Literal["parent_organization_required"]  # pyright: ignore[reportIncompatibleVariableOverride]
    details: ParentOrganizationRequiredErrorDetails  # pyright: ignore[reportIncompatibleVariableOverride]
