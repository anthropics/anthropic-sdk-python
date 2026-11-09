from typing_extensions import Literal

from ....._models import BaseModel

__all__ = ["BetaRBACConnectorScopePermissionResource"]


class BetaRBACConnectorScopePermissionResource(BaseModel):
    connector_id: str
    """ID of the connector the permission applies to."""

    scope: str
    """
    OAuth scope the permission names — the role may receive this scope when tokens
    are minted for the connector.

    Subject to the same encoding rule as `tool_name`: a scope containing characters
    outside `[a-zA-Z0-9_-]` (or colliding with a reserved form) appears
    server-encoded in a stable `{prefix}_{32-hex}` form. OAuth scopes routinely
    contain `:` and `/`, so most appear encoded.
    """

    type: Literal["connector_scope"]
    """Kind of resource the permission applies to."""
