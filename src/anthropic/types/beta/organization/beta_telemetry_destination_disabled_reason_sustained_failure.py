from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaTelemetryDestinationDisabledReasonSustainedFailure"]


class BetaTelemetryDestinationDisabledReasonSustainedFailure(BaseModel):
    """
    The API disabled the destination because deliveries to it failed, with no successful delivery in between, for longer than a threshold that Anthropic configures and that is not part of this contract. The reason is `invalid_address` instead when the most recent failed delivery failed with an invalid address.
    """

    type: Literal["sustained_failure"]
