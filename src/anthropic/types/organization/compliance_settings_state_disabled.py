from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["ComplianceSettingsStateDisabled"]


class ComplianceSettingsStateDisabled(BaseModel):
    type: Literal["disabled"]
