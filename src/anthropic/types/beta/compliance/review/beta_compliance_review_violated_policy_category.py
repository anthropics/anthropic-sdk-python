from typing_extensions import Literal, TypeAlias

__all__ = ["BetaComplianceReviewViolatedPolicyCategory"]

BetaComplianceReviewViolatedPolicyCategory: TypeAlias = Literal[
    "cyber",
    "bio",
    "chem",
    "radnuc",
    "cgw",
    "mgw",
    "io",
    "fraud",
    "violent_extremism",
    "surveillance",
    "human_exploitation",
    "self_harm",
    "adult_content",
    "reasoning_extraction",
    "frontier_llm",
    "compromised_key",
    "other",
]
