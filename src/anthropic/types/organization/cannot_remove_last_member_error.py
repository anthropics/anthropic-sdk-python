from typing_extensions import Literal

from ..._exceptions import BadRequestError
from .cannot_remove_last_member_error_details import CannotRemoveLastMemberErrorDetails

__all__ = ["CannotRemoveLastMemberError"]


class CannotRemoveLastMemberError(BadRequestError):
    """The user is the organization's only member.

    Add another member before removing this one.
    """

    error_code: Literal["cannot_remove_last_member"]  # pyright: ignore[reportIncompatibleVariableOverride]
    details: CannotRemoveLastMemberErrorDetails  # pyright: ignore[reportIncompatibleVariableOverride]
