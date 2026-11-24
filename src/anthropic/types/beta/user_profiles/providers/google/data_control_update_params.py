from __future__ import annotations

from typing import List
from typing_extensions import TypedDict

from .....anthropic_beta_param import AnthropicBetaParam
from .beta_google_managed_cmek_control_params import BetaGoogleManagedCMEKControlParams
from .beta_google_managed_storage_control_params import BetaGoogleManagedStorageControlParams

__all__ = ["DataControlUpdateParams"]


class DataControlUpdateParams(TypedDict, total=False):
    cmek: BetaGoogleManagedCMEKControlParams
    """The customer-managed encryption key control.

    Leave it out to keep the control as it is. Send `cmek`, `storage`, or both.
    """

    storage: BetaGoogleManagedStorageControlParams
    """The customer-owned storage control.

    Leave it out to keep the control as it is. Send `cmek`, `storage`, or both.
    """

    betas: List[AnthropicBetaParam]
    """
    This endpoint is in beta: requests must send
    `google-managed-data-controls-2026-09-01` in this header.
    """

    workspace_id: str
    """Optional header to select the Workspace for this request.

    The value is a Workspace ID (for example, `wrkspc_011CZkZaBF1tNoB5wlCeusgy`).

    Only needed for credentials that can act on more than one Workspace. A
    credential that belongs to a specific Workspace may omit it; if sent, it must
    match that Workspace.
    """
