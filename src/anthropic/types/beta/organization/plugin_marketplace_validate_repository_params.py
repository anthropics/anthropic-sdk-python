from __future__ import annotations

from typing import List, Optional
from typing_extensions import Required, TypedDict

from ...anthropic_beta_param import AnthropicBetaParam

__all__ = ["PluginMarketplaceValidateRepositoryParams"]


class PluginMarketplaceValidateRepositoryParams(TypedDict, total=False):
    repository_url: Required[str]
    """
    The `https://` URL of a public repository on github.com that holds the
    marketplace. A URL longer than 2,048 characters, on any other host or scheme,
    with a port other than 443 or 80, with credentials in it, or that does not name
    exactly `owner/repo` (a trailing `.git` or `/` is accepted) is a 400. A private
    or missing repository is reported in the response, not refused.
    """

    ref: Optional[str]
    """
    The branch to validate the tip of, or the full 40-character SHA of the commit to
    validate. When omitted, the branch a synchronization would read (usually the
    repository's default branch); if that is not the default branch, the report's
    `ref` says which branch was read. An empty string, a value longer than 255
    characters, or one that contains `..` or a character other than ASCII letters,
    digits, `.`, `_`, `-`, `+`, and `/`, is a 400. Any other value that is not a
    40-character SHA is read as a branch name; if the repository has no such branch,
    the response is a report with `valid: false`, not a 400.
    """

    betas: List[AnthropicBetaParam]
    """
    This endpoint is in beta: requests must send `ce-plugins-2026-09-01` in this
    header.
    """
