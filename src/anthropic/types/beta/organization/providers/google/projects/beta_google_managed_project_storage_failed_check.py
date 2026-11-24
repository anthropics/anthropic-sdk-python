from typing import Optional
from typing_extensions import Literal

from ......._models import BaseModel

__all__ = ["BetaGoogleManagedProjectStorageFailedCheck"]


class BetaGoogleManagedProjectStorageFailedCheck(BaseModel):
    """One check that a verification attempt failed."""

    check: Literal[
        "bucket_settings",
        "deletion_policy",
        "encryption",
        "grant_mismatch",
        "kms_key_refused",
        "label_mismatch",
        "lifecycle_rules",
        "location_mismatch",
        "probe_failed",
        "project_not_verified",
        "versioning",
    ]
    """Which check failed, such as `label_mismatch` or `grant_mismatch`.

    Anthropic may add values.
    """

    message: str
    """What failed and, where you can fix it, what to change."""

    role: Optional[Literal["ingest", "maintenance", "media_erasure", "read", "verify"]] = None
    """
    On a check about one of the accounts that Anthropic uses to reach the bucket,
    that account's kind of access, such as `ingest`. `null` on any other check.
    Anthropic may add values.
    """
