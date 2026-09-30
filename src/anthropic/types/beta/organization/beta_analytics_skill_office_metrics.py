from ...._models import BaseModel
from .beta_analytics_skill_office_product_metrics import BetaAnalyticsSkillOfficeProductMetrics

__all__ = ["BetaAnalyticsSkillOfficeMetrics"]


class BetaAnalyticsSkillOfficeMetrics(BaseModel):
    """
    Office Agent activity metrics for a single skill on a given day, broken out by Office product.
    """

    excel: BetaAnalyticsSkillOfficeProductMetrics
    """
    Office Agent activity metrics for a single skill on a given day within one
    Office product.
    """

    outlook: BetaAnalyticsSkillOfficeProductMetrics
    """
    Office Agent activity metrics for a single skill on a given day within one
    Office product.
    """

    powerpoint: BetaAnalyticsSkillOfficeProductMetrics
    """
    Office Agent activity metrics for a single skill on a given day within one
    Office product.
    """

    word: BetaAnalyticsSkillOfficeProductMetrics
    """
    Office Agent activity metrics for a single skill on a given day within one
    Office product.
    """
