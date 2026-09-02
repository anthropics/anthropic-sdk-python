# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Required, TypedDict

from ...._types import FileTypes, SequenceNotStr
from ...anthropic_beta_param import AnthropicBetaParam

__all__ = ["VersionCreateParams"]


class VersionCreateParams(TypedDict, total=False):
    files: Required[SequenceNotStr[FileTypes]]
    """Files to upload for the skill.

    All files must be in the same top-level directory and must include a SKILL.md
    file at the root of that directory.
    """

    betas: List[AnthropicBetaParam]
    """Optional header to specify the beta version(s) you want to use."""

    workspace_id: str
