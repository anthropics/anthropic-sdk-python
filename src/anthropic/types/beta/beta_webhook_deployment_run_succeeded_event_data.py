from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["BetaWebhookDeploymentRunSucceededEventData"]


class BetaWebhookDeploymentRunSucceededEventData(BaseModel):
    id: str
    """ID of the deployment run that triggered the event."""

    organization_id: str

    type: Literal["deployment_run.succeeded"]

    workspace_id: str
