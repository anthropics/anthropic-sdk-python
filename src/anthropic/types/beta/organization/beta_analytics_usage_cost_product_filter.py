from typing_extensions import Literal, TypeAlias

__all__ = ["BetaAnalyticsUsageCostProductFilter"]

BetaAnalyticsUsageCostProductFilter: TypeAlias = Literal[
    "chat",
    "chat_cowork_unified",
    "claude_code",
    "claude_console",
    "claude_design",
    "claude_in_chrome",
    "claude_tag",
    "cowork",
    "managed_agents_api",
    "message_batches_api",
    "messages_api",
    "office_agent",
]
