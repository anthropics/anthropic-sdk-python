from typing_extensions import Literal

from .._exceptions import NotFoundError
from .rbac_role_not_found_error_details import RBACRoleNotFoundErrorDetails

__all__ = ["RBACRoleNotFoundError"]


class RBACRoleNotFoundError(NotFoundError):
    """No RBAC Role with this ID was found."""

    error_code: Literal["rbac_role_not_found"]  # pyright: ignore[reportIncompatibleVariableOverride]
    details: RBACRoleNotFoundErrorDetails  # pyright: ignore[reportIncompatibleVariableOverride]
