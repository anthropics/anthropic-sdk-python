from __future__ import annotations

from typing import Dict, List, Union, Optional
from datetime import datetime
from typing_extensions import Literal, TypedDict

from ..anthropic_beta_param import AnthropicBetaParam
from .beta_user_profile_external_user_details_params import BetaUserProfileExternalUserDetailsParams

__all__ = ["UserProfileCreateParams"]


class UserProfileCreateParams(TypedDict, total=False):
    access_type: Literal["application", "passthrough"]
    """How the platform uses the API for this entity.

    `application` (default): the profile represents an individual end-user of the
    platform's product. `passthrough`: the profile identifies a company the platform
    resells Claude access to.

    - `application` - The user profile represents an individual end-user of a
      product that the platform builds on the API. New profiles get this value by
      default.
    - `passthrough` - The user profile represents a company that the platform
      resells Claude access to.
    """

    external_id: Optional[str]
    """Platform's own identifier for this user.

    Not enforced unique. Maximum 255 characters. Legacy field, accepted only under
    the `user-profiles-2026-03-24` and `user-profiles-2026-08-18` beta headers;
    without one of them, send `external_user_details.reference_id`.
    """

    external_user_details: BetaUserProfileExternalUserDetailsParams
    """Details about the entity this profile represents, as the platform states them.

    Every field is optional. Not accepted under the legacy
    `user-profiles-2026-03-24` and `user-profiles-2026-08-18` beta headers, which
    take the top-level `external_id` (and, under `user-profiles-2026-08-18`,
    `external_user_onboarded_at`) instead.
    """

    external_user_onboarded_at: Union[str, datetime]
    """
    When the entity this profile represents opened its account with the platform, in
    RFC 3339 format: for an `application` profile, when the end-user signed up; for
    a `passthrough` profile, when the company became the platform's customer. Must
    be a complete timestamp no more than 1 minute in the future. Optional. Legacy
    field, accepted only under the `user-profiles-2026-08-18` beta header; without a
    legacy header, send `external_user_details.onboarded_at`.
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

    betas: List[AnthropicBetaParam]
    """Optional header to specify the beta version(s) you want to use."""

    workspace_id: str
    """Optional header to select the Workspace for this request.

    The value is a Workspace ID (for example, `wrkspc_011CZkZaBF1tNoB5wlCeusgy`).

    Only needed for credentials that can act on more than one Workspace. A
    credential that belongs to a specific Workspace may omit it; if sent, it must
    match that Workspace.
    """
