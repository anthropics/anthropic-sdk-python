# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Optional
from typing_extensions import Required, Annotated, TypedDict

from ..._types import FileTypes, SequenceNotStr
from ..._utils import PropertyInfo
from ..anthropic_beta_param import AnthropicBetaParam

__all__ = ["SkillCreateParams"]


class SkillCreateParams(TypedDict, total=False):
    files: Required[SequenceNotStr[FileTypes]]
    """Files to upload for the skill.

    All files must be in the same top-level directory and must include a SKILL.md
    file at the root of that directory.
    """

    display_title: Optional[str]
    """Display title for the skill.

    This is a human-readable label that is not included in the prompt sent to the
    model.
    """

    betas: Annotated[List[AnthropicBetaParam], PropertyInfo(alias="anthropic-beta")]
    """Optional header to specify the beta version(s) you want to use."""
