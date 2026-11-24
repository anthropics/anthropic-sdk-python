from typing import Optional
from typing_extensions import Literal

from ......_models import BaseModel
from .beta_google_managed_bucket_reference import BetaGoogleManagedBucketReference

__all__ = ["BetaGoogleManagedStorageRegionNotConfigured"]


class BetaGoogleManagedStorageRegionNotConfigured(BaseModel):
    """No bucket is set for this region."""

    effective_bucket: Optional[BetaGoogleManagedBucketReference] = None
    """The bucket that the region applies now.

    While a replacement bucket is `pending` or `failed`, this is the previous
    bucket. `null` when the region applies no bucket.
    """

    type: Literal["not_configured"]
