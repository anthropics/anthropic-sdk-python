from typing import Dict, List
from typing_extensions import Literal

from ......_models import BaseModel
from .beta_google_managed_retired_bucket import BetaGoogleManagedRetiredBucket
from .beta_google_managed_storage_bucket import BetaGoogleManagedStorageBucket
from .beta_google_managed_storage_region_status import BetaGoogleManagedStorageRegionStatus

__all__ = ["BetaGoogleManagedStorageEnabled"]


class BetaGoogleManagedStorageEnabled(BaseModel):
    """The control is on and has a bucket for at least one region."""

    buckets: Dict[str, BetaGoogleManagedStorageBucket]
    """The bucket configured for each region, keyed by region code.

    A region with no bucket is left out.
    """

    retired_buckets: List[BetaGoogleManagedRetiredBucket]
    """Buckets that a region has retired, earliest `expires_at` first."""

    status: Dict[str, BetaGoogleManagedStorageRegionStatus]
    """Each region's status for the control, keyed by region code.

    A region that your organization is not offered may have no entry, and Anthropic
    may add regions.
    """

    type: Literal["enabled"]
