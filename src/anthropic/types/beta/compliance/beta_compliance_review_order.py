from typing_extensions import Literal, TypeAlias

__all__ = ["BetaComplianceReviewOrder"]

BetaComplianceReviewOrder: TypeAlias = Literal["asc", "desc"]
"""A sort direction: `asc` or `desc`.

- `asc` - Oldest first.
- `desc` - Newest first.
"""
