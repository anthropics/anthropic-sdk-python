# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Optional

import httpx2

from ......_types import Body, Omit, Query, Headers, NotGiven, omit, not_given
from ......_utils import is_given, path_template, maybe_transform, strip_not_given, async_maybe_transform
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
from ......types.beta.organization.federation.rules import workspace_add_params, workspace_list_params
from ......types.beta.organization.federation.beta_federation_rule_workspace import BetaFederationRuleWorkspace
from ......types.beta.organization.federation.rules.workspace_remove_response import WorkspaceRemoveResponse

__all__ = ["Workspaces", "AsyncWorkspaces"]


class Workspaces(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> WorkspacesWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#accessing-raw-response-data-eg-headers
        """
        return WorkspacesWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> WorkspacesWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#with_streaming_response
        """
        return WorkspacesWithStreamingResponse(self)

    def list(
        self,
        federation_rule_id: str,
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
    ) -> SyncPageCursor[BetaFederationRuleWorkspace]:
        """
        **Requires an OAuth access token with the `org:admin` scope**, from
        `ant auth login --scope org:admin` or a workload identity federation rule; Admin
        API keys are not accepted. See
        [Manage WIF with the Admin API](/docs/en/manage-claude/wif-admin-api).

        List workspaces where this federation rule is enabled.

        Returns all workspace enablements in a single response; the `limit` and `page`
        parameters are accepted but have no effect, and `next_page` is always `null`.
        Returns explicit per-workspace enablements only; for rules with
        `applies_to_all_workspaces` or a legacy single `workspace_id`, check those
        fields on the rule itself.

        Args:
          federation_rule_id: ID of the federation rule.

          limit: Number of results per page.

          page: Opaque cursor from a previous response's `next_page`.

          betas: Optional header to specify the beta version(s) you want to use.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not federation_rule_id:
            raise ValueError(f"Expected a non-empty value for `federation_rule_id` but received {federation_rule_id!r}")
        extra_headers = {
            **strip_not_given({"anthropic-beta": ",".join(str(e) for e in betas) if is_given(betas) else not_given}),
            **(extra_headers or {}),
        }
        return self._get_api_list(
            path_template(
                "/v1/organizations/federation_rules/{federation_rule_id}/workspaces?beta=true",
                federation_rule_id=federation_rule_id,
            ),
            page=SyncPageCursor[BetaFederationRuleWorkspace],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "limit": limit,
                        "page": page,
                    },
                    workspace_list_params.WorkspaceListParams,
                ),
            ),
            model=BetaFederationRuleWorkspace,
        )

    def add(
        self,
        federation_rule_id: str,
        *,
        workspace_id: str,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaFederationRuleWorkspace:
        """
        **Requires an OAuth access token with the `org:admin` scope**, from
        `ant auth login --scope org:admin` or a workload identity federation rule; Admin
        API keys are not accepted. See
        [Manage WIF with the Admin API](/docs/en/manage-claude/wif-admin-api).

        Enable a federation rule for a workspace.

        Idempotent; re-enabling returns the existing enablement. The rule and workspace
        must both belong to your organization. Membership of the rule's target service
        account in this workspace is not checked at enablement: token exchange into this
        workspace is rejected unless the target is a member (it is implicitly a member
        of the default workspace). Archived rules are rejected with 400. OAuth callers
        may only manage rules whose `oauth_scope` is `workspace:developer` or
        `workspace:inference`; other scopes require a Console session.

        Args:
          federation_rule_id: ID of the federation rule.

          workspace_id: Tagged ID of the workspace to enable this rule for.

          betas: Optional header to specify the beta version(s) you want to use.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not federation_rule_id:
            raise ValueError(f"Expected a non-empty value for `federation_rule_id` but received {federation_rule_id!r}")
        extra_headers = {
            **strip_not_given({"anthropic-beta": ",".join(str(e) for e in betas) if is_given(betas) else not_given}),
            **(extra_headers or {}),
        }
        return self._post(
            path_template(
                "/v1/organizations/federation_rules/{federation_rule_id}/workspaces?beta=true",
                federation_rule_id=federation_rule_id,
            ),
            body=maybe_transform({"workspace_id": workspace_id}, workspace_add_params.WorkspaceAddParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BetaFederationRuleWorkspace,
        )

    def remove(
        self,
        workspace_id: str,
        *,
        federation_rule_id: str,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> WorkspaceRemoveResponse:
        """
        **Requires an OAuth access token with the `org:admin` scope**, from
        `ant auth login --scope org:admin` or a workload identity federation rule; Admin
        API keys are not accepted. See
        [Manage WIF with the Admin API](/docs/en/manage-claude/wif-admin-api).

        Disable a federation rule for a workspace.

        Idempotent; succeeds even if the enablement was already removed. OAuth callers
        may only manage rules whose `oauth_scope` is `workspace:developer` or
        `workspace:inference`; other scopes require a Console session.

        Args:
          federation_rule_id: ID of the federation rule.

          workspace_id: ID of the workspace to disable for.

          betas: Optional header to specify the beta version(s) you want to use.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not federation_rule_id:
            raise ValueError(f"Expected a non-empty value for `federation_rule_id` but received {federation_rule_id!r}")
        if not workspace_id:
            raise ValueError(f"Expected a non-empty value for `workspace_id` but received {workspace_id!r}")
        extra_headers = {
            **strip_not_given({"anthropic-beta": ",".join(str(e) for e in betas) if is_given(betas) else not_given}),
            **(extra_headers or {}),
        }
        return self._delete(
            path_template(
                "/v1/organizations/federation_rules/{federation_rule_id}/workspaces/{workspace_id}?beta=true",
                federation_rule_id=federation_rule_id,
                workspace_id=workspace_id,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=WorkspaceRemoveResponse,
        )


class AsyncWorkspaces(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncWorkspacesWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#accessing-raw-response-data-eg-headers
        """
        return AsyncWorkspacesWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncWorkspacesWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#with_streaming_response
        """
        return AsyncWorkspacesWithStreamingResponse(self)

    def list(
        self,
        federation_rule_id: str,
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
    ) -> AsyncPaginator[BetaFederationRuleWorkspace, AsyncPageCursor[BetaFederationRuleWorkspace]]:
        """
        **Requires an OAuth access token with the `org:admin` scope**, from
        `ant auth login --scope org:admin` or a workload identity federation rule; Admin
        API keys are not accepted. See
        [Manage WIF with the Admin API](/docs/en/manage-claude/wif-admin-api).

        List workspaces where this federation rule is enabled.

        Returns all workspace enablements in a single response; the `limit` and `page`
        parameters are accepted but have no effect, and `next_page` is always `null`.
        Returns explicit per-workspace enablements only; for rules with
        `applies_to_all_workspaces` or a legacy single `workspace_id`, check those
        fields on the rule itself.

        Args:
          federation_rule_id: ID of the federation rule.

          limit: Number of results per page.

          page: Opaque cursor from a previous response's `next_page`.

          betas: Optional header to specify the beta version(s) you want to use.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not federation_rule_id:
            raise ValueError(f"Expected a non-empty value for `federation_rule_id` but received {federation_rule_id!r}")
        extra_headers = {
            **strip_not_given({"anthropic-beta": ",".join(str(e) for e in betas) if is_given(betas) else not_given}),
            **(extra_headers or {}),
        }
        return self._get_api_list(
            path_template(
                "/v1/organizations/federation_rules/{federation_rule_id}/workspaces?beta=true",
                federation_rule_id=federation_rule_id,
            ),
            page=AsyncPageCursor[BetaFederationRuleWorkspace],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "limit": limit,
                        "page": page,
                    },
                    workspace_list_params.WorkspaceListParams,
                ),
            ),
            model=BetaFederationRuleWorkspace,
        )

    async def add(
        self,
        federation_rule_id: str,
        *,
        workspace_id: str,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaFederationRuleWorkspace:
        """
        **Requires an OAuth access token with the `org:admin` scope**, from
        `ant auth login --scope org:admin` or a workload identity federation rule; Admin
        API keys are not accepted. See
        [Manage WIF with the Admin API](/docs/en/manage-claude/wif-admin-api).

        Enable a federation rule for a workspace.

        Idempotent; re-enabling returns the existing enablement. The rule and workspace
        must both belong to your organization. Membership of the rule's target service
        account in this workspace is not checked at enablement: token exchange into this
        workspace is rejected unless the target is a member (it is implicitly a member
        of the default workspace). Archived rules are rejected with 400. OAuth callers
        may only manage rules whose `oauth_scope` is `workspace:developer` or
        `workspace:inference`; other scopes require a Console session.

        Args:
          federation_rule_id: ID of the federation rule.

          workspace_id: Tagged ID of the workspace to enable this rule for.

          betas: Optional header to specify the beta version(s) you want to use.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not federation_rule_id:
            raise ValueError(f"Expected a non-empty value for `federation_rule_id` but received {federation_rule_id!r}")
        extra_headers = {
            **strip_not_given({"anthropic-beta": ",".join(str(e) for e in betas) if is_given(betas) else not_given}),
            **(extra_headers or {}),
        }
        return await self._post(
            path_template(
                "/v1/organizations/federation_rules/{federation_rule_id}/workspaces?beta=true",
                federation_rule_id=federation_rule_id,
            ),
            body=await async_maybe_transform({"workspace_id": workspace_id}, workspace_add_params.WorkspaceAddParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BetaFederationRuleWorkspace,
        )

    async def remove(
        self,
        workspace_id: str,
        *,
        federation_rule_id: str,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> WorkspaceRemoveResponse:
        """
        **Requires an OAuth access token with the `org:admin` scope**, from
        `ant auth login --scope org:admin` or a workload identity federation rule; Admin
        API keys are not accepted. See
        [Manage WIF with the Admin API](/docs/en/manage-claude/wif-admin-api).

        Disable a federation rule for a workspace.

        Idempotent; succeeds even if the enablement was already removed. OAuth callers
        may only manage rules whose `oauth_scope` is `workspace:developer` or
        `workspace:inference`; other scopes require a Console session.

        Args:
          federation_rule_id: ID of the federation rule.

          workspace_id: ID of the workspace to disable for.

          betas: Optional header to specify the beta version(s) you want to use.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not federation_rule_id:
            raise ValueError(f"Expected a non-empty value for `federation_rule_id` but received {federation_rule_id!r}")
        if not workspace_id:
            raise ValueError(f"Expected a non-empty value for `workspace_id` but received {workspace_id!r}")
        extra_headers = {
            **strip_not_given({"anthropic-beta": ",".join(str(e) for e in betas) if is_given(betas) else not_given}),
            **(extra_headers or {}),
        }
        return await self._delete(
            path_template(
                "/v1/organizations/federation_rules/{federation_rule_id}/workspaces/{workspace_id}?beta=true",
                federation_rule_id=federation_rule_id,
                workspace_id=workspace_id,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=WorkspaceRemoveResponse,
        )


class WorkspacesWithRawResponse:
    def __init__(self, workspaces: Workspaces) -> None:
        self._workspaces = workspaces

        self.list = to_raw_response_wrapper(
            workspaces.list,
        )
        self.add = to_raw_response_wrapper(
            workspaces.add,
        )
        self.remove = to_raw_response_wrapper(
            workspaces.remove,
        )


class AsyncWorkspacesWithRawResponse:
    def __init__(self, workspaces: AsyncWorkspaces) -> None:
        self._workspaces = workspaces

        self.list = async_to_raw_response_wrapper(
            workspaces.list,
        )
        self.add = async_to_raw_response_wrapper(
            workspaces.add,
        )
        self.remove = async_to_raw_response_wrapper(
            workspaces.remove,
        )


class WorkspacesWithStreamingResponse:
    def __init__(self, workspaces: Workspaces) -> None:
        self._workspaces = workspaces

        self.list = to_streamed_response_wrapper(
            workspaces.list,
        )
        self.add = to_streamed_response_wrapper(
            workspaces.add,
        )
        self.remove = to_streamed_response_wrapper(
            workspaces.remove,
        )


class AsyncWorkspacesWithStreamingResponse:
    def __init__(self, workspaces: AsyncWorkspaces) -> None:
        self._workspaces = workspaces

        self.list = async_to_streamed_response_wrapper(
            workspaces.list,
        )
        self.add = async_to_streamed_response_wrapper(
            workspaces.add,
        )
        self.remove = async_to_streamed_response_wrapper(
            workspaces.remove,
        )
