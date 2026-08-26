# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing_extensions import Literal

from ....._models import BaseModel

__all__ = ["MemberRemoveResponse"]


class MemberRemoveResponse(BaseModel):
    type: Literal["workspace_member_deleted"]
    """Deleted object type.

    For Workspace Members, this is always `"workspace_member_deleted"`.
    """

    user_id: str
    """ID of the User."""

    workspace_id: str
    """ID of the Workspace."""
