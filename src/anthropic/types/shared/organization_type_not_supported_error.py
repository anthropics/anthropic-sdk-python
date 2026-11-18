from typing_extensions import Literal

from ..._exceptions import BadRequestError
from .organization_type_not_supported_error_details import OrganizationTypeNotSupportedErrorDetails

__all__ = ["OrganizationTypeNotSupportedError"]


class OrganizationTypeNotSupportedError(BadRequestError):
    """The endpoint does not support the organization's type.

    Each endpoint's description says which organization types it supports.
    """

    error_code: Literal["organization_type_not_supported"]  # pyright: ignore[reportIncompatibleVariableOverride]
    details: OrganizationTypeNotSupportedErrorDetails  # pyright: ignore[reportIncompatibleVariableOverride]
