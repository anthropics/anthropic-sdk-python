from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaGrantRequiredErrorDetails"]


class BetaGrantRequiredErrorDetails(BaseModel):
    """
    Anthropic has not approved External Storage for the organization, for the Workspace or, for storage bound to a user profile, for that user profile. Contact your Anthropic account team.
    """

    error_code: Literal["grant_required"]
