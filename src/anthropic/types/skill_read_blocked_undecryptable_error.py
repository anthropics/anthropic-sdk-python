from typing_extensions import Literal

from .._exceptions import ConflictError
from .skill_read_blocked_undecryptable_error_details import SkillReadBlockedUndecryptableErrorDetails

__all__ = ["SkillReadBlockedUndecryptableError"]


class SkillReadBlockedUndecryptableError(ConflictError):
    """
    A custom skill the request names is stored under an encryption key state the workspace cannot currently decrypt.
    """

    error_code: Literal["skill_read_blocked_undecryptable"]  # pyright: ignore[reportIncompatibleVariableOverride]
    details: SkillReadBlockedUndecryptableErrorDetails  # pyright: ignore[reportIncompatibleVariableOverride]
