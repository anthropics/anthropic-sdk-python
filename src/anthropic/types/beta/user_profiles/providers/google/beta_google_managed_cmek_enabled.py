from typing import Dict, List
from typing_extensions import Literal

from ......_models import BaseModel
from .beta_google_managed_retired_key import BetaGoogleManagedRetiredKey
from .beta_google_managed_cmek_region_status import BetaGoogleManagedCMEKRegionStatus

__all__ = ["BetaGoogleManagedCMEKEnabled"]


class BetaGoogleManagedCMEKEnabled(BaseModel):
    """The control is on and has a key for at least one region."""

    external_key_ids: Dict[str, str]
    """
    The ID of the External Key configured for each region (`ekey_...`), keyed by
    region code. A region with no key is left out.
    """

    retired_keys: List[BetaGoogleManagedRetiredKey]
    """Keys that a region has retired, earliest `expires_at` first."""

    status: Dict[str, BetaGoogleManagedCMEKRegionStatus]
    """Each region's status for the control, keyed by region code.

    A region that your organization is not offered may have no entry, and Anthropic
    may add regions.
    """

    type: Literal["enabled"]
