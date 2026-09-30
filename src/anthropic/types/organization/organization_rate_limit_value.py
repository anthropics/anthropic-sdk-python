from ..._models import BaseModel

__all__ = ["OrganizationRateLimitValue"]


class OrganizationRateLimitValue(BaseModel):
    type: str
    """
    The limiter type (for example, `requests_per_minute` or
    `input_tokens_per_minute`).
    """

    value: int
    """The configured limit value for this limiter type."""
