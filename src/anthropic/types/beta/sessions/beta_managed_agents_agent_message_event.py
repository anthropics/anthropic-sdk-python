# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Union
from datetime import datetime
from typing_extensions import Literal, Annotated, TypeAlias

from ...._utils import PropertyInfo
from ...._models import BaseModel
from .beta_managed_agents_text_block import BetaManagedAgentsTextBlock
from .beta_managed_agents_redacted_block import BetaManagedAgentsRedactedBlock

__all__ = ["BetaManagedAgentsAgentMessageEvent", "Content"]

Content: TypeAlias = Annotated[
    Union[BetaManagedAgentsTextBlock, BetaManagedAgentsRedactedBlock], PropertyInfo(discriminator="type")
]


class BetaManagedAgentsAgentMessageEvent(BaseModel):
    """An agent response event in the session conversation."""

    id: str
    """Unique identifier for this event."""

    content: List[Content]
    """Array of text blocks comprising the agent response."""

    processed_at: datetime
    """A timestamp in RFC 3339 format"""

    type: Literal["agent.message"]
