from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["CmekContextUnavailableErrorDetails"]


class CmekContextUnavailableErrorDetails(BaseModel):
    """
    The request's workspace encryption context could not be resolved, so the request was refused. Retry in a few minutes.
    """

    error_code: Literal["cmek_context_unavailable"]
