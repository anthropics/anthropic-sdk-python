from __future__ import annotations

from typing import Union
from typing_extensions import Literal, Required, TypedDict

from ..._types import Base64FileInput
from ..._models import set_pydantic_config

__all__ = ["BetaBase64PDFSourceParam"]


class BetaBase64PDFSourceParam(TypedDict, total=False):
    data: Required[Union[str, Base64FileInput]]

    media_type: Required[Literal["application/pdf"]]

    type: Required[Literal["base64"]]


set_pydantic_config(BetaBase64PDFSourceParam, {"arbitrary_types_allowed": True})
