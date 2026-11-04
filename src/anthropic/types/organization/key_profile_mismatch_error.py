from typing_extensions import Literal

from ..._exceptions import BadRequestError
from .key_profile_mismatch_error_details import KeyProfileMismatchErrorDetails

__all__ = ["KeyProfileMismatchError"]


class KeyProfileMismatchError(BadRequestError):
    """
    The External Key is bound to a user profile, and the Workspace does not have that user profile. A Workspace can use only a key bound to its own user profile or a key that isn't bound to one.
    """

    error_code: Literal["key_profile_mismatch"]  # pyright: ignore[reportIncompatibleVariableOverride]
    details: KeyProfileMismatchErrorDetails  # pyright: ignore[reportIncompatibleVariableOverride]
