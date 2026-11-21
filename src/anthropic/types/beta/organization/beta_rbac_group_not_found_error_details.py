from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaRBACGroupNotFoundErrorDetails"]


class BetaRBACGroupNotFoundErrorDetails(BaseModel):
    """The RBAC Group is not one of the organization's groups."""

    error_code: Literal["rbac_group_not_found"]
