from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["ExternalKeyInWorkspacePolicyErrorDetails"]


class ExternalKeyInWorkspacePolicyErrorDetails(BaseModel):
    """
    The External Key can't be deleted or reconfigured while the organization's Workspace Policy lists it as an allowed key.
    """

    error_code: Literal["external_key_in_workspace_policy"]
