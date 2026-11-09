from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["Base64PDFSource"]


class Base64PDFSource(BaseModel):
    data: str

    media_type: Literal["application/pdf"]

    type: Literal["base64"]
