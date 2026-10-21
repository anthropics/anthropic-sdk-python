from __future__ import annotations

from typing import Union, Iterable
from typing_extensions import Literal, Required, TypedDict

from .text_block_param import TextBlockParam

__all__ = ["SystemMessageParam"]


class SystemMessageParam(TypedDict, total=False):
    content: Required[Union[str, Iterable[TextBlockParam]]]

    role: Required[Literal["system"]]
