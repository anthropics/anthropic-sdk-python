from __future__ import annotations

from typing import Union
from typing_extensions import TypeAlias

from .beta_text_block_param import BetaTextBlockParam
from .beta_image_block_param import BetaImageBlockParam

__all__ = ["BetaContentBlockSourceContentParam"]

BetaContentBlockSourceContentParam: TypeAlias = Union[BetaTextBlockParam, BetaImageBlockParam]
