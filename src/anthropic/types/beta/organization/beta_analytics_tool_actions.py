from ...._models import BaseModel
from .beta_analytics_tool_action_counts import BetaAnalyticsToolActionCounts

__all__ = ["BetaAnalyticsToolActions"]


class BetaAnalyticsToolActions(BaseModel):
    """Per-tool accepted/rejected counts for Claude Code file modification tools."""

    edit_tool: BetaAnalyticsToolActionCounts
    """Accepted/rejected counts for a single Claude Code tool type."""

    multi_edit_tool: BetaAnalyticsToolActionCounts
    """Accepted/rejected counts for a single Claude Code tool type."""

    notebook_edit_tool: BetaAnalyticsToolActionCounts
    """Accepted/rejected counts for a single Claude Code tool type."""

    write_tool: BetaAnalyticsToolActionCounts
    """Accepted/rejected counts for a single Claude Code tool type."""
