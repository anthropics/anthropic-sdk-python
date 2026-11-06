from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["RBACGroupOwnerAccessUnconfirmedErrorDetails"]


class RBACGroupOwnerAccessUnconfirmedErrorDetails(BaseModel):
    """
    The API could not finish checking whether an RBAC Group in the request grants owner access, so it made no change. Retrying the same request will not help. Make the change in the organization's admin settings in Claude.
    """

    error_code: Literal["rbac_group_owner_access_unconfirmed"]
