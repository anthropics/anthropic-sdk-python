# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Union
from typing_extensions import Literal, Annotated, TypeAlias

from ..._utils import PropertyInfo
from ..._models import BaseModel
from .sessions.beta_managed_agents_text_block import BetaManagedAgentsTextBlock
from .sessions.beta_managed_agents_image_block import BetaManagedAgentsImageBlock
from .sessions.beta_managed_agents_document_block import BetaManagedAgentsDocumentBlock

__all__ = ["BetaManagedAgentsDeploymentUserMessageEvent", "Content"]

Content: TypeAlias = Annotated[
    Union[BetaManagedAgentsTextBlock, BetaManagedAgentsImageBlock, BetaManagedAgentsDocumentBlock],
    PropertyInfo(discriminator="type"),
]


class BetaManagedAgentsDeploymentUserMessageEvent(BaseModel):
    """A user message sent to the session."""

    content: List[Content]
    """Array of content blocks for the user message."""

    type: Literal["user.message"]
