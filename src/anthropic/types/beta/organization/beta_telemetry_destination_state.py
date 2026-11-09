from typing import Union
from typing_extensions import Annotated, TypeAlias

from ...._models import UnionDiscriminator
from .beta_telemetry_destination_state_enabled import BetaTelemetryDestinationStateEnabled
from .beta_telemetry_destination_state_disabled import BetaTelemetryDestinationStateDisabled

__all__ = ["BetaTelemetryDestinationState"]

BetaTelemetryDestinationState: TypeAlias = Annotated[
    Union[BetaTelemetryDestinationStateEnabled, BetaTelemetryDestinationStateDisabled], UnionDiscriminator("type")
]
