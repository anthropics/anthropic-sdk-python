# File generated from our OpenAPI spec by Stainless.

from __future__ import annotations

from typing import Union, Iterable
from typing_extensions import Literal, Required, TypedDict

from .text_block_param import TextBlockParam

__all__ = ["MessageParam"]


class MessageParam(TypedDict, total=False):
    content: Required[Union[str, Iterable[TextBlockParam]]]

    role: Required[Literal["user", "assistant"]]
