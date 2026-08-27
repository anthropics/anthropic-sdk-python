# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from datetime import datetime
from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaSkillVersion"]


class BetaSkillVersion(BaseModel):
    id: str
    """Unique identifier for this Skill Version.

    The id addresses the version in paths and pins it in references.
    """

    created_at: datetime
    """ISO 8601 timestamp of when the skill was created."""

    description: str
    """Description of the skill version.

    This is extracted from the SKILL.md file in the skill upload.
    """

    name: str
    """
    The Skill's immutable kebab-case slug, set at creation from the first upload's
    SKILL.md frontmatter `name` (or its enclosing directory). Every later upload
    must resolve to the same value. Also the top-level directory of the Skill's
    mounted files and the base name of a downloaded archive.
    """

    skill_id: str
    """Unique identifier for the skill.

    The format and length of IDs may change over time.
    """

    type: Literal["skill_version"]
    """Object type.

    For Skill Versions, this is always `"skill_version"`.
    """
