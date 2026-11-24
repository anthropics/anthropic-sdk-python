from typing import Union
from typing_extensions import Annotated, TypeAlias

from ...._models import UnionDiscriminator
from .beta_telemetry_destination_state_enabled import BetaTelemetryDestinationStateEnabled
from .beta_telemetry_destination_state_disabled import BetaTelemetryDestinationStateDisabled

__all__ = ["BetaTelemetryDestinationState"]

BetaTelemetryDestinationState: TypeAlias = Annotated[
    Union[BetaTelemetryDestinationStateEnabled, BetaTelemetryDestinationStateDisabled], UnionDiscriminator("type")
]
"""Whether a telemetry destination receives deliveries.

A caller can set either state. The API also disables an enabled destination on its own in some cases. The `reason` of the disabled state says whether a caller or the API disabled the destination and, when the API did, why.

See the [OpenTelemetry export guide](https://platform.claude.com/docs/en/manage-claude/opentelemetry#delivery-and-health) to learn when the API disables a destination.
"""
