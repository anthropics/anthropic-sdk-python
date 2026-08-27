# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaDeletedSkillVersion"]


class BetaDeletedSkillVersion(BaseModel):
    id: str
    """Unique identifier for this Skill Version.

    The id addresses the version in paths and pins it in references.
    """

    type: Literal["skill_version_deleted"]
    """Deleted object type.

    For Skill Versions, this is always `"skill_version_deleted"`.
    """
