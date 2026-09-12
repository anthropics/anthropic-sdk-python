from __future__ import annotations

from typing import Dict, List, Union, Optional
from datetime import datetime
from typing_extensions import Literal, Annotated, TypedDict

from ..._utils import PropertyInfo
from ..anthropic_beta_param import AnthropicBetaParam
from .beta_user_profile_external_user_details_params import BetaUserProfileExternalUserDetailsParams

__all__ = ["UserProfileCreateParams"]


class UserProfileCreateParams(TypedDict, total=False):
    access_type: Literal["application", "passthrough"]
    """How the platform uses the API on behalf of the entity this profile represents.

    `application`: the platform sells a product that uses the API behind the scenes,
    and the profile represents an individual end-user of that product.
    `passthrough`: the platform resells raw inference, and the profile identifies
    the resold-to company.
    """

    external_id: Optional[str]
    """Platform's own identifier for this user.

    Not enforced unique. Maximum 255 characters. Accepted under the
    `user-profiles-2026-03-24` and `user-profiles-2026-08-18` beta headers; under
    `user-profiles-2026-09-04` send `external_user_details.reference_id` instead.
    """

    external_user_details: BetaUserProfileExternalUserDetailsParams
    """Details about the entity this profile represents, as the platform states them.

    Every field is optional. Accepted under the `user-profiles-2026-09-04` beta
    header only.
    """

    external_user_onboarded_at: Annotated[Union[str, datetime], PropertyInfo(format="iso8601")]
    """A timestamp in RFC 3339 format"""

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
