from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["BetaExternalKeyProviderMismatchErrorDetails"]


class BetaExternalKeyProviderMismatchErrorDetails(BaseModel):
    """
    The External Key is held by a key management service that this endpoint does not take. The message names the field and the service it takes.
    """

    error_code: Literal["external_key_provider_mismatch"]
