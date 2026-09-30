from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaSpendLimitRBACGroupScope"]


class BetaSpendLimitRBACGroupScope(BaseModel):
    rbac_group_id: str

    type: Literal["rbac_group"]
