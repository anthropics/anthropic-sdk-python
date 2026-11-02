from ..._models import BaseModel
from .analytics_skill_chat_cowork_unified_chat_metrics import AnalyticsSkillChatCoworkUnifiedChatMetrics
from .analytics_skill_chat_cowork_unified_sessions_metrics import AnalyticsSkillChatCoworkUnifiedSessionsMetrics

__all__ = ["AnalyticsSkillChatCoworkUnifiedMetrics"]


class AnalyticsSkillChatCoworkUnifiedMetrics(BaseModel):
    """
    A skill's use in Chat and Cowork unified on one day: `chat` holds its use
    in chat conversations and `sessions` its use in Cowork sessions.
    """

    chat: AnalyticsSkillChatCoworkUnifiedChatMetrics
    """
    A skill's use in chat conversations recorded while members had Chat and Cowork
    unified turned on.
    """

    sessions: AnalyticsSkillChatCoworkUnifiedSessionsMetrics
    """
    A skill's use in Cowork sessions recorded while members had Chat and Cowork
    unified turned on.
    """
