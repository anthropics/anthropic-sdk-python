from typing_extensions import Literal, TypeAlias

__all__ = ["WorkspaceRateLimitType"]

WorkspaceRateLimitType: TypeAlias = Literal[
    "fast_itpmca",
    "fast_otpm",
    "input_tokens_per_minute",
    "input_tokens_per_minute_cache_aware",
    "output_tokens_per_minute",
    "requests_per_minute",
    "tokens_per_day",
    "tokens_per_minute",
    "tool_uses_per_second",
]
