from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaDeletedOrganizationWebhookEndpoint"]


class BetaDeletedOrganizationWebhookEndpoint(BaseModel):
    """A deleted organization webhook endpoint."""

    id: str
    """ID of the deleted webhook endpoint."""

    type: Literal["webhook_endpoint_deleted"]
    """Always `webhook_endpoint_deleted`."""
