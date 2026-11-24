from __future__ import annotations

from typing import Union
from typing_extensions import TypeAlias

from .beta_google_managed_storage_enabled_params import BetaGoogleManagedStorageEnabledParams
from .beta_google_managed_storage_disabled_params import BetaGoogleManagedStorageDisabledParams

__all__ = ["BetaGoogleManagedStorageControlParams"]

BetaGoogleManagedStorageControlParams: TypeAlias = Union[
    BetaGoogleManagedStorageDisabledParams, BetaGoogleManagedStorageEnabledParams
]
"""How to set the `storage` control, discriminated by `type`."""
