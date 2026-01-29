# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import Literal, TypedDict

from .beta_json_output_format_param import BetaJSONOutputFormatParam

__all__ = ["BetaOutputConfigParam"]


class BetaOutputConfigParam(TypedDict, total=False):
    effort: Optional[Literal["low", "medium", "high"]]
    """How much effort the model should put into its response.

    Higher effort levels may result in more thorough analysis but take longer.

    Valid values are `low`, `medium`, or `high`.
    """

    format: Optional[BetaJSONOutputFormatParam]
    """A schema to specify Claude's output format in responses.

    See
    [structured outputs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs)
    """
