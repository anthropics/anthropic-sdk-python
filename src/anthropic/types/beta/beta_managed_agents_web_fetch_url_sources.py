from typing import Optional

from ..._models import BaseModel
from .beta_managed_agents_web_fetch_url_source_user_input import BetaManagedAgentsWebFetchURLSourceUserInput
from .beta_managed_agents_web_fetch_url_source_tool_filter import BetaManagedAgentsWebFetchURLSourceToolFilter

__all__ = ["BetaManagedAgentsWebFetchURLSources"]


class BetaManagedAgentsWebFetchURLSources(BaseModel):
    """Which sources contribute URLs the web_fetch tool may fetch.

    A key that is null was not set and allows every URL from that source.
    """

    client_tool_results: Optional[BetaManagedAgentsWebFetchURLSourceToolFilter] = None
    """Which custom tools' results contribute URLs that may be fetched.

    Null when not set, which allows every custom tool's results.
    """

    server_tool_results: Optional[BetaManagedAgentsWebFetchURLSourceToolFilter] = None
    """
    Which of the web_search and web_fetch tools' results contribute URLs that may be
    fetched. Null when not set, which allows both.
    """

    user_input: Optional[BetaManagedAgentsWebFetchURLSourceUserInput] = None
    """Whether URLs in the text of user messages may be fetched.

    Null when not set, which allows them.
    """
