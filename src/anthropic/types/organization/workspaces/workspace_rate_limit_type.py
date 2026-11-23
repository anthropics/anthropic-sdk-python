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
"""Rate limiter type.

`input_tokens_per_minute` counts every input token, cache reads included. `input_tokens_per_minute_cache_aware` does not count cache reads, and on current models the organization's input-token limit usually has this type. A workspace limit of either type applies alongside the organization's limit, not in place of it. Because cache reads count toward an `input_tokens_per_minute` limit, it can reject requests that read mostly from the cache while the organization's limit still has room.
"""
