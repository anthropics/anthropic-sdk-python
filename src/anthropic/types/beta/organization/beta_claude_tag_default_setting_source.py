from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaClaudeTagDefaultSettingSource"]


class BetaClaudeTagDefaultSettingSource(BaseModel):
    """No settings level sets a value, and the built-in default applies."""

    type: Literal["default"]
