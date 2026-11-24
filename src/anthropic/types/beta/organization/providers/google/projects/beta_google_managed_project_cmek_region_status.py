from typing import Union
from typing_extensions import Annotated, TypeAlias

from ......._models import UnionDiscriminator
from .beta_google_managed_project_cmek_region_active import BetaGoogleManagedProjectCMEKRegionActive
from .beta_google_managed_project_cmek_region_failed import BetaGoogleManagedProjectCMEKRegionFailed
from .beta_google_managed_project_cmek_region_pending import BetaGoogleManagedProjectCMEKRegionPending
from .beta_google_managed_project_cmek_region_suspended import BetaGoogleManagedProjectCMEKRegionSuspended
from .beta_google_managed_project_cmek_region_not_configured import BetaGoogleManagedProjectCMEKRegionNotConfigured

__all__ = ["BetaGoogleManagedProjectCMEKRegionStatus"]

BetaGoogleManagedProjectCMEKRegionStatus: TypeAlias = Annotated[
    Union[
        BetaGoogleManagedProjectCMEKRegionNotConfigured,
        BetaGoogleManagedProjectCMEKRegionPending,
        BetaGoogleManagedProjectCMEKRegionActive,
        BetaGoogleManagedProjectCMEKRegionFailed,
        BetaGoogleManagedProjectCMEKRegionSuspended,
    ],
    UnionDiscriminator("type"),
]
