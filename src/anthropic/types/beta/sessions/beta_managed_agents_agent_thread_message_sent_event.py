# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Union, Optional
from datetime import datetime
from typing_extensions import Literal, Annotated, TypeAlias

from ...._utils import PropertyInfo
from ...._models import BaseModel
from .beta_managed_agents_text_block import BetaManagedAgentsTextBlock
from .beta_managed_agents_image_block import BetaManagedAgentsImageBlock
from .beta_managed_agents_document_block import BetaManagedAgentsDocumentBlock

__all__ = ["BetaManagedAgentsAgentThreadMessageSentEvent", "Content"]

Content: TypeAlias = Annotated[
    Union[BetaManagedAgentsTextBlock, BetaManagedAgentsImageBlock, BetaManagedAgentsDocumentBlock],
    PropertyInfo(discriminator="type"),
]


class BetaManagedAgentsAgentThreadMessageSentEvent(BaseModel):
    """
    Observability event emitted to the sender's output stream when an agent-to-agent message is sent.
    """

    id: str
    """Unique identifier for this event."""

    content: List[Content]
    """Message content blocks."""

    processed_at: datetime
    """A timestamp in RFC 3339 format"""

    to_session_thread_id: str
    """Public `sthr_` ID of the thread the message was sent to."""

    type: Literal["agent.thread_message_sent"]

    to_agent_name: Optional[str] = None
    """Name of the callable agent this message was sent to.

    Absent when sent to the primary agent.
    """
