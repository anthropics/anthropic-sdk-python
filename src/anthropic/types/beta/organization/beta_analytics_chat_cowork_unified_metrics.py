from ...._models import BaseModel
from .beta_analytics_chat_cowork_unified_chat_metrics import BetaAnalyticsChatCoworkUnifiedChatMetrics
from .beta_analytics_chat_cowork_unified_sessions_metrics import BetaAnalyticsChatCoworkUnifiedSessionsMetrics

__all__ = ["BetaAnalyticsChatCoworkUnifiedMetrics"]


class BetaAnalyticsChatCoworkUnifiedMetrics(BaseModel):
    """
    Activity in Chat and Cowork unified for one user on one day: `chat` holds
    chat activity and `sessions` holds Cowork session activity.
    """

    chat: BetaAnalyticsChatCoworkUnifiedChatMetrics
    """Chat activity recorded while members had Chat and Cowork unified turned on."""

    sessions: BetaAnalyticsChatCoworkUnifiedSessionsMetrics
    """
    Cowork session activity recorded while members had Chat and Cowork unified
    turned on.
    """
