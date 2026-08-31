# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union
from typing_extensions import Required, TypeAlias, TypedDict

from .beta_compliance_settings_state_enabled_param import BetaComplianceSettingsStateEnabledParam
from .beta_compliance_settings_state_disabled_param import BetaComplianceSettingsStateDisabledParam

__all__ = ["ComplianceSettingUpdateParams", "State"]


class ComplianceSettingUpdateParams(TypedDict, total=False):
    state: Required[State]
    """Desired state.

    Accepts the string shorthand "enabled" or "disabled" in place of the object
    form; the response always returns the canonical object form.
    """


State: TypeAlias = Union[BetaComplianceSettingsStateEnabledParam, BetaComplianceSettingsStateDisabledParam]
