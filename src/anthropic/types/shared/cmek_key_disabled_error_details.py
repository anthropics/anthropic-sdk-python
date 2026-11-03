from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["CmekKeyDisabledErrorDetails"]


class CmekKeyDisabledErrorDetails(BaseModel):
    """The workspace's customer-managed encryption key is disabled or revoked.

    Re-enable the key, then retry.
    """

    error_code: Literal["cmek_key_disabled"]
