# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, List, Optional
from typing_extensions import Required, Annotated, TypedDict

from ...._utils import PropertyInfo
from ...anthropic_beta_param import AnthropicBetaParam
from .beta_data_residency_create_config_param import BetaDataResidencyCreateConfigParam

__all__ = ["WorkspaceCreateParams"]


class WorkspaceCreateParams(TypedDict, total=False):
    name: Required[str]
    """Name of the Workspace."""

    data_residency: Optional[BetaDataResidencyCreateConfigParam]
    """Data residency configuration for the workspace.

    If omitted, defaults to `workspace_geo: "us"`,
    `allowed_inference_geos: "unrestricted"`, and `default_inference_geo: "global"`.
    """

    display_color: Optional[str]
    """Hex color code representing the Workspace in the Anthropic Console."""

    external_key_id: Optional[str]
    """
    ID of the customer-managed encryption key (CMEK) configuration to use for this
    Workspace. Setting this field requires CMEK to be enabled for your organization.
    When set, data stored for this Workspace is encrypted with the referenced key.
    Create key configurations with the External Keys API. This field is write-once:
    once a key is attached to a Workspace it cannot be detached or replaced. To
    rotate key material, rotate the underlying key on your cloud KMS; the
    `external_key_id` stays the same.
    """

    tags: Optional[Dict[str, str]]
    """User-defined tags as string key-value pairs.

    Keys may not begin with `anthropic`.
    """

    betas: Annotated[List[AnthropicBetaParam], PropertyInfo(alias="anthropic-beta")]
    """Optional header to specify the beta version(s) you want to use."""
