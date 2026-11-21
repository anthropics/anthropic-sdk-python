from typing import Union
from typing_extensions import Annotated, TypeAlias

from ...._models import UnionDiscriminator
from .beta_rbac_role_source_custom import BetaRBACRoleSourceCustom
from .beta_rbac_role_source_built_in import BetaRBACRoleSourceBuiltIn

__all__ = ["BetaRBACRoleSource"]

BetaRBACRoleSource: TypeAlias = Annotated[
    Union[BetaRBACRoleSourceBuiltIn, BetaRBACRoleSourceCustom], UnionDiscriminator("type")
]
