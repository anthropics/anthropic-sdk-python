from typing_extensions import Literal

from ..._exceptions import BadRequestError
from .rbac_group_grants_owner_access_error_details import RBACGroupGrantsOwnerAccessErrorDetails

__all__ = ["RBACGroupGrantsOwnerAccessError"]


class RBACGroupGrantsOwnerAccessError(BadRequestError):
    """
    A role attached to an RBAC Group in the request grants owner access, so this API does not add members to that group (directly or through an invite), remove its members, or delete it. Make the change in the organization's admin settings in Claude.
    """

    error_code: Literal["rbac_group_grants_owner_access"]  # pyright: ignore[reportIncompatibleVariableOverride]
    details: RBACGroupGrantsOwnerAccessErrorDetails  # pyright: ignore[reportIncompatibleVariableOverride]
