from __future__ import annotations

from typing import Union
from typing_extensions import TypeAlias

from .beta_output_behavior_create_new_param import BetaOutputBehaviorCreateNewParam
from .beta_output_behavior_update_existing_param import BetaOutputBehaviorUpdateExistingParam

__all__ = ["BetaOutputBehaviorParam"]

BetaOutputBehaviorParam: TypeAlias = Union[BetaOutputBehaviorCreateNewParam, BetaOutputBehaviorUpdateExistingParam]
