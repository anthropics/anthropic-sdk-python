from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaSkillNameTakenErrorDetails"]


class BetaSkillNameTakenErrorDetails(BaseModel):
    """One of the Plugin's skills has the name of an organization skill.

    `skill_name` is that name.
    """

    error_code: Literal["skill_name_taken"]

    skill_name: str
