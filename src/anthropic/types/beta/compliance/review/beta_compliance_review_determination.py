from typing_extensions import Literal, TypeAlias

__all__ = ["BetaComplianceReviewDetermination"]

BetaComplianceReviewDetermination: TypeAlias = Literal["violation", "no_violation"]
"""A conclusion on flagged messages: `violation` or `no_violation`.

- `violation` - The messages violated a policy.
- `no_violation` - The messages violated no policy.
"""
