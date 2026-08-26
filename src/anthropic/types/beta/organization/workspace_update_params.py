# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Optional
from typing_extensions import TypedDict

from .beta_data_residency_update_config_param import BetaDataResidencyUpdateConfigParam

__all__ = ["WorkspaceUpdateParams"]


class WorkspaceUpdateParams(TypedDict, total=False):
    data_residency: Optional[BetaDataResidencyUpdateConfigParam]
    """Data residency configuration for the workspace."""

    display_color: str
    """Hex color code representing the Workspace in the Anthropic Console."""

    external_key_id: str
    """
    ID of the customer-managed encryption key (CMEK) configuration to use for this
    Workspace. Setting this field requires CMEK to be enabled for your organization.
    When set, data stored for this Workspace is encrypted with the referenced key.
    Create key configurations with the External Keys API. This field is write-once:
    once a key is attached to a Workspace it cannot be detached or replaced. To
    rotate key material, rotate the underlying key on your cloud KMS; the
    `external_key_id` stays the same.
    """

    name: str
    """Name of the Workspace."""

    tags: Optional[Dict[str, Optional[str]]]
    """User-defined tags as string key-value pairs.

    Keys may not begin with `anthropic`.
    """
