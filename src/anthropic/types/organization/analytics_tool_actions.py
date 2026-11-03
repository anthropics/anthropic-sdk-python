from ..._models import BaseModel
from .analytics_tool_action_counts import AnalyticsToolActionCounts

__all__ = ["AnalyticsToolActions"]


class AnalyticsToolActions(BaseModel):
    """Per-tool accepted/rejected counts for Claude Code file modification tools."""

    edit_tool: AnalyticsToolActionCounts
    """Accepted/rejected counts for a single Claude Code tool type."""

    multi_edit_tool: AnalyticsToolActionCounts
    """Accepted/rejected counts for a single Claude Code tool type."""

    notebook_edit_tool: AnalyticsToolActionCounts
    """Accepted/rejected counts for a single Claude Code tool type."""

    write_tool: AnalyticsToolActionCounts
    """Accepted/rejected counts for a single Claude Code tool type."""
