from ...._models import BaseModel
from .beta_analytics_connector_office_product_metrics import BetaAnalyticsConnectorOfficeProductMetrics

__all__ = ["BetaAnalyticsConnectorOfficeMetrics"]


class BetaAnalyticsConnectorOfficeMetrics(BaseModel):
    """
    Office Agent activity metrics for a single connector on a given day, broken out by Office product.
    """

    excel: BetaAnalyticsConnectorOfficeProductMetrics
    """
    Office Agent activity metrics for a single connector on a given day within one
    Office product.
    """

    outlook: BetaAnalyticsConnectorOfficeProductMetrics
    """
    Office Agent activity metrics for a single connector on a given day within one
    Office product.
    """

    powerpoint: BetaAnalyticsConnectorOfficeProductMetrics
    """
    Office Agent activity metrics for a single connector on a given day within one
    Office product.
    """

    word: BetaAnalyticsConnectorOfficeProductMetrics
    """
    Office Agent activity metrics for a single connector on a given day within one
    Office product.
    """
