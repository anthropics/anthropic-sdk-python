from ...._models import BaseModel

__all__ = ["BetaClaudeTagSlackWorkspaceIdentifiers"]


class BetaClaudeTagSlackWorkspaceIdentifiers(BaseModel):
    """The identifier Slack shows for a workspace.

    It is Slack's own, not an identifier of this API.
    """

    workspace_id: str
    """Slack's identifier for the workspace, starting with `T`, such as `T0123ABCD`."""
