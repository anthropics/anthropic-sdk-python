from typing_extensions import Literal

from ..._exceptions import BadRequestError
from .organization_on_hold_error_details import OrganizationOnHoldErrorDetails

__all__ = ["OrganizationOnHoldError"]


class OrganizationOnHoldError(BadRequestError):
    """Anthropic has disabled the organization for trust and safety reasons.

    An organization disabled for any other reason, such as billing, does not get this code. `appeal_url`, when present, is where the organization can appeal.
    """

    error_code: Literal["organization_on_hold"]  # pyright: ignore[reportIncompatibleVariableOverride]
    details: OrganizationOnHoldErrorDetails  # pyright: ignore[reportIncompatibleVariableOverride]
