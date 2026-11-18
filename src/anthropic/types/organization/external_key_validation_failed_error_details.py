from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["ExternalKeyValidationFailedErrorDetails"]


class ExternalKeyValidationFailedErrorDetails(BaseModel):
    """The External Key failed Anthropic's validation, so the request was refused.

    The message gives the reason, if there is one.
    """

    error_code: Literal["external_key_validation_failed"]
