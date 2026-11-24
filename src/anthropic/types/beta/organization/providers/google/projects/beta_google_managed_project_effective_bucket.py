from ......._models import BaseModel

__all__ = ["BetaGoogleManagedProjectEffectiveBucket"]


class BetaGoogleManagedProjectEffectiveBucket(BaseModel):
    """A Cloud Storage bucket, named by the project that holds it and by its own name."""

    bucket_name: str
    """The bucket's Cloud Storage name."""

    project_number: str
    """The number of the Google Cloud project that holds the bucket, in decimal."""
