from typing_extensions import Literal

from ..._exceptions import BadRequestError
from .rbac_group_owner_access_unconfirmed_error_details import RBACGroupOwnerAccessUnconfirmedErrorDetails

__all__ = ["RBACGroupOwnerAccessUnconfirmedError"]


class RBACGroupOwnerAccessUnconfirmedError(BadRequestError):
    """
    The API could not finish checking whether an RBAC Group in the request grants owner access, so it made no change. Retrying the same request will not help. Make the change in the organization's admin settings in Claude.
    """

    error_code: Literal["rbac_group_owner_access_unconfirmed"]  # pyright: ignore[reportIncompatibleVariableOverride]
    details: RBACGroupOwnerAccessUnconfirmedErrorDetails  # pyright: ignore[reportIncompatibleVariableOverride]
