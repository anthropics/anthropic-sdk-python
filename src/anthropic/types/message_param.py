from __future__ import annotations

from typing import Union
from typing_extensions import TypeAlias

from .user_message_param import UserMessageParam
from .system_message_param import SystemMessageParam
from .assistant_message_param import AssistantMessageParam

__all__ = ["MessageParam"]

MessageParam: TypeAlias = Union[UserMessageParam, AssistantMessageParam, SystemMessageParam]
