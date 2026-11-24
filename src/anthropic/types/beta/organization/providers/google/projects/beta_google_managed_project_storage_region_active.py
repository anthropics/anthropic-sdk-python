from typing import List, Optional
from datetime import datetime
from typing_extensions import Literal

from ......._models import BaseModel
from .beta_google_managed_project_effective_bucket import BetaGoogleManagedProjectEffectiveBucket
from .beta_google_managed_project_storage_failed_check import BetaGoogleManagedProjectStorageFailedCheck

__all__ = ["BetaGoogleManagedProjectStorageRegionActive"]


class BetaGoogleManagedProjectStorageRegionActive(BaseModel):
    """The configured bucket passed verification, and the region applies it."""

    effective_bucket: Optional[BetaGoogleManagedProjectEffectiveBucket] = None
    """The bucket that the region applies now.

    While a replacement bucket is `pending` or `failed`, this is the previous
    bucket. `null` when the region applies no bucket.
    """

    failed_checks: List[BetaGoogleManagedProjectStorageFailedCheck]
    """The checks that the latest reported daily verification failed.

    Empty when it passed.
    """

    type: Literal["active"]

    validated_at: datetime
    """When the status last became `active`, in RFC 3339 format."""
