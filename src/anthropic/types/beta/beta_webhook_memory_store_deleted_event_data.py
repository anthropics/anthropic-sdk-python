# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["BetaWebhookMemoryStoreDeletedEventData"]


class BetaWebhookMemoryStoreDeletedEventData(BaseModel):
    id: str
    """ID of the memory store that triggered the event."""

    organization_id: str

    type: Literal["memory_store.deleted"]

    workspace_id: str
