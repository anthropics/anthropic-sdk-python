from __future__ import annotations

from typing_extensions import Required, TypedDict

from .user_profile_enroll_end_user_action_param import UserProfileEnrollEndUserActionParam

__all__ = ["ActionURLCreateParams"]


class ActionURLCreateParams(TypedDict, total=False):
    action: Required[UserProfileEnrollEndUserActionParam]
    """The action that the person who opens the URL takes."""

    workspace_id: str
    """Optional header to select the Workspace for this request.

    The value is a Workspace ID (for example, `wrkspc_011CZkZaBF1tNoB5wlCeusgy`).

    Only needed for credentials that can act on more than one Workspace. A
    credential that belongs to a specific Workspace may omit it; if sent, it must
    match that Workspace.
    """
