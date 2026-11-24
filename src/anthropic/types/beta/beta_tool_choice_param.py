from __future__ import annotations

from typing import Union
from typing_extensions import TypeAlias

from .beta_tool_choice_any_param import BetaToolChoiceAnyParam
from .beta_tool_choice_auto_param import BetaToolChoiceAutoParam
from .beta_tool_choice_none_param import BetaToolChoiceNoneParam
from .beta_tool_choice_tool_param import BetaToolChoiceToolParam

__all__ = ["BetaToolChoiceParam"]

BetaToolChoiceParam: TypeAlias = Union[
    BetaToolChoiceAutoParam, BetaToolChoiceAnyParam, BetaToolChoiceToolParam, BetaToolChoiceNoneParam
]
"""How the model should use the provided tools.

The model can use a specific tool, any available tool, decide by itself, or not use tools at all.
"""
