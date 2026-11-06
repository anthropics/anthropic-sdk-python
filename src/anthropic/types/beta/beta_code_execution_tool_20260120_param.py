from __future__ import annotations

from typing import List, Optional
from typing_extensions import Literal, Required, TypedDict

from .beta_cache_control_ephemeral_param import BetaCacheControlEphemeralParam

__all__ = ["BetaCodeExecutionTool20260120Param"]


class BetaCodeExecutionTool20260120Param(TypedDict, total=False):
    """A `tools` entry for the code execution tool, version `code_execution_20260120`.

    It adds REPL state persistence to version `code_execution_20250825`.

    REPL state persistence applies with programmatic tool calling. With it, the Python interpreter state, such as variable bindings, persists across requests that reuse the container.

    See the [code execution tool guide](https://platform.claude.com/docs/en/agents-and-tools/tool-use/code-execution-tool#tool-versions) to learn what each tool version adds.
    """

    name: Required[Literal["code_execution"]]
    """Name of the tool.

    This is how the tool will be called by the model and in `tool_use` blocks.
    """

    type: Required[Literal["code_execution_20260120"]]

    allowed_callers: List[
        Literal["direct", "code_execution_20250825", "code_execution_20260120", "code_execution_20260521"]
    ]

    cache_control: Optional[BetaCacheControlEphemeralParam]
    """Create a cache control breakpoint at this content block."""

    defer_loading: bool
    """If true, tool will not be included in initial system prompt.

    Only loaded when returned via tool_reference from tool search.
    """

    strict: bool
    """When true, guarantees schema validation on tool names and inputs"""
