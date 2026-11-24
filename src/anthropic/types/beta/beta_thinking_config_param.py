from __future__ import annotations

from typing import Union
from typing_extensions import TypeAlias

from .beta_thinking_config_enabled_param import BetaThinkingConfigEnabledParam
from .beta_thinking_config_adaptive_param import BetaThinkingConfigAdaptiveParam
from .beta_thinking_config_disabled_param import BetaThinkingConfigDisabledParam
from .beta_thinking_config_between_tools_param import BetaThinkingConfigBetweenToolsParam

__all__ = ["BetaThinkingConfigParam"]

BetaThinkingConfigParam: TypeAlias = Union[
    BetaThinkingConfigEnabledParam,
    BetaThinkingConfigDisabledParam,
    BetaThinkingConfigBetweenToolsParam,
    BetaThinkingConfigAdaptiveParam,
]
"""Configuration for Claude's thinking.

With `{"type": "adaptive"}`, Claude decides when and how much to think. With `{"type": "enabled"}` (manual extended thinking), you set a `budget_tokens` of at least 1,024. Thinking tokens count toward your `max_tokens` limit.

Which `type` values are accepted, and what happens when you omit `thinking`, depend on the model. See [thinking](https://platform.claude.com/docs/en/build-with-claude/thinking#configuring-thinking) for each model's behavior.
"""
