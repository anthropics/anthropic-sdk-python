from typing import Union, Optional
from datetime import datetime
from typing_extensions import Literal, Annotated, TypeAlias

from ..._models import BaseModel, UnionDiscriminator
from .api_key_created_by import APIKeyCreatedBy
from .api_key_user_actor import APIKeyUserActor
from .api_key_workspace_scope import APIKeyWorkspaceScope
from .api_key_organization_scope import APIKeyOrganizationScope
from .api_key_service_account_actor import APIKeyServiceAccountActor

__all__ = ["APIKey", "Principal", "Scope"]

Principal: TypeAlias = Annotated[Union[APIKeyUserActor, APIKeyServiceAccountActor, None], UnionDiscriminator("type")]

Scope: TypeAlias = Annotated[Union[APIKeyOrganizationScope, APIKeyWorkspaceScope], UnionDiscriminator("type")]


class APIKey(BaseModel):
    id: str
    """ID of the API key."""

    created_at: datetime
    """RFC 3339 datetime string indicating when the API Key was created."""

    created_by: Optional[APIKeyCreatedBy] = None
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
