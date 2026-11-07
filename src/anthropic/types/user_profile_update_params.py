from __future__ import annotations

from typing import Dict, Optional
from typing_extensions import TypedDict

from .user_profile_access_type import UserProfileAccessType
from .user_profile_external_user_details_params import UserProfileExternalUserDetailsParams

__all__ = ["UserProfileUpdateParams"]


class UserProfileUpdateParams(TypedDict, total=False):
    access_type: Optional[UserProfileAccessType]
    """If present, replaces the stored access type. Omit to leave unchanged."""

    external_user_details: UserProfileExternalUserDetailsParams
    """Details about the entity this profile represents, as the platform states them.

    Each field sent replaces the stored value; omit a field to leave it unchanged.
    Once set, a value cannot be cleared and `null` is rejected. Not accepted under
    the legacy `user-profiles-2026-03-24` and `user-profiles-2026-08-18` beta
    headers.
    """

    metadata: Dict[str, str]
    """Key-value pairs to merge into the stored metadata.

    Keys provided overwrite existing values. To remove a key, set its value to an
    empty string. Keys not provided are left unchanged. Maximum 16 keys, with keys
    up to 64 characters and values up to 512 characters.
    """

    name: Optional[str]
    """If present, replaces the stored name.

    Omit to leave unchanged. Maximum 255 characters.
    """

    workspace_id: str
    """Optional header to select the Workspace for this request.

    The value is a Workspace ID (for example, `wrkspc_011CZkZaBF1tNoB5wlCeusgy`).

    Only needed for credentials that can act on more than one Workspace. A
    credential that belongs to a specific Workspace may omit it; if sent, it must
    match that Workspace.
    """
