from __future__ import annotations

from typing import List

import httpx2

from ...._types import Body, Omit, Query, Headers, NotGiven, omit, not_given
from ...._utils import is_given, strip_not_given
from ...._compat import cached_property
from ...._resource import SyncAPIResource, AsyncAPIResource
from ...._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ...._base_client import make_request_options
from ....types.beta.organization import BetaComplianceSettingsStateParam
from ....types.anthropic_beta_param import AnthropicBetaParam
from ....types.beta.organization.beta_compliance_settings import BetaComplianceSettings
from ....types.beta.organization.beta_compliance_settings_state_param import BetaComplianceSettingsStateParam

__all__ = ["ComplianceSettings", "AsyncComplianceSettings"]


class ComplianceSettings(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> ComplianceSettingsWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://platform.claude.com/docs/en/api/sdks/python
        """
        return ComplianceSettingsWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ComplianceSettingsWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://platform.claude.com/docs/en/api/sdks/python
        """
        return ComplianceSettingsWithStreamingResponse(self)

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
    ) -> BetaComplianceSettings:
        """
        Retrieve your organization's Compliance Settings.

        Compliance Settings is a singleton resource: there is exactly one per
        organization, addressed without an identifier. The `state` field reflects
        whether the Compliance API is enabled. An organization with a parent
        organization reads the state inherited from the parent's configuration.

        Args:
          betas: Optional. Send `efs-2026-10-01` in this header to use this endpoint's beta
              features: additional parameters, accepted values and response fields.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {
            **strip_not_given({"anthropic-beta": ",".join(str(e) for e in betas) if is_given(betas) else not_given}),
            **(extra_headers or {}),
        }
        return self._get(
            "/v1/organizations/compliance_settings",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                qualifiers={"beta": "true"},
                span_name="anthropic.organization.compliance_settings.retrieve",
                span_route="/v1/organizations/compliance_settings",
            ),
            cast_to=BetaComplianceSettings,
        )

    def update(
        self,
        *,
        state: BetaComplianceSettingsStateParam,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaComplianceSettings:
        """
        Update your organization's Compliance Settings.

        Setting `state` to `enabled` turns on the Compliance API and begins capturing
        organization activity events. Setting it to `disabled` turns both off. Access
        Transparency events are an exception: they are still captured while the
        Compliance API is disabled, and the Compliance API activity feed returns them
        once it is enabled again. `state` reflects whether the Compliance API is
        enabled.

        A request that sets `state` to its current value succeeds and leaves the
        resource unchanged. A `disabled` request stays in effect until a later `enabled`
        request or the organization's next provisioning action that enables Access
        Transparency: enabling Access Transparency also enables the Compliance API,
        which serves its activity events, so such provisioning (including re-runs)
        re-enables the Compliance API even after a `disabled` request. Automated
        provisioning never disables compliance settings.

        Args:
          state: Desired state. Accepts the string shorthand "enabled" or "disabled" in place of
              the object form; the response always returns the canonical object form.

          betas: Optional. Send `efs-2026-10-01` in this header to use this endpoint's beta
              features: additional parameters, accepted values and response fields.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

        Raises:
          SandboxEgressRestrictedError:
        """
        extra_headers = {
            **strip_not_given({"anthropic-beta": ",".join(str(e) for e in betas) if is_given(betas) else not_given}),
            **(extra_headers or {}),
        }
        return self._post(
            "/v1/organizations/compliance_settings",
            body={"state": state},
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                qualifiers={"beta": "true"},
                span_name="anthropic.organization.compliance_settings.update",
                span_route="/v1/organizations/compliance_settings",
            ),
            cast_to=BetaComplianceSettings,
        )


class AsyncComplianceSettings(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncComplianceSettingsWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://platform.claude.com/docs/en/api/sdks/python
        """
        return AsyncComplianceSettingsWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncComplianceSettingsWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://platform.claude.com/docs/en/api/sdks/python
        """
        return AsyncComplianceSettingsWithStreamingResponse(self)

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
    ) -> BetaComplianceSettings:
        """
        Retrieve your organization's Compliance Settings.

        Compliance Settings is a singleton resource: there is exactly one per
        organization, addressed without an identifier. The `state` field reflects
        whether the Compliance API is enabled. An organization with a parent
        organization reads the state inherited from the parent's configuration.

        Args:
          betas: Optional. Send `efs-2026-10-01` in this header to use this endpoint's beta
              features: additional parameters, accepted values and response fields.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {
            **strip_not_given({"anthropic-beta": ",".join(str(e) for e in betas) if is_given(betas) else not_given}),
            **(extra_headers or {}),
        }
        return await self._get(
            "/v1/organizations/compliance_settings",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                qualifiers={"beta": "true"},
                span_name="anthropic.organization.compliance_settings.retrieve",
                span_route="/v1/organizations/compliance_settings",
            ),
            cast_to=BetaComplianceSettings,
        )

    async def update(
        self,
        *,
        state: BetaComplianceSettingsStateParam,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaComplianceSettings:
        """
        Update your organization's Compliance Settings.

        Setting `state` to `enabled` turns on the Compliance API and begins capturing
        organization activity events. Setting it to `disabled` turns both off. Access
        Transparency events are an exception: they are still captured while the
        Compliance API is disabled, and the Compliance API activity feed returns them
        once it is enabled again. `state` reflects whether the Compliance API is
        enabled.

        A request that sets `state` to its current value succeeds and leaves the
        resource unchanged. A `disabled` request stays in effect until a later `enabled`
        request or the organization's next provisioning action that enables Access
        Transparency: enabling Access Transparency also enables the Compliance API,
        which serves its activity events, so such provisioning (including re-runs)
        re-enables the Compliance API even after a `disabled` request. Automated
        provisioning never disables compliance settings.

        Args:
          state: Desired state. Accepts the string shorthand "enabled" or "disabled" in place of
              the object form; the response always returns the canonical object form.

          betas: Optional. Send `efs-2026-10-01` in this header to use this endpoint's beta
              features: additional parameters, accepted values and response fields.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

        Raises:
          SandboxEgressRestrictedError:
        """
        extra_headers = {
            **strip_not_given({"anthropic-beta": ",".join(str(e) for e in betas) if is_given(betas) else not_given}),
            **(extra_headers or {}),
        }
        return await self._post(
            "/v1/organizations/compliance_settings",
            body={"state": state},
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                qualifiers={"beta": "true"},
                span_name="anthropic.organization.compliance_settings.update",
                span_route="/v1/organizations/compliance_settings",
            ),
            cast_to=BetaComplianceSettings,
        )


class ComplianceSettingsWithRawResponse:
    def __init__(self, compliance_settings: ComplianceSettings) -> None:
        self._compliance_settings = compliance_settings

        self.retrieve = to_raw_response_wrapper(
            compliance_settings.retrieve,
        )
        self.update = to_raw_response_wrapper(
            compliance_settings.update,
        )


class AsyncComplianceSettingsWithRawResponse:
    def __init__(self, compliance_settings: AsyncComplianceSettings) -> None:
        self._compliance_settings = compliance_settings

        self.retrieve = async_to_raw_response_wrapper(
            compliance_settings.retrieve,
        )
        self.update = async_to_raw_response_wrapper(
            compliance_settings.update,
        )


class ComplianceSettingsWithStreamingResponse:
    def __init__(self, compliance_settings: ComplianceSettings) -> None:
        self._compliance_settings = compliance_settings

        self.retrieve = to_streamed_response_wrapper(
            compliance_settings.retrieve,
        )
        self.update = to_streamed_response_wrapper(
            compliance_settings.update,
        )


class AsyncComplianceSettingsWithStreamingResponse:
    def __init__(self, compliance_settings: AsyncComplianceSettings) -> None:
        self._compliance_settings = compliance_settings

        self.retrieve = async_to_streamed_response_wrapper(
            compliance_settings.retrieve,
        )
        self.update = async_to_streamed_response_wrapper(
            compliance_settings.update,
        )
