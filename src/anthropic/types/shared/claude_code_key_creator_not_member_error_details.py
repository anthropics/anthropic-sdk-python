from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["ClaudeCodeKeyCreatorNotMemberErrorDetails"]


class ClaudeCodeKeyCreatorNotMemberErrorDetails(BaseModel):
    """
    The API key belongs to the Claude Code workspace, and the user who created it is no longer a member of the organization or of that workspace.
    """

    error_code: Literal["claude_code_key_creator_not_member"]
