from __future__ import annotations

from typing import Union
from typing_extensions import TypeAlias

from .beta_google_managed_project_cmek_enabled_params import BetaGoogleManagedProjectCMEKEnabledParams
from .beta_google_managed_project_cmek_disabled_params import BetaGoogleManagedProjectCMEKDisabledParams

__all__ = ["BetaGoogleManagedProjectCMEKControlParams"]

BetaGoogleManagedProjectCMEKControlParams: TypeAlias = Union[
    BetaGoogleManagedProjectCMEKDisabledParams, BetaGoogleManagedProjectCMEKEnabledParams
]
"""The customer-managed encryption key control.

Leave it out to keep the control as it is. Send `cmek`, `storage`, or both.
"""
