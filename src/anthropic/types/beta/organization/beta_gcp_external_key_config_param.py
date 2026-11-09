from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["BetaGCPExternalKeyConfigParam"]


class BetaGCPExternalKeyConfigParam(TypedDict, total=False):
    key_name: Required[str]
    """Full resource name of the Cloud KMS key."""

    type: Required[Literal["gcp"]]
