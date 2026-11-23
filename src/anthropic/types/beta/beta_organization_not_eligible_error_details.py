from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["BetaOrganizationNotEligibleErrorDetails"]


class BetaOrganizationNotEligibleErrorDetails(BaseModel):
    """The feature isn't offered to this organization.

    The error's `message` names the kind of organization or, when it names none, says to contact your Anthropic account team.
    """

    error_code: Literal["organization_not_eligible"]
