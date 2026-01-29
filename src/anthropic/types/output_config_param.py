# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import TypedDict

from .json_output_format_param import JSONOutputFormatParam

__all__ = ["OutputConfigParam"]


class OutputConfigParam(TypedDict, total=False):
    format: Optional[JSONOutputFormatParam]
    """A schema to specify Claude's output format in responses.

    See
    [structured outputs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs)
    """
