from typing import Union
from typing_extensions import Annotated, TypeAlias

from ..._models import UnionDiscriminator
from .compliance_settings_state_enabled import ComplianceSettingsStateEnabled
from .compliance_settings_state_disabled import ComplianceSettingsStateDisabled

__all__ = ["ComplianceSettingsState"]

ComplianceSettingsState: TypeAlias = Annotated[
    Union[ComplianceSettingsStateEnabled, ComplianceSettingsStateDisabled], UnionDiscriminator("type")
]
