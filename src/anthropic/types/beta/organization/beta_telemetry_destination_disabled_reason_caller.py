from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaTelemetryDestinationDisabledReasonCaller"]


class BetaTelemetryDestinationDisabledReasonCaller(BaseModel):
    """
    A caller disabled the destination with an update that set `state` to `disabled`.
    """

    type: Literal["caller"]
