from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["CMEKKeyNetworkBlockedErrorDetails"]


class CMEKKeyNetworkBlockedErrorDetails(BaseModel):
    """
    The key management service's network access controls blocked the request to the workspace's customer-managed encryption key. The key itself may be healthy.
    """

    error_code: Literal["cmek_key_network_blocked"]
