from ..._models import BaseModel
from .analytics_skill_office_product_metrics import AnalyticsSkillOfficeProductMetrics

__all__ = ["AnalyticsSkillOfficeMetrics"]


class AnalyticsSkillOfficeMetrics(BaseModel):
    """
    Office Agent activity metrics for a single skill on a given day, broken out by Office product.
    """

    excel: AnalyticsSkillOfficeProductMetrics
    """
    Office Agent activity metrics for a single skill on a given day within one
    Office product.
    """

    outlook: AnalyticsSkillOfficeProductMetrics
    """
    Office Agent activity metrics for a single skill on a given day within one
    Office product.
    """

    powerpoint: AnalyticsSkillOfficeProductMetrics
    """
    Office Agent activity metrics for a single skill on a given day within one
    Office product.
    """

    word: AnalyticsSkillOfficeProductMetrics
    """
    Office Agent activity metrics for a single skill on a given day within one
    Office product.
    """
