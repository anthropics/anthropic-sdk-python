from typing_extensions import Literal

from .._exceptions import BadRequestError
from .beta_cmek_not_approved_error_details import BetaCMEKNotApprovedErrorDetails

__all__ = ["BetaCMEKNotApprovedError"]


class BetaCMEKNotApprovedError(BadRequestError):
    """
    Anthropic has not approved customer-managed encryption keys for the organization, project or user profile this request applies to, or has paused or withdrawn its approval. If you did not expect this, contact Anthropic.
    """

    error_code: Literal["cmek_not_approved"]  # pyright: ignore[reportIncompatibleVariableOverride]
    details: BetaCMEKNotApprovedErrorDetails  # pyright: ignore[reportIncompatibleVariableOverride]
