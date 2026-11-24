from typing import List, Union
from typing_extensions import Literal, Annotated, TypeAlias

from ..._models import BaseModel, UnionDiscriminator
from .sessions.beta_managed_agents_text_block import BetaManagedAgentsTextBlock
from .sessions.beta_managed_agents_image_block import BetaManagedAgentsImageBlock
from .sessions.beta_managed_agents_document_block import BetaManagedAgentsDocumentBlock
from .sessions.beta_managed_agents_redacted_block import BetaManagedAgentsRedactedBlock

__all__ = ["BetaManagedAgentsDeploymentUserMessageEvent", "Content"]

Content: TypeAlias = Annotated[
    Union[
        BetaManagedAgentsTextBlock,
        BetaManagedAgentsImageBlock,
        BetaManagedAgentsDocumentBlock,
        BetaManagedAgentsRedactedBlock,
    ],
    UnionDiscriminator("type"),
]
"""Content block in a user message. Can be `text`, `image`, or `document`."""


class BetaManagedAgentsDeploymentUserMessageEvent(BaseModel):
    """A user message sent to the session."""

    content: List[Content]
    """Array of content blocks for the user message."""

    type: Literal["user.message"]
