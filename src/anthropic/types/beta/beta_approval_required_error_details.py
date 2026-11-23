from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["BetaApprovalRequiredErrorDetails"]


class BetaApprovalRequiredErrorDetails(BaseModel):
    """
    Turning human review off needs Anthropic's approval for the organization, and the organization doesn't have it. Contact Anthropic support to request approval.
    """

    error_code: Literal["approval_required"]

    field: str
    """The request field that needs the approval."""
