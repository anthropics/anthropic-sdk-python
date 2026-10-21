from typing_extensions import Literal, TypeAlias

__all__ = ["BetaAnalyticsTokenType"]

BetaAnalyticsTokenType: TypeAlias = Literal[
    "cache_creation.ephemeral_1h_input_tokens",
    "cache_creation.ephemeral_5m_input_tokens",
    "cache_read_input_tokens",
    "output_tokens",
    "uncached_input_tokens",
]
