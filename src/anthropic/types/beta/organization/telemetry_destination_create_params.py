from __future__ import annotations

from typing import Dict, List, Optional
from typing_extensions import Required, TypedDict

from ...anthropic_beta_param import AnthropicBetaParam
from .beta_telemetry_destination_traces_params import BetaTelemetryDestinationTracesParams
from .beta_telemetry_destination_workspaces_params import BetaTelemetryDestinationWorkspacesParams

__all__ = ["TelemetryDestinationCreateParams"]


class TelemetryDestinationCreateParams(TypedDict, total=False):
    endpoint_url: Required[str]
    """
    The base URL of your collector's OTLP/HTTP endpoint, for example
    `https://gateway.example.com`.

    The URL must use `https` and a hostname, not an IP address. The port, if given,
    must be 443. The URL must not contain a query string, a fragment, or a username
    and password. At most 2,048 characters.

    A path prefix, such as `/otlp`, is allowed. Don't include the per-signal path
    (`/v1/traces`), because the API appends it on delivery. If your collector takes
    traces on another path, also set `traces.endpoint_url`.
    """

    workspaces: Required[BetaTelemetryDestinationWorkspacesParams]
    """Which of the organization's workspaces the destination covers."""

    display_name: Optional[str]
    """Human-readable name for the destination. Optional. 1 to 255 characters."""

    headers: Dict[str, str]
    """
    Request headers that the API sends with every delivery, typically your
    collector's authentication header (for example `authorization`).

    The API stores the values encrypted and never returns them. Reads show only
    `header_names`.

    At most 20 headers. Names are at most 128 characters. Two names can't differ
    only in case. Values are printable ASCII, at most 4,096 characters, and can't
    begin or end with a space. Names and values together are at most 16,384 bytes.

    Reserved names are rejected, for example `host`, `cookie`, `user-agent`, and
    names that start with `content-`, `proxy-`, `x-forwarded-`, or `anthropic-`. For
    this check, `_` in a name counts as `-`.
    """

    traces: BetaTelemetryDestinationTracesParams
    """The settings for the traces that the destination receives.

    If you leave it out, every setting takes its default.
    """

    betas: List[AnthropicBetaParam]
    """
    This endpoint is in beta: requests must send `telemetry-destinations-2026-08-11`
    in this header.
    """
