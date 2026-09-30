from typing_extensions import Literal

from ....._models import BaseModel

__all__ = ["BetaRBACConnectorPermissionResource"]


class BetaRBACConnectorPermissionResource(BaseModel):
    connector_id: str
    """ID of the connector the permission applies to."""

    type: Literal["connector"]
    """Kind of resource the permission applies to."""
