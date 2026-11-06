from typing_extensions import Literal

from ..._exceptions import BadRequestError
from .claude_code_key_creator_not_member_error_details import ClaudeCodeKeyCreatorNotMemberErrorDetails

__all__ = ["ClaudeCodeKeyCreatorNotMemberError"]


class ClaudeCodeKeyCreatorNotMemberError(BadRequestError):
    """
    The API key belongs to the Claude Code workspace, and the user who created it is no longer a member of the organization or of that workspace.
    """

    error_code: Literal["claude_code_key_creator_not_member"]  # pyright: ignore[reportIncompatibleVariableOverride]
    details: ClaudeCodeKeyCreatorNotMemberErrorDetails  # pyright: ignore[reportIncompatibleVariableOverride]
