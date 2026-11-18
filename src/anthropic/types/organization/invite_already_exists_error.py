from typing_extensions import Literal

from ..._exceptions import BadRequestError
from .invite_already_exists_error_details import InviteAlreadyExistsErrorDetails

__all__ = ["InviteAlreadyExistsError"]


class InviteAlreadyExistsError(BadRequestError):
    """A pending invite already exists for the email address.

    The message names the invite.
    """

    error_code: Literal["invite_already_exists"]  # pyright: ignore[reportIncompatibleVariableOverride]
    details: InviteAlreadyExistsErrorDetails  # pyright: ignore[reportIncompatibleVariableOverride]
