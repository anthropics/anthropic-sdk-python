# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Optional
from itertools import chain

import httpx

from .... import _legacy_response
from ...._types import Body, Omit, Query, Headers, NotGiven, omit, not_given
from ...._utils import is_given, path_template, maybe_transform, strip_not_given, async_maybe_transform
from ...._compat import cached_property
from ...._resource import SyncAPIResource, AsyncAPIResource
from ...._response import to_streamed_response_wrapper, async_to_streamed_response_wrapper
from .certificates import (
    Certificates,
    AsyncCertificates,
    CertificatesWithRawResponse,
    AsyncCertificatesWithRawResponse,
    CertificatesWithStreamingResponse,
    AsyncCertificatesWithStreamingResponse,
)
from ....pagination import SyncPageCursor, AsyncPageCursor
from ....types.beta import tunnel_list_params, tunnel_create_params, tunnel_rotate_token_params
from ...._base_client import AsyncPaginator, make_request_options
from ....types.beta.beta_tunnel import BetaTunnel
from ....types.anthropic_beta_param import AnthropicBetaParam
from ....types.beta.beta_tunnel_token import BetaTunnelToken

__all__ = ["Tunnels", "AsyncTunnels"]


class Tunnels(SyncAPIResource):
    @cached_property
    def certificates(self) -> Certificates:
        return Certificates(self._client)

    @cached_property
    def with_raw_response(self) -> TunnelsWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#accessing-raw-response-data-eg-headers
        """
        return TunnelsWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> TunnelsWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#with_streaming_response
        """
        return TunnelsWithStreamingResponse(self)

    def create(
        self,
        *,
        display_name: Optional[str] | Omit = omit,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> BetaTunnel:
        """The Tunnels API is in research preview.

        It requires the
        `anthropic-beta: mcp-tunnels-2026-06-22` header and may change without a
        deprecation period. It supersedes the Admin API endpoints at
        `/v1/organizations/tunnels`, which remain available during a migration window.

        Creates a tunnel. Creation allocates a fresh hostname and provisions the tunnel;
        it is not idempotent. The new tunnel rejects MCP traffic until at least one CA
        certificate is added.

        Args:
          display_name: Optional human-readable name for the tunnel (1-255 characters).

          betas: Optional header to specify the beta version(s) you want to use.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {
            **strip_not_given(
                {
                    "anthropic-beta": ",".join(chain((str(e) for e in betas), ["mcp-tunnels-2026-06-22"]))
                    if is_given(betas)
                    else not_given
                }
            ),
            **(extra_headers or {}),
        }
        extra_headers = {"anthropic-beta": "mcp-tunnels-2026-06-22", **(extra_headers or {})}
        return self._post(
            "/v1/tunnels?beta=true",
            body=maybe_transform({"display_name": display_name}, tunnel_create_params.TunnelCreateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BetaTunnel,
        )

    def retrieve(
        self,
        tunnel_id: str,
        *,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> BetaTunnel:
        """The Tunnels API is in research preview.

        It requires the
        `anthropic-beta: mcp-tunnels-2026-06-22` header and may change without a
        deprecation period. It supersedes the Admin API endpoints at
        `/v1/organizations/tunnels`, which remain available during a migration window.

        Fetches a tunnel by ID.

        Args:
          betas: Optional header to specify the beta version(s) you want to use.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not tunnel_id:
            raise ValueError(f"Expected a non-empty value for `tunnel_id` but received {tunnel_id!r}")
        extra_headers = {
            **strip_not_given(
                {
                    "anthropic-beta": ",".join(chain((str(e) for e in betas), ["mcp-tunnels-2026-06-22"]))
                    if is_given(betas)
                    else not_given
                }
            ),
            **(extra_headers or {}),
        }
        extra_headers = {"anthropic-beta": "mcp-tunnels-2026-06-22", **(extra_headers or {})}
        return self._get(
            path_template("/v1/tunnels/{tunnel_id}?beta=true", tunnel_id=tunnel_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BetaTunnel,
        )

    def list(
        self,
        *,
        include_archived: bool | Omit = omit,
        limit: int | Omit = omit,
        page: str | Omit = omit,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SyncPageCursor[BetaTunnel]:
        """The Tunnels API is in research preview.

        It requires the
        `anthropic-beta: mcp-tunnels-2026-06-22` header and may change without a
        deprecation period. It supersedes the Admin API endpoints at
        `/v1/organizations/tunnels`, which remain available during a migration window.

        Lists tunnels. Results are ordered by creation time, newest first; archived
        tunnels are excluded unless include_archived is set.

        Args:
          include_archived: Whether to include archived tunnels in the results. Defaults to false.

          limit: Maximum number of tunnels to return per page. Defaults to 20, maximum 1000.

          page: Opaque pagination cursor from a previous `list_tunnels` response.

          betas: Optional header to specify the beta version(s) you want to use.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {
            **strip_not_given(
                {
                    "anthropic-beta": ",".join(chain((str(e) for e in betas), ["mcp-tunnels-2026-06-22"]))
                    if is_given(betas)
                    else not_given
                }
            ),
            **(extra_headers or {}),
        }
        extra_headers = {"anthropic-beta": "mcp-tunnels-2026-06-22", **(extra_headers or {})}
        return self._get_api_list(
            "/v1/tunnels?beta=true",
            page=SyncPageCursor[BetaTunnel],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "include_archived": include_archived,
                        "limit": limit,
                        "page": page,
                    },
                    tunnel_list_params.TunnelListParams,
                ),
            ),
            model=BetaTunnel,
        )

    def archive(
        self,
        tunnel_id: str,
        *,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> BetaTunnel:
        """The Tunnels API is in research preview.

        It requires the
        `anthropic-beta: mcp-tunnels-2026-06-22` header and may change without a
        deprecation period. It supersedes the Admin API endpoints at
        `/v1/organizations/tunnels`, which remain available during a migration window.

        Archives a tunnel. Archival is irreversible: every non-archived certificate on
        the tunnel is archived in the same operation, the hostname is retired and never
        re-allocated, and the tunnel token is invalidated. Retrying against an
        already-archived tunnel returns the existing record unchanged.

        Args:
          betas: Optional header to specify the beta version(s) you want to use.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not tunnel_id:
            raise ValueError(f"Expected a non-empty value for `tunnel_id` but received {tunnel_id!r}")
        extra_headers = {
            **strip_not_given(
                {
                    "anthropic-beta": ",".join(chain((str(e) for e in betas), ["mcp-tunnels-2026-06-22"]))
                    if is_given(betas)
                    else not_given
                }
            ),
            **(extra_headers or {}),
        }
        extra_headers = {"anthropic-beta": "mcp-tunnels-2026-06-22", **(extra_headers or {})}
        return self._post(
            path_template("/v1/tunnels/{tunnel_id}/archive?beta=true", tunnel_id=tunnel_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BetaTunnel,
        )

    def reveal_token(
        self,
        tunnel_id: str,
        *,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> BetaTunnelToken:
        """The Tunnels API is in research preview.

        It requires the
        `anthropic-beta: mcp-tunnels-2026-06-22` header and may change without a
        deprecation period. It supersedes the Admin API endpoints at
        `/v1/organizations/tunnels`, which remain available during a migration window.

        Reveals a tunnel's connector token. The value is fetched live on each call;
        Anthropic does not store it. Repeated calls return the same value until the
        token is rotated. Exposed as POST so the token does not appear in intermediary
        access logs.

        Args:
          betas: Optional header to specify the beta version(s) you want to use.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not tunnel_id:
            raise ValueError(f"Expected a non-empty value for `tunnel_id` but received {tunnel_id!r}")
        extra_headers = {
            **strip_not_given(
                {
                    "anthropic-beta": ",".join(chain((str(e) for e in betas), ["mcp-tunnels-2026-06-22"]))
                    if is_given(betas)
                    else not_given
                }
            ),
            **(extra_headers or {}),
        }
        extra_headers = {"anthropic-beta": "mcp-tunnels-2026-06-22", **(extra_headers or {})}
        return self._post(
            path_template("/v1/tunnels/{tunnel_id}/reveal_token?beta=true", tunnel_id=tunnel_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BetaTunnelToken,
        )

    def rotate_token(
        self,
        tunnel_id: str,
        *,
        reason: Optional[str] | Omit = omit,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> BetaTunnelToken:
        """The Tunnels API is in research preview.

        It requires the
        `anthropic-beta: mcp-tunnels-2026-06-22` header and may change without a
        deprecation period. It supersedes the Admin API endpoints at
        `/v1/organizations/tunnels`, which remain available during a migration window.

        Rotates a tunnel's connector token. Rotation invalidates the current token for
        new connections and returns a fresh value; established connections are not
        severed. A connector restarted after rotation must use the new value.

        Args:
          reason: Optional free-text reason for the rotation, recorded for audit.

          betas: Optional header to specify the beta version(s) you want to use.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not tunnel_id:
            raise ValueError(f"Expected a non-empty value for `tunnel_id` but received {tunnel_id!r}")
        extra_headers = {
            **strip_not_given(
                {
                    "anthropic-beta": ",".join(chain((str(e) for e in betas), ["mcp-tunnels-2026-06-22"]))
                    if is_given(betas)
                    else not_given
                }
            ),
            **(extra_headers or {}),
        }
        extra_headers = {"anthropic-beta": "mcp-tunnels-2026-06-22", **(extra_headers or {})}
        return self._post(
            path_template("/v1/tunnels/{tunnel_id}/rotate_token?beta=true", tunnel_id=tunnel_id),
            body=maybe_transform({"reason": reason}, tunnel_rotate_token_params.TunnelRotateTokenParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BetaTunnelToken,
        )


class AsyncTunnels(AsyncAPIResource):
    @cached_property
    def certificates(self) -> AsyncCertificates:
        return AsyncCertificates(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncTunnelsWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#accessing-raw-response-data-eg-headers
        """
        return AsyncTunnelsWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncTunnelsWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#with_streaming_response
        """
        return AsyncTunnelsWithStreamingResponse(self)

    async def create(
        self,
        *,
        display_name: Optional[str] | Omit = omit,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> BetaTunnel:
        """The Tunnels API is in research preview.

        It requires the
        `anthropic-beta: mcp-tunnels-2026-06-22` header and may change without a
        deprecation period. It supersedes the Admin API endpoints at
        `/v1/organizations/tunnels`, which remain available during a migration window.

        Creates a tunnel. Creation allocates a fresh hostname and provisions the tunnel;
        it is not idempotent. The new tunnel rejects MCP traffic until at least one CA
        certificate is added.

        Args:
          display_name: Optional human-readable name for the tunnel (1-255 characters).

          betas: Optional header to specify the beta version(s) you want to use.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {
            **strip_not_given(
                {
                    "anthropic-beta": ",".join(chain((str(e) for e in betas), ["mcp-tunnels-2026-06-22"]))
                    if is_given(betas)
                    else not_given
                }
            ),
            **(extra_headers or {}),
        }
        extra_headers = {"anthropic-beta": "mcp-tunnels-2026-06-22", **(extra_headers or {})}
        return await self._post(
            "/v1/tunnels?beta=true",
            body=await async_maybe_transform({"display_name": display_name}, tunnel_create_params.TunnelCreateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BetaTunnel,
        )

    async def retrieve(
        self,
        tunnel_id: str,
        *,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> BetaTunnel:
        """The Tunnels API is in research preview.

        It requires the
        `anthropic-beta: mcp-tunnels-2026-06-22` header and may change without a
        deprecation period. It supersedes the Admin API endpoints at
        `/v1/organizations/tunnels`, which remain available during a migration window.

        Fetches a tunnel by ID.

        Args:
          betas: Optional header to specify the beta version(s) you want to use.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not tunnel_id:
            raise ValueError(f"Expected a non-empty value for `tunnel_id` but received {tunnel_id!r}")
        extra_headers = {
            **strip_not_given(
                {
                    "anthropic-beta": ",".join(chain((str(e) for e in betas), ["mcp-tunnels-2026-06-22"]))
                    if is_given(betas)
                    else not_given
                }
            ),
            **(extra_headers or {}),
        }
        extra_headers = {"anthropic-beta": "mcp-tunnels-2026-06-22", **(extra_headers or {})}
        return await self._get(
            path_template("/v1/tunnels/{tunnel_id}?beta=true", tunnel_id=tunnel_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BetaTunnel,
        )

    def list(
        self,
        *,
        include_archived: bool | Omit = omit,
        limit: int | Omit = omit,
        page: str | Omit = omit,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AsyncPaginator[BetaTunnel, AsyncPageCursor[BetaTunnel]]:
        """The Tunnels API is in research preview.

        It requires the
        `anthropic-beta: mcp-tunnels-2026-06-22` header and may change without a
        deprecation period. It supersedes the Admin API endpoints at
        `/v1/organizations/tunnels`, which remain available during a migration window.

        Lists tunnels. Results are ordered by creation time, newest first; archived
        tunnels are excluded unless include_archived is set.

        Args:
          include_archived: Whether to include archived tunnels in the results. Defaults to false.

          limit: Maximum number of tunnels to return per page. Defaults to 20, maximum 1000.

          page: Opaque pagination cursor from a previous `list_tunnels` response.

          betas: Optional header to specify the beta version(s) you want to use.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {
            **strip_not_given(
                {
                    "anthropic-beta": ",".join(chain((str(e) for e in betas), ["mcp-tunnels-2026-06-22"]))
                    if is_given(betas)
                    else not_given
                }
            ),
            **(extra_headers or {}),
        }
        extra_headers = {"anthropic-beta": "mcp-tunnels-2026-06-22", **(extra_headers or {})}
        return self._get_api_list(
            "/v1/tunnels?beta=true",
            page=AsyncPageCursor[BetaTunnel],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "include_archived": include_archived,
                        "limit": limit,
                        "page": page,
                    },
                    tunnel_list_params.TunnelListParams,
                ),
            ),
            model=BetaTunnel,
        )

    async def archive(
        self,
        tunnel_id: str,
        *,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> BetaTunnel:
        """The Tunnels API is in research preview.

        It requires the
        `anthropic-beta: mcp-tunnels-2026-06-22` header and may change without a
        deprecation period. It supersedes the Admin API endpoints at
        `/v1/organizations/tunnels`, which remain available during a migration window.

        Archives a tunnel. Archival is irreversible: every non-archived certificate on
        the tunnel is archived in the same operation, the hostname is retired and never
        re-allocated, and the tunnel token is invalidated. Retrying against an
        already-archived tunnel returns the existing record unchanged.

        Args:
          betas: Optional header to specify the beta version(s) you want to use.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not tunnel_id:
            raise ValueError(f"Expected a non-empty value for `tunnel_id` but received {tunnel_id!r}")
        extra_headers = {
            **strip_not_given(
                {
                    "anthropic-beta": ",".join(chain((str(e) for e in betas), ["mcp-tunnels-2026-06-22"]))
                    if is_given(betas)
                    else not_given
                }
            ),
            **(extra_headers or {}),
        }
        extra_headers = {"anthropic-beta": "mcp-tunnels-2026-06-22", **(extra_headers or {})}
        return await self._post(
            path_template("/v1/tunnels/{tunnel_id}/archive?beta=true", tunnel_id=tunnel_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BetaTunnel,
        )

    async def reveal_token(
        self,
        tunnel_id: str,
        *,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> BetaTunnelToken:
        """The Tunnels API is in research preview.

        It requires the
        `anthropic-beta: mcp-tunnels-2026-06-22` header and may change without a
        deprecation period. It supersedes the Admin API endpoints at
        `/v1/organizations/tunnels`, which remain available during a migration window.

        Reveals a tunnel's connector token. The value is fetched live on each call;
        Anthropic does not store it. Repeated calls return the same value until the
        token is rotated. Exposed as POST so the token does not appear in intermediary
        access logs.

        Args:
          betas: Optional header to specify the beta version(s) you want to use.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not tunnel_id:
            raise ValueError(f"Expected a non-empty value for `tunnel_id` but received {tunnel_id!r}")
        extra_headers = {
            **strip_not_given(
                {
                    "anthropic-beta": ",".join(chain((str(e) for e in betas), ["mcp-tunnels-2026-06-22"]))
                    if is_given(betas)
                    else not_given
                }
            ),
            **(extra_headers or {}),
        }
        extra_headers = {"anthropic-beta": "mcp-tunnels-2026-06-22", **(extra_headers or {})}
        return await self._post(
            path_template("/v1/tunnels/{tunnel_id}/reveal_token?beta=true", tunnel_id=tunnel_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BetaTunnelToken,
        )

    async def rotate_token(
        self,
        tunnel_id: str,
        *,
        reason: Optional[str] | Omit = omit,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> BetaTunnelToken:
        """The Tunnels API is in research preview.

        It requires the
        `anthropic-beta: mcp-tunnels-2026-06-22` header and may change without a
        deprecation period. It supersedes the Admin API endpoints at
        `/v1/organizations/tunnels`, which remain available during a migration window.

        Rotates a tunnel's connector token. Rotation invalidates the current token for
        new connections and returns a fresh value; established connections are not
        severed. A connector restarted after rotation must use the new value.

        Args:
          reason: Optional free-text reason for the rotation, recorded for audit.

          betas: Optional header to specify the beta version(s) you want to use.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not tunnel_id:
            raise ValueError(f"Expected a non-empty value for `tunnel_id` but received {tunnel_id!r}")
        extra_headers = {
            **strip_not_given(
                {
                    "anthropic-beta": ",".join(chain((str(e) for e in betas), ["mcp-tunnels-2026-06-22"]))
                    if is_given(betas)
                    else not_given
                }
            ),
            **(extra_headers or {}),
        }
        extra_headers = {"anthropic-beta": "mcp-tunnels-2026-06-22", **(extra_headers or {})}
        return await self._post(
            path_template("/v1/tunnels/{tunnel_id}/rotate_token?beta=true", tunnel_id=tunnel_id),
            body=await async_maybe_transform({"reason": reason}, tunnel_rotate_token_params.TunnelRotateTokenParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BetaTunnelToken,
        )


class TunnelsWithRawResponse:
    def __init__(self, tunnels: Tunnels) -> None:
        self._tunnels = tunnels

        self.create = _legacy_response.to_raw_response_wrapper(
            tunnels.create,
        )
        self.retrieve = _legacy_response.to_raw_response_wrapper(
            tunnels.retrieve,
        )
        self.list = _legacy_response.to_raw_response_wrapper(
            tunnels.list,
        )
        self.archive = _legacy_response.to_raw_response_wrapper(
            tunnels.archive,
        )
        self.reveal_token = _legacy_response.to_raw_response_wrapper(
            tunnels.reveal_token,
        )
        self.rotate_token = _legacy_response.to_raw_response_wrapper(
            tunnels.rotate_token,
        )

    @cached_property
    def certificates(self) -> CertificatesWithRawResponse:
        return CertificatesWithRawResponse(self._tunnels.certificates)


class AsyncTunnelsWithRawResponse:
    def __init__(self, tunnels: AsyncTunnels) -> None:
        self._tunnels = tunnels

        self.create = _legacy_response.async_to_raw_response_wrapper(
            tunnels.create,
        )
        self.retrieve = _legacy_response.async_to_raw_response_wrapper(
            tunnels.retrieve,
        )
        self.list = _legacy_response.async_to_raw_response_wrapper(
            tunnels.list,
        )
        self.archive = _legacy_response.async_to_raw_response_wrapper(
            tunnels.archive,
        )
        self.reveal_token = _legacy_response.async_to_raw_response_wrapper(
            tunnels.reveal_token,
        )
        self.rotate_token = _legacy_response.async_to_raw_response_wrapper(
            tunnels.rotate_token,
        )

    @cached_property
    def certificates(self) -> AsyncCertificatesWithRawResponse:
        return AsyncCertificatesWithRawResponse(self._tunnels.certificates)


class TunnelsWithStreamingResponse:
    def __init__(self, tunnels: Tunnels) -> None:
        self._tunnels = tunnels

        self.create = to_streamed_response_wrapper(
            tunnels.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            tunnels.retrieve,
        )
        self.list = to_streamed_response_wrapper(
            tunnels.list,
        )
        self.archive = to_streamed_response_wrapper(
            tunnels.archive,
        )
        self.reveal_token = to_streamed_response_wrapper(
            tunnels.reveal_token,
        )
        self.rotate_token = to_streamed_response_wrapper(
            tunnels.rotate_token,
        )

    @cached_property
    def certificates(self) -> CertificatesWithStreamingResponse:
        return CertificatesWithStreamingResponse(self._tunnels.certificates)


class AsyncTunnelsWithStreamingResponse:
    def __init__(self, tunnels: AsyncTunnels) -> None:
        self._tunnels = tunnels

        self.create = async_to_streamed_response_wrapper(
            tunnels.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            tunnels.retrieve,
        )
        self.list = async_to_streamed_response_wrapper(
            tunnels.list,
        )
        self.archive = async_to_streamed_response_wrapper(
            tunnels.archive,
        )
        self.reveal_token = async_to_streamed_response_wrapper(
            tunnels.reveal_token,
        )
        self.rotate_token = async_to_streamed_response_wrapper(
            tunnels.rotate_token,
        )

    @cached_property
    def certificates(self) -> AsyncCertificatesWithStreamingResponse:
        return AsyncCertificatesWithStreamingResponse(self._tunnels.certificates)
