from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaComplianceSettingsStateEnabled"]


class BetaComplianceSettingsStateEnabled(BaseModel):
    type: Literal["enabled"]
