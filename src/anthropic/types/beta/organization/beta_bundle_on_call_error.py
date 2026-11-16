from typing_extensions import Literal

from ...._exceptions import BadRequestError
from .beta_bundle_on_call_error_details import BetaBundleOnCallErrorDetails

__all__ = ["BetaBundleOnCallError"]


class BetaBundleOnCallError(BadRequestError):
    """
    This Bundle's instructions are managed in claude.ai and can't be changed through the API.
    """

    error_code: Literal["bundle_on_call"]  # pyright: ignore[reportIncompatibleVariableOverride]
    details: BetaBundleOnCallErrorDetails  # pyright: ignore[reportIncompatibleVariableOverride]
