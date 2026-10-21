from __future__ import annotations

from typing import List
from typing_extensions import Required, TypedDict

from ...._types import FileTypes, SequenceNotStr
from ...anthropic_beta_param import AnthropicBetaParam

__all__ = ["PluginCreateParams"]


class PluginCreateParams(TypedDict, total=False):
    files: Required[SequenceNotStr[FileTypes]]
    """
    The version's files: one part per file, the part's filename being the file's
    path within the Plugin (for example `skills/review-pr/SKILL.md`), or a single
    `.zip` or `.plugin` archive holding them all. On the wire each part is named
    `files[]`, and a part named plain `files` is not read; with cURL,
    `-F 'files[]=@SKILL.md;filename=skills/review-pr/SKILL.md'`. The files must
    include the manifest, `.claude-plugin/plugin.json`.
    """

    marketplace_id: str
    """
    ID of the organization-owned plugin marketplace to create the Plugin in
    (prefixed `marketplace_`). It must be a `manual` marketplace, one whose Plugins
    are uploaded rather than synchronized from a repository. When omitted, the
    Plugin is created in the organization's library marketplace, an
    organization-owned `manual` marketplace created on first use.
    """

    release_notes: str
    """
    Release notes stored with the version and shown in its version history in
    claude.ai; up to 5,000 characters.
    """

    betas: List[AnthropicBetaParam]
    """
    This endpoint is in beta: requests must send `ce-plugins-2026-09-01` in this
    header.
    """
