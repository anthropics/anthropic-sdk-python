from typing import Optional
from typing_extensions import Literal

from ......_models import BaseModel

__all__ = ["BetaGoogleManagedCMEKRegionFailed"]


class BetaGoogleManagedCMEKRegionFailed(BaseModel):
    """The region stopped retrying validation before the configured key passed.

    To restart validation, send the region a key again. It can be the same key.
    """

    effective_external_key_id: Optional[str] = None
    """The ID of the External Key that the region applies now (`ekey_...`).

    While a replacement key is `pending` or `failed`, this is the previous key.
    `null` when the region applies no key.
    """

    error: str
    """Why the region cannot use the configured key."""

    type: Literal["failed"]
