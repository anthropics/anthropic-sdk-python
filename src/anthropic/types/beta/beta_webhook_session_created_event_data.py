from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["BetaWebhookSessionCreatedEventData"]


class BetaWebhookSessionCreatedEventData(BaseModel):
    id: str
    """ID of the session that triggered the event."""

    organization_id: str

    type: Literal["session.created"]

    workspace_id: str
