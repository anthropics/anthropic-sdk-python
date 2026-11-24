from datetime import datetime

from ......._models import BaseModel

__all__ = ["BetaGoogleManagedProjectRetiredKey"]


class BetaGoogleManagedProjectRetiredKey(BaseModel):
    """A key that a region has retired. Keep the key usable until `expires_at`."""

    expires_at: datetime
    """When this entry is removed, in RFC 3339 format."""

    external_key_id: str
    """The ID of the retired External Key (`ekey_...`)."""

    region: str
    """The code of the region that retired the key."""
