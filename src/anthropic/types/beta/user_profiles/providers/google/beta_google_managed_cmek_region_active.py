from typing import Optional
from datetime import datetime
from typing_extensions import Literal

from ......_models import BaseModel

__all__ = ["BetaGoogleManagedCMEKRegionActive"]


class BetaGoogleManagedCMEKRegionActive(BaseModel):
    """The configured key passed validation, and the region applies it."""

    effective_external_key_id: Optional[str] = None
    """The ID of the External Key that the region applies now (`ekey_...`).

    While a replacement key is `pending` or `failed`, this is the previous key.
    `null` when the region applies no key.
    """

    error: Optional[str] = None
    """Why Google Cloud KMS refused the region's latest use of the key.

    `null` when the region has no refusal to report. A `null` does not mean that the
    key works.
    """

    last_checked_at: Optional[datetime] = None
    """
    When the region last got a successful answer from Google Cloud KMS for the key,
    in RFC 3339 format. `null` when it has none to report.
    """

    type: Literal["active"]

    validated_at: datetime
    """When the status last became `active`, in RFC 3339 format."""
