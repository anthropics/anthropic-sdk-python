# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Union
from typing_extensions import Annotated, TypeAlias

from ...._models import UnionDiscriminator
from .beta_compliance_settings_state_enabled import BetaComplianceSettingsStateEnabled
from .beta_compliance_settings_state_disabled import BetaComplianceSettingsStateDisabled

__all__ = ["BetaComplianceSettingsState"]

BetaComplianceSettingsState: TypeAlias = Annotated[
    Union[BetaComplianceSettingsStateEnabled, BetaComplianceSettingsStateDisabled], UnionDiscriminator("type")
]
