# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["InviteDeleteResponse"]


class InviteDeleteResponse(BaseModel):
    id: str
    """ID of the Invite."""

    type: Literal["invite_deleted"]
    """Deleted object type.

    For Invites, this is always `"invite_deleted"`.
    """
