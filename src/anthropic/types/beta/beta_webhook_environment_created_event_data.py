from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["BetaWebhookEnvironmentCreatedEventData"]


class BetaWebhookEnvironmentCreatedEventData(BaseModel):
    id: str
    """ID of the environment that triggered the event."""

    organization_id: str

    type: Literal["environment.created"]

    workspace_id: str
