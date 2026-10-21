from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["BetaWebhookEnvironmentDeletedEventData"]


class BetaWebhookEnvironmentDeletedEventData(BaseModel):
    id: str
    """ID of the environment that triggered the event."""

    organization_id: str

    type: Literal["environment.deleted"]

    workspace_id: str
