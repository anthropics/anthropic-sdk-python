# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["BetaAdvisorRedactedResultBlock"]


class BetaAdvisorRedactedResultBlock(BaseModel):
    encrypted_content: str
    """Opaque blob containing the advisor's output.

    Round-trip verbatim; do not inspect or modify.
    """

    stop_reason: Optional[str] = None
    """
    The advisor sub-inference's stop reason (same values as the top-level message
    `stop_reason`).
    """

    type: Literal["advisor_redacted_result"]
