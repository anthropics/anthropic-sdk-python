from __future__ import annotations

from typing import List
from itertools import chain

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
from .....types.beta.organization.beta_claude_tag_settings_update_param import BetaClaudeTagSettingsUpdateParam
from .....types.beta.organization.claude_tag.beta_claude_tag_slack_workspace import BetaClaudeTagSlackWorkspace

__all__ = ["SlackWorkspaces", "AsyncSlackWorkspaces"]


class SlackWorkspaces(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> SlackWorkspacesWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#accessing-raw-response-data-eg-headers
        """
        return SlackWorkspacesWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> SlackWorkspacesWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#with_streaming_response
        """
        return SlackWorkspacesWithStreamingResponse(self)

    def retrieve(
        self,
        id: str,
        *,
        include_inherited: bool | Omit = omit,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaClaudeTagSlackWorkspace:
        """Get one Slack workspace and its settings.

        By default `settings` holds what the
        workspace itself stores: a setting that is null there is not set on the
        workspace and is inherited. With `include_inherited=true`, `settings` holds what
        applies in the workspace once the organization's Slack defaults are taken into
        account, and the request fails with 503 rather than resolve against a settings
        level that could not be read. Either way `sources` names the settings level each
        value comes from.

        Args:
          id: The workspace's identifier, starting with `slws_`.

          include_inherited: When `true`, `settings` holds what applies in the workspace once the
              organization's Slack defaults are taken into account, and every member of
              `sources` names the level a value comes from. When `false` or left out,
              `settings` holds what the workspace itself stores.

          betas: This endpoint is in beta: requests must send
              `experimental-claude-tag-2026-10-21` in this header.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        extra_headers = {
            **strip_not_given(
                {
                    "anthropic-beta": ",".join(chain((str(e) for e in betas), ["experimental-claude-tag-2026-10-21"]))
                    if is_given(betas)
                    else not_given
                }
            ),
            **(extra_headers or {}),
        }
        extra_headers = {"anthropic-beta": "experimental-claude-tag-2026-10-21", **(extra_headers or {})}
        return self._get(
            path_template("/v1/organizations/claude_tag/slack_workspaces/{id}", id=id),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query={"include_inherited": include_inherited},
                qualifiers={"beta": "true"},
                span_name="anthropic.organization.claude_tag.slack_workspaces.retrieve",
                span_route="/v1/organizations/claude_tag/slack_workspaces/{id}",
                span_attributes={"anthropic.organization.claude_tag.slack_workspace.id": id},
            ),
            cast_to=BetaClaudeTagSlackWorkspace,
        )

    def update(
        self,
        id: str,
        *,
        settings: BetaClaudeTagSettingsUpdateParam,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaClaudeTagSlackWorkspace:
        """Change the settings a Slack workspace stores.

        The update is partial: a setting
        left out is unchanged, and a setting sent as null is cleared, so the workspace
        inherits it. If any value is refused, no setting in the request is stored.

        Args:
          id: The workspace's identifier, starting with `slws_`.

          settings: The settings to change.

          betas: This endpoint is in beta: requests must send
              `experimental-claude-tag-2026-10-21` in this header.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        extra_headers = {
            **strip_not_given(
                {
                    "anthropic-beta": ",".join(chain((str(e) for e in betas), ["experimental-claude-tag-2026-10-21"]))
                    if is_given(betas)
                    else not_given
                }
            ),
            **(extra_headers or {}),
        }
        extra_headers = {"anthropic-beta": "experimental-claude-tag-2026-10-21", **(extra_headers or {})}
        return self._post(
            path_template("/v1/organizations/claude_tag/slack_workspaces/{id}", id=id),
            body={"settings": settings},
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                qualifiers={"beta": "true"},
                span_name="anthropic.organization.claude_tag.slack_workspaces.update",
                span_route="/v1/organizations/claude_tag/slack_workspaces/{id}",
                span_attributes={"anthropic.organization.claude_tag.slack_workspace.id": id},
            ),
            cast_to=BetaClaudeTagSlackWorkspace,
        )

    def list(
        self,
        *,
        include_inherited: bool | Omit = omit,
        limit: int | Omit = omit,
        page: str | Omit = omit,
        slack_workspace_id: str | Omit = omit,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> SyncPageCursor[BetaClaudeTagSlackWorkspace]:
        """
        List the set-up Slack workspaces the organization owns, newest first by
        `created_at`. Pass `slack_workspace_id` to look one workspace up by its Slack
        identifier: `data` then holds that workspace, or is empty when it is not set up.
        A workspace of a Slack Enterprise Grid the organization has connected returns
        404 until it is set up. With `include_inherited=true` each workspace's
        `settings` holds what applies in it, and the request fails with 503 rather than
        resolve against a settings level that could not be read. A `page` cursor resumes
        only a request with the same `include_inherited`.

        Args:
          include_inherited: When `true`, `settings` holds what applies in each workspace once the
              organization's Slack defaults are taken into account, and every member of
              `sources` names the level a value comes from. When `false` or left out,
              `settings` holds what each workspace itself stores.

          limit: Number of items to return per page, between 1 and 100. Defaults to 20.

          page: Opaque cursor from a previous response's `next_page`.

          slack_workspace_id: Slack's identifier for one workspace, as in the workspace object's
              `slack.workspace_id`, not its `id`. With it `data` holds that workspace alone,
              or nothing when it is not set up.

          betas: This endpoint is in beta: requests must send
              `experimental-claude-tag-2026-10-21` in this header.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {
            **strip_not_given(
                {
                    "anthropic-beta": ",".join(chain((str(e) for e in betas), ["experimental-claude-tag-2026-10-21"]))
                    if is_given(betas)
                    else not_given
                }
            ),
            **(extra_headers or {}),
        }
        extra_headers = {"anthropic-beta": "experimental-claude-tag-2026-10-21", **(extra_headers or {})}
        return self._get_api_list(
            "/v1/organizations/claude_tag/slack_workspaces",
            page=SyncPageCursor[BetaClaudeTagSlackWorkspace],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query={
                    "include_inherited": include_inherited,
                    "limit": limit,
                    "page": page,
                    "slack_workspace_id": slack_workspace_id,
                },
                qualifiers={"beta": "true"},
                span_name="anthropic.organization.claude_tag.slack_workspaces.list",
                span_route="/v1/organizations/claude_tag/slack_workspaces",
            ),
            model=BetaClaudeTagSlackWorkspace,
        )


class AsyncSlackWorkspaces(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncSlackWorkspacesWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#accessing-raw-response-data-eg-headers
        """
        return AsyncSlackWorkspacesWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncSlackWorkspacesWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#with_streaming_response
        """
        return AsyncSlackWorkspacesWithStreamingResponse(self)

    async def retrieve(
        self,
        id: str,
        *,
        include_inherited: bool | Omit = omit,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaClaudeTagSlackWorkspace:
        """Get one Slack workspace and its settings.

        By default `settings` holds what the
        workspace itself stores: a setting that is null there is not set on the
        workspace and is inherited. With `include_inherited=true`, `settings` holds what
        applies in the workspace once the organization's Slack defaults are taken into
        account, and the request fails with 503 rather than resolve against a settings
        level that could not be read. Either way `sources` names the settings level each
        value comes from.

        Args:
          id: The workspace's identifier, starting with `slws_`.

          include_inherited: When `true`, `settings` holds what applies in the workspace once the
              organization's Slack defaults are taken into account, and every member of
              `sources` names the level a value comes from. When `false` or left out,
              `settings` holds what the workspace itself stores.

          betas: This endpoint is in beta: requests must send
              `experimental-claude-tag-2026-10-21` in this header.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        extra_headers = {
            **strip_not_given(
                {
                    "anthropic-beta": ",".join(chain((str(e) for e in betas), ["experimental-claude-tag-2026-10-21"]))
                    if is_given(betas)
                    else not_given
                }
            ),
            **(extra_headers or {}),
        }
        extra_headers = {"anthropic-beta": "experimental-claude-tag-2026-10-21", **(extra_headers or {})}
        return await self._get(
            path_template("/v1/organizations/claude_tag/slack_workspaces/{id}", id=id),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query={"include_inherited": include_inherited},
                qualifiers={"beta": "true"},
                span_name="anthropic.organization.claude_tag.slack_workspaces.retrieve",
                span_route="/v1/organizations/claude_tag/slack_workspaces/{id}",
                span_attributes={"anthropic.organization.claude_tag.slack_workspace.id": id},
            ),
            cast_to=BetaClaudeTagSlackWorkspace,
        )

    async def update(
        self,
        id: str,
        *,
        settings: BetaClaudeTagSettingsUpdateParam,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaClaudeTagSlackWorkspace:
        """Change the settings a Slack workspace stores.

        The update is partial: a setting
        left out is unchanged, and a setting sent as null is cleared, so the workspace
        inherits it. If any value is refused, no setting in the request is stored.

        Args:
          id: The workspace's identifier, starting with `slws_`.

          settings: The settings to change.

          betas: This endpoint is in beta: requests must send
              `experimental-claude-tag-2026-10-21` in this header.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        extra_headers = {
            **strip_not_given(
                {
                    "anthropic-beta": ",".join(chain((str(e) for e in betas), ["experimental-claude-tag-2026-10-21"]))
                    if is_given(betas)
                    else not_given
                }
            ),
            **(extra_headers or {}),
        }
        extra_headers = {"anthropic-beta": "experimental-claude-tag-2026-10-21", **(extra_headers or {})}
        return await self._post(
            path_template("/v1/organizations/claude_tag/slack_workspaces/{id}", id=id),
            body={"settings": settings},
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                qualifiers={"beta": "true"},
                span_name="anthropic.organization.claude_tag.slack_workspaces.update",
                span_route="/v1/organizations/claude_tag/slack_workspaces/{id}",
                span_attributes={"anthropic.organization.claude_tag.slack_workspace.id": id},
            ),
            cast_to=BetaClaudeTagSlackWorkspace,
        )

    def list(
        self,
        *,
        include_inherited: bool | Omit = omit,
        limit: int | Omit = omit,
        page: str | Omit = omit,
        slack_workspace_id: str | Omit = omit,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> AsyncPaginator[BetaClaudeTagSlackWorkspace, AsyncPageCursor[BetaClaudeTagSlackWorkspace]]:
        """
        List the set-up Slack workspaces the organization owns, newest first by
        `created_at`. Pass `slack_workspace_id` to look one workspace up by its Slack
        identifier: `data` then holds that workspace, or is empty when it is not set up.
        A workspace of a Slack Enterprise Grid the organization has connected returns
        404 until it is set up. With `include_inherited=true` each workspace's
        `settings` holds what applies in it, and the request fails with 503 rather than
        resolve against a settings level that could not be read. A `page` cursor resumes
        only a request with the same `include_inherited`.

        Args:
          include_inherited: When `true`, `settings` holds what applies in each workspace once the
              organization's Slack defaults are taken into account, and every member of
              `sources` names the level a value comes from. When `false` or left out,
              `settings` holds what each workspace itself stores.

          limit: Number of items to return per page, between 1 and 100. Defaults to 20.

          page: Opaque cursor from a previous response's `next_page`.

          slack_workspace_id: Slack's identifier for one workspace, as in the workspace object's
              `slack.workspace_id`, not its `id`. With it `data` holds that workspace alone,
              or nothing when it is not set up.

          betas: This endpoint is in beta: requests must send
              `experimental-claude-tag-2026-10-21` in this header.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {
            **strip_not_given(
                {
                    "anthropic-beta": ",".join(chain((str(e) for e in betas), ["experimental-claude-tag-2026-10-21"]))
                    if is_given(betas)
                    else not_given
                }
            ),
            **(extra_headers or {}),
        }
        extra_headers = {"anthropic-beta": "experimental-claude-tag-2026-10-21", **(extra_headers or {})}
        return self._get_api_list(
            "/v1/organizations/claude_tag/slack_workspaces",
            page=AsyncPageCursor[BetaClaudeTagSlackWorkspace],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query={
                    "include_inherited": include_inherited,
                    "limit": limit,
                    "page": page,
                    "slack_workspace_id": slack_workspace_id,
                },
                qualifiers={"beta": "true"},
                span_name="anthropic.organization.claude_tag.slack_workspaces.list",
                span_route="/v1/organizations/claude_tag/slack_workspaces",
            ),
            model=BetaClaudeTagSlackWorkspace,
        )


class SlackWorkspacesWithRawResponse:
    def __init__(self, slack_workspaces: SlackWorkspaces) -> None:
        self._slack_workspaces = slack_workspaces

        self.retrieve = to_raw_response_wrapper(
            slack_workspaces.retrieve,
        )
        self.update = to_raw_response_wrapper(
            slack_workspaces.update,
        )
        self.list = to_raw_response_wrapper(
            slack_workspaces.list,
        )


class AsyncSlackWorkspacesWithRawResponse:
    def __init__(self, slack_workspaces: AsyncSlackWorkspaces) -> None:
        self._slack_workspaces = slack_workspaces

        self.retrieve = async_to_raw_response_wrapper(
            slack_workspaces.retrieve,
        )
        self.update = async_to_raw_response_wrapper(
            slack_workspaces.update,
        )
        self.list = async_to_raw_response_wrapper(
            slack_workspaces.list,
        )


class SlackWorkspacesWithStreamingResponse:
    def __init__(self, slack_workspaces: SlackWorkspaces) -> None:
        self._slack_workspaces = slack_workspaces

        self.retrieve = to_streamed_response_wrapper(
            slack_workspaces.retrieve,
        )
        self.update = to_streamed_response_wrapper(
            slack_workspaces.update,
        )
        self.list = to_streamed_response_wrapper(
            slack_workspaces.list,
        )


class AsyncSlackWorkspacesWithStreamingResponse:
    def __init__(self, slack_workspaces: AsyncSlackWorkspaces) -> None:
        self._slack_workspaces = slack_workspaces

        self.retrieve = async_to_streamed_response_wrapper(
            slack_workspaces.retrieve,
        )
        self.update = async_to_streamed_response_wrapper(
            slack_workspaces.update,
        )
        self.list = async_to_streamed_response_wrapper(
            slack_workspaces.list,
        )
