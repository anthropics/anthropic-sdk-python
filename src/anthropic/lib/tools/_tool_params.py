"""Serializing SDK tool objects into the ``tools[]`` entries the Messages API accepts."""

from __future__ import annotations

from typing import Union, Iterable
from typing_extensions import Protocol, TypeAlias, runtime_checkable

from ..._types import Omit, NotGiven, omit
from ..._utils import is_given
from .._stainless_helpers import carry_helper_tag
from ...types.beta.beta_tool_union_param import BetaToolUnionParam

__all__ = ["BetaToolLike"]


@runtime_checkable
class SupportsToDict(Protocol):
    """An object whose ``to_dict()`` is the ``tools[]`` entry to send for it.

    ``@beta_tool`` function tools and builtin tools satisfy this, as does anything else
    with a matching ``to_dict()``.
    """

    def to_dict(self) -> BetaToolUnionParam: ...


BetaToolLike: TypeAlias = Union[BetaToolUnionParam, SupportsToDict]
"""A ``tools[]`` entry, or an object that serializes to one through ``to_dict()``."""


def to_tool_params(tools: Iterable[BetaToolLike] | Omit | NotGiven) -> list[BetaToolUnionParam] | Omit:
    """Replace every ``to_dict()``-bearing object in ``tools`` with its entry, keeping order and helper tags."""
    if not is_given(tools):
        return omit
    return [carry_helper_tag(tool, tool.to_dict()) if isinstance(tool, SupportsToDict) else tool for tool in tools]
