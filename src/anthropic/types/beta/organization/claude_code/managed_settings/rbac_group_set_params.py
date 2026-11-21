from __future__ import annotations

from typing import Dict, List
from typing_extensions import Required, TypedDict

from .....anthropic_beta_param import AnthropicBetaParam

__all__ = ["RBACGroupSetParams"]


class RBACGroupSetParams(TypedDict, total=False):
    settings: Required[Dict[str, object]]
    """The whole settings document, a JSON object of Claude Code managed settings.

    It replaces any stored document. At most 1 MiB as the server stores it, which
    can be larger than the request body.
    """

    betas: List[AnthropicBetaParam]
    """
    This endpoint is in beta: requests must send
    `ce-claude-code-managed-settings-2026-10-06` in this header.
    """
