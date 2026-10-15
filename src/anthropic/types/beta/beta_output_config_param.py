from __future__ import annotations

from typing import Optional
from typing_extensions import Literal, TypedDict

from .beta_token_task_budget_param import BetaTokenTaskBudgetParam
from .beta_json_output_format_param import BetaJSONOutputFormatParam

__all__ = ["BetaOutputConfigParam"]


class BetaOutputConfigParam(TypedDict, total=False):
    effort: Optional[Literal["low", "medium", "high", "xhigh", "max"]]
    """How much effort the model should put into its response.

    Higher effort levels may result in more thorough analysis but take longer.

    Valid values are `low`, `medium`, `high`, `xhigh`, or `max`.
    """

    format: Optional[BetaJSONOutputFormatParam]
    """A schema to specify Claude's output format in responses.

    See
    [structured outputs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs)
    """

    task_budget: Optional[BetaTokenTaskBudgetParam]
    """Configuration for token budget tracking across contexts."""
