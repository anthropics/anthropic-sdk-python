from __future__ import annotations

from ....._compat import cached_property
from ....._resource import SyncAPIResource, AsyncAPIResource
from .slack_channels import (
    SlackChannels,
    AsyncSlackChannels,
    SlackChannelsWithRawResponse,
    AsyncSlackChannelsWithRawResponse,
    SlackChannelsWithStreamingResponse,
    AsyncSlackChannelsWithStreamingResponse,
)
from .bundles.bundles import (
    Bundles,
    AsyncBundles,
    BundlesWithRawResponse,
    AsyncBundlesWithRawResponse,
    BundlesWithStreamingResponse,
    AsyncBundlesWithStreamingResponse,
)
from .slack_workspaces import (
    SlackWorkspaces,
    AsyncSlackWorkspaces,
    SlackWorkspacesWithRawResponse,
    AsyncSlackWorkspacesWithRawResponse,
    SlackWorkspacesWithStreamingResponse,
    AsyncSlackWorkspacesWithStreamingResponse,
)

__all__ = ["ClaudeTag", "AsyncClaudeTag"]


class ClaudeTag(SyncAPIResource):
    @cached_property
    def slack_channels(self) -> SlackChannels:
        return SlackChannels(self._client)

    @cached_property
    def slack_workspaces(self) -> SlackWorkspaces:
        return SlackWorkspaces(self._client)

    @cached_property
    def bundles(self) -> Bundles:
        return Bundles(self._client)

    @cached_property
    def with_raw_response(self) -> ClaudeTagWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#accessing-raw-response-data-eg-headers
        """
        return ClaudeTagWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ClaudeTagWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#with_streaming_response
        """
        return ClaudeTagWithStreamingResponse(self)


class AsyncClaudeTag(AsyncAPIResource):
    @cached_property
    def slack_channels(self) -> AsyncSlackChannels:
        return AsyncSlackChannels(self._client)

    @cached_property
    def slack_workspaces(self) -> AsyncSlackWorkspaces:
        return AsyncSlackWorkspaces(self._client)

    @cached_property
    def bundles(self) -> AsyncBundles:
        return AsyncBundles(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncClaudeTagWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#accessing-raw-response-data-eg-headers
        """
        return AsyncClaudeTagWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncClaudeTagWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#with_streaming_response
        """
        return AsyncClaudeTagWithStreamingResponse(self)


class ClaudeTagWithRawResponse:
    def __init__(self, claude_tag: ClaudeTag) -> None:
        self._claude_tag = claude_tag

    @cached_property
    def slack_channels(self) -> SlackChannelsWithRawResponse:
        return SlackChannelsWithRawResponse(self._claude_tag.slack_channels)

    @cached_property
    def slack_workspaces(self) -> SlackWorkspacesWithRawResponse:
        return SlackWorkspacesWithRawResponse(self._claude_tag.slack_workspaces)

    @cached_property
    def bundles(self) -> BundlesWithRawResponse:
        return BundlesWithRawResponse(self._claude_tag.bundles)


class AsyncClaudeTagWithRawResponse:
    def __init__(self, claude_tag: AsyncClaudeTag) -> None:
        self._claude_tag = claude_tag

    @cached_property
    def slack_channels(self) -> AsyncSlackChannelsWithRawResponse:
        return AsyncSlackChannelsWithRawResponse(self._claude_tag.slack_channels)

    @cached_property
    def slack_workspaces(self) -> AsyncSlackWorkspacesWithRawResponse:
        return AsyncSlackWorkspacesWithRawResponse(self._claude_tag.slack_workspaces)

    @cached_property
    def bundles(self) -> AsyncBundlesWithRawResponse:
        return AsyncBundlesWithRawResponse(self._claude_tag.bundles)


class ClaudeTagWithStreamingResponse:
    def __init__(self, claude_tag: ClaudeTag) -> None:
        self._claude_tag = claude_tag

    @cached_property
    def slack_channels(self) -> SlackChannelsWithStreamingResponse:
        return SlackChannelsWithStreamingResponse(self._claude_tag.slack_channels)

    @cached_property
    def slack_workspaces(self) -> SlackWorkspacesWithStreamingResponse:
        return SlackWorkspacesWithStreamingResponse(self._claude_tag.slack_workspaces)

    @cached_property
    def bundles(self) -> BundlesWithStreamingResponse:
        return BundlesWithStreamingResponse(self._claude_tag.bundles)


class AsyncClaudeTagWithStreamingResponse:
    def __init__(self, claude_tag: AsyncClaudeTag) -> None:
        self._claude_tag = claude_tag

    @cached_property
    def slack_channels(self) -> AsyncSlackChannelsWithStreamingResponse:
        return AsyncSlackChannelsWithStreamingResponse(self._claude_tag.slack_channels)

    @cached_property
    def slack_workspaces(self) -> AsyncSlackWorkspacesWithStreamingResponse:
        return AsyncSlackWorkspacesWithStreamingResponse(self._claude_tag.slack_workspaces)

    @cached_property
    def bundles(self) -> AsyncBundlesWithStreamingResponse:
        return AsyncBundlesWithStreamingResponse(self._claude_tag.bundles)
