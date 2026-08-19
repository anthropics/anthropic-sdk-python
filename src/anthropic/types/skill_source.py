# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["SkillSource"]


class SkillSource(BaseModel):
    type: Literal["custom", "anthropic", "anthropic_example", "plugin"]
    """Where the Skill comes from.

    Possible values:

    - `"custom"`: authored by the platform user; private to their workspace
    - `"anthropic"`: published by Anthropic; shared and read-only
    - `"anthropic_example"`: Anthropic-published sample Skill
    - `"plugin"`: resolved from an installed plugin
    """
