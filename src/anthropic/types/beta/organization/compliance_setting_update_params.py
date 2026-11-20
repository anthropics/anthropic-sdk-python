from __future__ import annotations

from typing import List
from typing_extensions import Required, TypedDict

from ...anthropic_beta_param import AnthropicBetaParam
from .beta_compliance_settings_state_param import BetaComplianceSettingsStateParam

__all__ = ["ComplianceSettingUpdateParams"]


class ComplianceSettingUpdateParams(TypedDict, total=False):
    state: Required[BetaComplianceSettingsStateParam]
    """Desired state.

    Accepts the string shorthand "enabled" or "disabled" in place of the object
    form; the response always returns the canonical object form.
    """

    betas: List[AnthropicBetaParam]
    """Optional.

    Send `efs-2026-10-01` in this header to use this endpoint's beta features:
    additional parameters, accepted values and response fields.
    """
