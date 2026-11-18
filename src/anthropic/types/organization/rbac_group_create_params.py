from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["RBACGroupCreateParams"]


class RBACGroupCreateParams(TypedDict, total=False):
    name: Required[str]
    """Name of the RBAC Group. Not uniqueness-enforced."""
