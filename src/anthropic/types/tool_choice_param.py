from __future__ import annotations

from typing import Union
from typing_extensions import TypeAlias

from .tool_choice_any_param import ToolChoiceAnyParam
from .tool_choice_auto_param import ToolChoiceAutoParam
from .tool_choice_none_param import ToolChoiceNoneParam
from .tool_choice_tool_param import ToolChoiceToolParam

__all__ = ["ToolChoiceParam"]

ToolChoiceParam: TypeAlias = Union[ToolChoiceAutoParam, ToolChoiceAnyParam, ToolChoiceToolParam, ToolChoiceNoneParam]
"""How the model should use the provided tools.

The model can use a specific tool, any available tool, decide by itself, or not use tools at all.
"""
