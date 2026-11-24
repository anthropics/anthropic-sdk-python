from typing import Union
from typing_extensions import Annotated, TypeAlias

from ......._models import UnionDiscriminator
from .beta_google_managed_project_storage_enabled import BetaGoogleManagedProjectStorageEnabled
from .beta_google_managed_project_storage_disabled import BetaGoogleManagedProjectStorageDisabled

__all__ = ["BetaGoogleManagedProjectStorageControl"]

BetaGoogleManagedProjectStorageControl: TypeAlias = Annotated[
    Union[BetaGoogleManagedProjectStorageDisabled, BetaGoogleManagedProjectStorageEnabled], UnionDiscriminator("type")
]
"""
The customer-owned storage control: your Cloud Storage bucket that is set for each region. It covers the project's requests that name no user profile, or a user profile that has no bucket of its own for the project.
"""
