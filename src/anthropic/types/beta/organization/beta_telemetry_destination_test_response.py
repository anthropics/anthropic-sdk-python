from typing_extensions import Literal

from ...._models import BaseModel
from .beta_telemetry_destination_test_result import BetaTelemetryDestinationTestResult

__all__ = ["BetaTelemetryDestinationTestResponse"]


class BetaTelemetryDestinationTestResponse(BaseModel):
    """The result of one test span sent to a destination."""

    result: BetaTelemetryDestinationTestResult
    """
    How the test went: `success` when the destination answered with a 2xx status,
    else `failure` with the reason.
    """

    type: Literal["telemetry_destination_test"]
