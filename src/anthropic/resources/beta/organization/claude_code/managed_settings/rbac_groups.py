from __future__ import annotations

from typing import Dict, List, Optional
from itertools import chain

import httpx2

from ......_types import Body, Omit, Query, Headers, NotGiven, omit, not_given
from ......_utils import is_given, path_template, strip_not_given
from ......_compat import cached_property
from ......_resource import SyncAPIResource, AsyncAPIResource
from ......_response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ......pagination import SyncPageCursor, AsyncPageCursor
from ......_base_client import AsyncPaginator, make_request_options
from ......types.anthropic_beta_param import AnthropicBetaParam
from ......types.beta.organization.claude_code.managed_settings.beta_claude_code_rbac_group_managed_settings import (
    BetaClaudeCodeRBACGroupManagedSettings,
)
from ......types.beta.organization.claude_code.managed_settings.beta_claude_code_rbac_group_managed_settings_summary import (
    BetaClaudeCodeRBACGroupManagedSettingsSummary,
)
from ......types.beta.organization.claude_code.managed_settings.beta_deleted_claude_code_rbac_group_managed_settings import (
    BetaDeletedClaudeCodeRBACGroupManagedSettings,
)

__all__ = ["RBACGroups", "AsyncRBACGroups"]


class RBACGroups(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> RBACGroupsWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://platform.claude.com/docs/en/api/sdks/python
        """
        return RBACGroupsWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> RBACGroupsWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://platform.claude.com/docs/en/api/sdks/python
        """
        return RBACGroupsWithStreamingResponse(self)

    def retrieve(
        self,
        rbac_group_id: str,
        *,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaClaudeCodeRBACGroupManagedSettings:
        """
        Retrieve an RBAC Group's Claude Code managed settings.

        **Accepted credentials:** an organization-level Admin API key with the
        `read:claude_code_managed_settings` scope.

        Every request must include the beta header
        `anthropic-beta: ce-claude-code-managed-settings-2026-10-06`. A request without
        it, or from an organization not enabled for this beta, returns `404`. The Claude
        Code Managed Settings API is in beta and is available to Claude Enterprise
        organizations only.

        Args:
          rbac_group_id: The RBAC Group's ID, prefixed `rbac_group_`.

          betas: This endpoint is in beta: requests must send
              `ce-claude-code-managed-settings-2026-10-06` in this header.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

        Raises:
          BetaCMEKFeatureUnsupportedError:

          CMEKKeyDisabledError:

          BetaRBACGroupManagedSettingsNotFoundError:
        """
        if not rbac_group_id:
            raise ValueError(f"Expected a non-empty value for `rbac_group_id` but received {rbac_group_id!r}")
        extra_headers = {
            **strip_not_given(
                {
                    "anthropic-beta": ",".join(
                        chain((str(e) for e in betas), ["ce-claude-code-managed-settings-2026-10-06"])
                    )
                    if is_given(betas)
                    else not_given
                }
            ),
            **(extra_headers or {}),
        }
        extra_headers = {"anthropic-beta": "ce-claude-code-managed-settings-2026-10-06", **(extra_headers or {})}
        return self._get(
            path_template(
                "/v1/organizations/claude_code/managed_settings/rbac_groups/{rbac_group_id}",
                rbac_group_id=rbac_group_id,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                qualifiers={"beta": "true"},
                span_name="anthropic.organization.claude_code.managed_settings.rbac_groups.retrieve",
                span_route="/v1/organizations/claude_code/managed_settings/rbac_groups/{rbac_group_id}",
                span_attributes={"anthropic.organization.claude_code.managed_setting.rbac_group.id": rbac_group_id},
            ),
            cast_to=BetaClaudeCodeRBACGroupManagedSettings,
        )

    def list(
        self,
        *,
        limit: int | Omit = omit,
        page: Optional[str] | Omit = omit,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> SyncPageCursor[BetaClaudeCodeRBACGroupManagedSettingsSummary]:
        """
        List the RBAC Groups that have Claude Code managed settings, highest precedence
        first.

        Each entry gives the group's status and timestamps, not its settings. The list
        includes deleted groups that still have settings, and leaves out the default
        settings. If the order changes between pages, the request returns `409`: list
        again from the first page.

        **Accepted credentials:** an organization-level Admin API key with the
        `read:claude_code_managed_settings` scope.

        Every request must include the beta header
        `anthropic-beta: ce-claude-code-managed-settings-2026-10-06`. A request without
        it, or from an organization not enabled for this beta, returns `404`. The Claude
        Code Managed Settings API is in beta and is available to Claude Enterprise
        organizations only.

        Args:
          limit: Number of items to return per page.

              Defaults to `20`. Ranges from `1` to `100`.

          page: Optionally set to the `next_page` token from the previous response.

          betas: This endpoint is in beta: requests must send
              `ce-claude-code-managed-settings-2026-10-06` in this header.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {
            **strip_not_given(
                {
                    "anthropic-beta": ",".join(
                        chain((str(e) for e in betas), ["ce-claude-code-managed-settings-2026-10-06"])
                    )
                    if is_given(betas)
                    else not_given
                }
            ),
            **(extra_headers or {}),
        }
        extra_headers = {"anthropic-beta": "ce-claude-code-managed-settings-2026-10-06", **(extra_headers or {})}
        return self._get_api_list(
            "/v1/organizations/claude_code/managed_settings/rbac_groups",
            page=SyncPageCursor[BetaClaudeCodeRBACGroupManagedSettingsSummary],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query={
                    "limit": limit,
                    "page": page,
                },
                qualifiers={"beta": "true"},
                span_name="anthropic.organization.claude_code.managed_settings.rbac_groups.list",
                span_route="/v1/organizations/claude_code/managed_settings/rbac_groups",
            ),
            model=BetaClaudeCodeRBACGroupManagedSettingsSummary,
        )

    def delete(
        self,
        rbac_group_id: str,
        *,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaDeletedClaudeCodeRBACGroupManagedSettings:
        """
        Delete an RBAC Group's Claude Code managed settings and remove the group from
        `rbac_group_order`.

        A group with no settings returns `404` with the error code
        `rbac_group_managed_settings_not_found`. That code on a retry of a delete that
        returned `503` means the settings are gone.

        **Accepted credentials:** an organization-level Admin API key with the
        `write:claude_code_managed_settings` scope.

        Every request must include the beta header
        `anthropic-beta: ce-claude-code-managed-settings-2026-10-06`. A request without
        it, or from an organization not enabled for this beta, returns `404`. The Claude
        Code Managed Settings API is in beta and is available to Claude Enterprise
        organizations only.

        A write that returns `503` may have applied. Retrying it is safe.

        Args:
          rbac_group_id: The RBAC Group's ID, prefixed `rbac_group_`.

          betas: This endpoint is in beta: requests must send
              `ce-claude-code-managed-settings-2026-10-06` in this header.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

        Raises:
          CMEKKeyDisabledError:

          BetaSettingsHistoryLimitExceededError:

          SandboxEgressRestrictedError:

          BetaRBACGroupManagedSettingsNotFoundError:
        """
        if not rbac_group_id:
            raise ValueError(f"Expected a non-empty value for `rbac_group_id` but received {rbac_group_id!r}")
        extra_headers = {
            **strip_not_given(
                {
                    "anthropic-beta": ",".join(
                        chain((str(e) for e in betas), ["ce-claude-code-managed-settings-2026-10-06"])
                    )
                    if is_given(betas)
                    else not_given
                }
            ),
            **(extra_headers or {}),
        }
        extra_headers = {"anthropic-beta": "ce-claude-code-managed-settings-2026-10-06", **(extra_headers or {})}
        return self._delete(
            path_template(
                "/v1/organizations/claude_code/managed_settings/rbac_groups/{rbac_group_id}",
                rbac_group_id=rbac_group_id,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                qualifiers={"beta": "true"},
                span_name="anthropic.organization.claude_code.managed_settings.rbac_groups.delete",
                span_route="/v1/organizations/claude_code/managed_settings/rbac_groups/{rbac_group_id}",
                span_attributes={"anthropic.organization.claude_code.managed_setting.rbac_group.id": rbac_group_id},
            ),
            cast_to=BetaDeletedClaudeCodeRBACGroupManagedSettings,
        )

    def set(
        self,
        rbac_group_id: str,
        *,
        settings: Dict[str, object],
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaClaudeCodeRBACGroupManagedSettings:
        """
        Create or replace an RBAC Group's Claude Code managed settings.

        New settings join the end of `rbac_group_order`, and existing settings keep
        their place. Until the group is moved up, its members who also belong to an
        earlier group keep that group's settings. In `organization` mode a write changes
        no member's settings until the organization switches to `rbac_groups` mode. Once
        a group has settings, that switch no longer copies the organization settings
        into default settings, so members in no RBAC Group in `rbac_group_order` receive
        no settings unless you set the default settings before the switch.

        Get the group's ID from the RBAC Groups API. One key can hold `read:rbac_groups`
        and `write:claude_code_managed_settings`.

        **Accepted credentials:** an organization-level Admin API key with the
        `write:claude_code_managed_settings` scope.

        Every request must include the beta header
        `anthropic-beta: ce-claude-code-managed-settings-2026-10-06`. A request without
        it, or from an organization not enabled for this beta, returns `404`. The Claude
        Code Managed Settings API is in beta and is available to Claude Enterprise
        organizations only.

        A write that returns `503` may have applied. Retrying it is safe.

        Args:
          rbac_group_id: The RBAC Group's ID, prefixed `rbac_group_`.

          settings: The whole settings document, a JSON object of Claude Code managed settings. It
              replaces any stored document. At most 1 MiB as the server stores it, which can
              be larger than the request body.

          betas: This endpoint is in beta: requests must send
              `ce-claude-code-managed-settings-2026-10-06` in this header.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

        Raises:
          BetaCMEKFeatureUnsupportedError:

          CMEKKeyDisabledError:

          BetaRBACGroupOrderLimitExceededError:

          BetaRequestBodyTimeoutError:

          BetaSettingsDocumentLimitExceededError:

          BetaSettingsHistoryLimitExceededError:

          SandboxEgressRestrictedError:

          BetaRBACGroupNotFoundError:
        """
        if not rbac_group_id:
            raise ValueError(f"Expected a non-empty value for `rbac_group_id` but received {rbac_group_id!r}")
        extra_headers = {
            **strip_not_given(
                {
                    "anthropic-beta": ",".join(
                        chain((str(e) for e in betas), ["ce-claude-code-managed-settings-2026-10-06"])
                    )
                    if is_given(betas)
                    else not_given
                }
            ),
            **(extra_headers or {}),
        }
        extra_headers = {"anthropic-beta": "ce-claude-code-managed-settings-2026-10-06", **(extra_headers or {})}
        return self._post(
            path_template(
                "/v1/organizations/claude_code/managed_settings/rbac_groups/{rbac_group_id}",
                rbac_group_id=rbac_group_id,
            ),
            body={"settings": settings},
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                qualifiers={"beta": "true"},
                span_name="anthropic.organization.claude_code.managed_settings.rbac_groups.set",
                span_route="/v1/organizations/claude_code/managed_settings/rbac_groups/{rbac_group_id}",
                span_attributes={"anthropic.organization.claude_code.managed_setting.rbac_group.id": rbac_group_id},
            ),
            cast_to=BetaClaudeCodeRBACGroupManagedSettings,
        )


class AsyncRBACGroups(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncRBACGroupsWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://platform.claude.com/docs/en/api/sdks/python
        """
        return AsyncRBACGroupsWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncRBACGroupsWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://platform.claude.com/docs/en/api/sdks/python
        """
        return AsyncRBACGroupsWithStreamingResponse(self)

    async def retrieve(
        self,
        rbac_group_id: str,
        *,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaClaudeCodeRBACGroupManagedSettings:
        """
        Retrieve an RBAC Group's Claude Code managed settings.

        **Accepted credentials:** an organization-level Admin API key with the
        `read:claude_code_managed_settings` scope.

        Every request must include the beta header
        `anthropic-beta: ce-claude-code-managed-settings-2026-10-06`. A request without
        it, or from an organization not enabled for this beta, returns `404`. The Claude
        Code Managed Settings API is in beta and is available to Claude Enterprise
        organizations only.

        Args:
          rbac_group_id: The RBAC Group's ID, prefixed `rbac_group_`.

          betas: This endpoint is in beta: requests must send
              `ce-claude-code-managed-settings-2026-10-06` in this header.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

        Raises:
          BetaCMEKFeatureUnsupportedError:

          CMEKKeyDisabledError:

          BetaRBACGroupManagedSettingsNotFoundError:
        """
        if not rbac_group_id:
            raise ValueError(f"Expected a non-empty value for `rbac_group_id` but received {rbac_group_id!r}")
        extra_headers = {
            **strip_not_given(
                {
                    "anthropic-beta": ",".join(
                        chain((str(e) for e in betas), ["ce-claude-code-managed-settings-2026-10-06"])
                    )
                    if is_given(betas)
                    else not_given
                }
            ),
            **(extra_headers or {}),
        }
        extra_headers = {"anthropic-beta": "ce-claude-code-managed-settings-2026-10-06", **(extra_headers or {})}
        return await self._get(
            path_template(
                "/v1/organizations/claude_code/managed_settings/rbac_groups/{rbac_group_id}",
                rbac_group_id=rbac_group_id,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                qualifiers={"beta": "true"},
                span_name="anthropic.organization.claude_code.managed_settings.rbac_groups.retrieve",
                span_route="/v1/organizations/claude_code/managed_settings/rbac_groups/{rbac_group_id}",
                span_attributes={"anthropic.organization.claude_code.managed_setting.rbac_group.id": rbac_group_id},
            ),
            cast_to=BetaClaudeCodeRBACGroupManagedSettings,
        )

    def list(
        self,
        *,
        limit: int | Omit = omit,
        page: Optional[str] | Omit = omit,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> AsyncPaginator[
        BetaClaudeCodeRBACGroupManagedSettingsSummary, AsyncPageCursor[BetaClaudeCodeRBACGroupManagedSettingsSummary]
    ]:
        """
        List the RBAC Groups that have Claude Code managed settings, highest precedence
        first.

        Each entry gives the group's status and timestamps, not its settings. The list
        includes deleted groups that still have settings, and leaves out the default
        settings. If the order changes between pages, the request returns `409`: list
        again from the first page.

        **Accepted credentials:** an organization-level Admin API key with the
        `read:claude_code_managed_settings` scope.

        Every request must include the beta header
        `anthropic-beta: ce-claude-code-managed-settings-2026-10-06`. A request without
        it, or from an organization not enabled for this beta, returns `404`. The Claude
        Code Managed Settings API is in beta and is available to Claude Enterprise
        organizations only.

        Args:
          limit: Number of items to return per page.

              Defaults to `20`. Ranges from `1` to `100`.

          page: Optionally set to the `next_page` token from the previous response.

          betas: This endpoint is in beta: requests must send
              `ce-claude-code-managed-settings-2026-10-06` in this header.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {
            **strip_not_given(
                {
                    "anthropic-beta": ",".join(
                        chain((str(e) for e in betas), ["ce-claude-code-managed-settings-2026-10-06"])
                    )
                    if is_given(betas)
                    else not_given
                }
            ),
            **(extra_headers or {}),
        }
        extra_headers = {"anthropic-beta": "ce-claude-code-managed-settings-2026-10-06", **(extra_headers or {})}
        return self._get_api_list(
            "/v1/organizations/claude_code/managed_settings/rbac_groups",
            page=AsyncPageCursor[BetaClaudeCodeRBACGroupManagedSettingsSummary],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query={
                    "limit": limit,
                    "page": page,
                },
                qualifiers={"beta": "true"},
                span_name="anthropic.organization.claude_code.managed_settings.rbac_groups.list",
                span_route="/v1/organizations/claude_code/managed_settings/rbac_groups",
            ),
            model=BetaClaudeCodeRBACGroupManagedSettingsSummary,
        )

    async def delete(
        self,
        rbac_group_id: str,
        *,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaDeletedClaudeCodeRBACGroupManagedSettings:
        """
        Delete an RBAC Group's Claude Code managed settings and remove the group from
        `rbac_group_order`.

        A group with no settings returns `404` with the error code
        `rbac_group_managed_settings_not_found`. That code on a retry of a delete that
        returned `503` means the settings are gone.

        **Accepted credentials:** an organization-level Admin API key with the
        `write:claude_code_managed_settings` scope.

        Every request must include the beta header
        `anthropic-beta: ce-claude-code-managed-settings-2026-10-06`. A request without
        it, or from an organization not enabled for this beta, returns `404`. The Claude
        Code Managed Settings API is in beta and is available to Claude Enterprise
        organizations only.

        A write that returns `503` may have applied. Retrying it is safe.

        Args:
          rbac_group_id: The RBAC Group's ID, prefixed `rbac_group_`.

          betas: This endpoint is in beta: requests must send
              `ce-claude-code-managed-settings-2026-10-06` in this header.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

        Raises:
          CMEKKeyDisabledError:

          BetaSettingsHistoryLimitExceededError:

          SandboxEgressRestrictedError:

          BetaRBACGroupManagedSettingsNotFoundError:
        """
        if not rbac_group_id:
            raise ValueError(f"Expected a non-empty value for `rbac_group_id` but received {rbac_group_id!r}")
        extra_headers = {
            **strip_not_given(
                {
                    "anthropic-beta": ",".join(
                        chain((str(e) for e in betas), ["ce-claude-code-managed-settings-2026-10-06"])
                    )
                    if is_given(betas)
                    else not_given
                }
            ),
            **(extra_headers or {}),
        }
        extra_headers = {"anthropic-beta": "ce-claude-code-managed-settings-2026-10-06", **(extra_headers or {})}
        return await self._delete(
            path_template(
                "/v1/organizations/claude_code/managed_settings/rbac_groups/{rbac_group_id}",
                rbac_group_id=rbac_group_id,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                qualifiers={"beta": "true"},
                span_name="anthropic.organization.claude_code.managed_settings.rbac_groups.delete",
                span_route="/v1/organizations/claude_code/managed_settings/rbac_groups/{rbac_group_id}",
                span_attributes={"anthropic.organization.claude_code.managed_setting.rbac_group.id": rbac_group_id},
            ),
            cast_to=BetaDeletedClaudeCodeRBACGroupManagedSettings,
        )

    async def set(
        self,
        rbac_group_id: str,
        *,
        settings: Dict[str, object],
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaClaudeCodeRBACGroupManagedSettings:
        """
        Create or replace an RBAC Group's Claude Code managed settings.

        New settings join the end of `rbac_group_order`, and existing settings keep
        their place. Until the group is moved up, its members who also belong to an
        earlier group keep that group's settings. In `organization` mode a write changes
        no member's settings until the organization switches to `rbac_groups` mode. Once
        a group has settings, that switch no longer copies the organization settings
        into default settings, so members in no RBAC Group in `rbac_group_order` receive
        no settings unless you set the default settings before the switch.

        Get the group's ID from the RBAC Groups API. One key can hold `read:rbac_groups`
        and `write:claude_code_managed_settings`.

        **Accepted credentials:** an organization-level Admin API key with the
        `write:claude_code_managed_settings` scope.

        Every request must include the beta header
        `anthropic-beta: ce-claude-code-managed-settings-2026-10-06`. A request without
        it, or from an organization not enabled for this beta, returns `404`. The Claude
        Code Managed Settings API is in beta and is available to Claude Enterprise
        organizations only.

        A write that returns `503` may have applied. Retrying it is safe.

        Args:
          rbac_group_id: The RBAC Group's ID, prefixed `rbac_group_`.

          settings: The whole settings document, a JSON object of Claude Code managed settings. It
              replaces any stored document. At most 1 MiB as the server stores it, which can
              be larger than the request body.

          betas: This endpoint is in beta: requests must send
              `ce-claude-code-managed-settings-2026-10-06` in this header.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

        Raises:
          BetaCMEKFeatureUnsupportedError:

          CMEKKeyDisabledError:

          BetaRBACGroupOrderLimitExceededError:

          BetaRequestBodyTimeoutError:

          BetaSettingsDocumentLimitExceededError:

          BetaSettingsHistoryLimitExceededError:

          SandboxEgressRestrictedError:

          BetaRBACGroupNotFoundError:
        """
        if not rbac_group_id:
            raise ValueError(f"Expected a non-empty value for `rbac_group_id` but received {rbac_group_id!r}")
        extra_headers = {
            **strip_not_given(
                {
                    "anthropic-beta": ",".join(
                        chain((str(e) for e in betas), ["ce-claude-code-managed-settings-2026-10-06"])
                    )
                    if is_given(betas)
                    else not_given
                }
            ),
            **(extra_headers or {}),
        }
        extra_headers = {"anthropic-beta": "ce-claude-code-managed-settings-2026-10-06", **(extra_headers or {})}
        return await self._post(
            path_template(
                "/v1/organizations/claude_code/managed_settings/rbac_groups/{rbac_group_id}",
                rbac_group_id=rbac_group_id,
            ),
            body={"settings": settings},
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                qualifiers={"beta": "true"},
                span_name="anthropic.organization.claude_code.managed_settings.rbac_groups.set",
                span_route="/v1/organizations/claude_code/managed_settings/rbac_groups/{rbac_group_id}",
                span_attributes={"anthropic.organization.claude_code.managed_setting.rbac_group.id": rbac_group_id},
            ),
            cast_to=BetaClaudeCodeRBACGroupManagedSettings,
        )


class RBACGroupsWithRawResponse:
    def __init__(self, rbac_groups: RBACGroups) -> None:
        self._rbac_groups = rbac_groups

        self.retrieve = to_raw_response_wrapper(
            rbac_groups.retrieve,
        )
        self.list = to_raw_response_wrapper(
            rbac_groups.list,
        )
        self.delete = to_raw_response_wrapper(
            rbac_groups.delete,
        )
        self.set = to_raw_response_wrapper(
            rbac_groups.set,
        )


class AsyncRBACGroupsWithRawResponse:
    def __init__(self, rbac_groups: AsyncRBACGroups) -> None:
        self._rbac_groups = rbac_groups

        self.retrieve = async_to_raw_response_wrapper(
            rbac_groups.retrieve,
        )
        self.list = async_to_raw_response_wrapper(
            rbac_groups.list,
        )
        self.delete = async_to_raw_response_wrapper(
            rbac_groups.delete,
        )
        self.set = async_to_raw_response_wrapper(
            rbac_groups.set,
        )


class RBACGroupsWithStreamingResponse:
    def __init__(self, rbac_groups: RBACGroups) -> None:
        self._rbac_groups = rbac_groups

        self.retrieve = to_streamed_response_wrapper(
            rbac_groups.retrieve,
        )
        self.list = to_streamed_response_wrapper(
            rbac_groups.list,
        )
        self.delete = to_streamed_response_wrapper(
            rbac_groups.delete,
        )
        self.set = to_streamed_response_wrapper(
            rbac_groups.set,
        )


class AsyncRBACGroupsWithStreamingResponse:
    def __init__(self, rbac_groups: AsyncRBACGroups) -> None:
        self._rbac_groups = rbac_groups

        self.retrieve = async_to_streamed_response_wrapper(
            rbac_groups.retrieve,
        )
        self.list = async_to_streamed_response_wrapper(
            rbac_groups.list,
        )
        self.delete = async_to_streamed_response_wrapper(
            rbac_groups.delete,
        )
        self.set = async_to_streamed_response_wrapper(
            rbac_groups.set,
        )
