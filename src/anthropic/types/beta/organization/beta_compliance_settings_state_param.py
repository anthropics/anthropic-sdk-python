from __future__ import annotations

from typing import Union
from typing_extensions import TypeAlias

from .beta_compliance_settings_state_enabled_param import BetaComplianceSettingsStateEnabledParam
from .beta_compliance_settings_state_disabled_param import BetaComplianceSettingsStateDisabledParam

__all__ = ["BetaComplianceSettingsStateParam"]

BetaComplianceSettingsStateParam: TypeAlias = Union[
    BetaComplianceSettingsStateEnabledParam, BetaComplianceSettingsStateDisabledParam
]
