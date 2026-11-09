from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaAPIKeyScopeMissingErrorDetails"]


class BetaAPIKeyScopeMissingErrorDetails(BaseModel):
    """
    The API key lacks the scope the request needs: `read:claude_tag` for a read, `write:claude_tag` for a change.
    """

    error_code: Literal["api_key_scope_missing"]
