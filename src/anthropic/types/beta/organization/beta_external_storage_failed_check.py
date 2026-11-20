from typing import Optional
from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaExternalStorageFailedCheck"]


class BetaExternalStorageFailedCheck(BaseModel):
    """One check that an External Storage's verification failed."""

    check: Literal[
        "already_registered",
        "assume_role",
        "bucket_empty",
        "bucket_not_confirmed",
        "bucket_policy",
        "bucket_settings",
        "default_encryption",
        "deletion_policy",
        "encryption",
        "grant_mismatch",
        "key_usable",
        "kms_key_refused",
        "lifecycle_no_archive",
        "lifecycle_rules",
        "lifecycle_template",
        "location_mismatch",
        "object_lock",
        "other",
        "ownership_enforced",
        "probe_failed",
        "probe_object",
        "probe_storage_class",
        "public_access_block",
        "region",
        "replication",
        "request_metrics",
        "request_payment",
        "transcripts_support",
        "trust_ingest_role",
        "trust_maintenance_role",
        "trust_media_erasure_role",
        "trust_read_role",
        "trust_transcripts_role",
        "trust_transcripts_verify_role",
        "trust_verify_role",
        "versioning",
    ]
    """Name of the check that failed, such as `versioning`, for code to branch on.

    New names may be added; `other` is a check this API does not name. The value is
    a name with no data of its own.
    """

    message: str
    """What failed and how to fix it, in plain words."""

    role: Optional[
        Literal["ingest", "maintenance", "media_erasure", "read", "transcripts", "transcripts_verify", "verify"]
    ] = None
    """
    The part of your access grant that the check is about, such as `ingest`: on AWS,
    one of the IAM roles your setup created; on Google Cloud, the grant to one of
    Anthropic's service accounts. `null` when the check is not about one. New names
    may be added. The value is a name with no data of its own.
    """
