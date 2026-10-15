from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["BetaWebhookSessionUpdatedEventData"]


class BetaWebhookSessionUpdatedEventData(BaseModel):
    id: str
    """ID of the session that triggered the event."""

    organization_id: str

    type: Literal["session.updated"]

    workspace_id: str
