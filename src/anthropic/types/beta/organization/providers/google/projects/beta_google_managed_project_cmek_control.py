from typing import Union
from typing_extensions import Annotated, TypeAlias

from ......._models import UnionDiscriminator
from .beta_google_managed_project_cmek_enabled import BetaGoogleManagedProjectCMEKEnabled
from .beta_google_managed_project_cmek_disabled import BetaGoogleManagedProjectCMEKDisabled

__all__ = ["BetaGoogleManagedProjectCMEKControl"]

BetaGoogleManagedProjectCMEKControl: TypeAlias = Annotated[
    Union[BetaGoogleManagedProjectCMEKDisabled, BetaGoogleManagedProjectCMEKEnabled], UnionDiscriminator("type")
]
"""
The customer-managed encryption key control: the key in your Google Cloud KMS that is set for each region. It covers the project's requests that name no user profile, or a user profile that has no key of its own for the project.
"""
