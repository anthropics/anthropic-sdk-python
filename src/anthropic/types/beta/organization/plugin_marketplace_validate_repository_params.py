from __future__ import annotations

from typing import List, Optional
from typing_extensions import Required, TypedDict

from ...anthropic_beta_param import AnthropicBetaParam

__all__ = ["PluginMarketplaceValidateRepositoryParams"]


class PluginMarketplaceValidateRepositoryParams(TypedDict, total=False):
    repository_url: Required[str]
    """
    The `https://` URL of a public repository on github.com that holds the
    marketplace. Any other host, a URL with credentials in it, or one that does not
    name a repository is a 400.
    """

    ref: Optional[str]
    """
    The branch to validate the tip of, or the full 40-character SHA of the commit to
    validate. When omitted, the branch a synchronization would read (usually the
    repository's default branch); if that is not the default branch, the report's
    `ref` says which branch was read. An empty string, or a value that is neither a
    branch name nor a 40-character SHA, is a 400.
    """

    betas: List[AnthropicBetaParam]
    """
    This endpoint is in beta: requests must send `ce-plugins-2026-09-01` in this
    header.
    """
