from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["BetaWebhookSessionStatusTerminatedEventData"]


class BetaWebhookSessionStatusTerminatedEventData(BaseModel):
    id: str
    """ID of the session that triggered the event."""

    organization_id: str

    type: Literal["session.status_terminated"]

    workspace_id: str
