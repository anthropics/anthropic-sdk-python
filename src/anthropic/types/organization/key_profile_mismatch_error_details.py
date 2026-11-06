from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["KeyProfileMismatchErrorDetails"]


class KeyProfileMismatchErrorDetails(BaseModel):
    """
    The External Key is bound to a user profile, and the Workspace does not have that user profile. A Workspace can use only a key bound to its own user profile or a key that isn't bound to one.
    """

    error_code: Literal["key_profile_mismatch"]
