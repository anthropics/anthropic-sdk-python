from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["ComplianceSettingsStateEnabled"]


class ComplianceSettingsStateEnabled(BaseModel):
    type: Literal["enabled"]
