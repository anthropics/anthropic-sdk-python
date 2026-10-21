from __future__ import annotations

from typing import Union
from typing_extensions import TypeAlias

from .beta_user_message_param import BetaUserMessageParam
from .beta_system_message_param import BetaSystemMessageParam
from .beta_assistant_message_param import BetaAssistantMessageParam

__all__ = ["BetaMessageParam"]

BetaMessageParam: TypeAlias = Union[BetaUserMessageParam, BetaAssistantMessageParam, BetaSystemMessageParam]
