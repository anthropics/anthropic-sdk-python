from typing import Optional
from typing_extensions import Literal

from ......_models import BaseModel

__all__ = ["BetaGoogleManagedCMEKRegionNotConfigured"]


class BetaGoogleManagedCMEKRegionNotConfigured(BaseModel):
    """No key is set for this region."""

    effective_external_key_id: Optional[str] = None
    """The ID of the External Key that the region applies now (`ekey_...`).

    While a replacement key is `pending` or `failed`, this is the previous key.
    `null` when the region applies no key.
    """

    type: Literal["not_configured"]
