from ..._models import BaseModel
from .analytics_connector_office_product_metrics import AnalyticsConnectorOfficeProductMetrics

__all__ = ["AnalyticsConnectorOfficeMetrics"]


class AnalyticsConnectorOfficeMetrics(BaseModel):
    """
    Office Agent activity metrics for a single connector on a given day, broken out by Office product.
    """

    excel: AnalyticsConnectorOfficeProductMetrics
    """
    Office Agent activity metrics for a single connector on a given day within one
    Office product.
    """

    outlook: AnalyticsConnectorOfficeProductMetrics
    """
    Office Agent activity metrics for a single connector on a given day within one
    Office product.
    """

    powerpoint: AnalyticsConnectorOfficeProductMetrics
    """
    Office Agent activity metrics for a single connector on a given day within one
    Office product.
    """

    word: AnalyticsConnectorOfficeProductMetrics
    """
    Office Agent activity metrics for a single connector on a given day within one
    Office product.
    """
