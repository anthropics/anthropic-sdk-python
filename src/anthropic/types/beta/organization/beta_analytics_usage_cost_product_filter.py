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
"""Publicly documented product surfaces.

`claude_tag` is Claude Tag, the Claude product in Slack. `chat_cowork_unified` is Chat and Cowork unified, Cowork's features inside claude.ai chat: chat and Cowork usage by a member who has it turned on is reported under this value instead of `chat` or `cowork`. It is accepted as a filter only where Chat and Cowork unified is available.
"""
