from typing_extensions import Literal

from .._exceptions import BadRequestError
from .beta_storage_not_approved_error_details import BetaStorageNotApprovedErrorDetails

__all__ = ["BetaStorageNotApprovedError"]


class BetaStorageNotApprovedError(BadRequestError):
    """
    Anthropic has not approved keeping data in a customer-owned storage bucket for the organization, project or user profile this request applies to, or has paused or withdrawn its approval. If you did not expect this, contact Anthropic.
    """

    error_code: Literal["storage_not_approved"]  # pyright: ignore[reportIncompatibleVariableOverride]
    details: BetaStorageNotApprovedErrorDetails  # pyright: ignore[reportIncompatibleVariableOverride]
