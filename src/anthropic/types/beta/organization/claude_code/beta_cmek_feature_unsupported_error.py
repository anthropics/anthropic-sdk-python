from typing_extensions import Literal

from ....._exceptions import BadRequestError
from .beta_cmek_feature_unsupported_error_details import BetaCMEKFeatureUnsupportedErrorDetails

__all__ = ["BetaCMEKFeatureUnsupportedError"]


class BetaCMEKFeatureUnsupportedError(BadRequestError):
    """This stored settings document currently cannot be read or replaced.

    Contact support, or, if you no longer need these settings, delete the group's settings or clear the default.
    """

    error_code: Literal["cmek_feature_unsupported"]  # pyright: ignore[reportIncompatibleVariableOverride]
    details: BetaCMEKFeatureUnsupportedErrorDetails  # pyright: ignore[reportIncompatibleVariableOverride]
