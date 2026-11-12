from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["RBACRoleNotFoundErrorDetails"]


class RBACRoleNotFoundErrorDetails(BaseModel):
    """No RBAC Role with this ID was found."""

    error_code: Literal["rbac_role_not_found"]
