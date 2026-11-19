from typing_extensions import Literal

from ....._models import BaseModel

__all__ = ["BetaCMEKFeatureUnsupportedErrorDetails"]


class BetaCMEKFeatureUnsupportedErrorDetails(BaseModel):
    """This stored settings document currently cannot be read or replaced.

    Contact support, or, if you no longer need these settings, delete the group's settings or clear the default.
    """

    error_code: Literal["cmek_feature_unsupported"]
