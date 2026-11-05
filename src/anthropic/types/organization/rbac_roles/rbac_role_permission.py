from typing import Union
from typing_extensions import Literal, Annotated, TypeAlias

from ...._models import BaseModel, UnionDiscriminator
from .rbac_connector_permission_resource import RBACConnectorPermissionResource
from .rbac_organization_permission_resource import RBACOrganizationPermissionResource
from .rbac_all_connectors_permission_resource import RBACAllConnectorsPermissionResource
from .rbac_connector_tool_permission_resource import RBACConnectorToolPermissionResource
from .rbac_connector_scope_permission_resource import RBACConnectorScopePermissionResource

__all__ = ["RBACRolePermission", "Resource"]

Resource: TypeAlias = Annotated[
    Union[
        RBACOrganizationPermissionResource,
        RBACConnectorToolPermissionResource,
        RBACConnectorScopePermissionResource,
        RBACConnectorPermissionResource,
        RBACAllConnectorsPermissionResource,
    ],
    UnionDiscriminator("type"),
]


class RBACRolePermission(BaseModel):
    action: str
    """Action the permission grants on the resource.

    The vocabulary follows the resource: an `organization` grant carries a
    product-feature entitlement (for example `chat`), an admin-panel permission
    entitlement (`permission_*`), or a blanket capability-access mode —
    `capability_access_all` grants every product-feature entitlement except
    `inference_hooks_inspection`, which a role holds only through its own row, and
    `capability_access_all_ga` grants the subset of those for stable features as it
    stands at permission-check time; neither mode grants model-access entitlements.
    A consumer enumerating a role's per-feature grants should treat a blanket row as
    granting every product-feature entitlement it covers, or it will under-report
    the role's effective access. A `connector_tool` grant carries a tool-access
    action (`use` or `always_allow`); a `connector_scope` grant carries the scope
    action `grant` (the role may receive the named OAuth scope when tokens are
    minted for the connector); `connector` and `all_connectors` grants carry a
    tool-access action, the scope action, or an authentication-method action
    (`interactive` or `managed`).
    """

    resource: Resource
    """What the permission applies to.

    A tagged union: `type` names the kind of resource and determines which
    identifier fields are present.
    """

    type: Literal["rbac_role_permission"]
    """Object type.

    For RBAC Role Permissions, this is always `"rbac_role_permission"`.
    """
