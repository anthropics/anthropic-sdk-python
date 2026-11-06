from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaClaudeTagSlackDefaultSettingSource"]


class BetaClaudeTagSlackDefaultSettingSource(BaseModel):
    """
    The value comes from the organization's Slack defaults, which have no identifier.
    """

    type: Literal["slack_default"]
