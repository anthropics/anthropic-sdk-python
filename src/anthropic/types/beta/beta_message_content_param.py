from __future__ import annotations

from typing import Union, Iterable
from typing_extensions import TypeAlias

from .beta_content_block_param import BetaContentBlockParam

__all__ = ["BetaMessageContentParam"]

BetaMessageContentParam: TypeAlias = Union[str, Iterable[BetaContentBlockParam]]
