from __future__ import annotations

from typing import List, Optional
from typing_extensions import Literal, Required, TypedDict

from ...anthropic_beta_param import AnthropicBetaParam

__all__ = ["ResourceAddParams"]


class ResourceAddParams(TypedDict, total=False):
    file_id: Required[str]
    """ID of a previously uploaded file."""

    type: Required[Literal["file"]]

    mount_path: Optional[str]
    """Mount path in the container. Defaults to `/mnt/session/uploads/<file_id>`."""

    betas: List[AnthropicBetaParam]
    """Optional header to specify the beta version(s) you want to use."""

    workspace_id: str
    """Optional header to select the Workspace for this request.

    The value is a Workspace ID (for example, `wrkspc_011CZkZaBF1tNoB5wlCeusgy`).

    Only needed for credentials that can act on more than one Workspace. A
    credential that belongs to a specific Workspace may omit it; if sent, it must
    match that Workspace.
    """
