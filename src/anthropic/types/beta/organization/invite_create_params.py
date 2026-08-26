# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

from ...._types import SequenceNotStr

__all__ = ["InviteCreateParams"]


class InviteCreateParams(TypedDict, total=False):
    email: Required[str]
    """Email of the User."""

    role: Required[Literal["billing", "claude_code_user", "developer", "managed", "user"]]
    """Role for the invited User.

    The accepted values depend on the organization type. Console and API
    organizations accept `user`, `developer`, `billing`, and `claude_code_user`;
    `admin` cannot be assigned through the API. Claude Enterprise organizations
    accept `user` and `managed`.
    """

    rbac_group_ids: SequenceNotStr[str]
    """RBAC group IDs to assign to the User when the Invite is accepted.

    A non-empty array is accepted only for a Claude Enterprise organization with
    RBAC groups, and requires the key to carry the `write:rbac_groups` scope.
    """
