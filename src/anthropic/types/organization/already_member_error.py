from typing_extensions import Literal

from ..._exceptions import BadRequestError
from .already_member_error_details import AlreadyMemberErrorDetails

__all__ = ["AlreadyMemberError"]


class AlreadyMemberError(BadRequestError):
    """The email address already belongs to a user in the organization.

    The message names the user.
    """

    error_code: Literal["already_member"]  # pyright: ignore[reportIncompatibleVariableOverride]
    details: AlreadyMemberErrorDetails  # pyright: ignore[reportIncompatibleVariableOverride]
