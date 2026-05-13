# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import TypedDict

__all__ = ["BetaDiagnosticsParam"]


class BetaDiagnosticsParam(TypedDict, total=False):
    """Request-level diagnostics.

    Currently carries the previous response
    id for prompt-cache divergence reporting.
    """

    previous_message_id: Optional[str]
    """The `id` (`msg_...`) from this client's previous /v1/messages response.

    The server compares that request's prompt fingerprint against this one and
    returns `diagnostics.cache_miss_reason` when the prompt-cache prefix could not
    be reused. Pass `null` on the first turn to opt in without a prior message to
    compare.
    """
