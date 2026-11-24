from typing import Optional
from typing_extensions import Literal

from ......_models import BaseModel

__all__ = ["BetaGoogleManagedCMEKRegionSuspended"]


class BetaGoogleManagedCMEKRegionSuspended(BaseModel):
    """
    Anthropic has withdrawn or paused its approval of customer-managed keys for this profile, so the region does not apply the control.
    """

    effective_external_key_id: Optional[str] = None
    """The ID of the External Key that the region applies now (`ekey_...`).

    While a replacement key is `pending` or `failed`, this is the previous key.
    `null` when the region applies no key.
    """

    type: Literal["suspended"]
