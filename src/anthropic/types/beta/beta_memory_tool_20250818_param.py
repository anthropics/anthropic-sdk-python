# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import Literal, Required, TypedDict

from .beta_cache_control_ephemeral_param import BetaCacheControlEphemeralParam

__all__ = ["BetaMemoryTool20250818Param"]


class BetaMemoryTool20250818Param(TypedDict, total=False):
    name: Required[Literal["memory"]]
    """Name of the tool.

    This is how the tool will be called by the model and in `tool_use` blocks.
    """

    type: Required[Literal["memory_20250818"]]

    cache_control: Optional[BetaCacheControlEphemeralParam]
    """Create a cache control breakpoint at this content block."""
