from __future__ import annotations

from typing import Union
from typing_extensions import TypeAlias

from .compliance_settings_state_enabled_param import ComplianceSettingsStateEnabledParam
from .compliance_settings_state_disabled_param import ComplianceSettingsStateDisabledParam

__all__ = ["ComplianceSettingsStateParam"]

ComplianceSettingsStateParam: TypeAlias = Union[
    ComplianceSettingsStateEnabledParam, ComplianceSettingsStateDisabledParam
]
