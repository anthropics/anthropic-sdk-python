# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["BetaWebhookDeploymentArchivedEventData"]


class BetaWebhookDeploymentArchivedEventData(BaseModel):
    id: str
    """ID of the deployment that triggered the event."""

    organization_id: str

    type: Literal["deployment.archived"]

    workspace_id: str
