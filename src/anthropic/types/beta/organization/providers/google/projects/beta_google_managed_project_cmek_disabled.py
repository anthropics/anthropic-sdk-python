from typing import List
from typing_extensions import Literal

from ......._models import BaseModel
from .beta_google_managed_project_retired_key import BetaGoogleManagedProjectRetiredKey

__all__ = ["BetaGoogleManagedProjectCMEKDisabled"]


class BetaGoogleManagedProjectCMEKDisabled(BaseModel):
    """The control is off and has no keys."""

    retired_keys: List[BetaGoogleManagedProjectRetiredKey]
    """Keys that a region has retired, earliest `expires_at` first."""

    type: Literal["disabled"]
