# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Union
from typing_extensions import Annotated, TypeAlias

from ..._utils import PropertyInfo
from .beta_output_behavior_create_new import BetaOutputBehaviorCreateNew
from .beta_output_behavior_update_existing import BetaOutputBehaviorUpdateExisting

__all__ = ["BetaOutputBehavior"]

BetaOutputBehavior: TypeAlias = Annotated[
    Union[BetaOutputBehaviorCreateNew, BetaOutputBehaviorUpdateExisting], PropertyInfo(discriminator="type")
]
