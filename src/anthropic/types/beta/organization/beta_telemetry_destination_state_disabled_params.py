from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["BetaTelemetryDestinationStateDisabledParams"]


class BetaTelemetryDestinationStateDisabledParams(TypedDict, total=False):
    """Stop deliveries to the telemetry destination.

    Spans produced while it is disabled aren't delivered later. A destination that is already disabled keeps its `reason`.
    """

    type: Required[Literal["disabled"]]
