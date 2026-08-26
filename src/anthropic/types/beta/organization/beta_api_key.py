# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Union, Optional
from datetime import datetime
from typing_extensions import Literal, Annotated, TypeAlias

from ...._utils import PropertyInfo
from ...._models import BaseModel
from .beta_api_key_created_by import BetaAPIKeyCreatedBy
from .beta_api_key_user_actor import BetaAPIKeyUserActor
from .beta_api_key_workspace_scope import BetaAPIKeyWorkspaceScope
from .beta_api_key_organization_scope import BetaAPIKeyOrganizationScope
from .beta_api_key_service_account_actor import BetaAPIKeyServiceAccountActor

__all__ = ["BetaAPIKey", "Principal", "Scope"]

Principal: TypeAlias = Annotated[
    Union[BetaAPIKeyUserActor, BetaAPIKeyServiceAccountActor, None], PropertyInfo(discriminator="type")
]

Scope: TypeAlias = Annotated[
    Union[BetaAPIKeyOrganizationScope, BetaAPIKeyWorkspaceScope], PropertyInfo(discriminator="type")
]


class BetaAPIKey(BaseModel):
    id: str
    """ID of the API key."""

    created_at: datetime
    """RFC 3339 datetime string indicating when the API Key was created."""

    created_by: Optional[BetaAPIKeyCreatedBy] = None
    """
    The ID and type of the actor that created the API key, or `null` when the
    creator is not recorded (legacy, workload-identity-federated, or system-created
    keys).
    """

    expires_at: Optional[datetime] = None
    """
    RFC 3339 datetime string indicating when the API Key expires, or `null` if it
    never expires.
    """

    name: str
    """Name of the API key."""

    partial_key_hint: Optional[str] = None
    """Partially redacted hint for the API key."""

    principal: Optional[Principal] = None
    """
    The principal the API key acts as (a User or a Service Account), or `null` if
    the API key is not bound to a principal.
    """

    scope: Scope
    """
    Where the API key belongs: its Workspace
    (`{"type": "workspace", "workspace_id": "wrkspc_..."}`, with the Workspace's
    real ID even when it is the organization's default Workspace), or the
    organization (`{"type": "organization"}`) for a principal-bound API key that has
    no Workspace.
    """

    status: Literal["active", "archived", "expired", "inactive"]
    """Status of the API key."""

    type: Literal["api_key"]
    """Object type.

    For API Keys, this is always `"api_key"`.
    """

    workspace_id: Optional[str] = None
    """Deprecated: use `scope` instead.

    ID of the Workspace associated with the API key, or `null` if the API key
    belongs to the default Workspace. Also `null` for a principal-bound API key that
    has no Workspace; `scope` tells the two apart.
    """
