from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["BetaGCPProjectNotVerifiedErrorDetails"]


class BetaGCPProjectNotVerifiedErrorDetails(BaseModel):
    """
    The organization has not proved that it owns the Google Cloud project that holds the key or bucket. The message names the field.
    """

    error_code: Literal["gcp_project_not_verified"]
