from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["BetaWebhookSessionRunningEventData"]


class BetaWebhookSessionRunningEventData(BaseModel):
    id: str
    """ID of the session that triggered the event."""

    organization_id: str

    type: Literal["session.running"]

    workspace_id: str
