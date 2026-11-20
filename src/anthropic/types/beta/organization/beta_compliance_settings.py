from typing import Optional
from typing_extensions import Literal

from ...._models import BaseModel
from .beta_access_transparency import BetaAccessTransparency
from .beta_compliance_settings_state import BetaComplianceSettingsState

__all__ = ["BetaComplianceSettings"]


class BetaComplianceSettings(BaseModel):
    state: BetaComplianceSettingsState
    """Whether the Compliance API is enabled for this organization."""

    type: Literal["compliance_settings"]

    access_transparency: Optional[BetaAccessTransparency] = None
    """Read-only.

    Whether Access Transparency is on for the organization. Returned only when the
    request sends the `anthropic-beta: efs-2026-10-01` header and Access
    Transparency is available to the organization; otherwise omitted. If the status
    can't be read, getting Compliance Settings returns an error; an update still
    saves, but then reports `disabled` whatever the real status, so get the settings
    again to check it.
    """
