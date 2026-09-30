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
from .connectors import (
    Connectors,
    AsyncConnectors,
    ConnectorsWithRawResponse,
    AsyncConnectorsWithRawResponse,
    ConnectorsWithStreamingResponse,
    AsyncConnectorsWithStreamingResponse,
)
from ....._compat import cached_property
from .cost_report import (
    CostReport,
    AsyncCostReport,
    CostReportWithRawResponse,
    AsyncCostReportWithRawResponse,
    CostReportWithStreamingResponse,
    AsyncCostReportWithStreamingResponse,
)
from .usage_report import (
    UsageReport,
    AsyncUsageReport,
    UsageReportWithRawResponse,
    AsyncUsageReportWithRawResponse,
    UsageReportWithStreamingResponse,
    AsyncUsageReportWithStreamingResponse,
)
from ....._resource import SyncAPIResource, AsyncAPIResource
from .user_cost_report import (
    UserCostReport,
    AsyncUserCostReport,
    UserCostReportWithRawResponse,
    AsyncUserCostReportWithRawResponse,
    UserCostReportWithStreamingResponse,
    AsyncUserCostReportWithStreamingResponse,
)
from .user_usage_report import (
    UserUsageReport,
    AsyncUserUsageReport,
    UserUsageReportWithRawResponse,
    AsyncUserUsageReportWithRawResponse,
    UserUsageReportWithStreamingResponse,
    AsyncUserUsageReportWithStreamingResponse,
)

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
    def usage_report(self) -> UsageReport:
        return UsageReport(self._client)

    @cached_property
    def user_usage_report(self) -> UserUsageReport:
        return UserUsageReport(self._client)

    @cached_property
    def cost_report(self) -> CostReport:
        return CostReport(self._client)

    @cached_property
    def user_cost_report(self) -> UserCostReport:
        return UserCostReport(self._client)

    @cached_property
    def with_raw_response(self) -> AnalyticsWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#accessing-raw-response-data-eg-headers
        """
        return AnalyticsWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AnalyticsWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#with_streaming_response
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
    def usage_report(self) -> AsyncUsageReport:
        return AsyncUsageReport(self._client)

    @cached_property
    def user_usage_report(self) -> AsyncUserUsageReport:
        return AsyncUserUsageReport(self._client)

    @cached_property
    def cost_report(self) -> AsyncCostReport:
        return AsyncCostReport(self._client)

    @cached_property
    def user_cost_report(self) -> AsyncUserCostReport:
        return AsyncUserCostReport(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncAnalyticsWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#accessing-raw-response-data-eg-headers
        """
        return AsyncAnalyticsWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncAnalyticsWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#with_streaming_response
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

    @cached_property
    def usage_report(self) -> UsageReportWithRawResponse:
        return UsageReportWithRawResponse(self._analytics.usage_report)

    @cached_property
    def user_usage_report(self) -> UserUsageReportWithRawResponse:
        return UserUsageReportWithRawResponse(self._analytics.user_usage_report)

    @cached_property
    def cost_report(self) -> CostReportWithRawResponse:
        return CostReportWithRawResponse(self._analytics.cost_report)

    @cached_property
    def user_cost_report(self) -> UserCostReportWithRawResponse:
        return UserCostReportWithRawResponse(self._analytics.user_cost_report)


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

    @cached_property
    def usage_report(self) -> AsyncUsageReportWithRawResponse:
        return AsyncUsageReportWithRawResponse(self._analytics.usage_report)

    @cached_property
    def user_usage_report(self) -> AsyncUserUsageReportWithRawResponse:
        return AsyncUserUsageReportWithRawResponse(self._analytics.user_usage_report)

    @cached_property
    def cost_report(self) -> AsyncCostReportWithRawResponse:
        return AsyncCostReportWithRawResponse(self._analytics.cost_report)

    @cached_property
    def user_cost_report(self) -> AsyncUserCostReportWithRawResponse:
        return AsyncUserCostReportWithRawResponse(self._analytics.user_cost_report)


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

    @cached_property
    def usage_report(self) -> UsageReportWithStreamingResponse:
        return UsageReportWithStreamingResponse(self._analytics.usage_report)

    @cached_property
    def user_usage_report(self) -> UserUsageReportWithStreamingResponse:
        return UserUsageReportWithStreamingResponse(self._analytics.user_usage_report)

    @cached_property
    def cost_report(self) -> CostReportWithStreamingResponse:
        return CostReportWithStreamingResponse(self._analytics.cost_report)

    @cached_property
    def user_cost_report(self) -> UserCostReportWithStreamingResponse:
        return UserCostReportWithStreamingResponse(self._analytics.user_cost_report)


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

    @cached_property
    def usage_report(self) -> AsyncUsageReportWithStreamingResponse:
        return AsyncUsageReportWithStreamingResponse(self._analytics.usage_report)

    @cached_property
    def user_usage_report(self) -> AsyncUserUsageReportWithStreamingResponse:
        return AsyncUserUsageReportWithStreamingResponse(self._analytics.user_usage_report)

    @cached_property
    def cost_report(self) -> AsyncCostReportWithStreamingResponse:
        return AsyncCostReportWithStreamingResponse(self._analytics.cost_report)

    @cached_property
    def user_cost_report(self) -> AsyncUserCostReportWithStreamingResponse:
        return AsyncUserCostReportWithStreamingResponse(self._analytics.user_cost_report)
