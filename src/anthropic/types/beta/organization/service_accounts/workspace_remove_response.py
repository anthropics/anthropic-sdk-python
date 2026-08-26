# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing_extensions import Literal

from ....._models import BaseModel

__all__ = ["WorkspaceRemoveResponse"]


class WorkspaceRemoveResponse(BaseModel):
    service_account_id: str
    """Tagged service account ID (`svac_...`) named in the delete request.

    Removal is idempotent; see the endpoint description for the implicit-membership
    no-op.
    """

    type: Literal["service_account_workspace_member_deleted"]

    workspace_id: str
    """Tagged workspace ID (`wrkspc_...`) named in the delete request."""
