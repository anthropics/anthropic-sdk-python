from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["ExternalKeyValidationTimedOutErrorDetails"]


class ExternalKeyValidationTimedOutErrorDetails(BaseModel):
    """
    Anthropic's validation of the External Key did not finish in time, so the request was refused. Wait a moment, then send the request again.
    """

    error_code: Literal["external_key_validation_timed_out"]
