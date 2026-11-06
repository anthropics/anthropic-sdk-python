from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaCannotSignOutManagedMemberErrorDetails"]


class BetaCannotSignOutManagedMemberErrorDetails(BaseModel):
    """
    On a public-sector deployment, only an API key or token that belongs to a person with owner permissions can sign out a member with the `managed` role.
    """

    error_code: Literal["cannot_sign_out_managed_member"]
