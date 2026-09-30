from __future__ import annotations

from typing import Optional
from typing_extensions import TypedDict

__all__ = ["RBACGroupUpdateParams"]


class RBACGroupUpdateParams(TypedDict, total=False):
    name: Optional[str]
    """Name of the RBAC Group. Not uniqueness-enforced."""
