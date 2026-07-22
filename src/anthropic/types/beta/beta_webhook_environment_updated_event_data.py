# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["BetaWebhookEnvironmentUpdatedEventData"]


class BetaWebhookEnvironmentUpdatedEventData(BaseModel):
    id: str
    """ID of the environment that triggered the event."""

    organization_id: str

    type: Literal["environment.updated"]

    workspace_id: str
