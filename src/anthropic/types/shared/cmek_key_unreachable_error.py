from typing_extensions import Literal

from ..._exceptions import ServiceUnavailableError
from .cmek_key_unreachable_error_details import CMEKKeyUnreachableErrorDetails

__all__ = ["CMEKKeyUnreachableError"]


class CMEKKeyUnreachableError(ServiceUnavailableError):
    """The workspace's customer-managed encryption key could not be reached.

    Retry the request; if this continues, check that the key is available in your key management service, or contact Anthropic support.
    """

    error_code: Literal["cmek_key_unreachable"]  # pyright: ignore[reportIncompatibleVariableOverride]
    details: CMEKKeyUnreachableErrorDetails  # pyright: ignore[reportIncompatibleVariableOverride]
