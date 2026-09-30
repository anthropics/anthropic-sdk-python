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
from .....types.beta.organization.plugins.beta_plugin_share import BetaPluginShare

__all__ = ["Shares", "AsyncShares"]


class Shares(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> SharesWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#accessing-raw-response-data-eg-headers
        """
        return SharesWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> SharesWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#with_streaming_response
        """
        return SharesWithStreamingResponse(self)

    def list(
        self,
        plugin_id: str,
        *,
        limit: int | Omit = omit,
        organization_id: Optional[str] | Omit = omit,
        page: Optional[str] | Omit = omit,
        target_type: Optional[Literal["organization", "organization_member", "rbac_group"]] | Omit = omit,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> SyncPageCursor[BetaPluginShare]:
        """
        List the shares the owner of a member-owned Plugin has given — to every member
        of the organization, to an RBAC Group, or to one member — most recently granted
        first.

        Shares are read-only in this API: members give and withdraw them in claude.ai,
        and who gave a share is recorded on the Compliance API activity feed rather than
        on the share. An organization-owned Plugin has installation settings instead, so
        this path returns 404 for one.

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

          target_type: Only shares with this kind of target: `organization` (every member),
              `rbac_group` (one RBAC Group), or `organization_member` (one member).

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
            path_template("/v1/organizations/plugins/{plugin_id}/shares?beta=true", plugin_id=plugin_id),
            page=SyncPageCursor[BetaPluginShare],
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
            model=BetaPluginShare,
        )


class AsyncShares(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncSharesWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#accessing-raw-response-data-eg-headers
        """
        return AsyncSharesWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncSharesWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#with_streaming_response
        """
        return AsyncSharesWithStreamingResponse(self)

    def list(
        self,
        plugin_id: str,
        *,
        limit: int | Omit = omit,
        organization_id: Optional[str] | Omit = omit,
        page: Optional[str] | Omit = omit,
        target_type: Optional[Literal["organization", "organization_member", "rbac_group"]] | Omit = omit,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> AsyncPaginator[BetaPluginShare, AsyncPageCursor[BetaPluginShare]]:
        """
        List the shares the owner of a member-owned Plugin has given — to every member
        of the organization, to an RBAC Group, or to one member — most recently granted
        first.

        Shares are read-only in this API: members give and withdraw them in claude.ai,
        and who gave a share is recorded on the Compliance API activity feed rather than
        on the share. An organization-owned Plugin has installation settings instead, so
        this path returns 404 for one.

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

          target_type: Only shares with this kind of target: `organization` (every member),
              `rbac_group` (one RBAC Group), or `organization_member` (one member).

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
            path_template("/v1/organizations/plugins/{plugin_id}/shares?beta=true", plugin_id=plugin_id),
            page=AsyncPageCursor[BetaPluginShare],
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
            model=BetaPluginShare,
        )


class SharesWithRawResponse:
    def __init__(self, shares: Shares) -> None:
        self._shares = shares

        self.list = to_raw_response_wrapper(
            shares.list,
        )


class AsyncSharesWithRawResponse:
    def __init__(self, shares: AsyncShares) -> None:
        self._shares = shares

        self.list = async_to_raw_response_wrapper(
            shares.list,
        )


class SharesWithStreamingResponse:
    def __init__(self, shares: Shares) -> None:
        self._shares = shares

        self.list = to_streamed_response_wrapper(
            shares.list,
        )


class AsyncSharesWithStreamingResponse:
    def __init__(self, shares: AsyncShares) -> None:
        self._shares = shares

        self.list = async_to_streamed_response_wrapper(
            shares.list,
        )
