from __future__ import annotations

from typing import Dict, List, Optional
from typing_extensions import TypedDict

from ...anthropic_beta_param import AnthropicBetaParam
from .beta_telemetry_destination_state_params import BetaTelemetryDestinationStateParams
from .beta_telemetry_destination_traces_params import BetaTelemetryDestinationTracesParams
from .beta_telemetry_destination_workspaces_params import BetaTelemetryDestinationWorkspacesParams

__all__ = ["TelemetryDestinationUpdateParams"]


class TelemetryDestinationUpdateParams(TypedDict, total=False):
    display_name: Optional[str]
    """New human-readable name, 1 to 255 characters. Null clears it."""

    endpoint_url: str
    """The new base URL of the destination's OTLP/HTTP endpoint.

    The same rules as on create apply.

    A change of hostname or port first removes every registered header, so send the
    headers for the new endpoint in the same request. When the destination has a
    `traces.endpoint_url`, such a change must also set `traces.endpoint_url` to a
    URL with the new hostname and port, or to `null`. A change of the path alone
    keeps the headers.
    """

    headers: Optional[Dict[str, Optional[str]]]
    """Headers to set or remove.

    The API merges them into the destination's headers by name.

    Names compare case-insensitively. A string value sets or replaces that header. A
    `null` value removes it. Headers that you omit don't change. The field itself
    can't be `null`.

    A request that sets a header value must also include `endpoint_url`. The current
    URL is accepted.

    The resulting set must stay within the same limits as on create. When the
    request sets a value, each stored value that it doesn't set counts as 4,096
    bytes toward the 16,384-byte limit, because you can't read its real length. So
    to change one header of a destination that has four or more other headers, send
    the values of the others again in the same request.
    """

    state: BetaTelemetryDestinationStateParams
    """Whether the destination receives deliveries after the update.

    The field can't be `null`.
    """

    traces: Optional[BetaTelemetryDestinationTracesParams]
    """The traces settings to change. Omitted settings keep their stored values.

    `null` sets every traces setting to its create default.
    """

    workspaces: BetaTelemetryDestinationWorkspacesParams
    """The new workspace scope, in the same form as on create.

    The field can't be `null`.

    The API refuses an update that changes the type or sends `workspace_ids` while
    the destination's list has more than 750 workspaces. Remove workspaces one at a
    time until 750 or fewer remain, then send the update again.
    """

    betas: List[AnthropicBetaParam]
    """
    This endpoint is in beta: requests must send `telemetry-destinations-2026-08-11`
    in this header.
    """
