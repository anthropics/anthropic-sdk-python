from typing_extensions import Literal

from ...._exceptions import ConflictError
from .beta_skill_name_taken_error_details import BetaSkillNameTakenErrorDetails

__all__ = ["BetaSkillNameTakenError"]


class BetaSkillNameTakenError(ConflictError):
    """One of the Plugin's skills has the name of an organization skill.

    `skill_name` is that name.
    """

    error_code: Literal["skill_name_taken"]  # pyright: ignore[reportIncompatibleVariableOverride]
    details: BetaSkillNameTakenErrorDetails  # pyright: ignore[reportIncompatibleVariableOverride]
