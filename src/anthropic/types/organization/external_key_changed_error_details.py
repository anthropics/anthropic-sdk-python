from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["ExternalKeyChangedErrorDetails"]


class ExternalKeyChangedErrorDetails(BaseModel):
    """The external key changed while the request was validating it.

    Send the request again.
    """

    error_code: Literal["external_key_changed"]
