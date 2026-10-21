from __future__ import annotations

from typing import Union
from typing_extensions import TypeAlias, TypedDict

from .beta_web_fetch_url_source_all_param import BetaWebFetchURLSourceAllParam
from .beta_web_fetch_url_source_none_param import BetaWebFetchURLSourceNoneParam
from .beta_web_fetch_url_source_only_param import BetaWebFetchURLSourceOnlyParam
from .beta_web_fetch_url_source_except_param import BetaWebFetchURLSourceExceptParam

__all__ = ["BetaWebFetchURLSourcesParam", "ClientToolResults", "ServerToolResults", "UserInput"]

ClientToolResults: TypeAlias = Union[
    BetaWebFetchURLSourceAllParam,
    BetaWebFetchURLSourceNoneParam,
    BetaWebFetchURLSourceOnlyParam,
    BetaWebFetchURLSourceExceptParam,
]

ServerToolResults: TypeAlias = Union[
    BetaWebFetchURLSourceAllParam,
    BetaWebFetchURLSourceNoneParam,
    BetaWebFetchURLSourceOnlyParam,
    BetaWebFetchURLSourceExceptParam,
]

UserInput: TypeAlias = Union[BetaWebFetchURLSourceAllParam, BetaWebFetchURLSourceNoneParam]


class BetaWebFetchURLSourcesParam(TypedDict, total=False):
    """Which sources contribute to the set of URLs web fetch may fetch.

    Each key is a tagged variant: ``user_input`` is ``all`` or ``none``; the
    two tool filters are ``all``, ``none``, ``only`` (only the named tools'
    results) or ``except`` (every result but the named tools'). A named tool
    must be declared in this request's ``tools[]``.
    """

    client_tool_results: ClientToolResults
    """
    Which client tools' results contribute fetchable URLs: "all", "none", or an only
    or except list of client tool names from tools[].
    """

    server_tool_results: ServerToolResults
    """
    Which server tools' results contribute fetchable URLs: "all", "none", or an only
    or except list of server tool names from tools[]; only web_search and web_fetch
    results ever contribute.
    """

    user_input: UserInput
    """Whether URLs in user messages are fetchable: "all" or "none"."""
