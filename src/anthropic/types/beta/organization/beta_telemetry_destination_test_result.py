from typing import Union
from typing_extensions import Annotated, TypeAlias

from ...._models import UnionDiscriminator
from .beta_telemetry_destination_test_failure import BetaTelemetryDestinationTestFailure
from .beta_telemetry_destination_test_success import BetaTelemetryDestinationTestSuccess

__all__ = ["BetaTelemetryDestinationTestResult"]

BetaTelemetryDestinationTestResult: TypeAlias = Annotated[
    Union[BetaTelemetryDestinationTestSuccess, BetaTelemetryDestinationTestFailure], UnionDiscriminator("type")
]
