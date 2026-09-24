from __future__ import annotations

from typing import Union
from typing_extensions import Literal, Required, TypeAlias, TypedDict

from .beta_thinking_config_enabled_param import BetaThinkingConfigEnabledParam
from .beta_thinking_config_adaptive_param import BetaThinkingConfigAdaptiveParam
from .beta_thinking_config_disabled_param import BetaThinkingConfigDisabledParam

__all__ = ["BetaThinkingConfigParam", "BetaThinkingConfigBetweenTools"]


class BetaThinkingConfigBetweenTools(TypedDict, total=False):
    type: Required[Literal["between_tools"]]


BetaThinkingConfigParam: TypeAlias = Union[
    BetaThinkingConfigEnabledParam,
    BetaThinkingConfigDisabledParam,
    BetaThinkingConfigBetweenTools,
    BetaThinkingConfigAdaptiveParam,
]
