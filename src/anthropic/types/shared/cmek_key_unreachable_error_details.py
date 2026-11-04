from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["CMEKKeyUnreachableErrorDetails"]


class CMEKKeyUnreachableErrorDetails(BaseModel):
    """The workspace's customer-managed encryption key could not be reached.

    Retry the request; if this continues, check that the key is available in your key management service, or contact Anthropic support.
    """

    error_code: Literal["cmek_key_unreachable"]
