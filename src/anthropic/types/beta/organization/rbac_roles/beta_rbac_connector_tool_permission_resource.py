from typing_extensions import Literal

from ....._models import BaseModel

__all__ = ["BetaRBACConnectorToolPermissionResource"]


class BetaRBACConnectorToolPermissionResource(BaseModel):
    connector_id: str
    """ID of the connector the permission applies to."""

    tool_name: str
    """Published name of the connector tool the permission applies to.

    When the published name contains characters outside `[a-zA-Z0-9_-]` (or collides
    with a reserved form), it is server-encoded into a stable `{prefix}_{32-hex}`
    form — a shortened readable prefix of the name plus a hash — from which the
    published name is not recoverable.
    """

    type: Literal["connector_tool"]
    """Kind of resource the permission applies to."""
