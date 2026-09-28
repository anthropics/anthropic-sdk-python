from typing import List, Union, Optional
from datetime import datetime
from typing_extensions import Literal, Annotated, TypeAlias

from ...._models import BaseModel, UnionDiscriminator
from .beta_managed_agents_text_block import BetaManagedAgentsTextBlock
from .beta_managed_agents_image_block import BetaManagedAgentsImageBlock
from .beta_managed_agents_document_block import BetaManagedAgentsDocumentBlock
from .beta_managed_agents_search_result_block import BetaManagedAgentsSearchResultBlock

__all__ = ["BetaManagedAgentsAgentMCPToolResultEvent", "Content"]

Content: TypeAlias = Annotated[
    Union[
        BetaManagedAgentsTextBlock,
        BetaManagedAgentsImageBlock,
        BetaManagedAgentsDocumentBlock,
        BetaManagedAgentsSearchResultBlock,
    ],
    UnionDiscriminator("type"),
]


class BetaManagedAgentsAgentMCPToolResultEvent(BaseModel):
    """Event representing the result of an MCP tool execution."""

    id: str
    """Unique identifier for this event."""

    mcp_tool_use_id: str
    """The id of the `agent.mcp_tool_use` event this result corresponds to."""

    processed_at: datetime
    """Timestamp when this event was processed."""

    type: Literal["agent.mcp_tool_result"]

    content: Optional[List[Content]] = None
    """The result content returned by the tool."""

    is_error: Optional[bool] = None
    """Whether the tool execution resulted in an error."""
