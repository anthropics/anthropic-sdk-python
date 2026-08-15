# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Type, Union, Optional
from typing_extensions import Literal, TypedDict

import pydantic

from .json_output_format_param import JSONOutputFormatParam

__all__ = ["OutputConfigParam"]


class OutputConfigParam(TypedDict, total=False):
    effort: Optional[Literal["low", "medium", "high", "xhigh", "max"]]
    """All possible effort levels."""

    format: Optional[Union[JSONOutputFormatParam, Type[pydantic.BaseModel]]]
    """A schema to specify Claude's output format in responses.

    See
    [structured outputs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs)
    """
