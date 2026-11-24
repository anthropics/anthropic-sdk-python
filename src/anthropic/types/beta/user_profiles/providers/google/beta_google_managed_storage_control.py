from typing import Union
from typing_extensions import Annotated, TypeAlias

from ......_models import UnionDiscriminator
from .beta_google_managed_storage_enabled import BetaGoogleManagedStorageEnabled
from .beta_google_managed_storage_disabled import BetaGoogleManagedStorageDisabled

__all__ = ["BetaGoogleManagedStorageControl"]

BetaGoogleManagedStorageControl: TypeAlias = Annotated[
    Union[BetaGoogleManagedStorageDisabled, BetaGoogleManagedStorageEnabled], UnionDiscriminator("type")
]
"""The customer-owned storage control, discriminated by `type`."""
