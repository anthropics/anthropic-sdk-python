from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["BetaWebhookSessionPendingEventData"]


class BetaWebhookSessionPendingEventData(BaseModel):
    id: str
    """ID of the session that triggered the event."""

    organization_id: str

    type: Literal["session.pending"]

    workspace_id: str
