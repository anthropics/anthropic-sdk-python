from typing_extensions import Literal

from ..._models import BaseModel
from .compliance_settings_state import ComplianceSettingsState

__all__ = ["OrganizationComplianceSettings"]


class OrganizationComplianceSettings(BaseModel):
    state: ComplianceSettingsState
    """Whether the Compliance API is enabled for this organization."""

    type: Literal["compliance_settings"]
