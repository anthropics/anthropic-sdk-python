from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["RBACRoleSourceBuiltIn"]


class RBACRoleSourceBuiltIn(BaseModel):
    type: Literal["built_in"]
    """
    Anthropic provisions the RBAC Role, and the organization's administrators cannot
    change or delete it.
    """
