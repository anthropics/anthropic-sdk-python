from typing import List
from typing_extensions import Literal

from ......._models import BaseModel
from .beta_google_managed_project_retired_bucket import BetaGoogleManagedProjectRetiredBucket

__all__ = ["BetaGoogleManagedProjectStorageDisabled"]


class BetaGoogleManagedProjectStorageDisabled(BaseModel):
    """The control is off and has no buckets."""

    retired_buckets: List[BetaGoogleManagedProjectRetiredBucket]
    """Buckets that a region has retired, earliest `expires_at` first."""

    type: Literal["disabled"]
