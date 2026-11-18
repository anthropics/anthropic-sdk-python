from ..._models import BaseModel
from .analytics_chat_cowork_unified_chat_metrics import AnalyticsChatCoworkUnifiedChatMetrics
from .analytics_chat_cowork_unified_sessions_metrics import AnalyticsChatCoworkUnifiedSessionsMetrics

__all__ = ["AnalyticsChatCoworkUnifiedMetrics"]


class AnalyticsChatCoworkUnifiedMetrics(BaseModel):
    """
    Activity in Chat and Cowork unified for one user on one day: `chat` holds
    chat activity and `sessions` holds Cowork session activity.
    """

    chat: AnalyticsChatCoworkUnifiedChatMetrics
    """Chat activity recorded while members had Chat and Cowork unified turned on."""

    sessions: AnalyticsChatCoworkUnifiedSessionsMetrics
    """
    Cowork session activity recorded while members had Chat and Cowork unified
    turned on.
    """
