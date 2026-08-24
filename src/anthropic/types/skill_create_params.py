# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import Required, TypedDict

from .._types import FileTypes, SequenceNotStr

__all__ = ["SkillCreateParams"]


class SkillCreateParams(TypedDict, total=False):
    files: Required[SequenceNotStr[FileTypes]]
    """Files to upload for the skill.

    All files must be in the same top-level directory and must include a SKILL.md
    file at the root of that directory.
    """

    display_name: Optional[str]
    """Human-readable, single-line label for the Skill.

    Maximum 255 characters. Always set: derived from the SKILL.md frontmatter `name`
    when omitted at creation. Not unique.
    """
