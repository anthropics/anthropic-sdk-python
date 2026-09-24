from __future__ import annotations

from typing import Union
from typing_extensions import Literal, Required, TypeAlias, TypedDict

from .thinking_config_enabled_param import ThinkingConfigEnabledParam
from .thinking_config_adaptive_param import ThinkingConfigAdaptiveParam
from .thinking_config_disabled_param import ThinkingConfigDisabledParam

__all__ = ["ThinkingConfigParam", "ThinkingConfigBetweenTools"]


class ThinkingConfigBetweenTools(TypedDict, total=False):
    type: Required[Literal["between_tools"]]


ThinkingConfigParam: TypeAlias = Union[
    ThinkingConfigEnabledParam, ThinkingConfigDisabledParam, ThinkingConfigBetweenTools, ThinkingConfigAdaptiveParam
]
