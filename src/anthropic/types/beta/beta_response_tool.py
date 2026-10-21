from typing import Dict, List, Optional
from typing_extensions import Literal

from ..._models import BaseModel
from .beta_response_tool_input_schema import BetaResponseToolInputSchema

__all__ = ["BetaResponseTool"]


class BetaResponseTool(BaseModel):
    """A custom tool definition, as sent."""

    input_schema: BetaResponseToolInputSchema
    """[JSON schema](https://json-schema.org/draft/2020-12) for this tool's input.

    This defines the shape of the `input` that your tool accepts and that the model
    will produce.
    """

    name: str
    """Name of the tool.

    This is how the tool will be called by the model and in `tool_use` blocks.
    """

    allowed_callers: Optional[
        List[Literal["direct", "code_execution_20250825", "code_execution_20260120", "code_execution_20260521"]]
    ] = None

    defer_loading: Optional[bool] = None
    """If true, tool will not be included in initial system prompt.

    Only loaded when returned via tool_reference from tool search.
    """

    description: Optional[str] = None
    """Description of what this tool does.

    Tool descriptions should be as detailed as possible. The more information that
    the model has about what the tool is and how to use it, the better it will
    perform. You can use natural language descriptions to reinforce important
    aspects of the tool input JSON schema.
    """

    eager_input_streaming: Optional[bool] = None
    """Enable eager input streaming for this tool.

    When true, tool input parameters will be streamed incrementally as they are
    generated, and types will be inferred on-the-fly rather than buffering the full
    JSON output. When false, streaming is disabled for this tool even if the
    fine-grained-tool-streaming beta is active. When null (default), uses the
    default behavior based on beta headers.
    """

    input_examples: Optional[List[Dict[str, object]]] = None

    strict: Optional[bool] = None
    """When true, guarantees schema validation on tool names and inputs"""

    type: Optional[Literal["custom"]] = None
