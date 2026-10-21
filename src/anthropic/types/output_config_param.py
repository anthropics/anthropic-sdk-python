from __future__ import annotations

from typing import Optional
from typing_extensions import Literal, TypedDict

from .json_output_format_param import JSONOutputFormatParam

__all__ = ["OutputConfigParam"]


class OutputConfigParam(TypedDict, total=False):
    effort: Optional[Literal["low", "medium", "high", "xhigh", "max"]]
    """How much effort the model should put into its response.

    Higher effort levels may result in more thorough analysis but take longer.

    Valid values are `low`, `medium`, `high`, `xhigh`, or `max`.
    """

    format: Optional[JSONOutputFormatParam]
    """A schema to specify Claude's output format in responses.

    See
    [structured outputs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs)
    """
