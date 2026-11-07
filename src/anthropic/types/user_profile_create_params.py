from __future__ import annotations

from typing import Dict, Optional
from typing_extensions import TypedDict

from .user_profile_access_type import UserProfileAccessType
from .user_profile_external_user_details_params import UserProfileExternalUserDetailsParams

__all__ = ["UserProfileCreateParams"]


class UserProfileCreateParams(TypedDict, total=False):
    access_type: UserProfileAccessType
    """How the platform uses the API for this entity.

    `application` (default): the profile represents an individual end-user of the
    platform's product. `passthrough`: the profile identifies a company the platform
    resells Claude access to.
    """

    external_user_details: UserProfileExternalUserDetailsParams
    """Details about the entity this profile represents, as the platform states them.

    Every field is optional. Not accepted under the legacy
    `user-profiles-2026-03-24` and `user-profiles-2026-08-18` beta headers, which
    take the top-level `external_id` (and, under `user-profiles-2026-08-18`,
    `external_user_onboarded_at`) instead.
    """

    metadata: Dict[str, str]
    """Free-form key-value data to attach to this user profile.

    Maximum 16 keys, with keys up to 64 characters and values up to 512 characters.
    Values must be non-empty strings.
    """

    name: Optional[str]
    """Optional for all profiles.

    Real-world name of the entity this profile represents (company or individual);
    for a company the platform resells Claude access to (`access_type`
    `passthrough`), that company's name where known. Maximum 255 characters.
    """

    workspace_id: str
    """Optional header to select the Workspace for this request.

    The value is a Workspace ID (for example, `wrkspc_011CZkZaBF1tNoB5wlCeusgy`).

    Only needed for credentials that can act on more than one Workspace. A
    credential that belongs to a specific Workspace may omit it; if sent, it must
    match that Workspace.
    """
