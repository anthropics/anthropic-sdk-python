from __future__ import annotations

from typing import List, Union
from datetime import datetime
from typing_extensions import TypedDict

from .beta_dream_status import BetaDreamStatus
from ..anthropic_beta_param import AnthropicBetaParam

__all__ = ["DreamListParams"]


class DreamListParams(TypedDict, total=False):
    created_at_gt: Union[str, datetime]
    """Return only dreams created after this time (exclusive), in RFC 3339."""

    created_at_lt: Union[str, datetime]
    """Return only dreams created before this time (exclusive), in RFC 3339."""

    include_archived: bool
    """Whether to include archived dreams. Defaults to `false`."""

    limit: int
    """The maximum number of dreams to return, from 1 to 100. Defaults to 20."""

    page: str
    """
    The cursor for the page to return, taken from `next_page` in a previous
    response.

    Leave it out to get the first page.
    """

    statuses: List[BetaDreamStatus]
    """Return only dreams that have one of these statuses.

    Repeat the parameter to give more than one status. Leave it out to return dreams
    of every status.
    """

    betas: List[AnthropicBetaParam]
    """Optional header to specify the beta version(s) you want to use."""

    workspace_id: str
    """Optional header to select the Workspace for this request.

    The value is a Workspace ID (for example, `wrkspc_011CZkZaBF1tNoB5wlCeusgy`).

    Only needed for credentials that can act on more than one Workspace. A
    credential that belongs to a specific Workspace may omit it; if sent, it must
    match that Workspace.
    """
