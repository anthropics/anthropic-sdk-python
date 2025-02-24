# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union
from typing_extensions import TypeAlias

from .tool_param import ToolParam
from .tool_bash_20250124_param import ToolBash20250124Param
from .tool_text_editor_20250124_param import ToolTextEditor20250124Param

__all__ = ["ToolUnionParam"]

ToolUnionParam: TypeAlias = Union[ToolBash20250124Param, ToolTextEditor20250124Param, ToolParam]
