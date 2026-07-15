# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["BetaWebhookAgentCreatedEventData"]


class BetaWebhookAgentCreatedEventData(BaseModel):
    id: str
    """ID of the agent that triggered the event."""

    organization_id: str

    type: Literal["agent.created"]

    workspace_id: str
