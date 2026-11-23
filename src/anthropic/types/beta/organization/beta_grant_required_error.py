from typing_extensions import Literal

from ...._exceptions import BadRequestError
from .beta_grant_required_error_details import BetaGrantRequiredErrorDetails

__all__ = ["BetaGrantRequiredError"]


class BetaGrantRequiredError(BadRequestError):
    """
    Anthropic has not approved External Storage for the organization, for the Workspace or, for storage bound to a user profile, for that user profile. Contact your Anthropic account team.
    """

    error_code: Literal["grant_required"]  # pyright: ignore[reportIncompatibleVariableOverride]
    details: BetaGrantRequiredErrorDetails  # pyright: ignore[reportIncompatibleVariableOverride]
