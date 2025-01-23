# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Union
from typing_extensions import Annotated, TypeAlias

from .._utils import PropertyInfo
from .citation_char_location import CitationCharLocation
from .citation_page_location import CitationPageLocation
from .citation_content_block_location import CitationContentBlockLocation

__all__ = ["TextCitation"]

TextCitation: TypeAlias = Annotated[
    Union[CitationCharLocation, CitationPageLocation, CitationContentBlockLocation], PropertyInfo(discriminator="type")
]
