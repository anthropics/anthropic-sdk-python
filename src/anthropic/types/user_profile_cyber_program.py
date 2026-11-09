from typing import Dict, Optional

from .._models import BaseModel
from .user_profile_cyber_tier import UserProfileCyberTier
from .user_profile_program_status import UserProfileProgramStatus
from .user_profile_cyber_requirements import UserProfileCyberRequirements

__all__ = ["UserProfileCyberProgram"]


class UserProfileCyberProgram(BaseModel):
    """
    A user profile's standing in the Cyber Verification Program, which relaxes cyber safeguards for requests that name the profile.
    """

    requirements: Optional[UserProfileCyberRequirements] = None
    """
    What a request that names the profile must allow to get the relaxed safeguards
    of every `active` tier. `null` when no tier is `active`, and wherever `tiers` is
    `{}`.
    """

    status: UserProfileProgramStatus
    """
    `active` when at least one tier is `active`, or when the profile has the
    program's access to earlier models. That access is not a tier: a profile that
    has it alone reads `active` with every tier `inactive`, or with `tiers` `{}` on
    a response that does not report tiers. When nothing is `active`, `pending` means
    that an application or enrollment is under review, or that what Anthropic
    approved does not yet apply to this profile, and `rejected` means that the
    application or enrollment was declined.
    """

    tiers: Dict[str, UserProfileCyberTier]
    """
    The program's tiers, keyed by tier: `a` (Specialized Access), `b` (Red Team
    Access) and `c` (Defense Access). A response reports either every tier or none.
    When it reports them, as retrieving the profile normally does, every tier has a
    key, whether or not it applies to the profile. When it does not, as in the list
    of user profiles, `tiers` is `{}`, which does not mean that the tiers are
    inactive. No tier implies another, so read the tier you need. Anthropic may add
    tiers; ignore a key you do not recognize.
    """
