from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["BetaGoogleManagedBucketReferenceParam"]


class BetaGoogleManagedBucketReferenceParam(TypedDict, total=False):
    """A Cloud Storage bucket, named by the project that holds it and by its own name."""

    bucket_name: Required[str]
    """The bucket's Cloud Storage name."""

    project_number: Required[str]
    """The number of the Google Cloud project that holds the bucket, in decimal."""
