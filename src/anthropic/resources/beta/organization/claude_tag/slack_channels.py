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
from .....types.beta.organization.beta_claude_tag_settings_create_param import BetaClaudeTagSettingsCreateParam
from .....types.beta.organization.beta_claude_tag_settings_update_param import BetaClaudeTagSettingsUpdateParam
from .....types.beta.organization.claude_tag.beta_claude_tag_slack_channel import BetaClaudeTagSlackChannel
from .....types.beta.organization.beta_claude_tag_slack_channel_identifiers_param import (
    BetaClaudeTagSlackChannelIdentifiersParam,
)
from .....types.beta.organization.claude_tag.beta_claude_tag_deleted_slack_channel import (
    BetaClaudeTagDeletedSlackChannel,
)

__all__ = ["SlackChannels", "AsyncSlackChannels"]


class SlackChannels(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> SlackChannelsWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#accessing-raw-response-data-eg-headers
        """
        return SlackChannelsWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> SlackChannelsWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#with_streaming_response
        """
        return SlackChannelsWithStreamingResponse(self)

    def create(
        self,
        *,
        slack: BetaClaudeTagSlackChannelIdentifiersParam,
        settings: BetaClaudeTagSettingsCreateParam | Omit = omit,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaClaudeTagSlackChannel:
        """Set a Slack channel up for Claude Tag and return it with its identifier.

        If the
        channel is already set up, whether in claude.ai, by Claude's first use in it or
        by an earlier request, the existing channel is returned, so the request can be
        repeated. `settings`, when sent, is applied as an update applies it. Before a
        channel is set up, Claude's Slack app confirms with Slack that the channel is in
        the workspace, is not archived and is visible to the app; a channel that fails
        the confirmation returns 404. Setting the channel up and applying `settings` are
        two steps: when the second is refused, the response is the refusal, the channel
        stays set up with every setting unset, and the error's
        `details.slack_channel_id` holds the channel's identifier.

        Args:
          slack: Slack's own identifiers for the channel to set up. The organization must own the
              workspace.

          settings: Settings to store on the channel, applied as Update Slack Channel applies them.

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
        return self._post(
            "/v1/organizations/claude_tag/slack_channels",
            body={
                "slack": slack,
                "settings": settings,
            },
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                qualifiers={"beta": "true"},
                span_name="anthropic.organization.claude_tag.slack_channels.create",
                span_route="/v1/organizations/claude_tag/slack_channels",
                span_created_id="anthropic.organization.claude_tag.slack_channel.id",
            ),
            cast_to=BetaClaudeTagSlackChannel,
        )

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
    ) -> BetaClaudeTagSlackChannel:
        """Get one Slack channel and its settings.

        By default `settings` holds what the
        channel itself stores: a setting that is null there is not set on the channel
        and is inherited. With `include_inherited=true`, `settings` holds what applies
        in the channel once the settings levels above it are taken into account, and the
        request fails with 503 rather than resolve against a settings level that could
        not be read. Either way `sources` names the settings level each value comes
        from, so a caller tells the channel's own value from an inherited one by its
        source, not by whether it is null.

        Args:
          id: The channel's identifier, starting with `slch_`.

          include_inherited: When `true`, `settings` holds what applies in the channel once the settings
              levels above it are taken into account, and every member of `sources` names the
              level a value comes from. When `false` or left out, `settings` holds what the
              channel itself stores.

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
            path_template("/v1/organizations/claude_tag/slack_channels/{id}", id=id),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query={"include_inherited": include_inherited},
                qualifiers={"beta": "true"},
                span_name="anthropic.organization.claude_tag.slack_channels.retrieve",
                span_route="/v1/organizations/claude_tag/slack_channels/{id}",
                span_attributes={"anthropic.organization.claude_tag.slack_channel.id": id},
            ),
            cast_to=BetaClaudeTagSlackChannel,
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
    ) -> BetaClaudeTagSlackChannel:
        """Change the settings a Slack channel stores.

        The update is partial: a setting
        left out is unchanged, and a setting sent as null is cleared, so the channel
        inherits it. If any value is refused, no setting in the request is stored. A
        group direct message takes no settings and returns 400.

        Args:
          id: The channel's identifier, starting with `slch_`.

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
            path_template("/v1/organizations/claude_tag/slack_channels/{id}", id=id),
            body={"settings": settings},
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                qualifiers={"beta": "true"},
                span_name="anthropic.organization.claude_tag.slack_channels.update",
                span_route="/v1/organizations/claude_tag/slack_channels/{id}",
                span_attributes={"anthropic.organization.claude_tag.slack_channel.id": id},
            ),
            cast_to=BetaClaudeTagSlackChannel,
        )

    def list(
        self,
        *,
        slack_workspace_id: str,
        include_inherited: bool | Omit = omit,
        limit: int | Omit = omit,
        page: str | Omit = omit,
        slack_channel_id: str | Omit = omit,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> SyncPageCursor[BetaClaudeTagSlackChannel]:
        """
        List the set-up Slack channels of one Slack workspace, newest first by
        `created_at`. A channel that is not set up is not listed: Slack holds the full
        list of a workspace's channels. Pass `slack_channel_id` as well to look one
        channel up by its Slack identifiers: `data` then holds that channel, or is empty
        when it is not set up, and `limit` and `page` are ignored. A workspace that the
        organization owns only through a Slack Enterprise Grid returns 404 until it is
        set up. With `include_inherited=true` each channel's `settings` holds what
        applies in it, and the request fails with 503 rather than resolve against a
        settings level that could not be read. A `page` cursor resumes only a request
        with the same `include_inherited`.

        Args:
          slack_workspace_id: The Slack workspace whose channels to list: Slack's identifier for it, as in the
              channel object's `slack.workspace_id`, not the workspace object's `id`.

          include_inherited: When `true`, `settings` holds what applies in each channel once the settings
              levels above it are taken into account, and every member of `sources` names the
              level a value comes from. When `false` or left out, `settings` holds what each
              channel itself stores.

          limit: Number of items to return per page, between 1 and 100. Defaults to 20.

          page: Opaque cursor from a previous response's `next_page`.

          slack_channel_id: Slack's identifier for one channel of that workspace, as in the channel object's
              `slack.channel_id`. It is not the channel object's `id`. With it `data` holds
              that channel alone, or nothing when the channel is not set up.

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
            "/v1/organizations/claude_tag/slack_channels",
            page=SyncPageCursor[BetaClaudeTagSlackChannel],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query={
                    "slack_workspace_id": slack_workspace_id,
                    "include_inherited": include_inherited,
                    "limit": limit,
                    "page": page,
                    "slack_channel_id": slack_channel_id,
                },
                qualifiers={"beta": "true"},
                span_name="anthropic.organization.claude_tag.slack_channels.list",
                span_route="/v1/organizations/claude_tag/slack_channels",
            ),
            model=BetaClaudeTagSlackChannel,
        )

    def delete(
        self,
        id: str,
        *,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaClaudeTagDeletedSlackChannel:
        """Remove a Slack channel from Claude Tag.

        This deletes the channel's stored
        settings and its Bundle Targets at once, and then, in the background, the
        channel's sessions and their transcripts, its memory, its routines and the
        artifacts published from it. None of it can be restored. The channel in Slack
        and its messages are unchanged. The request is refused with 400 and
        `error.details.error_code` `slack_channel_enabled` while `enabled` resolves to
        `true` for the channel, as a read with `include_inherited=true` returns it: set
        `enabled` to `false` on the channel first. This guards against removing a
        channel in use by mistake; it is not a way to keep Claude out, because the
        removal deletes the channel's own `enabled: false` with its other settings,
        after which the channel inherits again and Claude's next use of it can set it up
        anew with a new identifier. The identifier returns 404 as soon as the request
        returns, so a repeated removal returns 404. A group direct message returns 400,
        and so does a channel that holds configuration this API does not manage.

        Args:
          id: The channel's identifier, starting with `slch_`.

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
        return self._delete(
            path_template("/v1/organizations/claude_tag/slack_channels/{id}", id=id),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                qualifiers={"beta": "true"},
                span_name="anthropic.organization.claude_tag.slack_channels.delete",
                span_route="/v1/organizations/claude_tag/slack_channels/{id}",
                span_attributes={"anthropic.organization.claude_tag.slack_channel.id": id},
            ),
            cast_to=BetaClaudeTagDeletedSlackChannel,
        )


class AsyncSlackChannels(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncSlackChannelsWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#accessing-raw-response-data-eg-headers
        """
        return AsyncSlackChannelsWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncSlackChannelsWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#with_streaming_response
        """
        return AsyncSlackChannelsWithStreamingResponse(self)

    async def create(
        self,
        *,
        slack: BetaClaudeTagSlackChannelIdentifiersParam,
        settings: BetaClaudeTagSettingsCreateParam | Omit = omit,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaClaudeTagSlackChannel:
        """Set a Slack channel up for Claude Tag and return it with its identifier.

        If the
        channel is already set up, whether in claude.ai, by Claude's first use in it or
        by an earlier request, the existing channel is returned, so the request can be
        repeated. `settings`, when sent, is applied as an update applies it. Before a
        channel is set up, Claude's Slack app confirms with Slack that the channel is in
        the workspace, is not archived and is visible to the app; a channel that fails
        the confirmation returns 404. Setting the channel up and applying `settings` are
        two steps: when the second is refused, the response is the refusal, the channel
        stays set up with every setting unset, and the error's
        `details.slack_channel_id` holds the channel's identifier.

        Args:
          slack: Slack's own identifiers for the channel to set up. The organization must own the
              workspace.

          settings: Settings to store on the channel, applied as Update Slack Channel applies them.

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
        return await self._post(
            "/v1/organizations/claude_tag/slack_channels",
            body={
                "slack": slack,
                "settings": settings,
            },
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                qualifiers={"beta": "true"},
                span_name="anthropic.organization.claude_tag.slack_channels.create",
                span_route="/v1/organizations/claude_tag/slack_channels",
                span_created_id="anthropic.organization.claude_tag.slack_channel.id",
            ),
            cast_to=BetaClaudeTagSlackChannel,
        )

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
    ) -> BetaClaudeTagSlackChannel:
        """Get one Slack channel and its settings.

        By default `settings` holds what the
        channel itself stores: a setting that is null there is not set on the channel
        and is inherited. With `include_inherited=true`, `settings` holds what applies
        in the channel once the settings levels above it are taken into account, and the
        request fails with 503 rather than resolve against a settings level that could
        not be read. Either way `sources` names the settings level each value comes
        from, so a caller tells the channel's own value from an inherited one by its
        source, not by whether it is null.

        Args:
          id: The channel's identifier, starting with `slch_`.

          include_inherited: When `true`, `settings` holds what applies in the channel once the settings
              levels above it are taken into account, and every member of `sources` names the
              level a value comes from. When `false` or left out, `settings` holds what the
              channel itself stores.

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
            path_template("/v1/organizations/claude_tag/slack_channels/{id}", id=id),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query={"include_inherited": include_inherited},
                qualifiers={"beta": "true"},
                span_name="anthropic.organization.claude_tag.slack_channels.retrieve",
                span_route="/v1/organizations/claude_tag/slack_channels/{id}",
                span_attributes={"anthropic.organization.claude_tag.slack_channel.id": id},
            ),
            cast_to=BetaClaudeTagSlackChannel,
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
    ) -> BetaClaudeTagSlackChannel:
        """Change the settings a Slack channel stores.

        The update is partial: a setting
        left out is unchanged, and a setting sent as null is cleared, so the channel
        inherits it. If any value is refused, no setting in the request is stored. A
        group direct message takes no settings and returns 400.

        Args:
          id: The channel's identifier, starting with `slch_`.

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
            path_template("/v1/organizations/claude_tag/slack_channels/{id}", id=id),
            body={"settings": settings},
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                qualifiers={"beta": "true"},
                span_name="anthropic.organization.claude_tag.slack_channels.update",
                span_route="/v1/organizations/claude_tag/slack_channels/{id}",
                span_attributes={"anthropic.organization.claude_tag.slack_channel.id": id},
            ),
            cast_to=BetaClaudeTagSlackChannel,
        )

    def list(
        self,
        *,
        slack_workspace_id: str,
        include_inherited: bool | Omit = omit,
        limit: int | Omit = omit,
        page: str | Omit = omit,
        slack_channel_id: str | Omit = omit,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> AsyncPaginator[BetaClaudeTagSlackChannel, AsyncPageCursor[BetaClaudeTagSlackChannel]]:
        """
        List the set-up Slack channels of one Slack workspace, newest first by
        `created_at`. A channel that is not set up is not listed: Slack holds the full
        list of a workspace's channels. Pass `slack_channel_id` as well to look one
        channel up by its Slack identifiers: `data` then holds that channel, or is empty
        when it is not set up, and `limit` and `page` are ignored. A workspace that the
        organization owns only through a Slack Enterprise Grid returns 404 until it is
        set up. With `include_inherited=true` each channel's `settings` holds what
        applies in it, and the request fails with 503 rather than resolve against a
        settings level that could not be read. A `page` cursor resumes only a request
        with the same `include_inherited`.

        Args:
          slack_workspace_id: The Slack workspace whose channels to list: Slack's identifier for it, as in the
              channel object's `slack.workspace_id`, not the workspace object's `id`.

          include_inherited: When `true`, `settings` holds what applies in each channel once the settings
              levels above it are taken into account, and every member of `sources` names the
              level a value comes from. When `false` or left out, `settings` holds what each
              channel itself stores.

          limit: Number of items to return per page, between 1 and 100. Defaults to 20.

          page: Opaque cursor from a previous response's `next_page`.

          slack_channel_id: Slack's identifier for one channel of that workspace, as in the channel object's
              `slack.channel_id`. It is not the channel object's `id`. With it `data` holds
              that channel alone, or nothing when the channel is not set up.

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
            "/v1/organizations/claude_tag/slack_channels",
            page=AsyncPageCursor[BetaClaudeTagSlackChannel],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query={
                    "slack_workspace_id": slack_workspace_id,
                    "include_inherited": include_inherited,
                    "limit": limit,
                    "page": page,
                    "slack_channel_id": slack_channel_id,
                },
                qualifiers={"beta": "true"},
                span_name="anthropic.organization.claude_tag.slack_channels.list",
                span_route="/v1/organizations/claude_tag/slack_channels",
            ),
            model=BetaClaudeTagSlackChannel,
        )

    async def delete(
        self,
        id: str,
        *,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaClaudeTagDeletedSlackChannel:
        """Remove a Slack channel from Claude Tag.

        This deletes the channel's stored
        settings and its Bundle Targets at once, and then, in the background, the
        channel's sessions and their transcripts, its memory, its routines and the
        artifacts published from it. None of it can be restored. The channel in Slack
        and its messages are unchanged. The request is refused with 400 and
        `error.details.error_code` `slack_channel_enabled` while `enabled` resolves to
        `true` for the channel, as a read with `include_inherited=true` returns it: set
        `enabled` to `false` on the channel first. This guards against removing a
        channel in use by mistake; it is not a way to keep Claude out, because the
        removal deletes the channel's own `enabled: false` with its other settings,
        after which the channel inherits again and Claude's next use of it can set it up
        anew with a new identifier. The identifier returns 404 as soon as the request
        returns, so a repeated removal returns 404. A group direct message returns 400,
        and so does a channel that holds configuration this API does not manage.

        Args:
          id: The channel's identifier, starting with `slch_`.

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
        return await self._delete(
            path_template("/v1/organizations/claude_tag/slack_channels/{id}", id=id),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                qualifiers={"beta": "true"},
                span_name="anthropic.organization.claude_tag.slack_channels.delete",
                span_route="/v1/organizations/claude_tag/slack_channels/{id}",
                span_attributes={"anthropic.organization.claude_tag.slack_channel.id": id},
            ),
            cast_to=BetaClaudeTagDeletedSlackChannel,
        )


class SlackChannelsWithRawResponse:
    def __init__(self, slack_channels: SlackChannels) -> None:
        self._slack_channels = slack_channels

        self.create = to_raw_response_wrapper(
            slack_channels.create,
        )
        self.retrieve = to_raw_response_wrapper(
            slack_channels.retrieve,
        )
        self.update = to_raw_response_wrapper(
            slack_channels.update,
        )
        self.list = to_raw_response_wrapper(
            slack_channels.list,
        )
        self.delete = to_raw_response_wrapper(
            slack_channels.delete,
        )


class AsyncSlackChannelsWithRawResponse:
    def __init__(self, slack_channels: AsyncSlackChannels) -> None:
        self._slack_channels = slack_channels

        self.create = async_to_raw_response_wrapper(
            slack_channels.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            slack_channels.retrieve,
        )
        self.update = async_to_raw_response_wrapper(
            slack_channels.update,
        )
        self.list = async_to_raw_response_wrapper(
            slack_channels.list,
        )
        self.delete = async_to_raw_response_wrapper(
            slack_channels.delete,
        )


class SlackChannelsWithStreamingResponse:
    def __init__(self, slack_channels: SlackChannels) -> None:
        self._slack_channels = slack_channels

        self.create = to_streamed_response_wrapper(
            slack_channels.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            slack_channels.retrieve,
        )
        self.update = to_streamed_response_wrapper(
            slack_channels.update,
        )
        self.list = to_streamed_response_wrapper(
            slack_channels.list,
        )
        self.delete = to_streamed_response_wrapper(
            slack_channels.delete,
        )


class AsyncSlackChannelsWithStreamingResponse:
    def __init__(self, slack_channels: AsyncSlackChannels) -> None:
        self._slack_channels = slack_channels

        self.create = async_to_streamed_response_wrapper(
            slack_channels.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            slack_channels.retrieve,
        )
        self.update = async_to_streamed_response_wrapper(
            slack_channels.update,
        )
        self.list = async_to_streamed_response_wrapper(
            slack_channels.list,
        )
        self.delete = async_to_streamed_response_wrapper(
            slack_channels.delete,
        )
