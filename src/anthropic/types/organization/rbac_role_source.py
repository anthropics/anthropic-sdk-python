from typing import Union
from typing_extensions import Annotated, TypeAlias

from ..._models import UnionDiscriminator
from .rbac_role_source_custom import RBACRoleSourceCustom
from .rbac_role_source_built_in import RBACRoleSourceBuiltIn

__all__ = ["RBACRoleSource"]

RBACRoleSource: TypeAlias = Annotated[Union[RBACRoleSourceBuiltIn, RBACRoleSourceCustom], UnionDiscriminator("type")]
