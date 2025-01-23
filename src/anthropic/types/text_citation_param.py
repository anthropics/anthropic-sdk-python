# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union
from typing_extensions import TypeAlias

from .citation_char_location_param import CitationCharLocationParam
from .citation_page_location_param import CitationPageLocationParam
from .citation_content_block_location_param import CitationContentBlockLocationParam

__all__ = ["TextCitationParam"]

TextCitationParam: TypeAlias = Union[
    CitationCharLocationParam, CitationPageLocationParam, CitationContentBlockLocationParam
]
