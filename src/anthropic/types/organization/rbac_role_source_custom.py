from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["RBACRoleSourceCustom"]


class RBACRoleSourceCustom(BaseModel):
    type: Literal["custom"]
    """The organization's administrators can change and delete the RBAC Role."""
