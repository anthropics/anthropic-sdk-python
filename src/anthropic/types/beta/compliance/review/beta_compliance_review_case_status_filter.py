from typing_extensions import Literal, TypeAlias

__all__ = ["BetaComplianceReviewCaseStatusFilter"]

BetaComplianceReviewCaseStatusFilter: TypeAlias = Literal["open", "closed"]
"""A review case status to filter by: `open` or `closed`.

- `open` - Cases that Anthropic is waiting for a response to.
- `closed` - Cases that Anthropic has stopped waiting on.
"""
