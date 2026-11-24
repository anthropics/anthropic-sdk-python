from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["BetaExternalKeyNotFoundErrorDetails"]


class BetaExternalKeyNotFoundErrorDetails(BaseModel):
    """The organization has no active External Key with this ID.

    The message names the field.
    """

    error_code: Literal["external_key_not_found"]
