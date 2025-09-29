# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List

from ..._models import BaseModel
from .beta_clear_tool_uses_20250919_edit_response import BetaClearToolUses20250919EditResponse

__all__ = ["BetaContextManagementResponse"]


class BetaContextManagementResponse(BaseModel):
    applied_edits: List[BetaClearToolUses20250919EditResponse]
    """List of context management edits that were applied."""
