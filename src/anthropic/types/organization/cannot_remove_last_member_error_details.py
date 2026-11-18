from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["CannotRemoveLastMemberErrorDetails"]


class CannotRemoveLastMemberErrorDetails(BaseModel):
    """The user is the organization's only member.

    Add another member before removing this one.
    """

    error_code: Literal["cannot_remove_last_member"]
