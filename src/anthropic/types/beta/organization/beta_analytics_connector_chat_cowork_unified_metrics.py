from ...._models import BaseModel
from .beta_analytics_connector_chat_cowork_unified_chat_metrics import (
    BetaAnalyticsConnectorChatCoworkUnifiedChatMetrics,
)
from .beta_analytics_connector_chat_cowork_unified_sessions_metrics import (
    BetaAnalyticsConnectorChatCoworkUnifiedSessionsMetrics,
)

__all__ = ["BetaAnalyticsConnectorChatCoworkUnifiedMetrics"]


class BetaAnalyticsConnectorChatCoworkUnifiedMetrics(BaseModel):
    """
    A connector's use in Chat and Cowork unified on one day: `chat` holds its
    use in chat conversations and `sessions` its use in Cowork sessions.
    """

    chat: BetaAnalyticsConnectorChatCoworkUnifiedChatMetrics
    """
    A connector's use in chat conversations recorded while members had Chat and
    Cowork unified turned on.
    """

    sessions: BetaAnalyticsConnectorChatCoworkUnifiedSessionsMetrics
    """
    A connector's use in Cowork sessions recorded while members had Chat and Cowork
    unified turned on.
    """
