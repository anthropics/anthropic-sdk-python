from __future__ import annotations

from typing import List
from itertools import chain

import httpx2

from ......_types import Body, Omit, Query, Headers, NotGiven, SequenceNotStr, omit, not_given
from ......_utils import is_given, strip_not_given
from ......_compat import cached_property
from ......_resource import SyncAPIResource, AsyncAPIResource
from ......_response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ......_base_client import make_request_options
from ......types.anthropic_beta_param import AnthropicBetaParam
from ......types.beta.organization.claude_code.managed_settings import (
    BetaClaudeCodeManagedSettingsModeParam,
)
from ......types.beta.organization.claude_code.managed_settings.beta_claude_code_managed_settings_mode_param import (
    BetaClaudeCodeManagedSettingsModeParam,
)
from ......types.beta.organization.claude_code.managed_settings.beta_claude_code_managed_settings_configuration import (
    BetaClaudeCodeManagedSettingsConfiguration,
)

__all__ = ["Configuration", "AsyncConfiguration"]


class Configuration(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> ConfigurationWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://platform.claude.com/docs/en/api/sdks/python
        """
        return ConfigurationWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ConfigurationWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://platform.claude.com/docs/en/api/sdks/python
        """
        return ConfigurationWithStreamingResponse(self)

    def retrieve(
        self,
        *,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaClaudeCodeManagedSettingsConfiguration:
        """
        Retrieve the organization's Claude Code managed settings mode and RBAC Group
        order.

        **Accepted credentials:** an organization-level Admin API key with the
        `read:claude_code_managed_settings` scope.

        Every request must include the beta header
        `anthropic-beta: ce-claude-code-managed-settings-2026-10-06`. A request without
        it, or from an organization not enabled for this beta, returns `404`. The Claude
        Code Managed Settings API is in beta and is available to Claude Enterprise
        organizations only.

        Args:
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
        return self._get(
            "/v1/organizations/claude_code/managed_settings/configuration",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                qualifiers={"beta": "true"},
                span_name="anthropic.organization.claude_code.managed_settings.configuration.retrieve",
                span_route="/v1/organizations/claude_code/managed_settings/configuration",
            ),
            cast_to=BetaClaudeCodeManagedSettingsConfiguration,
        )

    def update(
        self,
        *,
        mode: BetaClaudeCodeManagedSettingsModeParam | Omit = omit,
        rbac_group_order: SequenceNotStr[str] | Omit = omit,
        rbac_group_order_version: str | Omit = omit,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaClaudeCodeManagedSettingsConfiguration:
        """
        Change the organization's Claude Code managed settings mode, the RBAC Group
        order, or both, in one atomic write.

        To change the order, send `rbac_group_order` with the `rbac_group_order_version`
        from the read the change is based on. If the order has changed since that read,
        the request returns `409`: read it again and retry. To switch modes only if the
        order has not changed, send the current `rbac_group_order` and
        `rbac_group_order_version` with the new `mode`.

        A switch to `rbac_groups` mode with no RBAC Group settings and no default
        settings copies the organization settings into a new default, in the same write,
        so members keep the settings they had. The copy does not follow later changes to
        the organization settings. If the organization settings cannot be copied, the
        request returns `400` and changes nothing. If they cannot be read, are over 1
        MiB or are not valid, setting the default settings first avoids the copy.

        After a switch to `rbac_groups` mode, a member in no listed RBAC Group receives
        the default settings, or no settings if no default is set, not the organization
        settings.

        **Accepted credentials:** an organization-level Admin API key with the
        `write:claude_code_managed_settings` scope.

        Every request must include the beta header
        `anthropic-beta: ce-claude-code-managed-settings-2026-10-06`. A request without
        it, or from an organization not enabled for this beta, returns `404`. The Claude
        Code Managed Settings API is in beta and is available to Claude Enterprise
        organizations only.

        A write that returns `503` may have applied. Retrying it is safe.

        Args:
          mode: The new mode, as an object such as `{"type": "rbac_groups"}`.

          rbac_group_order: Every RBAC Group that has settings, each listed once, in the new order, highest
              precedence first. Requires `rbac_group_order_version`.

          rbac_group_order_version: The `rbac_group_order_version` from the read this change is based on. Requires
              `rbac_group_order`.

          betas: This endpoint is in beta: requests must send
              `ce-claude-code-managed-settings-2026-10-06` in this header.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

        Raises:
          CMEKKeyDisabledError:

          BetaRequestBodyTimeoutError:

          BetaSettingsDocumentLimitExceededError:

          BetaSettingsHistoryLimitExceededError:

          SandboxEgressRestrictedError:
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
        return self._post(
            "/v1/organizations/claude_code/managed_settings/configuration",
            body={
                "mode": mode,
                "rbac_group_order": rbac_group_order,
                "rbac_group_order_version": rbac_group_order_version,
            },
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                qualifiers={"beta": "true"},
                span_name="anthropic.organization.claude_code.managed_settings.configuration.update",
                span_route="/v1/organizations/claude_code/managed_settings/configuration",
            ),
            cast_to=BetaClaudeCodeManagedSettingsConfiguration,
        )


class AsyncConfiguration(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncConfigurationWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://platform.claude.com/docs/en/api/sdks/python
        """
        return AsyncConfigurationWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncConfigurationWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://platform.claude.com/docs/en/api/sdks/python
        """
        return AsyncConfigurationWithStreamingResponse(self)

    async def retrieve(
        self,
        *,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaClaudeCodeManagedSettingsConfiguration:
        """
        Retrieve the organization's Claude Code managed settings mode and RBAC Group
        order.

        **Accepted credentials:** an organization-level Admin API key with the
        `read:claude_code_managed_settings` scope.

        Every request must include the beta header
        `anthropic-beta: ce-claude-code-managed-settings-2026-10-06`. A request without
        it, or from an organization not enabled for this beta, returns `404`. The Claude
        Code Managed Settings API is in beta and is available to Claude Enterprise
        organizations only.

        Args:
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
        return await self._get(
            "/v1/organizations/claude_code/managed_settings/configuration",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                qualifiers={"beta": "true"},
                span_name="anthropic.organization.claude_code.managed_settings.configuration.retrieve",
                span_route="/v1/organizations/claude_code/managed_settings/configuration",
            ),
            cast_to=BetaClaudeCodeManagedSettingsConfiguration,
        )

    async def update(
        self,
        *,
        mode: BetaClaudeCodeManagedSettingsModeParam | Omit = omit,
        rbac_group_order: SequenceNotStr[str] | Omit = omit,
        rbac_group_order_version: str | Omit = omit,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaClaudeCodeManagedSettingsConfiguration:
        """
        Change the organization's Claude Code managed settings mode, the RBAC Group
        order, or both, in one atomic write.

        To change the order, send `rbac_group_order` with the `rbac_group_order_version`
        from the read the change is based on. If the order has changed since that read,
        the request returns `409`: read it again and retry. To switch modes only if the
        order has not changed, send the current `rbac_group_order` and
        `rbac_group_order_version` with the new `mode`.

        A switch to `rbac_groups` mode with no RBAC Group settings and no default
        settings copies the organization settings into a new default, in the same write,
        so members keep the settings they had. The copy does not follow later changes to
        the organization settings. If the organization settings cannot be copied, the
        request returns `400` and changes nothing. If they cannot be read, are over 1
        MiB or are not valid, setting the default settings first avoids the copy.

        After a switch to `rbac_groups` mode, a member in no listed RBAC Group receives
        the default settings, or no settings if no default is set, not the organization
        settings.

        **Accepted credentials:** an organization-level Admin API key with the
        `write:claude_code_managed_settings` scope.

        Every request must include the beta header
        `anthropic-beta: ce-claude-code-managed-settings-2026-10-06`. A request without
        it, or from an organization not enabled for this beta, returns `404`. The Claude
        Code Managed Settings API is in beta and is available to Claude Enterprise
        organizations only.

        A write that returns `503` may have applied. Retrying it is safe.

        Args:
          mode: The new mode, as an object such as `{"type": "rbac_groups"}`.

          rbac_group_order: Every RBAC Group that has settings, each listed once, in the new order, highest
              precedence first. Requires `rbac_group_order_version`.

          rbac_group_order_version: The `rbac_group_order_version` from the read this change is based on. Requires
              `rbac_group_order`.

          betas: This endpoint is in beta: requests must send
              `ce-claude-code-managed-settings-2026-10-06` in this header.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

        Raises:
          CMEKKeyDisabledError:

          BetaRequestBodyTimeoutError:

          BetaSettingsDocumentLimitExceededError:

          BetaSettingsHistoryLimitExceededError:

          SandboxEgressRestrictedError:
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
        return await self._post(
            "/v1/organizations/claude_code/managed_settings/configuration",
            body={
                "mode": mode,
                "rbac_group_order": rbac_group_order,
                "rbac_group_order_version": rbac_group_order_version,
            },
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                qualifiers={"beta": "true"},
                span_name="anthropic.organization.claude_code.managed_settings.configuration.update",
                span_route="/v1/organizations/claude_code/managed_settings/configuration",
            ),
            cast_to=BetaClaudeCodeManagedSettingsConfiguration,
        )


class ConfigurationWithRawResponse:
    def __init__(self, configuration: Configuration) -> None:
        self._configuration = configuration

        self.retrieve = to_raw_response_wrapper(
            configuration.retrieve,
        )
        self.update = to_raw_response_wrapper(
            configuration.update,
        )


class AsyncConfigurationWithRawResponse:
    def __init__(self, configuration: AsyncConfiguration) -> None:
        self._configuration = configuration

        self.retrieve = async_to_raw_response_wrapper(
            configuration.retrieve,
        )
        self.update = async_to_raw_response_wrapper(
            configuration.update,
        )


class ConfigurationWithStreamingResponse:
    def __init__(self, configuration: Configuration) -> None:
        self._configuration = configuration

        self.retrieve = to_streamed_response_wrapper(
            configuration.retrieve,
        )
        self.update = to_streamed_response_wrapper(
            configuration.update,
        )


class AsyncConfigurationWithStreamingResponse:
    def __init__(self, configuration: AsyncConfiguration) -> None:
        self._configuration = configuration

        self.retrieve = async_to_streamed_response_wrapper(
            configuration.retrieve,
        )
        self.update = async_to_streamed_response_wrapper(
            configuration.update,
        )
