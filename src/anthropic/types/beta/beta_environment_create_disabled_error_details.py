from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["BetaEnvironmentCreateDisabledErrorDetails"]


class BetaEnvironmentCreateDisabledErrorDetails(BaseModel):
    """Anthropic has turned off creating environments for this organization.

    Existing environments still work.
    """

    error_code: Literal["environment_create_disabled"]
