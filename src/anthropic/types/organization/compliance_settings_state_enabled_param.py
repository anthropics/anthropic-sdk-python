from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["ComplianceSettingsStateEnabledParam"]


class ComplianceSettingsStateEnabledParam(TypedDict, total=False):
    type: Required[Literal["enabled"]]
