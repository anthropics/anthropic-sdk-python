from typing_extensions import Literal

from ....._models import BaseModel

__all__ = ["BetaClaudeTagDeletedSlackChannel"]


class BetaClaudeTagDeletedSlackChannel(BaseModel):
    """Confirms that a Slack channel was removed from Claude Tag."""

    id: str
    """The removed channel's identifier."""

    type: Literal["slack_channel_deleted"]
