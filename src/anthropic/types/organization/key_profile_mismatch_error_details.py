from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["KeyProfileMismatchErrorDetails"]


class KeyProfileMismatchErrorDetails(BaseModel):
    """
    After this request, the External Key and the Workspace would not have the same user profile. A key and its Workspace must have the same user profile, or both have none.
    """

    error_code: Literal["key_profile_mismatch"]
