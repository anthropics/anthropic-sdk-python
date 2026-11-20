from typing_extensions import Literal

from ..._exceptions import BadRequestError
from .beta_organization_not_eligible_error_details import BetaOrganizationNotEligibleErrorDetails

__all__ = ["BetaOrganizationNotEligibleError"]


class BetaOrganizationNotEligibleError(BadRequestError):
    """The feature isn't offered to this organization.

    The error's `message` names the kind of organization or, when it names none, says to contact your Anthropic account team.
    """

    error_code: Literal["organization_not_eligible"]  # pyright: ignore[reportIncompatibleVariableOverride]
    details: BetaOrganizationNotEligibleErrorDetails  # pyright: ignore[reportIncompatibleVariableOverride]
