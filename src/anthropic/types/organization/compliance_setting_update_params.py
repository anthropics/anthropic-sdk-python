from __future__ import annotations

from typing_extensions import Required, TypedDict

from .compliance_settings_state_param import ComplianceSettingsStateParam

__all__ = ["ComplianceSettingUpdateParams"]


class ComplianceSettingUpdateParams(TypedDict, total=False):
    state: Required[ComplianceSettingsStateParam]
    """Desired state.

    Accepts the string shorthand "enabled" or "disabled" in place of the object
    form; the response always returns the canonical object form.
    """
