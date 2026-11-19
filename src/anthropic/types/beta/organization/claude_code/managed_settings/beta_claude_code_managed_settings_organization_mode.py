from typing_extensions import Literal

from ......_models import BaseModel

__all__ = ["BetaClaudeCodeManagedSettingsOrganizationMode"]


class BetaClaudeCodeManagedSettingsOrganizationMode(BaseModel):
    type: Literal["organization"]
    """Always `organization`."""
