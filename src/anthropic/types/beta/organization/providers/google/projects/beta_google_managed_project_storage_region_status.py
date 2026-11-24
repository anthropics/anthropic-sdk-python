from typing import Union
from typing_extensions import Annotated, TypeAlias

from ......._models import UnionDiscriminator
from .beta_google_managed_project_storage_region_active import BetaGoogleManagedProjectStorageRegionActive
from .beta_google_managed_project_storage_region_failed import BetaGoogleManagedProjectStorageRegionFailed
from .beta_google_managed_project_storage_region_pending import BetaGoogleManagedProjectStorageRegionPending
from .beta_google_managed_project_storage_region_suspended import BetaGoogleManagedProjectStorageRegionSuspended
from .beta_google_managed_project_storage_region_not_configured import (
    BetaGoogleManagedProjectStorageRegionNotConfigured,
)

__all__ = ["BetaGoogleManagedProjectStorageRegionStatus"]

BetaGoogleManagedProjectStorageRegionStatus: TypeAlias = Annotated[
    Union[
        BetaGoogleManagedProjectStorageRegionNotConfigured,
        BetaGoogleManagedProjectStorageRegionPending,
        BetaGoogleManagedProjectStorageRegionActive,
        BetaGoogleManagedProjectStorageRegionFailed,
        BetaGoogleManagedProjectStorageRegionSuspended,
    ],
    UnionDiscriminator("type"),
]
