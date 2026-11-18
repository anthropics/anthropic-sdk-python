from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["SkillReadBlockedUndecryptableErrorDetails"]


class SkillReadBlockedUndecryptableErrorDetails(BaseModel):
    """
    A custom skill the request names is stored under an encryption key state the workspace cannot currently decrypt.
    """

    error_code: Literal["skill_read_blocked_undecryptable"]
