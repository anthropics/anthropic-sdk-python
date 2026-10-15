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
    """Sparse per-member overrides, keyed by member name.

    Absent, null, and {} are equivalent; a member's defaults apply wherever its key
    is absent.
    """
