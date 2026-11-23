from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaProviderNotAllowedErrorDetails"]


class BetaProviderNotAllowedErrorDetails(BaseModel):
    """The request can't use External Storage on this cloud provider.

    The error's message says why.
    """

    error_code: Literal["provider_not_allowed"]
