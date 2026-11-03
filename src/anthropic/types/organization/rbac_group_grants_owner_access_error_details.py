from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["RBACGroupGrantsOwnerAccessErrorDetails"]


class RBACGroupGrantsOwnerAccessErrorDetails(BaseModel):
    """
    A role attached to an RBAC Group in the request grants owner access, so this API does not add members to that group (directly or through an invite), remove its members, or delete it. Make the change in the organization's admin settings in Claude.
    """

    error_code: Literal["rbac_group_grants_owner_access"]
