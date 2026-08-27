# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from datetime import datetime
from typing_extensions import Literal

from ..._models import BaseModel
from .beta_skill_source import BetaSkillSource

__all__ = ["BetaSkill"]


class BetaSkill(BaseModel):
    id: str
    """Unique identifier for the skill.

    The format and length of IDs may change over time.
    """

    created_at: datetime
    """ISO 8601 timestamp of when the skill was created."""

    display_name: str
    """Human-readable, single-line label for the Skill.

    Maximum 255 characters. Always set: derived from the SKILL.md frontmatter `name`
    when omitted at creation. Not unique.
    """

    latest_version_id: str
    """ID of the newest Skill Version — what `latest` references resolve to.

    Always set: a Skill holds at least one version.
    """

    source: BetaSkillSource
    """Where the Skill comes from.

    Possible values:

    - `"custom"`: authored by the platform user; private to their workspace
    - `"anthropic"`: published by Anthropic; shared and read-only
    - `"anthropic_example"`: Anthropic-published sample Skill
    - `"plugin"`: resolved from an installed plugin
    """

    type: Literal["skill"]
    """Object type.

    For Skills, this is always `"skill"`.
    """

    updated_at: datetime
    """ISO 8601 timestamp of when the skill was last updated."""
