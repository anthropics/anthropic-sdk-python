from datetime import datetime
from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["BetaManagedAgentsScheduleTriggerContext"]


class BetaManagedAgentsScheduleTriggerContext(BaseModel):
    """The run was fired by the deployment's cron schedule."""

    scheduled_at: datetime
    """
    The UTC instant at which the cron expression matched in the configured timezone,
    before jitter is applied. At most one run is recorded per (`deployment_id`,
    `scheduled_at`) pair.
    """

    type: Literal["schedule"]
