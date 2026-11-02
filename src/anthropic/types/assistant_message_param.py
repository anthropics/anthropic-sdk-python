from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

from .message_content_param import MessageContentParam

__all__ = ["AssistantMessageParam"]


class AssistantMessageParam(TypedDict, total=False):
    content: Required[MessageContentParam]

    role: Required[Literal["assistant"]]
