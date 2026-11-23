from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["ChangeOutcomeUnknownErrorDetails"]


class ChangeOutcomeUnknownErrorDetails(BaseModel):
    """Some of the request's changes may have been saved and others not.

    Send the same request again to finish it; changes already saved aren't repeated.
    """

    error_code: Literal["change_outcome_unknown"]
