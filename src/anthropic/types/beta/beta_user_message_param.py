from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

from .beta_message_content_param import BetaMessageContentParam

__all__ = ["BetaUserMessageParam"]


class BetaUserMessageParam(TypedDict, total=False):
    content: Required[BetaMessageContentParam]

    role: Required[Literal["user"]]
