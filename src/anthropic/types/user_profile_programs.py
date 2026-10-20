from typing import Optional

from .._models import BaseModel
from .user_profile_efs_program import UserProfileEfsProgram
from .user_profile_cyber_program import UserProfileCyberProgram

__all__ = ["UserProfilePrograms"]


class UserProfilePrograms(BaseModel):
    """A user profile's standing in each program.

    A program is a set of capabilities or exemptions that Anthropic approves for the entity the profile represents. A program reads `null` when the profile has no status in it, when the caller's organization is not entitled to read programs, or when the response does not report that program. Retrieving the profile reports every program. Anthropic may add programs; ignore a key you do not recognize.
    """

    cyber: Optional[UserProfileCyberProgram] = None
    """The profile's standing in the Cyber Verification Program.

    `null` when the profile has no status in it. Only retrieving the profile gives
    the full answer: a list or update response can show `null`, or a status other
    than `active`, for a profile that reads `active` when retrieved.
    """

    efs: Optional[UserProfileEfsProgram] = None
    """The profile's standing in Enterprise Frontier Safeguards.

    `null` unless the platform's attestation for the program is in place on this
    profile, or the entity it represents has applied to the program. A list of user
    profiles does not report this program: there it reads `null` for every profile,
    so retrieve the profile to read it.
    """
