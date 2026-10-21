from typing import Dict

from .._models import BaseModel
from .user_profile_efs_feature import UserProfileEfsFeature
from .user_profile_program_status import UserProfileProgramStatus

__all__ = ["UserProfileEfsProgram"]


class UserProfileEfsProgram(BaseModel):
    """
    A user profile's standing in Enterprise Frontier Safeguards, a program under which Anthropic approves the entity the profile represents and may approve any of the program's features.
    """

    features: Dict[str, UserProfileEfsFeature]
    """
    The program's features, keyed by feature: `data_retention_exemption` (use of
    models that normally require data retention, without the data being retained),
    `cmek` (customer-managed encryption keys) and `storage` (customer-owned
    storage). Every feature that the caller's organization may read has a key,
    whether or not it is approved; a missing key does not mean that the feature is
    inactive. Anthropic may add features; ignore a key you do not recognize.
    """

    status: UserProfileProgramStatus
    """
    Anthropic's decision on the entity the profile represents: `pending` while it is
    awaited, `active` once Anthropic has approved the entity for the program, or
    `rejected` once Anthropic has declined or has removed the entity from the
    program. `active` does not mean that any one feature is approved: read the
    feature you need in `features`.
    """
