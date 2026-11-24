from __future__ import annotations

from typing import Union
from typing_extensions import TypeAlias

from .beta_google_managed_cmek_enabled_params import BetaGoogleManagedCMEKEnabledParams
from .beta_google_managed_cmek_disabled_params import BetaGoogleManagedCMEKDisabledParams

__all__ = ["BetaGoogleManagedCMEKControlParams"]

BetaGoogleManagedCMEKControlParams: TypeAlias = Union[
    BetaGoogleManagedCMEKDisabledParams, BetaGoogleManagedCMEKEnabledParams
]
"""How to set the `cmek` control, discriminated by `type`."""
