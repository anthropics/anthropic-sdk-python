from typing import Dict, List, Optional
from typing_extensions import Literal

from ..._models import BaseModel
from .beta_cache_control_ephemeral import BetaCacheControlEphemeral

__all__ = ["BetaMemoryTool20250818"]


class BetaMemoryTool20250818(BaseModel):
    name: Literal["memory"]
    """Name of the tool.

    This is how the tool will be called by the model and in `tool_use` blocks.
    """

    type: Literal["memory_20250818"]

    allowed_callers: Optional[
        List[Literal["direct", "code_execution_20250825", "code_execution_20260120", "code_execution_20260521"]]
    ] = None

    cache_control: Optional[BetaCacheControlEphemeral] = None
    """Create a cache control breakpoint at this content block."""

    defer_loading: Optional[bool] = None
    """If true, tool will not be included in initial system prompt.

    Only loaded when returned via tool_reference from tool search.
    """

    input_examples: Optional[List[Dict[str, object]]] = None

    strict: Optional[bool] = None
    """When true, guarantees schema validation on tool names and inputs"""
