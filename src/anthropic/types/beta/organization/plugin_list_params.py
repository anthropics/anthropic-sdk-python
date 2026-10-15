from __future__ import annotations

from typing import List, Union, Optional
from datetime import datetime
from typing_extensions import Literal, TypedDict

from ...anthropic_beta_param import AnthropicBetaParam

__all__ = ["PluginListParams"]


class PluginListParams(TypedDict, total=False):
    created_at_gt: Union[str, datetime, None]
    """RFC 3339 timestamp bound; combine [gte], [gt], [lte], [lt]."""

    created_at_gte: Union[str, datetime, None]
    """RFC 3339 timestamp bound; combine [gte], [gt], [lte], [lt]."""

    created_at_lt: Union[str, datetime, None]
    """RFC 3339 timestamp bound; combine [gte], [gt], [lte], [lt]."""

    created_at_lte: Union[str, datetime, None]
    """RFC 3339 timestamp bound; combine [gte], [gt], [lte], [lt]."""

    limit: int
    """Number of items to return per page.

    Defaults to `20`. Ranges from `1` to `100`.
    """

    marketplace_id: Optional[str]
    """Only Plugins in this plugin marketplace (prefixed `marketplace_`)."""

    organization_id: Optional[str]
    """
    For a `read:org_audit` or `read:compliance_org_data` key created for all of a
    parent organization's linked organizations: a child organization of that parent
    to read instead of the organization the key was created in, given as the
    organization's UUID or its `org_`-prefixed ID. A value that is neither returns a
    400; an organization that is not a child of the key's parent, or where the
    Plugins API is not available, returns a 404. Any other key may pass only its own
    organization's ID here; another organization returns a 404.
    """

    owner_type: Optional[Literal["organization", "user"]]
    """
    `organization` for Plugins in the organization's plugin marketplaces, `user` for
    Plugins in members' personal plugin marketplaces.
    """

    owner_user_id: Optional[str]
    """
    Only Plugins in this member's personal plugin marketplaces (prefixed `user_`); a
    removed member's ID is accepted.
    """

    page: Optional[str]
    """Optionally set to the `next_page` token from the previous response."""

    betas: List[AnthropicBetaParam]
    """
    This endpoint is in beta: requests must send `ce-plugins-2026-09-01` in this
    header.
    """
