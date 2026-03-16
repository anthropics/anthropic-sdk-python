# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Union
from typing_extensions import Annotated, TypeAlias

from ..._utils import PropertyInfo
from .beta_message_iteration_usage import BetaMessageIterationUsage
from .beta_compaction_iteration_usage import BetaCompactionIterationUsage

__all__ = ["BetaIterationsUsage", "BetaIterationsUsageItem"]

BetaIterationsUsageItem: TypeAlias = Annotated[
    Union[BetaMessageIterationUsage, BetaCompactionIterationUsage], PropertyInfo(discriminator="type")
]

BetaIterationsUsage: TypeAlias = List[BetaIterationsUsageItem]
