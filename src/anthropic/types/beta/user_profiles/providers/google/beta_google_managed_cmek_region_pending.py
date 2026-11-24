from typing import Optional
from typing_extensions import Literal

from ......_models import BaseModel

__all__ = ["BetaGoogleManagedCMEKRegionPending"]


class BetaGoogleManagedCMEKRegionPending(BaseModel):
    """
    The region is validating the configured key, or the key has passed validation and the region has not started to apply it.
    """

    effective_external_key_id: Optional[str] = None
    """The ID of the External Key that the region applies now (`ekey_...`).

    While a replacement key is `pending` or `failed`, this is the previous key.
    `null` when the region applies no key.
    """

    error: Optional[str] = None
    """Why the latest validation attempt failed. `null` when no attempt has failed."""

    type: Literal["pending"]
