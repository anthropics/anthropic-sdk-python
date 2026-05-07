# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["BetaWebhookVaultCreatedEventData"]


class BetaWebhookVaultCreatedEventData(BaseModel):
    id: str
    """ID of the resource that triggered the event."""

    organization_id: str

    type: Literal["vault.created"]

    workspace_id: str
