from typing import Dict, List
from typing_extensions import Literal

from ......._models import BaseModel
from .beta_google_managed_project_retired_key import BetaGoogleManagedProjectRetiredKey
from .beta_google_managed_project_cmek_region_status import BetaGoogleManagedProjectCMEKRegionStatus

__all__ = ["BetaGoogleManagedProjectCMEKEnabled"]


class BetaGoogleManagedProjectCMEKEnabled(BaseModel):
    """The control is on and has a key for at least one region."""

    external_key_ids: Dict[str, str]
    """
    The ID of the External Key configured for each region (`ekey_...`), keyed by
    region code. A region with no key is left out.
    """

    retired_keys: List[BetaGoogleManagedProjectRetiredKey]
    """Keys that a region has retired, earliest `expires_at` first."""

    status: Dict[str, BetaGoogleManagedProjectCMEKRegionStatus]
    """Each region's status for the control, keyed by region code.

    A region that your organization is not offered may have no entry, and Anthropic
    may add regions.
    """

    type: Literal["enabled"]
