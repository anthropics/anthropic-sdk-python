from __future__ import annotations

from typing import List
from typing_extensions import TypedDict

from ......anthropic_beta_param import AnthropicBetaParam
from .beta_google_managed_project_cmek_control_params import BetaGoogleManagedProjectCMEKControlParams
from .beta_google_managed_project_storage_control_params import BetaGoogleManagedProjectStorageControlParams

__all__ = ["DataControlUpdateParams"]


class DataControlUpdateParams(TypedDict, total=False):
    cmek: BetaGoogleManagedProjectCMEKControlParams
    """The customer-managed encryption key control.

    Leave it out to keep the control as it is. Send `cmek`, `storage`, or both.
    """

    storage: BetaGoogleManagedProjectStorageControlParams
    """The customer-owned storage control.

    Leave it out to keep the control as it is. Send `cmek`, `storage`, or both.
    """

    betas: List[AnthropicBetaParam]
    """
    This endpoint is in beta: requests must send
    `google-managed-data-controls-2026-09-01` in this header.
    """
