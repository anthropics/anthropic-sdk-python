# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Union
from typing_extensions import Literal, Annotated, TypeAlias

from ...._models import BaseModel, UnionDiscriminator
from .beta_compliance_settings_state_enabled import BetaComplianceSettingsStateEnabled
from .beta_compliance_settings_state_disabled import BetaComplianceSettingsStateDisabled

__all__ = ["BetaComplianceSettings", "State"]

State: TypeAlias = Annotated[
    Union[BetaComplianceSettingsStateEnabled, BetaComplianceSettingsStateDisabled], UnionDiscriminator("type")
]


class BetaComplianceSettings(BaseModel):
    state: State
    """Whether the Compliance API is enabled for this organization."""

    type: Literal["compliance_settings"]
