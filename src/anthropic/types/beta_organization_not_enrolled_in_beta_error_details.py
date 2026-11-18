from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["BetaOrganizationNotEnrolledInBetaErrorDetails"]


class BetaOrganizationNotEnrolledInBetaErrorDetails(BaseModel):
    """The beta that the endpoint requires is not enabled for the organization.

    The message names the beta value.
    """

    error_code: Literal["organization_not_enrolled_in_beta"]
