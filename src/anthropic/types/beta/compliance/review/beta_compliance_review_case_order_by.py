from typing_extensions import Literal, TypeAlias

__all__ = ["BetaComplianceReviewCaseOrderBy"]

BetaComplianceReviewCaseOrderBy: TypeAlias = Literal["created_at", "updated_at"]
"""
The field that a list of review cases is sorted by: `created_at` or `updated_at`.

- `created_at` - Sort by when Anthropic sent the case.
- `updated_at` - Sort by when the case last changed.
"""
