from ..._models import BaseModel
from .analytics_office_product_metrics import AnalyticsOfficeProductMetrics

__all__ = ["AnalyticsOfficeMetrics"]


class AnalyticsOfficeMetrics(BaseModel):
    """
    Office Agent activity metrics for a single user on a given day, broken out by Office product.
    """

    excel: AnalyticsOfficeProductMetrics
    """
    Office Agent activity metrics for a single user on a given day within one Office
    product.
    """

    outlook: AnalyticsOfficeProductMetrics
    """
    Office Agent activity metrics for a single user on a given day within one Office
    product.
    """

    powerpoint: AnalyticsOfficeProductMetrics
    """
    Office Agent activity metrics for a single user on a given day within one Office
    product.
    """

    word: AnalyticsOfficeProductMetrics
    """
    Office Agent activity metrics for a single user on a given day within one Office
    product.
    """
