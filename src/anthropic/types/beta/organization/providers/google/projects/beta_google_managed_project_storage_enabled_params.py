from __future__ import annotations

from typing import Dict, Optional
from typing_extensions import Literal, Required, TypedDict

from .beta_google_managed_project_bucket_reference_param import BetaGoogleManagedProjectBucketReferenceParam

__all__ = ["BetaGoogleManagedProjectStorageEnabledParams"]


class BetaGoogleManagedProjectStorageEnabledParams(TypedDict, total=False):
    """Turns the control on, or changes its buckets while it is on."""

    type: Required[Literal["enabled"]]

    buckets: Dict[str, Optional[BetaGoogleManagedProjectBucketReferenceParam]]
    """The bucket to use in each region, keyed by region code, such as `us` or `eu`.

    An object with `project_number` and `bucket_name` sets that region's bucket,
    `null` removes it, and a region you leave out keeps its bucket. A bucket can
    serve only one region. While the control is on, at least one region must have a
    bucket.
    """
