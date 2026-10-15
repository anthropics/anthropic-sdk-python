from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["BetaBase64PDFSource"]


class BetaBase64PDFSource(BaseModel):
    data: str

    media_type: Literal["application/pdf"]

    type: Literal["base64"]
