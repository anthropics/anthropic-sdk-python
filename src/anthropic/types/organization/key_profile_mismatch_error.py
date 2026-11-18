from typing_extensions import Literal

from ..._exceptions import BadRequestError
from .key_profile_mismatch_error_details import KeyProfileMismatchErrorDetails

__all__ = ["KeyProfileMismatchError"]


class KeyProfileMismatchError(BadRequestError):
    """
    After this request, the External Key and the Workspace would not have the same user profile. A key and its Workspace must have the same user profile, or both have none.
    """

    error_code: Literal["key_profile_mismatch"]  # pyright: ignore[reportIncompatibleVariableOverride]
    details: KeyProfileMismatchErrorDetails  # pyright: ignore[reportIncompatibleVariableOverride]
