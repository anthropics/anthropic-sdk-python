# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union
from typing_extensions import TypeAlias

from .beta_citation_char_location_param import BetaCitationCharLocationParam
from .beta_citation_page_location_param import BetaCitationPageLocationParam
from .beta_citation_content_block_location_param import BetaCitationContentBlockLocationParam

__all__ = ["BetaTextCitationParam"]

BetaTextCitationParam: TypeAlias = Union[
    BetaCitationCharLocationParam, BetaCitationPageLocationParam, BetaCitationContentBlockLocationParam
]
