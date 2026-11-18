from typing_extensions import Literal

from ..._exceptions import ServiceUnavailableError
from .cmek_context_unavailable_error_details import CMEKContextUnavailableErrorDetails

__all__ = ["CMEKContextUnavailableError"]


class CMEKContextUnavailableError(ServiceUnavailableError):
    """
    The workspace's encryption settings could not be read, so the request was refused. Retry in a few minutes.
    """

    error_code: Literal["cmek_context_unavailable"]  # pyright: ignore[reportIncompatibleVariableOverride]
    details: CMEKContextUnavailableErrorDetails  # pyright: ignore[reportIncompatibleVariableOverride]
