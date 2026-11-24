from typing import List
from typing_extensions import Literal

from ......_models import BaseModel
from .beta_google_managed_retired_key import BetaGoogleManagedRetiredKey

__all__ = ["BetaGoogleManagedCMEKDisabled"]


class BetaGoogleManagedCMEKDisabled(BaseModel):
    """The control is off and has no keys."""

    retired_keys: List[BetaGoogleManagedRetiredKey]
    """Keys that a region has retired, earliest `expires_at` first."""

    type: Literal["disabled"]
