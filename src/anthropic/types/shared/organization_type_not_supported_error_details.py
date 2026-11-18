from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["OrganizationTypeNotSupportedErrorDetails"]


class OrganizationTypeNotSupportedErrorDetails(BaseModel):
    """The endpoint does not support the organization's type.

    Each endpoint's description says which organization types it supports.
    """

    error_code: Literal["organization_type_not_supported"]
