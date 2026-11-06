from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["BetaInvalidConfigTypeChangeErrorDetails"]


class BetaInvalidConfigTypeChangeErrorDetails(BaseModel):
    """
    `config.type` differs from the environment's stored type, which cannot change after creation.
    """

    error_code: Literal["invalid_config_type_change"]
