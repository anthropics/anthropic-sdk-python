from __future__ import annotations

from typing import Union
from typing_extensions import TypeAlias

from .thinking_config_enabled_param import ThinkingConfigEnabledParam
from .thinking_config_adaptive_param import ThinkingConfigAdaptiveParam
from .thinking_config_disabled_param import ThinkingConfigDisabledParam
from .thinking_config_between_tools_param import ThinkingConfigBetweenToolsParam

__all__ = ["ThinkingConfigParam"]

ThinkingConfigParam: TypeAlias = Union[
    ThinkingConfigEnabledParam,
    ThinkingConfigDisabledParam,
    ThinkingConfigBetweenToolsParam,
    ThinkingConfigAdaptiveParam,
]
