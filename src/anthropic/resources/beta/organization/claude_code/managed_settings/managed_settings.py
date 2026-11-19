from __future__ import annotations

from .rbac_groups import (
    RBACGroups,
    AsyncRBACGroups,
    RBACGroupsWithRawResponse,
    AsyncRBACGroupsWithRawResponse,
    RBACGroupsWithStreamingResponse,
    AsyncRBACGroupsWithStreamingResponse,
)
from ......_compat import cached_property
from .configuration import (
    Configuration,
    AsyncConfiguration,
    ConfigurationWithRawResponse,
    AsyncConfigurationWithRawResponse,
    ConfigurationWithStreamingResponse,
    AsyncConfigurationWithStreamingResponse,
)
from ......_resource import SyncAPIResource, AsyncAPIResource
from .rbac_group_default import (
    RBACGroupDefault,
    AsyncRBACGroupDefault,
    RBACGroupDefaultWithRawResponse,
    AsyncRBACGroupDefaultWithRawResponse,
    RBACGroupDefaultWithStreamingResponse,
    AsyncRBACGroupDefaultWithStreamingResponse,
)

__all__ = ["ManagedSettings", "AsyncManagedSettings"]


class ManagedSettings(SyncAPIResource):
    @cached_property
    def configuration(self) -> Configuration:
        return Configuration(self._client)

    @cached_property
    def rbac_groups(self) -> RBACGroups:
        return RBACGroups(self._client)

    @cached_property
    def rbac_group_default(self) -> RBACGroupDefault:
        return RBACGroupDefault(self._client)

    @cached_property
    def with_raw_response(self) -> ManagedSettingsWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://platform.claude.com/docs/en/api/sdks/python
        """
        return ManagedSettingsWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ManagedSettingsWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://platform.claude.com/docs/en/api/sdks/python
        """
        return ManagedSettingsWithStreamingResponse(self)


class AsyncManagedSettings(AsyncAPIResource):
    @cached_property
    def configuration(self) -> AsyncConfiguration:
        return AsyncConfiguration(self._client)

    @cached_property
    def rbac_groups(self) -> AsyncRBACGroups:
        return AsyncRBACGroups(self._client)

    @cached_property
    def rbac_group_default(self) -> AsyncRBACGroupDefault:
        return AsyncRBACGroupDefault(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncManagedSettingsWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://platform.claude.com/docs/en/api/sdks/python
        """
        return AsyncManagedSettingsWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncManagedSettingsWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://platform.claude.com/docs/en/api/sdks/python
        """
        return AsyncManagedSettingsWithStreamingResponse(self)


class ManagedSettingsWithRawResponse:
    def __init__(self, managed_settings: ManagedSettings) -> None:
        self._managed_settings = managed_settings

    @cached_property
    def configuration(self) -> ConfigurationWithRawResponse:
        return ConfigurationWithRawResponse(self._managed_settings.configuration)

    @cached_property
    def rbac_groups(self) -> RBACGroupsWithRawResponse:
        return RBACGroupsWithRawResponse(self._managed_settings.rbac_groups)

    @cached_property
    def rbac_group_default(self) -> RBACGroupDefaultWithRawResponse:
        return RBACGroupDefaultWithRawResponse(self._managed_settings.rbac_group_default)


class AsyncManagedSettingsWithRawResponse:
    def __init__(self, managed_settings: AsyncManagedSettings) -> None:
        self._managed_settings = managed_settings

    @cached_property
    def configuration(self) -> AsyncConfigurationWithRawResponse:
        return AsyncConfigurationWithRawResponse(self._managed_settings.configuration)

    @cached_property
    def rbac_groups(self) -> AsyncRBACGroupsWithRawResponse:
        return AsyncRBACGroupsWithRawResponse(self._managed_settings.rbac_groups)

    @cached_property
    def rbac_group_default(self) -> AsyncRBACGroupDefaultWithRawResponse:
        return AsyncRBACGroupDefaultWithRawResponse(self._managed_settings.rbac_group_default)


class ManagedSettingsWithStreamingResponse:
    def __init__(self, managed_settings: ManagedSettings) -> None:
        self._managed_settings = managed_settings

    @cached_property
    def configuration(self) -> ConfigurationWithStreamingResponse:
        return ConfigurationWithStreamingResponse(self._managed_settings.configuration)

    @cached_property
    def rbac_groups(self) -> RBACGroupsWithStreamingResponse:
        return RBACGroupsWithStreamingResponse(self._managed_settings.rbac_groups)

    @cached_property
    def rbac_group_default(self) -> RBACGroupDefaultWithStreamingResponse:
        return RBACGroupDefaultWithStreamingResponse(self._managed_settings.rbac_group_default)


class AsyncManagedSettingsWithStreamingResponse:
    def __init__(self, managed_settings: AsyncManagedSettings) -> None:
        self._managed_settings = managed_settings

    @cached_property
    def configuration(self) -> AsyncConfigurationWithStreamingResponse:
        return AsyncConfigurationWithStreamingResponse(self._managed_settings.configuration)

    @cached_property
    def rbac_groups(self) -> AsyncRBACGroupsWithStreamingResponse:
        return AsyncRBACGroupsWithStreamingResponse(self._managed_settings.rbac_groups)

    @cached_property
    def rbac_group_default(self) -> AsyncRBACGroupDefaultWithStreamingResponse:
        return AsyncRBACGroupDefaultWithStreamingResponse(self._managed_settings.rbac_group_default)
