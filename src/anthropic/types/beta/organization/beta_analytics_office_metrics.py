from ...._models import BaseModel
from .beta_analytics_office_product_metrics import BetaAnalyticsOfficeProductMetrics

__all__ = ["BetaAnalyticsOfficeMetrics"]


class BetaAnalyticsOfficeMetrics(BaseModel):
    """
    Office Agent activity metrics for a single user on a given day, broken out by Office product.
    """

    excel: BetaAnalyticsOfficeProductMetrics
    """
    Office Agent activity metrics for a single user on a given day within one Office
    product.
    """

    outlook: BetaAnalyticsOfficeProductMetrics
    """
    Office Agent activity metrics for a single user on a given day within one Office
    product.
    """

    powerpoint: BetaAnalyticsOfficeProductMetrics
    """
    Office Agent activity metrics for a single user on a given day within one Office
    product.
    """

    word: BetaAnalyticsOfficeProductMetrics
    """
    Office Agent activity metrics for a single user on a given day within one Office
    product.
    """
