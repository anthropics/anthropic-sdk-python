from __future__ import annotations

from typing import Dict, Optional
from typing_extensions import Literal, Required, TypedDict

__all__ = ["BetaGoogleManagedProjectCMEKEnabledParams"]


class BetaGoogleManagedProjectCMEKEnabledParams(TypedDict, total=False):
    """Turns the control on, or changes its keys while it is on."""

    type: Required[Literal["enabled"]]

    external_key_ids: Dict[str, Optional[str]]
    """
    The External Key to use in each region, keyed by region code, such as `us` or
    `eu`. An External Key ID (`ekey_...`) sets that region's key, `null` removes it,
    and a region you leave out keeps its key. While the control is on, at least one
    region must have a key.
    """
