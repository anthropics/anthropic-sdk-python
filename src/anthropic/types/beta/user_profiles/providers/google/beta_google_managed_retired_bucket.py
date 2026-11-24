from datetime import datetime

from ......_models import BaseModel

__all__ = ["BetaGoogleManagedRetiredBucket"]


class BetaGoogleManagedRetiredBucket(BaseModel):
    """A bucket that a region has retired.

    Until `expires_at`, keep the bucket and Anthropic's access to it as they were when the bucket passed verification.
    """

    bucket_name: str
    """The bucket's Cloud Storage name."""

    expires_at: datetime
    """When this entry is removed, in RFC 3339 format."""

    project_number: str
    """The number of the Google Cloud project that holds the bucket, in decimal."""

    region: str
    """The code of the region that retired the bucket."""
