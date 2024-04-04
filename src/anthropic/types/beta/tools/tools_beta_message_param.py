# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union, Iterable
from typing_extensions import Literal, Required, TypedDict

from ...text_block_param import TextBlockParam
from ...image_block_param import ImageBlockParam
from .tool_use_block_param import ToolUseBlockParam
from .tool_result_block_param import ToolResultBlockParam
from .tools_beta_content_block import ToolsBetaContentBlock

__all__ = ["ToolsBetaMessageParam"]


class ToolsBetaMessageParam(TypedDict, total=False):
    content: Required[
        Union[
            str,
            Iterable[
                Union[TextBlockParam, ImageBlockParam, ToolUseBlockParam, ToolResultBlockParam, ToolsBetaContentBlock]
            ],
        ]
    ]

    role: Required[Literal["user", "assistant"]]
