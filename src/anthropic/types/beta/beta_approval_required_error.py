from typing_extensions import Literal

from ..._exceptions import BadRequestError
from .beta_approval_required_error_details import BetaApprovalRequiredErrorDetails

__all__ = ["BetaApprovalRequiredError"]


class BetaApprovalRequiredError(BadRequestError):
    """
    Turning human review off needs Anthropic's approval for the organization, and the organization doesn't have it. Contact Anthropic support to request approval.
    """

    error_code: Literal["approval_required"]  # pyright: ignore[reportIncompatibleVariableOverride]
    details: BetaApprovalRequiredErrorDetails  # pyright: ignore[reportIncompatibleVariableOverride]
