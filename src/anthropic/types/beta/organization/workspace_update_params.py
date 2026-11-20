from __future__ import annotations

from typing import Dict, List, Optional
from typing_extensions import TypedDict

from ...anthropic_beta_param import AnthropicBetaParam
from .beta_data_residency_update_config_param import BetaDataResidencyUpdateConfigParam
from .beta_inference_data_privacy_update_param import BetaInferenceDataPrivacyUpdateParam

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
    Create key configurations with the External Keys API. On Claude Platform on AWS
    the value for an AWS KMS key is the key's ARN, and your organization's own key
    must be a single-Region key in the same Region as the Workspace. If that key is
    outside the Workspace's AWS account, it can be attached only by updating an
    active Workspace. On that platform the key is validated against this Workspace
    when it is attached, so a key-policy problem is reported as an error on this
    request. This field is write-once: once a key is attached to a Workspace it
    cannot be detached or replaced. To rotate key material, rotate the underlying
    key on your cloud KMS; the `external_key_id` stays the same.
    """

    inference_data_privacy: Optional[BetaInferenceDataPrivacyUpdateParam]
    """
    Changes to where the Workspace's retained inference data and transcript copies
    go, and to whether Anthropic's human review applies. Requires the
    `efs-2026-10-01` `anthropic-beta` value. An omitted member is unchanged. Cannot
    be null. An Admin API key can't set this field, because it doesn't belong to a
    user or a service account. Use an API key that belongs to one, or an OAuth
    token.
    """

    name: str
    """Name of the Workspace."""

    tags: Optional[Dict[str, Optional[str]]]
    """User-defined tags as string key-value pairs.

    Keys may not begin with `anthropic`.
    """

    user_profile_id: str
    """ID of a user profile to attach to the Workspace.

    Every inference request through the Workspace must then name this user profile;
    the API rejects a request that names none or a different one. Once set, it can't
    be replaced or removed (sending the same ID again changes nothing); only
    deleting the user profile clears it. It can't be set on a Workspace whose
    External Key isn't bound to this user profile. The default Workspace can't have
    a user profile.
    """

    betas: List[AnthropicBetaParam]
    """Optional.

    Send `efs-2026-10-01` in this header to use this endpoint's beta features:
    additional parameters, accepted values and response fields.
    """
