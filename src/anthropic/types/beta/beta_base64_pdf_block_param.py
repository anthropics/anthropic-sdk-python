# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union, Optional
from typing_extensions import Literal, Required, TypeAlias, TypedDict

from .beta_citations_config_param import BetaCitationsConfigParam
from .beta_base64_pdf_source_param import BetaBase64PDFSourceParam
from .beta_plain_text_source_param import BetaPlainTextSourceParam
from .beta_content_block_source_param import BetaContentBlockSourceParam
from .beta_cache_control_ephemeral_param import BetaCacheControlEphemeralParam

__all__ = ["BetaBase64PDFBlockParam", "Source"]

Source: TypeAlias = Union[BetaBase64PDFSourceParam, BetaPlainTextSourceParam, BetaContentBlockSourceParam]


class BetaBase64PDFBlockParam(TypedDict, total=False):
    source: Required[Source]

    type: Required[Literal["document"]]

    cache_control: Optional[BetaCacheControlEphemeralParam]

    citations: BetaCitationsConfigParam

    context: Optional[str]

    title: Optional[str]
