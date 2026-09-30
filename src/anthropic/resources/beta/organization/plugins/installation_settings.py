from __future__ import annotations

from typing import List, Optional
from itertools import chain
from typing_extensions import Literal

import httpx2

from ....._types import Body, Omit, Query, Headers, NotGiven, omit, not_given
from ....._utils import is_given, path_template, strip_not_given
from ....._compat import cached_property
from ....._resource import SyncAPIResource, AsyncAPIResource
from ....._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from .....pagination import SyncPageCursor, AsyncPageCursor
from ....._base_client import AsyncPaginator, make_request_options
from .....types.anthropic_beta_param import AnthropicBetaParam
from .....types.beta.organization.plugins.beta_plugin_installation_setting import BetaPluginInstallationSetting
from .....types.beta.organization.plugins.beta_deleted_plugin_installation_setting import (
    BetaDeletedPluginInstallationSetting,
)

__all__ = ["InstallationSettings", "AsyncInstallationSettings"]


class InstallationSettings(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> InstallationSettingsWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#accessing-raw-response-data-eg-headers
        """
        return InstallationSettingsWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> InstallationSettingsWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#with_streaming_response
        """
        return InstallationSettingsWithStreamingResponse(self)

    def list(
        self,
        plugin_id: str,
        *,
        limit: int | Omit = omit,
        organization_id: Optional[str] | Omit = omit,
        page: Optional[str] | Omit = omit,
        target_type: Optional[Literal["organization", "rbac_group"]] | Omit = omit,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> SyncPageCursor[BetaPluginInstallationSetting]:
        """
        List an organization-owned Plugin's installation settings, which say which
        members it is for, most recently created first.

        The list holds the Plugin's own organization-wide setting (absent while the
        Plugin inherits its marketplace's default) and each RBAC Group's own setting. A
        member-owned Plugin has shares instead, so this path returns 404 for one.

        **Accepted credentials:** an Admin API key with the `read:plugins` or
        `read:org_audit` scope, or a Compliance Access Key with the
        `read:compliance_org_data` scope.

        Every request must include the beta header
        `anthropic-beta: ce-plugins-2026-09-01`. A request without it returns `404`,
        exactly as if the endpoint did not exist. The Plugins API is in beta and is
        available to Claude Enterprise organizations only. It is not available to Claude
        Platform (Claude Console) organizations, or to organizations with HIPAA
        readiness enabled.

        Args:
          plugin_id: ID of the Plugin (prefixed `plugin_`).

          limit: Number of items to return per page.

              Defaults to `20`. Ranges from `1` to `100`.

          organization_id: For a `read:org_audit` or `read:compliance_org_data` key created for all of a
              parent organization's linked organizations: a child organization of that parent
              to read instead of the organization the key was created in, given as the
              organization's UUID or its `org_`-prefixed ID. A value that is neither returns a
              400; an organization that is not a child of the key's parent, or where the
              Plugins API is not available, returns a 404. Any other key may pass only its own
              organization's ID here; another organization returns a 404.

          page: Optionally set to the `next_page` token from the previous response.

          target_type: Only settings for this kind of target: `organization` (the organization-wide
              setting) or `rbac_group` (an RBAC Group's).

          betas: This endpoint is in beta: requests must send `ce-plugins-2026-09-01` in this
              header.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not plugin_id:
            raise ValueError(f"Expected a non-empty value for `plugin_id` but received {plugin_id!r}")
        extra_headers = {
            **strip_not_given(
                {
                    "anthropic-beta": ",".join(chain((str(e) for e in betas), ["ce-plugins-2026-09-01"]))
                    if is_given(betas)
                    else not_given
                }
            ),
            **(extra_headers or {}),
        }
        extra_headers = {"anthropic-beta": "ce-plugins-2026-09-01", **(extra_headers or {})}
        return self._get_api_list(
            path_template("/v1/organizations/plugins/{plugin_id}/installation_settings?beta=true", plugin_id=plugin_id),
            page=SyncPageCursor[BetaPluginInstallationSetting],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query={
                    "limit": limit,
                    "organization_id": organization_id,
                    "page": page,
                    "target_type": target_type,
                },
            ),
            model=BetaPluginInstallationSetting,
        )

    def remove(
        self,
        target: str,
        *,
        plugin_id: str,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaDeletedPluginInstallationSetting:
        """
        Remove an organization-owned Plugin's own installation setting for the whole
        organization or for one RBAC Group.

        Removing the `organization` target returns the Plugin to its marketplace's
        default installation setting and leaves the groups' settings in place. Removing
        a group's setting makes the group's members fall back to the Plugin's
        organization-wide setting or to the settings of their other groups.

        A target that holds no setting of its own returns 404 (a Plugin that already
        inherits its marketplace's default holds no `organization` setting), and so does
        a member-owned Plugin.

        A removal counts as one of the Plugin's installation-setting writes: send all of
        those writes one at a time. If several arrive for the same Plugin at the same
        time, the server handles them one after another and can answer some of them with
        `503` and `x-should-retry: true` instead of applying them; wait a second or two
        and send the removal again. A `404` on the repeat means the setting is already
        gone.

        **Accepted credentials:** an Admin API key with the `write:plugins` scope.

        Every request must include the beta header
        `anthropic-beta: ce-plugins-2026-09-01`. A request without it returns `404`,
        exactly as if the endpoint did not exist. The Plugins API is in beta and is
        available to Claude Enterprise organizations only. It is not available to Claude
        Platform (Claude Console) organizations, or to organizations with HIPAA
        readiness enabled.

        Args:
          plugin_id: ID of the Plugin (prefixed `plugin_`).

          target: The target whose own setting is removed: the literal `organization` for the
              Plugin's organization-wide setting, or an RBAC Group's ID (prefixed
              `rbac_group_`) for that group's own setting. Removing the `organization` setting
              returns the Plugin to its marketplace's default.

          betas: This endpoint is in beta: requests must send `ce-plugins-2026-09-01` in this
              header.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not plugin_id:
            raise ValueError(f"Expected a non-empty value for `plugin_id` but received {plugin_id!r}")
        if not target:
            raise ValueError(f"Expected a non-empty value for `target` but received {target!r}")
        extra_headers = {
            **strip_not_given(
                {
                    "anthropic-beta": ",".join(chain((str(e) for e in betas), ["ce-plugins-2026-09-01"]))
                    if is_given(betas)
                    else not_given
                }
            ),
            **(extra_headers or {}),
        }
        extra_headers = {"anthropic-beta": "ce-plugins-2026-09-01", **(extra_headers or {})}
        return self._delete(
            path_template(
                "/v1/organizations/plugins/{plugin_id}/installation_settings/{target}?beta=true",
                plugin_id=plugin_id,
                target=target,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
            ),
            cast_to=BetaDeletedPluginInstallationSetting,
        )

    def set(
        self,
        target: str,
        *,
        plugin_id: str,
        installation_preference: Literal["auto_install", "available", "not_available", "required"],
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaPluginInstallationSetting:
        """
        Set or change an organization-owned Plugin's installation setting for the whole
        organization or for one RBAC Group.

        Writing the value a target already holds of its own changes nothing.

        A member-owned Plugin has shares instead of installation settings, so this path
        returns 404 for one.

        Send a Plugin's installation-setting writes one at a time. If several writes for
        the same Plugin arrive at the same time, the server handles them one after
        another and can answer some of them with `503` instead of applying them. That
        `503` carries `x-should-retry: true`, and the write is safe to repeat: wait a
        second or two, then send it again.

        **Accepted credentials:** an Admin API key with the `write:plugins` scope.

        Every request must include the beta header
        `anthropic-beta: ce-plugins-2026-09-01`. A request without it returns `404`,
        exactly as if the endpoint did not exist. The Plugins API is in beta and is
        available to Claude Enterprise organizations only. It is not available to Claude
        Platform (Claude Console) organizations, or to organizations with HIPAA
        readiness enabled.

        Args:
          plugin_id: ID of the Plugin (prefixed `plugin_`).

          target: The target whose setting is written: the literal `organization` for the Plugin's
              organization-wide setting, or an RBAC Group's ID (prefixed `rbac_group_`) for
              that group's own setting. Writing the `organization` target stops the Plugin
              from inheriting its marketplace's default, even when the value written equals
              that default.

          installation_preference: The installation setting the target is to hold for this Plugin: one of
              `required`, `auto_install`, `available`, `not_available`.

          betas: This endpoint is in beta: requests must send `ce-plugins-2026-09-01` in this
              header.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not plugin_id:
            raise ValueError(f"Expected a non-empty value for `plugin_id` but received {plugin_id!r}")
        if not target:
            raise ValueError(f"Expected a non-empty value for `target` but received {target!r}")
        extra_headers = {
            **strip_not_given(
                {
                    "anthropic-beta": ",".join(chain((str(e) for e in betas), ["ce-plugins-2026-09-01"]))
                    if is_given(betas)
                    else not_given
                }
            ),
            **(extra_headers or {}),
        }
        extra_headers = {"anthropic-beta": "ce-plugins-2026-09-01", **(extra_headers or {})}
        return self._post(
            path_template(
                "/v1/organizations/plugins/{plugin_id}/installation_settings/{target}?beta=true",
                plugin_id=plugin_id,
                target=target,
            ),
            body={"installation_preference": installation_preference},
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
            ),
            cast_to=BetaPluginInstallationSetting,
        )


class AsyncInstallationSettings(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncInstallationSettingsWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#accessing-raw-response-data-eg-headers
        """
        return AsyncInstallationSettingsWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncInstallationSettingsWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#with_streaming_response
        """
        return AsyncInstallationSettingsWithStreamingResponse(self)

    def list(
        self,
        plugin_id: str,
        *,
        limit: int | Omit = omit,
        organization_id: Optional[str] | Omit = omit,
        page: Optional[str] | Omit = omit,
        target_type: Optional[Literal["organization", "rbac_group"]] | Omit = omit,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> AsyncPaginator[BetaPluginInstallationSetting, AsyncPageCursor[BetaPluginInstallationSetting]]:
        """
        List an organization-owned Plugin's installation settings, which say which
        members it is for, most recently created first.

        The list holds the Plugin's own organization-wide setting (absent while the
        Plugin inherits its marketplace's default) and each RBAC Group's own setting. A
        member-owned Plugin has shares instead, so this path returns 404 for one.

        **Accepted credentials:** an Admin API key with the `read:plugins` or
        `read:org_audit` scope, or a Compliance Access Key with the
        `read:compliance_org_data` scope.

        Every request must include the beta header
        `anthropic-beta: ce-plugins-2026-09-01`. A request without it returns `404`,
        exactly as if the endpoint did not exist. The Plugins API is in beta and is
        available to Claude Enterprise organizations only. It is not available to Claude
        Platform (Claude Console) organizations, or to organizations with HIPAA
        readiness enabled.

        Args:
          plugin_id: ID of the Plugin (prefixed `plugin_`).

          limit: Number of items to return per page.

              Defaults to `20`. Ranges from `1` to `100`.

          organization_id: For a `read:org_audit` or `read:compliance_org_data` key created for all of a
              parent organization's linked organizations: a child organization of that parent
              to read instead of the organization the key was created in, given as the
              organization's UUID or its `org_`-prefixed ID. A value that is neither returns a
              400; an organization that is not a child of the key's parent, or where the
              Plugins API is not available, returns a 404. Any other key may pass only its own
              organization's ID here; another organization returns a 404.

          page: Optionally set to the `next_page` token from the previous response.

          target_type: Only settings for this kind of target: `organization` (the organization-wide
              setting) or `rbac_group` (an RBAC Group's).

          betas: This endpoint is in beta: requests must send `ce-plugins-2026-09-01` in this
              header.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not plugin_id:
            raise ValueError(f"Expected a non-empty value for `plugin_id` but received {plugin_id!r}")
        extra_headers = {
            **strip_not_given(
                {
                    "anthropic-beta": ",".join(chain((str(e) for e in betas), ["ce-plugins-2026-09-01"]))
                    if is_given(betas)
                    else not_given
                }
            ),
            **(extra_headers or {}),
        }
        extra_headers = {"anthropic-beta": "ce-plugins-2026-09-01", **(extra_headers or {})}
        return self._get_api_list(
            path_template("/v1/organizations/plugins/{plugin_id}/installation_settings?beta=true", plugin_id=plugin_id),
            page=AsyncPageCursor[BetaPluginInstallationSetting],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query={
                    "limit": limit,
                    "organization_id": organization_id,
                    "page": page,
                    "target_type": target_type,
                },
            ),
            model=BetaPluginInstallationSetting,
        )

    async def remove(
        self,
        target: str,
        *,
        plugin_id: str,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaDeletedPluginInstallationSetting:
        """
        Remove an organization-owned Plugin's own installation setting for the whole
        organization or for one RBAC Group.

        Removing the `organization` target returns the Plugin to its marketplace's
        default installation setting and leaves the groups' settings in place. Removing
        a group's setting makes the group's members fall back to the Plugin's
        organization-wide setting or to the settings of their other groups.

        A target that holds no setting of its own returns 404 (a Plugin that already
        inherits its marketplace's default holds no `organization` setting), and so does
        a member-owned Plugin.

        A removal counts as one of the Plugin's installation-setting writes: send all of
        those writes one at a time. If several arrive for the same Plugin at the same
        time, the server handles them one after another and can answer some of them with
        `503` and `x-should-retry: true` instead of applying them; wait a second or two
        and send the removal again. A `404` on the repeat means the setting is already
        gone.

        **Accepted credentials:** an Admin API key with the `write:plugins` scope.

        Every request must include the beta header
        `anthropic-beta: ce-plugins-2026-09-01`. A request without it returns `404`,
        exactly as if the endpoint did not exist. The Plugins API is in beta and is
        available to Claude Enterprise organizations only. It is not available to Claude
        Platform (Claude Console) organizations, or to organizations with HIPAA
        readiness enabled.

        Args:
          plugin_id: ID of the Plugin (prefixed `plugin_`).

          target: The target whose own setting is removed: the literal `organization` for the
              Plugin's organization-wide setting, or an RBAC Group's ID (prefixed
              `rbac_group_`) for that group's own setting. Removing the `organization` setting
              returns the Plugin to its marketplace's default.

          betas: This endpoint is in beta: requests must send `ce-plugins-2026-09-01` in this
              header.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not plugin_id:
            raise ValueError(f"Expected a non-empty value for `plugin_id` but received {plugin_id!r}")
        if not target:
            raise ValueError(f"Expected a non-empty value for `target` but received {target!r}")
        extra_headers = {
            **strip_not_given(
                {
                    "anthropic-beta": ",".join(chain((str(e) for e in betas), ["ce-plugins-2026-09-01"]))
                    if is_given(betas)
                    else not_given
                }
            ),
            **(extra_headers or {}),
        }
        extra_headers = {"anthropic-beta": "ce-plugins-2026-09-01", **(extra_headers or {})}
        return await self._delete(
            path_template(
                "/v1/organizations/plugins/{plugin_id}/installation_settings/{target}?beta=true",
                plugin_id=plugin_id,
                target=target,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
            ),
            cast_to=BetaDeletedPluginInstallationSetting,
        )

    async def set(
        self,
        target: str,
        *,
        plugin_id: str,
        installation_preference: Literal["auto_install", "available", "not_available", "required"],
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaPluginInstallationSetting:
        """
        Set or change an organization-owned Plugin's installation setting for the whole
        organization or for one RBAC Group.

        Writing the value a target already holds of its own changes nothing.

        A member-owned Plugin has shares instead of installation settings, so this path
        returns 404 for one.

        Send a Plugin's installation-setting writes one at a time. If several writes for
        the same Plugin arrive at the same time, the server handles them one after
        another and can answer some of them with `503` instead of applying them. That
        `503` carries `x-should-retry: true`, and the write is safe to repeat: wait a
        second or two, then send it again.

        **Accepted credentials:** an Admin API key with the `write:plugins` scope.

        Every request must include the beta header
        `anthropic-beta: ce-plugins-2026-09-01`. A request without it returns `404`,
        exactly as if the endpoint did not exist. The Plugins API is in beta and is
        available to Claude Enterprise organizations only. It is not available to Claude
        Platform (Claude Console) organizations, or to organizations with HIPAA
        readiness enabled.

        Args:
          plugin_id: ID of the Plugin (prefixed `plugin_`).

          target: The target whose setting is written: the literal `organization` for the Plugin's
              organization-wide setting, or an RBAC Group's ID (prefixed `rbac_group_`) for
              that group's own setting. Writing the `organization` target stops the Plugin
              from inheriting its marketplace's default, even when the value written equals
              that default.

          installation_preference: The installation setting the target is to hold for this Plugin: one of
              `required`, `auto_install`, `available`, `not_available`.

          betas: This endpoint is in beta: requests must send `ce-plugins-2026-09-01` in this
              header.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not plugin_id:
            raise ValueError(f"Expected a non-empty value for `plugin_id` but received {plugin_id!r}")
        if not target:
            raise ValueError(f"Expected a non-empty value for `target` but received {target!r}")
        extra_headers = {
            **strip_not_given(
                {
                    "anthropic-beta": ",".join(chain((str(e) for e in betas), ["ce-plugins-2026-09-01"]))
                    if is_given(betas)
                    else not_given
                }
            ),
            **(extra_headers or {}),
        }
        extra_headers = {"anthropic-beta": "ce-plugins-2026-09-01", **(extra_headers or {})}
        return await self._post(
            path_template(
                "/v1/organizations/plugins/{plugin_id}/installation_settings/{target}?beta=true",
                plugin_id=plugin_id,
                target=target,
            ),
            body={"installation_preference": installation_preference},
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
            ),
            cast_to=BetaPluginInstallationSetting,
        )


class InstallationSettingsWithRawResponse:
    def __init__(self, installation_settings: InstallationSettings) -> None:
        self._installation_settings = installation_settings

        self.list = to_raw_response_wrapper(
            installation_settings.list,
        )
        self.remove = to_raw_response_wrapper(
            installation_settings.remove,
        )
        self.set = to_raw_response_wrapper(
            installation_settings.set,
        )


class AsyncInstallationSettingsWithRawResponse:
    def __init__(self, installation_settings: AsyncInstallationSettings) -> None:
        self._installation_settings = installation_settings

        self.list = async_to_raw_response_wrapper(
            installation_settings.list,
        )
        self.remove = async_to_raw_response_wrapper(
            installation_settings.remove,
        )
        self.set = async_to_raw_response_wrapper(
            installation_settings.set,
        )


class InstallationSettingsWithStreamingResponse:
    def __init__(self, installation_settings: InstallationSettings) -> None:
        self._installation_settings = installation_settings

        self.list = to_streamed_response_wrapper(
            installation_settings.list,
        )
        self.remove = to_streamed_response_wrapper(
            installation_settings.remove,
        )
        self.set = to_streamed_response_wrapper(
            installation_settings.set,
        )


class AsyncInstallationSettingsWithStreamingResponse:
    def __init__(self, installation_settings: AsyncInstallationSettings) -> None:
        self._installation_settings = installation_settings

        self.list = async_to_streamed_response_wrapper(
            installation_settings.list,
        )
        self.remove = async_to_streamed_response_wrapper(
            installation_settings.remove,
        )
        self.set = async_to_streamed_response_wrapper(
            installation_settings.set,
        )
