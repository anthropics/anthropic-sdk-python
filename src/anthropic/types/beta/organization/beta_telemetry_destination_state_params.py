from __future__ import annotations

from typing import Union
from typing_extensions import TypeAlias

from .beta_telemetry_destination_state_enabled_params import BetaTelemetryDestinationStateEnabledParams
from .beta_telemetry_destination_state_disabled_params import BetaTelemetryDestinationStateDisabledParams

__all__ = ["BetaTelemetryDestinationStateParams"]

BetaTelemetryDestinationStateParams: TypeAlias = Union[
    BetaTelemetryDestinationStateEnabledParams, BetaTelemetryDestinationStateDisabledParams
]
"""The state to set on a telemetry destination, by `type` alone.

A caller can't set the `reason` of a disabled state. Only the API sets it.
"""
