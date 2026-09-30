from typing_extensions import Literal, TypeAlias

__all__ = ["BetaAnalyticsProductFilter"]

BetaAnalyticsProductFilter: TypeAlias = Literal[
    "chat", "claude-tag", "claude_code", "claude_design", "claude_in_chrome", "cowork", "office_agent"
]
