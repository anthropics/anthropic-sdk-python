# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Union
from typing_extensions import Annotated, TypeAlias

from ..._utils import PropertyInfo
from .beta_citation_char_location import BetaCitationCharLocation
from .beta_citation_page_location import BetaCitationPageLocation
from .beta_citation_content_block_location import BetaCitationContentBlockLocation

__all__ = ["BetaTextCitation"]

BetaTextCitation: TypeAlias = Annotated[
    Union[BetaCitationCharLocation, BetaCitationPageLocation, BetaCitationContentBlockLocation],
    PropertyInfo(discriminator="type"),
]
