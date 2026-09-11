from __future__ import annotations

from typing import Dict, List, Union, Optional
from datetime import datetime
from typing_extensions import Literal, Annotated, TypedDict

from ..._utils import PropertyInfo
from ..anthropic_beta_param import AnthropicBetaParam
from .beta_user_profile_external_user_details_params import BetaUserProfileExternalUserDetailsParams

__all__ = ["UserProfileUpdateParams"]


class UserProfileUpdateParams(TypedDict, total=False):
    access_type: Optional[Literal["application", "passthrough"]]
    """How the platform uses the API on behalf of the entity this profile represents.

    `application`: the platform sells a product that uses the API behind the scenes,
    and the profile represents an individual end-user of that product.
    `passthrough`: the platform resells raw inference, and the profile identifies
    the resold-to company.
    """

    external_id: Optional[str]
    """If present, replaces the stored external_id.

    Omit to leave unchanged. Maximum 255 characters. Accepted under the
    `user-profiles-2026-03-24` and `user-profiles-2026-08-18` beta headers; under
    `user-profiles-2026-09-04` send `external_user_details.reference_id` instead.
    """

    external_user_details: BetaUserProfileExternalUserDetailsParams
    """Details about the entity this profile represents, as the platform states them.

    Each field sent replaces the stored value; omit a field to leave it unchanged.
    Once set, a value cannot be cleared and `null` is rejected. Accepted under the
    `user-profiles-2026-09-04` beta header only.
    """

    external_user_onboarded_at: Annotated[Union[str, datetime], PropertyInfo(format="iso8601")]
    """A timestamp in RFC 3339 format"""

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
