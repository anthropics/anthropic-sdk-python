from __future__ import annotations

from typing import Optional
from typing_extensions import Literal, Required, TypedDict

__all__ = ["BetaAdvisorResultBlockParam"]


class BetaAdvisorResultBlockParam(TypedDict, total=False):
    text: Required[str]

    type: Required[Literal["advisor_result"]]

    stop_reason: Optional[str]
