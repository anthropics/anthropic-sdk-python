from __future__ import annotations

from typing import Union
from typing_extensions import TypeAlias

from .beta_google_managed_project_storage_enabled_params import BetaGoogleManagedProjectStorageEnabledParams
from .beta_google_managed_project_storage_disabled_params import BetaGoogleManagedProjectStorageDisabledParams

__all__ = ["BetaGoogleManagedProjectStorageControlParams"]

BetaGoogleManagedProjectStorageControlParams: TypeAlias = Union[
    BetaGoogleManagedProjectStorageDisabledParams, BetaGoogleManagedProjectStorageEnabledParams
]
"""The customer-owned storage control.

Leave it out to keep the control as it is. Send `cmek`, `storage`, or both.
"""
