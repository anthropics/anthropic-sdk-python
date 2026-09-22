from typing import Optional
from typing_extensions import Literal

from ..._models import BaseModel
from .beta_browser_toolset_configs import BetaBrowserToolsetConfigs
from .beta_cache_control_ephemeral import BetaCacheControlEphemeral

__all__ = ["BetaBrowserToolset20260801"]


class BetaBrowserToolset20260801(BaseModel):
    """
    The browser toolset: a single ``tools[]`` entry (carrying no
    ``name``) that declares the browser tool family. The model is served
    the family's tool with any members disabled via ``configs`` removed
    from its schema.
    """

    type: Literal["browser_toolset_20260801"]

    cache_control: Optional[BetaCacheControlEphemeral] = None
    """Create a cache control breakpoint at this content block."""

    configs: Optional[BetaBrowserToolsetConfigs] = None
    """
    Per-member configuration for `browser_toolset_20260801`: one optional field per
    member tool, keyed by the member name — the same name the member's `tool_use`
    blocks carry. Every member is an accepted key, and a member's defaults apply
    wherever its key is absent. Unknown keys are rejected: the field set is this
    toolset version's complete member set.
    """
