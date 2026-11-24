from typing import Union
from typing_extensions import Annotated, TypeAlias

from ......_models import UnionDiscriminator
from .beta_google_managed_storage_region_active import BetaGoogleManagedStorageRegionActive
from .beta_google_managed_storage_region_failed import BetaGoogleManagedStorageRegionFailed
from .beta_google_managed_storage_region_pending import BetaGoogleManagedStorageRegionPending
from .beta_google_managed_storage_region_suspended import BetaGoogleManagedStorageRegionSuspended
from .beta_google_managed_storage_region_not_configured import BetaGoogleManagedStorageRegionNotConfigured

__all__ = ["BetaGoogleManagedStorageRegionStatus"]

BetaGoogleManagedStorageRegionStatus: TypeAlias = Annotated[
    Union[
        BetaGoogleManagedStorageRegionNotConfigured,
        BetaGoogleManagedStorageRegionPending,
        BetaGoogleManagedStorageRegionActive,
        BetaGoogleManagedStorageRegionFailed,
        BetaGoogleManagedStorageRegionSuspended,
    ],
    UnionDiscriminator("type"),
]
"""One region's status for the `storage` control, discriminated by `type`."""
