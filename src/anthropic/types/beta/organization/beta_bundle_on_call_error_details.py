from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaBundleOnCallErrorDetails"]


class BetaBundleOnCallErrorDetails(BaseModel):
    """
    This Bundle's instructions are managed in claude.ai and can't be changed through the API.
    """

    error_code: Literal["bundle_on_call"]
