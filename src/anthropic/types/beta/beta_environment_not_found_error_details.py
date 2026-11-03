from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["BetaEnvironmentNotFoundErrorDetails"]


class BetaEnvironmentNotFoundErrorDetails(BaseModel):
    """`settings.environment_id` names no Environment within the organization's reach."""

    error_code: Literal["environment_not_found"]
