from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaGCPExternalKeyConfig"]


class BetaGCPExternalKeyConfig(BaseModel):
    key_name: str
    """Full resource name of the Cloud KMS key."""

    type: Literal["gcp"]
