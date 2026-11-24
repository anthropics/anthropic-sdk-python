from typing import Optional

from ......._models import BaseModel

__all__ = ["BetaGoogleManagedProjectStorageBucket"]


class BetaGoogleManagedProjectStorageBucket(BaseModel):
    """The bucket configured for a region."""

    bucket_name: str
    """The bucket's Cloud Storage name."""

    kms_key_name: Optional[str] = None
    """
    The resource name of the Cloud KMS key that the bucket encrypts objects under by
    default. `null` until the region has confirmed the bucket, and when the bucket
    has no default key.
    """

    location: Optional[str] = None
    """The bucket's location, as Cloud Storage reports it.

    `null` until the region has confirmed the bucket.
    """

    project_id: Optional[str] = None
    """The ID of the project that holds the bucket.

    `null` until the region has confirmed the bucket.
    """

    project_number: str
    """The number of the Google Cloud project that holds the bucket, in decimal."""
