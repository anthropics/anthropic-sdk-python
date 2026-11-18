from typing import Union
from typing_extensions import Annotated, TypeAlias

from ....._models import UnionDiscriminator
from ..beta_spend_limit_user_actor import BetaSpendLimitUserActor
from ..beta_spend_limit_scoped_api_key_actor import BetaSpendLimitScopedAPIKeyActor

__all__ = ["BetaSpendLimitIncreaseRequestActor"]

BetaSpendLimitIncreaseRequestActor: TypeAlias = Annotated[
    Union[BetaSpendLimitUserActor, BetaSpendLimitScopedAPIKeyActor], UnionDiscriminator("type")
]
