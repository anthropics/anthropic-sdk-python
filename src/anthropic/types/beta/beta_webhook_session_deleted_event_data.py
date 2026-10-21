from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["BetaWebhookSessionDeletedEventData"]


class BetaWebhookSessionDeletedEventData(BaseModel):
    id: str
    """ID of the session that triggered the event."""

    organization_id: str

    type: Literal["session.deleted"]

    workspace_id: str
