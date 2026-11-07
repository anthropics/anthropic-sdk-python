from __future__ import annotations

from typing import Dict
from typing_extensions import Literal, Required, TypedDict

__all__ = ["JSONOutputFormatParam"]


class JSONOutputFormatParam(TypedDict, total=False):
    schema: Required[Dict[str, object]]
    """The JSON schema of the format"""

    type: Required[Literal["json_schema"]]
