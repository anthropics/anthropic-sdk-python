from typing import Union
from typing_extensions import Annotated, TypeAlias

from ...._models import UnionDiscriminator
from .beta_telemetry_destination_disabled_reason_caller import BetaTelemetryDestinationDisabledReasonCaller
from .beta_telemetry_destination_disabled_reason_redirect import BetaTelemetryDestinationDisabledReasonRedirect
from .beta_telemetry_destination_disabled_reason_invalid_address import (
    BetaTelemetryDestinationDisabledReasonInvalidAddress,
)
from .beta_telemetry_destination_disabled_reason_sustained_failure import (
    BetaTelemetryDestinationDisabledReasonSustainedFailure,
)

__all__ = ["BetaTelemetryDestinationDisabledReason"]

BetaTelemetryDestinationDisabledReason: TypeAlias = Annotated[
    Union[
        BetaTelemetryDestinationDisabledReasonCaller,
        BetaTelemetryDestinationDisabledReasonSustainedFailure,
        BetaTelemetryDestinationDisabledReasonInvalidAddress,
        BetaTelemetryDestinationDisabledReasonRedirect,
    ],
    UnionDiscriminator("type"),
]
"""
Why the destination is disabled: `caller` when a caller disabled it, or the reason the API disabled it automatically (`sustained_failure`, `invalid_address`, or `redirect`). Every automatic disable is reversible with an update that sets `state` to `enabled`. An update that sets `disabled` on a destination that is already disabled keeps its reason.
"""
