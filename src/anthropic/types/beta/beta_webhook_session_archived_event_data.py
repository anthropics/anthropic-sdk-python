from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["BetaWebhookSessionArchivedEventData"]


class BetaWebhookSessionArchivedEventData(BaseModel):
    id: str
    """ID of the session that triggered the event."""

    organization_id: str

    type: Literal["session.archived"]

    workspace_id: str
