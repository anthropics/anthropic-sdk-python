from typing import Union
from typing_extensions import Annotated, TypeAlias

from ...._models import UnionDiscriminator
from .beta_internal_storage import BetaInternalStorage
from .beta_external_storage_member import BetaExternalStorageMember

__all__ = ["BetaStorageMember"]

BetaStorageMember: TypeAlias = Annotated[
    Union[BetaInternalStorage, BetaExternalStorageMember], UnionDiscriminator("type")
]
