from typing import Union
from typing_extensions import Annotated, TypeAlias

from ......_models import UnionDiscriminator
from .beta_google_managed_cmek_region_active import BetaGoogleManagedCMEKRegionActive
from .beta_google_managed_cmek_region_failed import BetaGoogleManagedCMEKRegionFailed
from .beta_google_managed_cmek_region_pending import BetaGoogleManagedCMEKRegionPending
from .beta_google_managed_cmek_region_suspended import BetaGoogleManagedCMEKRegionSuspended
from .beta_google_managed_cmek_region_not_configured import BetaGoogleManagedCMEKRegionNotConfigured

__all__ = ["BetaGoogleManagedCMEKRegionStatus"]

BetaGoogleManagedCMEKRegionStatus: TypeAlias = Annotated[
    Union[
        BetaGoogleManagedCMEKRegionNotConfigured,
        BetaGoogleManagedCMEKRegionPending,
        BetaGoogleManagedCMEKRegionActive,
        BetaGoogleManagedCMEKRegionFailed,
        BetaGoogleManagedCMEKRegionSuspended,
    ],
    UnionDiscriminator("type"),
]
"""One region's status for the `cmek` control, discriminated by `type`."""
