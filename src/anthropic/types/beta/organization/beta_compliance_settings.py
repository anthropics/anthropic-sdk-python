from typing_extensions import Literal

from ...._models import BaseModel
from .beta_compliance_settings_state import BetaComplianceSettingsState

__all__ = ["BetaComplianceSettings"]


class BetaComplianceSettings(BaseModel):
    state: BetaComplianceSettingsState
    """Whether the Compliance API is enabled for this organization."""

    type: Literal["compliance_settings"]
