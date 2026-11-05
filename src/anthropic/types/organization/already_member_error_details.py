from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["AlreadyMemberErrorDetails"]


class AlreadyMemberErrorDetails(BaseModel):
    """The email address already belongs to a user in the organization.

    The message names the user.
    """

    error_code: Literal["already_member"]
