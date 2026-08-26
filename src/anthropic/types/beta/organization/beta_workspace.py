# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, Optional
from datetime import datetime
from typing_extensions import Literal

from ...._models import BaseModel
from .beta_data_residency import BetaDataResidency

__all__ = ["BetaWorkspace"]


class BetaWorkspace(BaseModel):
    id: str
    """ID of the Workspace."""

    archived_at: Optional[datetime] = None
    """
    RFC 3339 datetime string indicating when the Workspace was archived, or `null`
    if the Workspace is not archived.
    """

    compartment_id: str
    """Identifier for this Workspace's encryption compartment.

    When you configure a customer-managed encryption key (CMEK) on AWS, reference
    this value in your KMS key-policy condition so the key is scoped to this
    compartment. On GCP and Azure, Anthropic enforces the compartment binding
    automatically; you do not need to reference this value in your key
    configuration. See the CMEK integration guide for the required key
    configuration, including the value used during key validation.
    """

    created_at: datetime
    """RFC 3339 datetime string indicating when the Workspace was created."""

    data_residency: BetaDataResidency
    """Data residency configuration."""

    display_color: str
    """Hex color code representing the Workspace in the Anthropic Console."""

    external_key_id: Optional[str] = None
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

    tags: Dict[str, str]
    """User-defined tags as string key-value pairs.

    Keys may not begin with `anthropic`.
    """

    type: Literal["workspace"]
    """Object type.

    For Workspaces, this is always `"workspace"`.
    """
