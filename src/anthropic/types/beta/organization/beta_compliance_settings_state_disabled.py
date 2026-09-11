from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaComplianceSettingsStateDisabled"]


class BetaComplianceSettingsStateDisabled(BaseModel):
    type: Literal["disabled"]
