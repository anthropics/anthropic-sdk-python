from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["CMEKContextUnavailableErrorDetails"]


class CMEKContextUnavailableErrorDetails(BaseModel):
    """
    The workspace's encryption settings could not be read, so the request was refused. Retry in a few minutes.
    """

    error_code: Literal["cmek_context_unavailable"]
