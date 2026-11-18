from typing_extensions import Literal

from .._exceptions import BadRequestError
from .beta_organization_not_enrolled_in_beta_error_details import BetaOrganizationNotEnrolledInBetaErrorDetails

__all__ = ["BetaOrganizationNotEnrolledInBetaError"]


class BetaOrganizationNotEnrolledInBetaError(BadRequestError):
    """The beta that the endpoint requires is not enabled for the organization.

    The message names the beta value.
    """

    error_code: Literal["organization_not_enrolled_in_beta"]  # pyright: ignore[reportIncompatibleVariableOverride]
    details: BetaOrganizationNotEnrolledInBetaErrorDetails  # pyright: ignore[reportIncompatibleVariableOverride]
