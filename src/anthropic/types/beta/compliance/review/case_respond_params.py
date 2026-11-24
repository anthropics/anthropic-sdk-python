from __future__ import annotations

from typing import List, Iterable
from typing_extensions import Required, TypedDict

from ....anthropic_beta_param import AnthropicBetaParam
from .beta_compliance_review_determination import BetaComplianceReviewDetermination
from .beta_compliance_review_verdict_param import BetaComplianceReviewVerdictParam
from .beta_compliance_review_violated_policy_category import BetaComplianceReviewViolatedPolicyCategory

__all__ = ["CaseRespondParams"]


class CaseRespondParams(TypedDict, total=False):
    determination: Required[BetaComplianceReviewDetermination]
    """Your conclusion on the case as a whole.

    Anthropic doesn't check it against `verdicts`.
    """

    policy_categories: List[BetaComplianceReviewViolatedPolicyCategory]
    """The policy categories that you found were violated.

    Send one to four with `violation`, and none with `no_violation`. They need not
    match the case's own. Each value is one of `cyber`, `bio`, `chem`, `radnuc`
    (radiological or nuclear weapons), `cgw` (conventional weapons), `mgw`
    (military-grade weapons systems), `io` (influence operations), `fraud`,
    `violent_extremism`, `surveillance`, `human_exploitation`, `self_harm`,
    `adult_content`, `reasoning_extraction`, `frontier_llm` (use of the model to
    accelerate frontier AI research and development in restricted ways),
    `compromised_key` or `other`, and can appear once.
    """

    verdicts: Iterable[BetaComplianceReviewVerdictParam]
    """Your conclusions on individual messages of the case.

    They need not cover every message, and each `item_id` can appear once.
    """

    betas: List[AnthropicBetaParam]
    """Optional header to specify the beta version(s) you want to use."""
