from __future__ import annotations

from typing import List, Optional
from typing_extensions import Required, TypedDict

from ....anthropic_beta_param import AnthropicBetaParam

__all__ = ["VersionRetrieveParams"]


class VersionRetrieveParams(TypedDict, total=False):
    plugin_id: Required[str]
    """ID of the Plugin (prefixed `plugin_`)."""

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

    betas: List[AnthropicBetaParam]
    """
    This endpoint is in beta: requests must send `ce-plugins-2026-09-01` in this
    header.
    """
