from __future__ import annotations

from ....._compat import cached_property
from ....._resource import SyncAPIResource, AsyncAPIResource
from .managed_settings.managed_settings import (
    ManagedSettings,
    AsyncManagedSettings,
    ManagedSettingsWithRawResponse,
    AsyncManagedSettingsWithRawResponse,
    ManagedSettingsWithStreamingResponse,
    AsyncManagedSettingsWithStreamingResponse,
)

__all__ = ["ClaudeCode", "AsyncClaudeCode"]


class ClaudeCode(SyncAPIResource):
    @cached_property
    def managed_settings(self) -> ManagedSettings:
        return ManagedSettings(self._client)

    @cached_property
    def with_raw_response(self) -> ClaudeCodeWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://platform.claude.com/docs/en/api/sdks/python
        """
        return ClaudeCodeWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ClaudeCodeWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://platform.claude.com/docs/en/api/sdks/python
        """
        return ClaudeCodeWithStreamingResponse(self)


class AsyncClaudeCode(AsyncAPIResource):
    @cached_property
    def managed_settings(self) -> AsyncManagedSettings:
        return AsyncManagedSettings(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncClaudeCodeWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://platform.claude.com/docs/en/api/sdks/python
        """
        return AsyncClaudeCodeWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncClaudeCodeWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://platform.claude.com/docs/en/api/sdks/python
        """
        return AsyncClaudeCodeWithStreamingResponse(self)


class ClaudeCodeWithRawResponse:
    def __init__(self, claude_code: ClaudeCode) -> None:
        self._claude_code = claude_code

    @cached_property
    def managed_settings(self) -> ManagedSettingsWithRawResponse:
        return ManagedSettingsWithRawResponse(self._claude_code.managed_settings)


class AsyncClaudeCodeWithRawResponse:
    def __init__(self, claude_code: AsyncClaudeCode) -> None:
        self._claude_code = claude_code

    @cached_property
    def managed_settings(self) -> AsyncManagedSettingsWithRawResponse:
        return AsyncManagedSettingsWithRawResponse(self._claude_code.managed_settings)


class ClaudeCodeWithStreamingResponse:
    def __init__(self, claude_code: ClaudeCode) -> None:
        self._claude_code = claude_code

    @cached_property
    def managed_settings(self) -> ManagedSettingsWithStreamingResponse:
        return ManagedSettingsWithStreamingResponse(self._claude_code.managed_settings)


class AsyncClaudeCodeWithStreamingResponse:
    def __init__(self, claude_code: AsyncClaudeCode) -> None:
        self._claude_code = claude_code

    @cached_property
    def managed_settings(self) -> AsyncManagedSettingsWithStreamingResponse:
        return AsyncManagedSettingsWithStreamingResponse(self._claude_code.managed_settings)
