from __future__ import annotations

from .users import (
    Users,
    AsyncUsers,
    UsersWithRawResponse,
    AsyncUsersWithRawResponse,
    UsersWithStreamingResponse,
    AsyncUsersWithStreamingResponse,
)
from .skills import (
    Skills,
    AsyncSkills,
    SkillsWithRawResponse,
    AsyncSkillsWithRawResponse,
    SkillsWithStreamingResponse,
    AsyncSkillsWithStreamingResponse,
)
from .plugins import (
    Plugins,
    AsyncPlugins,
    PluginsWithRawResponse,
    AsyncPluginsWithRawResponse,
    PluginsWithStreamingResponse,
    AsyncPluginsWithStreamingResponse,
)
from .apps.apps import (
    Apps,
    AsyncApps,
    AppsWithRawResponse,
    AsyncAppsWithRawResponse,
    AppsWithStreamingResponse,
    AsyncAppsWithStreamingResponse,
)
from .artifacts import (
    Artifacts,
    AsyncArtifacts,
    ArtifactsWithRawResponse,
    AsyncArtifactsWithRawResponse,
    ArtifactsWithStreamingResponse,
    AsyncArtifactsWithStreamingResponse,
)
from .summaries import (
    Summaries,
    AsyncSummaries,
    SummariesWithRawResponse,
    AsyncSummariesWithRawResponse,
    SummariesWithStreamingResponse,
    AsyncSummariesWithStreamingResponse,
)
from ...._compat import cached_property
from .connectors import (
    Connectors,
    AsyncConnectors,
    ConnectorsWithRawResponse,
    AsyncConnectorsWithRawResponse,
    ConnectorsWithStreamingResponse,
    AsyncConnectorsWithStreamingResponse,
)
from ...._resource import SyncAPIResource, AsyncAPIResource

__all__ = ["Analytics", "AsyncAnalytics"]


class Analytics(SyncAPIResource):
    @cached_property
    def summaries(self) -> Summaries:
        return Summaries(self._client)

    @cached_property
    def users(self) -> Users:
        return Users(self._client)

    @cached_property
    def apps(self) -> Apps:
        return Apps(self._client)

    @cached_property
    def connectors(self) -> Connectors:
        return Connectors(self._client)

    @cached_property
    def plugins(self) -> Plugins:
        return Plugins(self._client)

    @cached_property
    def skills(self) -> Skills:
        return Skills(self._client)

    @cached_property
    def artifacts(self) -> Artifacts:
        return Artifacts(self._client)

    @cached_property
    def with_raw_response(self) -> AnalyticsWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://platform.claude.com/docs/en/api/sdks/python
        """
        return AnalyticsWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AnalyticsWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://platform.claude.com/docs/en/api/sdks/python
        """
        return AnalyticsWithStreamingResponse(self)


class AsyncAnalytics(AsyncAPIResource):
    @cached_property
    def summaries(self) -> AsyncSummaries:
        return AsyncSummaries(self._client)

    @cached_property
    def users(self) -> AsyncUsers:
        return AsyncUsers(self._client)

    @cached_property
    def apps(self) -> AsyncApps:
        return AsyncApps(self._client)

    @cached_property
    def connectors(self) -> AsyncConnectors:
        return AsyncConnectors(self._client)

    @cached_property
    def plugins(self) -> AsyncPlugins:
        return AsyncPlugins(self._client)

    @cached_property
    def skills(self) -> AsyncSkills:
        return AsyncSkills(self._client)

    @cached_property
    def artifacts(self) -> AsyncArtifacts:
        return AsyncArtifacts(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncAnalyticsWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://platform.claude.com/docs/en/api/sdks/python
        """
        return AsyncAnalyticsWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncAnalyticsWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://platform.claude.com/docs/en/api/sdks/python
        """
        return AsyncAnalyticsWithStreamingResponse(self)


class AnalyticsWithRawResponse:
    def __init__(self, analytics: Analytics) -> None:
        self._analytics = analytics

    @cached_property
    def summaries(self) -> SummariesWithRawResponse:
        return SummariesWithRawResponse(self._analytics.summaries)

    @cached_property
    def users(self) -> UsersWithRawResponse:
        return UsersWithRawResponse(self._analytics.users)

    @cached_property
    def apps(self) -> AppsWithRawResponse:
        return AppsWithRawResponse(self._analytics.apps)

    @cached_property
    def connectors(self) -> ConnectorsWithRawResponse:
        return ConnectorsWithRawResponse(self._analytics.connectors)

    @cached_property
    def plugins(self) -> PluginsWithRawResponse:
        return PluginsWithRawResponse(self._analytics.plugins)

    @cached_property
    def skills(self) -> SkillsWithRawResponse:
        return SkillsWithRawResponse(self._analytics.skills)

    @cached_property
    def artifacts(self) -> ArtifactsWithRawResponse:
        return ArtifactsWithRawResponse(self._analytics.artifacts)


class AsyncAnalyticsWithRawResponse:
    def __init__(self, analytics: AsyncAnalytics) -> None:
        self._analytics = analytics

    @cached_property
    def summaries(self) -> AsyncSummariesWithRawResponse:
        return AsyncSummariesWithRawResponse(self._analytics.summaries)

    @cached_property
    def users(self) -> AsyncUsersWithRawResponse:
        return AsyncUsersWithRawResponse(self._analytics.users)

    @cached_property
    def apps(self) -> AsyncAppsWithRawResponse:
        return AsyncAppsWithRawResponse(self._analytics.apps)

    @cached_property
    def connectors(self) -> AsyncConnectorsWithRawResponse:
        return AsyncConnectorsWithRawResponse(self._analytics.connectors)

    @cached_property
    def plugins(self) -> AsyncPluginsWithRawResponse:
        return AsyncPluginsWithRawResponse(self._analytics.plugins)

    @cached_property
    def skills(self) -> AsyncSkillsWithRawResponse:
        return AsyncSkillsWithRawResponse(self._analytics.skills)

    @cached_property
    def artifacts(self) -> AsyncArtifactsWithRawResponse:
        return AsyncArtifactsWithRawResponse(self._analytics.artifacts)


class AnalyticsWithStreamingResponse:
    def __init__(self, analytics: Analytics) -> None:
        self._analytics = analytics

    @cached_property
    def summaries(self) -> SummariesWithStreamingResponse:
        return SummariesWithStreamingResponse(self._analytics.summaries)

    @cached_property
    def users(self) -> UsersWithStreamingResponse:
        return UsersWithStreamingResponse(self._analytics.users)

    @cached_property
    def apps(self) -> AppsWithStreamingResponse:
        return AppsWithStreamingResponse(self._analytics.apps)

    @cached_property
    def connectors(self) -> ConnectorsWithStreamingResponse:
        return ConnectorsWithStreamingResponse(self._analytics.connectors)

    @cached_property
    def plugins(self) -> PluginsWithStreamingResponse:
        return PluginsWithStreamingResponse(self._analytics.plugins)

    @cached_property
    def skills(self) -> SkillsWithStreamingResponse:
        return SkillsWithStreamingResponse(self._analytics.skills)

    @cached_property
    def artifacts(self) -> ArtifactsWithStreamingResponse:
        return ArtifactsWithStreamingResponse(self._analytics.artifacts)


class AsyncAnalyticsWithStreamingResponse:
    def __init__(self, analytics: AsyncAnalytics) -> None:
        self._analytics = analytics

    @cached_property
    def summaries(self) -> AsyncSummariesWithStreamingResponse:
        return AsyncSummariesWithStreamingResponse(self._analytics.summaries)

    @cached_property
    def users(self) -> AsyncUsersWithStreamingResponse:
        return AsyncUsersWithStreamingResponse(self._analytics.users)

    @cached_property
    def apps(self) -> AsyncAppsWithStreamingResponse:
        return AsyncAppsWithStreamingResponse(self._analytics.apps)

    @cached_property
    def connectors(self) -> AsyncConnectorsWithStreamingResponse:
        return AsyncConnectorsWithStreamingResponse(self._analytics.connectors)

    @cached_property
    def plugins(self) -> AsyncPluginsWithStreamingResponse:
        return AsyncPluginsWithStreamingResponse(self._analytics.plugins)

    @cached_property
    def skills(self) -> AsyncSkillsWithStreamingResponse:
        return AsyncSkillsWithStreamingResponse(self._analytics.skills)

    @cached_property
    def artifacts(self) -> AsyncArtifactsWithStreamingResponse:
        return AsyncArtifactsWithStreamingResponse(self._analytics.artifacts)
