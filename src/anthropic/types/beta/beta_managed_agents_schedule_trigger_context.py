from datetime import datetime
from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["BetaManagedAgentsScheduleTriggerContext"]


class BetaManagedAgentsScheduleTriggerContext(BaseModel):
    """The run was fired by the deployment's cron schedule."""

    scheduled_at: datetime
    """A timestamp in RFC 3339 format"""

    type: Literal["schedule"]
