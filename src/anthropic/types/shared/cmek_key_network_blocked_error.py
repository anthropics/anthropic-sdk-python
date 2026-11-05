from typing_extensions import Literal

from ..._exceptions import BadRequestError
from .cmek_key_network_blocked_error_details import CMEKKeyNetworkBlockedErrorDetails

__all__ = ["CMEKKeyNetworkBlockedError"]


class CMEKKeyNetworkBlockedError(BadRequestError):
    """
    The key management service's network access controls blocked the request to the workspace's customer-managed encryption key. The key itself may be healthy.
    """

    error_code: Literal["cmek_key_network_blocked"]  # pyright: ignore[reportIncompatibleVariableOverride]
    details: CMEKKeyNetworkBlockedErrorDetails  # pyright: ignore[reportIncompatibleVariableOverride]
