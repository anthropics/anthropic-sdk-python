# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

from .beta_compliance_settings_state_param import BetaComplianceSettingsStateParam

__all__ = ["ComplianceSettingUpdateParams"]


class ComplianceSettingUpdateParams(TypedDict, total=False):
    state: Required[BetaComplianceSettingsStateParam]
    """Desired state.

    Accepts the string shorthand "enabled" or "disabled" in place of the object
    form; the response always returns the canonical object form.
    """
