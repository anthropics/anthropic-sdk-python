from __future__ import annotations

from typing import Union
from typing_extensions import TypeAlias

from .beta_internal_storage_param import BetaInternalStorageParam
from .beta_external_storage_member_param import BetaExternalStorageMemberParam

__all__ = ["BetaStorageMemberParam"]

BetaStorageMemberParam: TypeAlias = Union[BetaInternalStorageParam, BetaExternalStorageMemberParam]
