from __future__ import annotations

from typing import List, Optional
from typing_extensions import Literal, TypedDict

from ....anthropic_beta_param import AnthropicBetaParam

__all__ = ["InstallationSettingListParams"]


class InstallationSettingListParams(TypedDict, total=False):
    limit: int
    """Number of items to return per page.

    Defaults to `20`. Ranges from `1` to `100`.
    """

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

    page: Optional[str]
    """Optionally set to the `next_page` token from the previous response."""

    target_type: Optional[Literal["organization", "rbac_group"]]
    """
    Only settings for this kind of target: `organization` (the organization-wide
    setting) or `rbac_group` (an RBAC Group's).
    """

    betas: List[AnthropicBetaParam]
    """
    This endpoint is in beta: requests must send `ce-plugins-2026-09-01` in this
    header.
    """
