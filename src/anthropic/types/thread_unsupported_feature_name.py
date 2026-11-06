from typing_extensions import Literal, TypeAlias

__all__ = ["ThreadUnsupportedFeatureName"]

ThreadUnsupportedFeatureName: TypeAlias = Literal[
    "cache_control", "context_management", "fallbacks", "hipaa", "inference_hooks", "thinking", "zdr"
]
