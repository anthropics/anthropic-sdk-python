from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["InviteAlreadyExistsErrorDetails"]


class InviteAlreadyExistsErrorDetails(BaseModel):
    """A pending invite already exists for the email address.

    The message names the invite.
    """

    error_code: Literal["invite_already_exists"]
