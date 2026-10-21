from typing import Optional
from typing_extensions import Literal

from ..._models import BaseModel
from .sessions.beta_managed_agents_text_block import BetaManagedAgentsTextBlock

__all__ = ["BetaManagedAgentsDeltaContent"]


class BetaManagedAgentsDeltaContent(BaseModel):
    content: BetaManagedAgentsTextBlock
    """
    A partial element of the content array at index, typed like the element itself —
    the same shape the buffered agent.message carries in content.
    """

    type: Literal["content_delta"]

    index: Optional[int] = None
    """Which entry in the previewed event's content array this fragment lands in.

    Insert content as that entry when the index is new; append to the existing entry
    otherwise.
    """
