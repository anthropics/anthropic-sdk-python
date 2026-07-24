# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["BetaFallbackCreditNotApplied"]


class BetaFallbackCreditNotApplied(BaseModel):
    """No reprice was applied; ``reason`` says why."""

    reason: Literal[
        "body_mismatch",
        "continuation_excluded",
        "continuation_only",
        "expired",
        "invalid_target_model",
        "not_enabled",
        "reprice_unavailable",
        "temporarily_unavailable",
        "variant_fields_present",
        "wrong_organization",
        "wrong_platform",
        "wrong_workspace",
    ]
    """Why the reprice was not applied.

    A closed enum; additions to the redemption-check vocabulary arrive as deliberate
    schema updates.
    """

    type: Literal["not_applied"]

    remove_to_redeem: Optional[List[str]] = None
    """Request fields to remove before retrying, so the retry can redeem this token.

    Present exactly when `reason` is `variant_fields_present` — never null, never an
    empty array; absent otherwise. Fields are named only from your own request, and
    only after the sealed variant hash matched. A served best-effort retry has
    already been billed at normal price; nothing redeems retroactively, but a
    corrected re-send inside the token's five-minute window can still redeem.
    """
