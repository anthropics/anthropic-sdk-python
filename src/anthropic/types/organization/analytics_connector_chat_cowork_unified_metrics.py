from ..._models import BaseModel
from .analytics_connector_chat_cowork_unified_chat_metrics import AnalyticsConnectorChatCoworkUnifiedChatMetrics
from .analytics_connector_chat_cowork_unified_sessions_metrics import AnalyticsConnectorChatCoworkUnifiedSessionsMetrics

__all__ = ["AnalyticsConnectorChatCoworkUnifiedMetrics"]


class AnalyticsConnectorChatCoworkUnifiedMetrics(BaseModel):
    """
    A connector's use in Chat and Cowork unified on one day: `chat` holds its
    use in chat conversations and `sessions` its use in Cowork sessions.
    """

    chat: AnalyticsConnectorChatCoworkUnifiedChatMetrics
    """
    A connector's use in chat conversations recorded while members had Chat and
    Cowork unified turned on.
    """

    sessions: AnalyticsConnectorChatCoworkUnifiedSessionsMetrics
    """
    A connector's use in Cowork sessions recorded while members had Chat and Cowork
    unified turned on.
    """
