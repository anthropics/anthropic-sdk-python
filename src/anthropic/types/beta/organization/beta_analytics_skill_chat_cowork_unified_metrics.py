from ...._models import BaseModel
from .beta_analytics_skill_chat_cowork_unified_chat_metrics import BetaAnalyticsSkillChatCoworkUnifiedChatMetrics
from .beta_analytics_skill_chat_cowork_unified_sessions_metrics import (
    BetaAnalyticsSkillChatCoworkUnifiedSessionsMetrics,
)

__all__ = ["BetaAnalyticsSkillChatCoworkUnifiedMetrics"]


class BetaAnalyticsSkillChatCoworkUnifiedMetrics(BaseModel):
    """
    A skill's use in Chat and Cowork unified on one day: `chat` holds its use
    in chat conversations and `sessions` its use in Cowork sessions.
    """

    chat: BetaAnalyticsSkillChatCoworkUnifiedChatMetrics
    """
    A skill's use in chat conversations recorded while members had Chat and Cowork
    unified turned on.
    """

    sessions: BetaAnalyticsSkillChatCoworkUnifiedSessionsMetrics
    """
    A skill's use in Cowork sessions recorded while members had Chat and Cowork
    unified turned on.
    """
