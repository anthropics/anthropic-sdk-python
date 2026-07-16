# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from .files import (
    Files,
    AsyncFiles,
    FilesWithRawResponse,
    AsyncFilesWithRawResponse,
    FilesWithStreamingResponse,
    AsyncFilesWithStreamingResponse,
)
from .dreams import (
    Dreams,
    AsyncDreams,
    DreamsWithRawResponse,
    AsyncDreamsWithRawResponse,
    DreamsWithStreamingResponse,
    AsyncDreamsWithStreamingResponse,
)
from .models import (
    Models,
    AsyncModels,
    ModelsWithRawResponse,
    AsyncModelsWithRawResponse,
    ModelsWithStreamingResponse,
    AsyncModelsWithStreamingResponse,
)
from .webhooks import Webhooks, AsyncWebhooks
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from .deployments import (
    Deployments,
    AsyncDeployments,
    DeploymentsWithRawResponse,
    AsyncDeploymentsWithRawResponse,
    DeploymentsWithStreamingResponse,
    AsyncDeploymentsWithStreamingResponse,
)
from .agents.agents import (
    Agents,
    AsyncAgents,
    AgentsWithRawResponse,
    AsyncAgentsWithRawResponse,
    AgentsWithStreamingResponse,
    AsyncAgentsWithStreamingResponse,
)
from .skills.skills import (
    Skills,
    AsyncSkills,
    SkillsWithRawResponse,
    AsyncSkillsWithRawResponse,
    SkillsWithStreamingResponse,
    AsyncSkillsWithStreamingResponse,
)
from .user_profiles import (
    UserProfiles,
    AsyncUserProfiles,
    UserProfilesWithRawResponse,
    AsyncUserProfilesWithRawResponse,
    UserProfilesWithStreamingResponse,
    AsyncUserProfilesWithStreamingResponse,
)
from .vaults.vaults import (
    Vaults,
    AsyncVaults,
    VaultsWithRawResponse,
    AsyncVaultsWithRawResponse,
    VaultsWithStreamingResponse,
    AsyncVaultsWithStreamingResponse,
)
from .deployment_runs import (
    DeploymentRuns,
    AsyncDeploymentRuns,
    DeploymentRunsWithRawResponse,
    AsyncDeploymentRunsWithRawResponse,
    DeploymentRunsWithStreamingResponse,
    AsyncDeploymentRunsWithStreamingResponse,
)
from .tunnels.tunnels import (
    Tunnels,
    AsyncTunnels,
    TunnelsWithRawResponse,
    AsyncTunnelsWithRawResponse,
    TunnelsWithStreamingResponse,
    AsyncTunnelsWithStreamingResponse,
)
from .messages.messages import (
    Messages,
    AsyncMessages,
    MessagesWithRawResponse,
    AsyncMessagesWithRawResponse,
    MessagesWithStreamingResponse,
    AsyncMessagesWithStreamingResponse,
)
from .sessions.sessions import (
    Sessions,
    AsyncSessions,
    SessionsWithRawResponse,
    AsyncSessionsWithRawResponse,
    SessionsWithStreamingResponse,
    AsyncSessionsWithStreamingResponse,
)
from .environments.environments import (
    Environments,
    AsyncEnvironments,
    EnvironmentsWithRawResponse,
    AsyncEnvironmentsWithRawResponse,
    EnvironmentsWithStreamingResponse,
    AsyncEnvironmentsWithStreamingResponse,
)
from .memory_stores.memory_stores import (
    MemoryStores,
    AsyncMemoryStores,
    MemoryStoresWithRawResponse,
    AsyncMemoryStoresWithRawResponse,
    MemoryStoresWithStreamingResponse,
    AsyncMemoryStoresWithStreamingResponse,
)

__all__ = ["Beta", "AsyncBeta"]


class Beta(SyncAPIResource):
    @cached_property
    def models(self) -> Models:
        return Models(self._client)

    @cached_property
    def messages(self) -> Messages:
        return Messages(self._client)

    @cached_property
    def agents(self) -> Agents:
        return Agents(self._client)

    @cached_property
    def environments(self) -> Environments:
        return Environments(self._client)

    @cached_property
    def sessions(self) -> Sessions:
        return Sessions(self._client)

    @cached_property
    def deployments(self) -> Deployments:
        return Deployments(self._client)

    @cached_property
    def deployment_runs(self) -> DeploymentRuns:
        return DeploymentRuns(self._client)

    @cached_property
    def vaults(self) -> Vaults:
        return Vaults(self._client)

    @cached_property
    def memory_stores(self) -> MemoryStores:
        return MemoryStores(self._client)

    @cached_property
    def files(self) -> Files:
        return Files(self._client)

    @cached_property
    def skills(self) -> Skills:
        return Skills(self._client)

    @cached_property
    def webhooks(self) -> Webhooks:
        return Webhooks(self._client)

    @cached_property
    def user_profiles(self) -> UserProfiles:
        return UserProfiles(self._client)

    @cached_property
    def dreams(self) -> Dreams:
        return Dreams(self._client)

    @cached_property
    def tunnels(self) -> Tunnels:
        return Tunnels(self._client)

    @cached_property
    def with_raw_response(self) -> BetaWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#accessing-raw-response-data-eg-headers
        """
        return BetaWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> BetaWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#with_streaming_response
        """
        return BetaWithStreamingResponse(self)


class AsyncBeta(AsyncAPIResource):
    @cached_property
    def models(self) -> AsyncModels:
        return AsyncModels(self._client)

    @cached_property
    def messages(self) -> AsyncMessages:
        return AsyncMessages(self._client)

    @cached_property
    def agents(self) -> AsyncAgents:
        return AsyncAgents(self._client)

    @cached_property
    def environments(self) -> AsyncEnvironments:
        return AsyncEnvironments(self._client)

    @cached_property
    def sessions(self) -> AsyncSessions:
        return AsyncSessions(self._client)

    @cached_property
    def deployments(self) -> AsyncDeployments:
        return AsyncDeployments(self._client)

    @cached_property
    def deployment_runs(self) -> AsyncDeploymentRuns:
        return AsyncDeploymentRuns(self._client)

    @cached_property
    def vaults(self) -> AsyncVaults:
        return AsyncVaults(self._client)

    @cached_property
    def memory_stores(self) -> AsyncMemoryStores:
        return AsyncMemoryStores(self._client)

    @cached_property
    def files(self) -> AsyncFiles:
        return AsyncFiles(self._client)

    @cached_property
    def skills(self) -> AsyncSkills:
        return AsyncSkills(self._client)

    @cached_property
    def webhooks(self) -> AsyncWebhooks:
        return AsyncWebhooks(self._client)

    @cached_property
    def user_profiles(self) -> AsyncUserProfiles:
        return AsyncUserProfiles(self._client)

    @cached_property
    def dreams(self) -> AsyncDreams:
        return AsyncDreams(self._client)

    @cached_property
    def tunnels(self) -> AsyncTunnels:
        return AsyncTunnels(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncBetaWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#accessing-raw-response-data-eg-headers
        """
        return AsyncBetaWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncBetaWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#with_streaming_response
        """
        return AsyncBetaWithStreamingResponse(self)


class BetaWithRawResponse:
    def __init__(self, beta: Beta) -> None:
        self._beta = beta

    @cached_property
    def models(self) -> ModelsWithRawResponse:
        return ModelsWithRawResponse(self._beta.models)

    @cached_property
    def messages(self) -> MessagesWithRawResponse:
        return MessagesWithRawResponse(self._beta.messages)

    @cached_property
    def agents(self) -> AgentsWithRawResponse:
        return AgentsWithRawResponse(self._beta.agents)

    @cached_property
    def environments(self) -> EnvironmentsWithRawResponse:
        return EnvironmentsWithRawResponse(self._beta.environments)

    @cached_property
    def sessions(self) -> SessionsWithRawResponse:
        return SessionsWithRawResponse(self._beta.sessions)

    @cached_property
    def deployments(self) -> DeploymentsWithRawResponse:
        return DeploymentsWithRawResponse(self._beta.deployments)

    @cached_property
    def deployment_runs(self) -> DeploymentRunsWithRawResponse:
        return DeploymentRunsWithRawResponse(self._beta.deployment_runs)

    @cached_property
    def vaults(self) -> VaultsWithRawResponse:
        return VaultsWithRawResponse(self._beta.vaults)

    @cached_property
    def memory_stores(self) -> MemoryStoresWithRawResponse:
        return MemoryStoresWithRawResponse(self._beta.memory_stores)

    @cached_property
    def files(self) -> FilesWithRawResponse:
        return FilesWithRawResponse(self._beta.files)

    @cached_property
    def skills(self) -> SkillsWithRawResponse:
        return SkillsWithRawResponse(self._beta.skills)

    @cached_property
    def user_profiles(self) -> UserProfilesWithRawResponse:
        return UserProfilesWithRawResponse(self._beta.user_profiles)

    @cached_property
    def dreams(self) -> DreamsWithRawResponse:
        return DreamsWithRawResponse(self._beta.dreams)

    @cached_property
    def tunnels(self) -> TunnelsWithRawResponse:
        return TunnelsWithRawResponse(self._beta.tunnels)


class AsyncBetaWithRawResponse:
    def __init__(self, beta: AsyncBeta) -> None:
        self._beta = beta

    @cached_property
    def models(self) -> AsyncModelsWithRawResponse:
        return AsyncModelsWithRawResponse(self._beta.models)

    @cached_property
    def messages(self) -> AsyncMessagesWithRawResponse:
        return AsyncMessagesWithRawResponse(self._beta.messages)

    @cached_property
    def agents(self) -> AsyncAgentsWithRawResponse:
        return AsyncAgentsWithRawResponse(self._beta.agents)

    @cached_property
    def environments(self) -> AsyncEnvironmentsWithRawResponse:
        return AsyncEnvironmentsWithRawResponse(self._beta.environments)

    @cached_property
    def sessions(self) -> AsyncSessionsWithRawResponse:
        return AsyncSessionsWithRawResponse(self._beta.sessions)

    @cached_property
    def deployments(self) -> AsyncDeploymentsWithRawResponse:
        return AsyncDeploymentsWithRawResponse(self._beta.deployments)

    @cached_property
    def deployment_runs(self) -> AsyncDeploymentRunsWithRawResponse:
        return AsyncDeploymentRunsWithRawResponse(self._beta.deployment_runs)

    @cached_property
    def vaults(self) -> AsyncVaultsWithRawResponse:
        return AsyncVaultsWithRawResponse(self._beta.vaults)

    @cached_property
    def memory_stores(self) -> AsyncMemoryStoresWithRawResponse:
        return AsyncMemoryStoresWithRawResponse(self._beta.memory_stores)

    @cached_property
    def files(self) -> AsyncFilesWithRawResponse:
        return AsyncFilesWithRawResponse(self._beta.files)

    @cached_property
    def skills(self) -> AsyncSkillsWithRawResponse:
        return AsyncSkillsWithRawResponse(self._beta.skills)

    @cached_property
    def user_profiles(self) -> AsyncUserProfilesWithRawResponse:
        return AsyncUserProfilesWithRawResponse(self._beta.user_profiles)

    @cached_property
    def dreams(self) -> AsyncDreamsWithRawResponse:
        return AsyncDreamsWithRawResponse(self._beta.dreams)

    @cached_property
    def tunnels(self) -> AsyncTunnelsWithRawResponse:
        return AsyncTunnelsWithRawResponse(self._beta.tunnels)


class BetaWithStreamingResponse:
    def __init__(self, beta: Beta) -> None:
        self._beta = beta

    @cached_property
    def models(self) -> ModelsWithStreamingResponse:
        return ModelsWithStreamingResponse(self._beta.models)

    @cached_property
    def messages(self) -> MessagesWithStreamingResponse:
        return MessagesWithStreamingResponse(self._beta.messages)

    @cached_property
    def agents(self) -> AgentsWithStreamingResponse:
        return AgentsWithStreamingResponse(self._beta.agents)

    @cached_property
    def environments(self) -> EnvironmentsWithStreamingResponse:
        return EnvironmentsWithStreamingResponse(self._beta.environments)

    @cached_property
    def sessions(self) -> SessionsWithStreamingResponse:
        return SessionsWithStreamingResponse(self._beta.sessions)

    @cached_property
    def deployments(self) -> DeploymentsWithStreamingResponse:
        return DeploymentsWithStreamingResponse(self._beta.deployments)

    @cached_property
    def deployment_runs(self) -> DeploymentRunsWithStreamingResponse:
        return DeploymentRunsWithStreamingResponse(self._beta.deployment_runs)

    @cached_property
    def vaults(self) -> VaultsWithStreamingResponse:
        return VaultsWithStreamingResponse(self._beta.vaults)

    @cached_property
    def memory_stores(self) -> MemoryStoresWithStreamingResponse:
        return MemoryStoresWithStreamingResponse(self._beta.memory_stores)

    @cached_property
    def files(self) -> FilesWithStreamingResponse:
        return FilesWithStreamingResponse(self._beta.files)

    @cached_property
    def skills(self) -> SkillsWithStreamingResponse:
        return SkillsWithStreamingResponse(self._beta.skills)

    @cached_property
    def user_profiles(self) -> UserProfilesWithStreamingResponse:
        return UserProfilesWithStreamingResponse(self._beta.user_profiles)

    @cached_property
    def dreams(self) -> DreamsWithStreamingResponse:
        return DreamsWithStreamingResponse(self._beta.dreams)

    @cached_property
    def tunnels(self) -> TunnelsWithStreamingResponse:
        return TunnelsWithStreamingResponse(self._beta.tunnels)


class AsyncBetaWithStreamingResponse:
    def __init__(self, beta: AsyncBeta) -> None:
        self._beta = beta

    @cached_property
    def models(self) -> AsyncModelsWithStreamingResponse:
        return AsyncModelsWithStreamingResponse(self._beta.models)

    @cached_property
    def messages(self) -> AsyncMessagesWithStreamingResponse:
        return AsyncMessagesWithStreamingResponse(self._beta.messages)

    @cached_property
    def agents(self) -> AsyncAgentsWithStreamingResponse:
        return AsyncAgentsWithStreamingResponse(self._beta.agents)

    @cached_property
    def environments(self) -> AsyncEnvironmentsWithStreamingResponse:
        return AsyncEnvironmentsWithStreamingResponse(self._beta.environments)

    @cached_property
    def sessions(self) -> AsyncSessionsWithStreamingResponse:
        return AsyncSessionsWithStreamingResponse(self._beta.sessions)

    @cached_property
    def deployments(self) -> AsyncDeploymentsWithStreamingResponse:
        return AsyncDeploymentsWithStreamingResponse(self._beta.deployments)

    @cached_property
    def deployment_runs(self) -> AsyncDeploymentRunsWithStreamingResponse:
        return AsyncDeploymentRunsWithStreamingResponse(self._beta.deployment_runs)

    @cached_property
    def vaults(self) -> AsyncVaultsWithStreamingResponse:
        return AsyncVaultsWithStreamingResponse(self._beta.vaults)

    @cached_property
    def memory_stores(self) -> AsyncMemoryStoresWithStreamingResponse:
        return AsyncMemoryStoresWithStreamingResponse(self._beta.memory_stores)

    @cached_property
    def files(self) -> AsyncFilesWithStreamingResponse:
        return AsyncFilesWithStreamingResponse(self._beta.files)

    @cached_property
    def skills(self) -> AsyncSkillsWithStreamingResponse:
        return AsyncSkillsWithStreamingResponse(self._beta.skills)

    @cached_property
    def user_profiles(self) -> AsyncUserProfilesWithStreamingResponse:
        return AsyncUserProfilesWithStreamingResponse(self._beta.user_profiles)

    @cached_property
    def dreams(self) -> AsyncDreamsWithStreamingResponse:
        return AsyncDreamsWithStreamingResponse(self._beta.dreams)

    @cached_property
    def tunnels(self) -> AsyncTunnelsWithStreamingResponse:
        return AsyncTunnelsWithStreamingResponse(self._beta.tunnels)
