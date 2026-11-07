from __future__ import annotations

from typing import List
from typing_extensions import Required, TypedDict

from ...anthropic_beta_param import AnthropicBetaParam

__all__ = ["PluginUpdateParams"]


class PluginUpdateParams(TypedDict, total=False):
    served_version_id: Required[str]
    """
    Serve this version of the Plugin (prefixed `pluginver_`) and pin the served
    version to it; `latest` is not accepted.
    """

    betas: List[AnthropicBetaParam]
    """
    This endpoint is in beta: requests must send `ce-plugins-2026-09-01` in this
    header.
    """
