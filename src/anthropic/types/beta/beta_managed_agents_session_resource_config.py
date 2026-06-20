# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Union
from typing_extensions import Annotated, TypeAlias

from ..._utils import PropertyInfo
from .beta_managed_agents_file_resource_config import BetaManagedAgentsFileResourceConfig
from .beta_managed_agents_memory_store_resource_config import BetaManagedAgentsMemoryStoreResourceConfig
from .beta_managed_agents_github_repository_resource_config import BetaManagedAgentsGitHubRepositoryResourceConfig

__all__ = ["BetaManagedAgentsSessionResourceConfig"]

BetaManagedAgentsSessionResourceConfig: TypeAlias = Annotated[
    Union[
        BetaManagedAgentsGitHubRepositoryResourceConfig,
        BetaManagedAgentsFileResourceConfig,
        BetaManagedAgentsMemoryStoreResourceConfig,
    ],
    PropertyInfo(discriminator="type"),
]
