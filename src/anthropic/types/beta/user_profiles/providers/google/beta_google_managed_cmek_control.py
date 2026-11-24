from typing import Union
from typing_extensions import Annotated, TypeAlias

from ......_models import UnionDiscriminator
from .beta_google_managed_cmek_enabled import BetaGoogleManagedCMEKEnabled
from .beta_google_managed_cmek_disabled import BetaGoogleManagedCMEKDisabled

__all__ = ["BetaGoogleManagedCMEKControl"]

BetaGoogleManagedCMEKControl: TypeAlias = Annotated[
    Union[BetaGoogleManagedCMEKDisabled, BetaGoogleManagedCMEKEnabled], UnionDiscriminator("type")
]
"""The customer-managed encryption key control, discriminated by `type`."""
