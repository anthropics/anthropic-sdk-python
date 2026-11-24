from typing import Dict, Optional
from typing_extensions import Literal

from ....._models import BaseModel
from ...beta_message import BetaMessage

__all__ = ["BetaComplianceReviewCreateMessageContent"]


class BetaComplianceReviewCreateMessageContent(BaseModel):
    """A request to create a message, and its response."""

    request: Dict[str, object]
    """
    The `POST /v1/messages` request body, without thinking blocks or unpublished
    fields. For a user's message from an Anthropic app, such as Claude Code,
    `system` is a placeholder.
    """

    response: Optional[BetaMessage] = None
    """The model's `Message`, without thinking blocks or unpublished fields.

    Null when no response was stored, for example because the client disconnected.
    """

    type: Literal["create_message"]
