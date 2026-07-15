# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["BetaWebhookDeploymentRunFailedEventData"]


class BetaWebhookDeploymentRunFailedEventData(BaseModel):
    id: str
    """ID of the deployment run that triggered the event."""

    organization_id: str

    type: Literal["deployment_run.failed"]

    workspace_id: str
