from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["GCPExternalKeyConfig"]


class GCPExternalKeyConfig(BaseModel):
    key_name: str
    """Full resource name of the Cloud KMS key."""

    type: Literal["gcp"]
