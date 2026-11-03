from typing import Union
from typing_extensions import Annotated, TypeAlias

from ...._models import UnionDiscriminator
from ..spend_limit_user_actor import SpendLimitUserActor
from ..spend_limit_scoped_api_key_actor import SpendLimitScopedAPIKeyActor

__all__ = ["SpendLimitIncreaseRequestResolvedBy"]

SpendLimitIncreaseRequestResolvedBy: TypeAlias = Annotated[
    Union[SpendLimitUserActor, SpendLimitScopedAPIKeyActor], UnionDiscriminator("type")
]
