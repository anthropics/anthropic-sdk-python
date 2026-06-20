# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Optional
from typing_extensions import Literal, Required, TypedDict

from ..._types import SequenceNotStr

__all__ = ["BetaManagedAgentsCustomToolInputSchemaParam"]


class BetaManagedAgentsCustomToolInputSchemaParam(TypedDict, total=False, extra_items=object):  # type: ignore[call-arg]
    """JSON Schema for custom tool input parameters."""

    type: Required[Literal["object"]]

    properties: Optional[Dict[str, object]]

    required: Optional[SequenceNotStr[str]]
