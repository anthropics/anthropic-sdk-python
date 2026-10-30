from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["SpendLimitRBACGroupScope"]


class SpendLimitRBACGroupScope(BaseModel):
    rbac_group_id: str

    type: Literal["rbac_group"]
