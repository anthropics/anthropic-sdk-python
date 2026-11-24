from typing import Optional
from typing_extensions import Literal

from ......_models import BaseModel

__all__ = ["BetaGoogleManagedStorageFailedCheck"]


class BetaGoogleManagedStorageFailedCheck(BaseModel):
    """One check that a verification attempt failed."""

    check: Literal[
        "label_mismatch",
        "location_mismatch",
        "encryption",
        "versioning",
        "bucket_settings",
        "lifecycle_rules",
        "deletion_policy",
        "grant_mismatch",
        "kms_key_refused",
        "probe_failed",
        "project_not_verified",
    ]
    """Which check failed, such as `label_mismatch` or `grant_mismatch`.

    Anthropic may add values.
    """

    message: str
    """What failed and, where the end customer can fix it, what to change."""

    role: Optional[Literal["ingest", "read", "maintenance", "media_erasure", "verify"]] = None
    """
    On a check about one of the accounts that Anthropic uses to reach the bucket,
    that account's kind of access, such as `ingest`. `null` on any other check.
    Anthropic may add values.
    """
