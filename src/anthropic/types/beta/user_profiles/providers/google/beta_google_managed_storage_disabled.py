from typing import List
from typing_extensions import Literal

from ......_models import BaseModel
from .beta_google_managed_retired_bucket import BetaGoogleManagedRetiredBucket

__all__ = ["BetaGoogleManagedStorageDisabled"]


class BetaGoogleManagedStorageDisabled(BaseModel):
    """The control is off and has no buckets."""

    retired_buckets: List[BetaGoogleManagedRetiredBucket]
    """Buckets that a region has retired, earliest `expires_at` first."""

    type: Literal["disabled"]
