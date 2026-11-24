from typing import Dict, List
from typing_extensions import Literal

from ......._models import BaseModel
from .beta_google_managed_project_retired_bucket import BetaGoogleManagedProjectRetiredBucket
from .beta_google_managed_project_storage_bucket import BetaGoogleManagedProjectStorageBucket
from .beta_google_managed_project_storage_region_status import BetaGoogleManagedProjectStorageRegionStatus

__all__ = ["BetaGoogleManagedProjectStorageEnabled"]


class BetaGoogleManagedProjectStorageEnabled(BaseModel):
    """The control is on and has a bucket for at least one region."""

    buckets: Dict[str, BetaGoogleManagedProjectStorageBucket]
    """The bucket configured for each region, keyed by region code.

    A region with no bucket is left out.
    """

    retired_buckets: List[BetaGoogleManagedProjectRetiredBucket]
    """Buckets that a region has retired, earliest `expires_at` first."""

    status: Dict[str, BetaGoogleManagedProjectStorageRegionStatus]
    """Each region's status for the control, keyed by region code.

    A region that your organization is not offered may have no entry, and Anthropic
    may add regions.
    """

    type: Literal["enabled"]
