from __future__ import annotations

from typing import List, Optional
from typing_extensions import Required, TypedDict

from ..._types import FileTypes, SequenceNotStr
from ..anthropic_beta_param import AnthropicBetaParam

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

    betas: List[AnthropicBetaParam]
    """Optional header to specify the beta version(s) you want to use."""

    workspace_id: str
    """Optional header to select the Workspace for this request.

    The value is a Workspace ID (for example, `wrkspc_011CZkZaBF1tNoB5wlCeusgy`).

    Only needed for credentials that can act on more than one Workspace. A
    credential that belongs to a specific Workspace may omit it; if sent, it must
    match that Workspace.
    """
