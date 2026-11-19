from __future__ import annotations

from typing import Dict, List, Optional
from itertools import chain

import httpx2

from ......_types import Body, Omit, Query, Headers, NotGiven, omit, not_given
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
from ......types.beta.organization.claude_code.managed_settings.beta_claude_code_rbac_group_default_managed_settings import (
    BetaClaudeCodeRBACGroupDefaultManagedSettings,
)

__all__ = ["RBACGroupDefault", "AsyncRBACGroupDefault"]


class RBACGroupDefault(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> RBACGroupDefaultWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://platform.claude.com/docs/en/api/sdks/python
        """
        return RBACGroupDefaultWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> RBACGroupDefaultWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://platform.claude.com/docs/en/api/sdks/python
        """
        return RBACGroupDefaultWithStreamingResponse(self)

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
    ) -> BetaClaudeCodeRBACGroupDefaultManagedSettings:
        """
        Retrieve the default Claude Code managed settings, which members who belong to
        no RBAC Group in `rbac_group_order` receive in `rbac_groups` mode.

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

        Raises:
          BetaCMEKFeatureUnsupportedError:

          CMEKKeyDisabledError:
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
            "/v1/organizations/claude_code/managed_settings/rbac_group_default",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                qualifiers={"beta": "true"},
                span_name="anthropic.organization.claude_code.managed_settings.rbac_group_default.retrieve",
                span_route="/v1/organizations/claude_code/managed_settings/rbac_group_default",
            ),
            cast_to=BetaClaudeCodeRBACGroupDefaultManagedSettings,
        )

    def update(
        self,
        *,
        settings: Optional[Dict[str, object]],
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaClaudeCodeRBACGroupDefaultManagedSettings:
        """
        Set or replace the default Claude Code managed settings, or clear them with
        `null`.

        **Accepted credentials:** an organization-level Admin API key with the
        `write:claude_code_managed_settings` scope.

        Every request must include the beta header
        `anthropic-beta: ce-claude-code-managed-settings-2026-10-06`. A request without
        it, or from an organization not enabled for this beta, returns `404`. The Claude
        Code Managed Settings API is in beta and is available to Claude Enterprise
        organizations only.

        A write that returns `503` may have applied. Retrying it is safe.

        Args:
          settings: The whole settings document, a JSON object of Claude Code managed settings. It
              replaces any stored document, or `null` clears the default settings. At most 1
              MiB as the server stores it, which can be larger than the request body.

          betas: This endpoint is in beta: requests must send
              `ce-claude-code-managed-settings-2026-10-06` in this header.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

        Raises:
          BetaCMEKFeatureUnsupportedError:

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
            "/v1/organizations/claude_code/managed_settings/rbac_group_default",
            body={"settings": settings},
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                qualifiers={"beta": "true"},
                span_name="anthropic.organization.claude_code.managed_settings.rbac_group_default.update",
                span_route="/v1/organizations/claude_code/managed_settings/rbac_group_default",
            ),
            cast_to=BetaClaudeCodeRBACGroupDefaultManagedSettings,
        )


class AsyncRBACGroupDefault(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncRBACGroupDefaultWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://platform.claude.com/docs/en/api/sdks/python
        """
        return AsyncRBACGroupDefaultWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncRBACGroupDefaultWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://platform.claude.com/docs/en/api/sdks/python
        """
        return AsyncRBACGroupDefaultWithStreamingResponse(self)

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
    ) -> BetaClaudeCodeRBACGroupDefaultManagedSettings:
        """
        Retrieve the default Claude Code managed settings, which members who belong to
        no RBAC Group in `rbac_group_order` receive in `rbac_groups` mode.

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

        Raises:
          BetaCMEKFeatureUnsupportedError:

          CMEKKeyDisabledError:
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
            "/v1/organizations/claude_code/managed_settings/rbac_group_default",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                qualifiers={"beta": "true"},
                span_name="anthropic.organization.claude_code.managed_settings.rbac_group_default.retrieve",
                span_route="/v1/organizations/claude_code/managed_settings/rbac_group_default",
            ),
            cast_to=BetaClaudeCodeRBACGroupDefaultManagedSettings,
        )

    async def update(
        self,
        *,
        settings: Optional[Dict[str, object]],
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaClaudeCodeRBACGroupDefaultManagedSettings:
        """
        Set or replace the default Claude Code managed settings, or clear them with
        `null`.

        **Accepted credentials:** an organization-level Admin API key with the
        `write:claude_code_managed_settings` scope.

        Every request must include the beta header
        `anthropic-beta: ce-claude-code-managed-settings-2026-10-06`. A request without
        it, or from an organization not enabled for this beta, returns `404`. The Claude
        Code Managed Settings API is in beta and is available to Claude Enterprise
        organizations only.

        A write that returns `503` may have applied. Retrying it is safe.

        Args:
          settings: The whole settings document, a JSON object of Claude Code managed settings. It
              replaces any stored document, or `null` clears the default settings. At most 1
              MiB as the server stores it, which can be larger than the request body.

          betas: This endpoint is in beta: requests must send
              `ce-claude-code-managed-settings-2026-10-06` in this header.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

        Raises:
          BetaCMEKFeatureUnsupportedError:

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
            "/v1/organizations/claude_code/managed_settings/rbac_group_default",
            body={"settings": settings},
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                qualifiers={"beta": "true"},
                span_name="anthropic.organization.claude_code.managed_settings.rbac_group_default.update",
                span_route="/v1/organizations/claude_code/managed_settings/rbac_group_default",
            ),
            cast_to=BetaClaudeCodeRBACGroupDefaultManagedSettings,
        )


class RBACGroupDefaultWithRawResponse:
    def __init__(self, rbac_group_default: RBACGroupDefault) -> None:
        self._rbac_group_default = rbac_group_default

        self.retrieve = to_raw_response_wrapper(
            rbac_group_default.retrieve,
        )
        self.update = to_raw_response_wrapper(
            rbac_group_default.update,
        )


class AsyncRBACGroupDefaultWithRawResponse:
    def __init__(self, rbac_group_default: AsyncRBACGroupDefault) -> None:
        self._rbac_group_default = rbac_group_default

        self.retrieve = async_to_raw_response_wrapper(
            rbac_group_default.retrieve,
        )
        self.update = async_to_raw_response_wrapper(
            rbac_group_default.update,
        )


class RBACGroupDefaultWithStreamingResponse:
    def __init__(self, rbac_group_default: RBACGroupDefault) -> None:
        self._rbac_group_default = rbac_group_default

        self.retrieve = to_streamed_response_wrapper(
            rbac_group_default.retrieve,
        )
        self.update = to_streamed_response_wrapper(
            rbac_group_default.update,
        )


class AsyncRBACGroupDefaultWithStreamingResponse:
    def __init__(self, rbac_group_default: AsyncRBACGroupDefault) -> None:
        self._rbac_group_default = rbac_group_default

        self.retrieve = async_to_streamed_response_wrapper(
            rbac_group_default.retrieve,
        )
        self.update = async_to_streamed_response_wrapper(
            rbac_group_default.update,
        )
