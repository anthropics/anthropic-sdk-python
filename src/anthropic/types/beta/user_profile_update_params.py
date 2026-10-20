from __future__ import annotations

from typing import Dict, List, Union, Optional
from datetime import datetime
from typing_extensions import Literal, TypedDict

from ..anthropic_beta_param import AnthropicBetaParam
from .beta_user_profile_external_user_details_params import BetaUserProfileExternalUserDetailsParams

__all__ = ["UserProfileUpdateParams"]


class UserProfileUpdateParams(TypedDict, total=False):
    access_type: Optional[Literal["application", "passthrough"]]
    """If present, replaces the stored access type. Omit to leave unchanged.

    - `application` - The user profile represents an individual end-user of a
      product that the platform builds on the API. New profiles get this value by
      default.
    - `passthrough` - The user profile represents a company that the platform
      resells Claude access to.
    """

    external_id: Optional[str]
    """If present, replaces the stored external_id.

    Omit to leave unchanged. Maximum 255 characters. Legacy field, accepted only
    under the `user-profiles-2026-03-24` and `user-profiles-2026-08-18` beta
    headers; without one of them, send `external_user_details.reference_id`.
    """

    external_user_details: BetaUserProfileExternalUserDetailsParams
    """Details about the entity this profile represents, as the platform states them.

    Each field sent replaces the stored value; omit a field to leave it unchanged.
    Once set, a value cannot be cleared and `null` is rejected. Not accepted under
    the legacy `user-profiles-2026-03-24` and `user-profiles-2026-08-18` beta
    headers.
    """

    external_user_onboarded_at: Union[str, datetime]
    """If present, replaces the stored account creation time.

    Omit to leave unchanged; once set, the value cannot be cleared and `null` is
    rejected. Must be a complete RFC 3339 timestamp no more than 1 minute in the
    future. Legacy field, accepted only under the `user-profiles-2026-08-18` beta
    header; without a legacy header, send `external_user_details.onboarded_at`.
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

    betas: List[AnthropicBetaParam]
    """Optional header to specify the beta version(s) you want to use."""

    workspace_id: str
    """Optional header to select the Workspace for this request.

    The value is a Workspace ID (for example, `wrkspc_011CZkZaBF1tNoB5wlCeusgy`).

    Only needed for credentials that can act on more than one Workspace. A
    credential that belongs to a specific Workspace may omit it; if sent, it must
    match that Workspace.
    """
