from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["BetaEnvironmentArchivedErrorDetails"]


class BetaEnvironmentArchivedErrorDetails(BaseModel):
    """The environment is archived, so it cannot be updated."""

    error_code: Literal["environment_archived"]
