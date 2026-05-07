# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Union, Optional
from datetime import datetime
from typing_extensions import Literal, Annotated, TypeAlias

from ...._utils import PropertyInfo
from ...._models import BaseModel
from .beta_managed_agents_text_block import BetaManagedAgentsTextBlock
from .beta_managed_agents_image_block import BetaManagedAgentsImageBlock
from .beta_managed_agents_document_block import BetaManagedAgentsDocumentBlock

__all__ = ["BetaManagedAgentsAgentThreadMessageReceivedEvent", "Content"]

Content: TypeAlias = Annotated[
    Union[BetaManagedAgentsTextBlock, BetaManagedAgentsImageBlock, BetaManagedAgentsDocumentBlock],
    PropertyInfo(discriminator="type"),
]


class BetaManagedAgentsAgentThreadMessageReceivedEvent(BaseModel):
    """
    Delivery event written to the target thread's input stream when an agent-to-agent message arrives.
    """

    id: str
    """Unique identifier for this event."""

    content: List[Content]
    """Message content blocks."""

    from_session_thread_id: str
    """Public `sthr_` ID of the thread that sent the message."""

    processed_at: datetime
    """A timestamp in RFC 3339 format"""

    type: Literal["agent.thread_message_received"]

    from_agent_name: Optional[str] = None
    """Name of the callable agent this message came from.

    Absent when received from the primary agent.
    """
