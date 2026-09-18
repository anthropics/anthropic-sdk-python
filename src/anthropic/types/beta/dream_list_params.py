from __future__ import annotations

from typing import List, Union
from datetime import datetime
from typing_extensions import Annotated, TypedDict

from ..._utils import PropertyInfo
from .beta_dream_status import BetaDreamStatus
from ..anthropic_beta_param import AnthropicBetaParam

__all__ = ["DreamListParams"]


class DreamListParams(TypedDict, total=False):
    created_at_gt: Annotated[Union[str, datetime], PropertyInfo(alias="created_at[gt]", format="iso8601")]
    """
    Return dreams with `created_at` strictly after this timestamp (exclusive lower
    bound, RFC 3339). Unset applies no lower bound.
    """

    created_at_lt: Annotated[Union[str, datetime], PropertyInfo(alias="created_at[lt]", format="iso8601")]
    """
    Return dreams with `created_at` strictly before this timestamp (exclusive upper
    bound, RFC 3339). Unset applies no upper bound.
    """

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
    """Filter by lifecycle status.

    Repeat the parameter to match any of multiple statuses. Empty applies no status
    filter.
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
