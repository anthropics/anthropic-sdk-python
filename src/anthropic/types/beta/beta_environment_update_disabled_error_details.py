from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["BetaEnvironmentUpdateDisabledErrorDetails"]


class BetaEnvironmentUpdateDisabledErrorDetails(BaseModel):
    """Anthropic has turned off updating environments for this organization.

    Existing environments still work as they are.
    """

    error_code: Literal["environment_update_disabled"]
