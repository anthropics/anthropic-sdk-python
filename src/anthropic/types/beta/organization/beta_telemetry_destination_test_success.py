from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaTelemetryDestinationTestSuccess"]


class BetaTelemetryDestinationTestSuccess(BaseModel):
    """The destination answered the test span with a 2xx status."""

    type: Literal["success"]
