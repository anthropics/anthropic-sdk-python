# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Union
from typing_extensions import Annotated, TypeAlias

from ..._utils import PropertyInfo
from .beta_managed_agents_bash_tool_config import BetaManagedAgentsBashToolConfig
from .beta_managed_agents_edit_tool_config import BetaManagedAgentsEditToolConfig
from .beta_managed_agents_glob_tool_config import BetaManagedAgentsGlobToolConfig
from .beta_managed_agents_grep_tool_config import BetaManagedAgentsGrepToolConfig
from .beta_managed_agents_read_tool_config import BetaManagedAgentsReadToolConfig
from .beta_managed_agents_write_tool_config import BetaManagedAgentsWriteToolConfig
from .beta_managed_agents_web_fetch_tool_config import BetaManagedAgentsWebFetchToolConfig
from .beta_managed_agents_web_search_tool_config import BetaManagedAgentsWebSearchToolConfig

__all__ = ["BetaManagedAgentsAgentToolConfig"]

BetaManagedAgentsAgentToolConfig: TypeAlias = Annotated[
    Union[
        BetaManagedAgentsBashToolConfig,
        BetaManagedAgentsEditToolConfig,
        BetaManagedAgentsReadToolConfig,
        BetaManagedAgentsWriteToolConfig,
        BetaManagedAgentsGlobToolConfig,
        BetaManagedAgentsGrepToolConfig,
        BetaManagedAgentsWebFetchToolConfig,
        BetaManagedAgentsWebSearchToolConfig,
    ],
    PropertyInfo(discriminator="type"),
]
