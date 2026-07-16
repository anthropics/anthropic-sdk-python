# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from itertools import chain

import httpx

from .... import _legacy_response
from ...._types import Body, Omit, Query, Headers, NotGiven, omit, not_given
from ...._utils import is_given, path_template, maybe_transform, strip_not_given, async_maybe_transform
from ...._compat import cached_property
from ...._resource import SyncAPIResource, AsyncAPIResource
from ...._response import to_streamed_response_wrapper, async_to_streamed_response_wrapper
from ....pagination import SyncPageCursor, AsyncPageCursor
from ...._base_client import AsyncPaginator, make_request_options
from ....types.beta.tunnels import certificate_list_params, certificate_create_params
from ....types.anthropic_beta_param import AnthropicBetaParam
from ....types.beta.tunnels.beta_tunnel_certificate import BetaTunnelCertificate

__all__ = ["Certificates", "AsyncCertificates"]


class Certificates(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> CertificatesWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#accessing-raw-response-data-eg-headers
        """
        return CertificatesWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> CertificatesWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#with_streaming_response
        """
        return CertificatesWithStreamingResponse(self)

    def create(
        self,
        tunnel_id: str,
        *,
        ca_certificate_pem: str,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> BetaTunnelCertificate:
        """The Tunnels API is in research preview.

        It requires the
        `anthropic-beta: mcp-tunnels-2026-06-22` header and may change without a
        deprecation period. It supersedes the Admin API endpoints at
        `/v1/organizations/tunnels`, which remain available during a migration window.

        Registers a public CA certificate on a tunnel. Anthropic verifies the gateway's
        server certificate against this CA when it terminates the inner TLS session. A
        tunnel holds at most two non-archived certificates.

        Args:
          ca_certificate_pem: PEM-encoded X.509 CA certificate. Must contain exactly one certificate and no
              private-key material. Maximum 8KB.

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
            path_template("/v1/tunnels/{tunnel_id}/certificates?beta=true", tunnel_id=tunnel_id),
            body=maybe_transform(
                {"ca_certificate_pem": ca_certificate_pem}, certificate_create_params.CertificateCreateParams
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BetaTunnelCertificate,
        )

    def retrieve(
        self,
        certificate_id: str,
        *,
        tunnel_id: str,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> BetaTunnelCertificate:
        """The Tunnels API is in research preview.

        It requires the
        `anthropic-beta: mcp-tunnels-2026-06-22` header and may change without a
        deprecation period. It supersedes the Admin API endpoints at
        `/v1/organizations/tunnels`, which remain available during a migration window.

        Fetches a tunnel certificate by ID.

        Args:
          betas: Optional header to specify the beta version(s) you want to use.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not tunnel_id:
            raise ValueError(f"Expected a non-empty value for `tunnel_id` but received {tunnel_id!r}")
        if not certificate_id:
            raise ValueError(f"Expected a non-empty value for `certificate_id` but received {certificate_id!r}")
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
            path_template(
                "/v1/tunnels/{tunnel_id}/certificates/{certificate_id}?beta=true",
                tunnel_id=tunnel_id,
                certificate_id=certificate_id,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BetaTunnelCertificate,
        )

    def list(
        self,
        tunnel_id: str,
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
    ) -> SyncPageCursor[BetaTunnelCertificate]:
        """The Tunnels API is in research preview.

        It requires the
        `anthropic-beta: mcp-tunnels-2026-06-22` header and may change without a
        deprecation period. It supersedes the Admin API endpoints at
        `/v1/organizations/tunnels`, which remain available during a migration window.

        Lists the certificates registered on a tunnel. Archived certificates are
        excluded unless include_archived is set.

        Args:
          include_archived: Whether to include archived certificates in the results. Defaults to false.

          limit: Maximum number of certificates to return per page. Defaults to 20, maximum 1000.

          page: Opaque pagination cursor from a previous `list_tunnel_certificates` response.

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
        return self._get_api_list(
            path_template("/v1/tunnels/{tunnel_id}/certificates?beta=true", tunnel_id=tunnel_id),
            page=SyncPageCursor[BetaTunnelCertificate],
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
                    certificate_list_params.CertificateListParams,
                ),
            ),
            model=BetaTunnelCertificate,
        )

    def archive(
        self,
        certificate_id: str,
        *,
        tunnel_id: str,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> BetaTunnelCertificate:
        """The Tunnels API is in research preview.

        It requires the
        `anthropic-beta: mcp-tunnels-2026-06-22` header and may change without a
        deprecation period. It supersedes the Admin API endpoints at
        `/v1/organizations/tunnels`, which remain available during a migration window.

        Archives a tunnel certificate, removing it from the set Anthropic trusts for the
        tunnel. The certificate record is retained. Archiving the last non-archived
        certificate is permitted; the tunnel rejects MCP traffic until a new certificate
        is added.

        Args:
          betas: Optional header to specify the beta version(s) you want to use.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not tunnel_id:
            raise ValueError(f"Expected a non-empty value for `tunnel_id` but received {tunnel_id!r}")
        if not certificate_id:
            raise ValueError(f"Expected a non-empty value for `certificate_id` but received {certificate_id!r}")
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
            path_template(
                "/v1/tunnels/{tunnel_id}/certificates/{certificate_id}/archive?beta=true",
                tunnel_id=tunnel_id,
                certificate_id=certificate_id,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BetaTunnelCertificate,
        )


class AsyncCertificates(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncCertificatesWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#accessing-raw-response-data-eg-headers
        """
        return AsyncCertificatesWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncCertificatesWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#with_streaming_response
        """
        return AsyncCertificatesWithStreamingResponse(self)

    async def create(
        self,
        tunnel_id: str,
        *,
        ca_certificate_pem: str,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> BetaTunnelCertificate:
        """The Tunnels API is in research preview.

        It requires the
        `anthropic-beta: mcp-tunnels-2026-06-22` header and may change without a
        deprecation period. It supersedes the Admin API endpoints at
        `/v1/organizations/tunnels`, which remain available during a migration window.

        Registers a public CA certificate on a tunnel. Anthropic verifies the gateway's
        server certificate against this CA when it terminates the inner TLS session. A
        tunnel holds at most two non-archived certificates.

        Args:
          ca_certificate_pem: PEM-encoded X.509 CA certificate. Must contain exactly one certificate and no
              private-key material. Maximum 8KB.

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
            path_template("/v1/tunnels/{tunnel_id}/certificates?beta=true", tunnel_id=tunnel_id),
            body=await async_maybe_transform(
                {"ca_certificate_pem": ca_certificate_pem}, certificate_create_params.CertificateCreateParams
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BetaTunnelCertificate,
        )

    async def retrieve(
        self,
        certificate_id: str,
        *,
        tunnel_id: str,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> BetaTunnelCertificate:
        """The Tunnels API is in research preview.

        It requires the
        `anthropic-beta: mcp-tunnels-2026-06-22` header and may change without a
        deprecation period. It supersedes the Admin API endpoints at
        `/v1/organizations/tunnels`, which remain available during a migration window.

        Fetches a tunnel certificate by ID.

        Args:
          betas: Optional header to specify the beta version(s) you want to use.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not tunnel_id:
            raise ValueError(f"Expected a non-empty value for `tunnel_id` but received {tunnel_id!r}")
        if not certificate_id:
            raise ValueError(f"Expected a non-empty value for `certificate_id` but received {certificate_id!r}")
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
            path_template(
                "/v1/tunnels/{tunnel_id}/certificates/{certificate_id}?beta=true",
                tunnel_id=tunnel_id,
                certificate_id=certificate_id,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BetaTunnelCertificate,
        )

    def list(
        self,
        tunnel_id: str,
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
    ) -> AsyncPaginator[BetaTunnelCertificate, AsyncPageCursor[BetaTunnelCertificate]]:
        """The Tunnels API is in research preview.

        It requires the
        `anthropic-beta: mcp-tunnels-2026-06-22` header and may change without a
        deprecation period. It supersedes the Admin API endpoints at
        `/v1/organizations/tunnels`, which remain available during a migration window.

        Lists the certificates registered on a tunnel. Archived certificates are
        excluded unless include_archived is set.

        Args:
          include_archived: Whether to include archived certificates in the results. Defaults to false.

          limit: Maximum number of certificates to return per page. Defaults to 20, maximum 1000.

          page: Opaque pagination cursor from a previous `list_tunnel_certificates` response.

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
        return self._get_api_list(
            path_template("/v1/tunnels/{tunnel_id}/certificates?beta=true", tunnel_id=tunnel_id),
            page=AsyncPageCursor[BetaTunnelCertificate],
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
                    certificate_list_params.CertificateListParams,
                ),
            ),
            model=BetaTunnelCertificate,
        )

    async def archive(
        self,
        certificate_id: str,
        *,
        tunnel_id: str,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> BetaTunnelCertificate:
        """The Tunnels API is in research preview.

        It requires the
        `anthropic-beta: mcp-tunnels-2026-06-22` header and may change without a
        deprecation period. It supersedes the Admin API endpoints at
        `/v1/organizations/tunnels`, which remain available during a migration window.

        Archives a tunnel certificate, removing it from the set Anthropic trusts for the
        tunnel. The certificate record is retained. Archiving the last non-archived
        certificate is permitted; the tunnel rejects MCP traffic until a new certificate
        is added.

        Args:
          betas: Optional header to specify the beta version(s) you want to use.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not tunnel_id:
            raise ValueError(f"Expected a non-empty value for `tunnel_id` but received {tunnel_id!r}")
        if not certificate_id:
            raise ValueError(f"Expected a non-empty value for `certificate_id` but received {certificate_id!r}")
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
            path_template(
                "/v1/tunnels/{tunnel_id}/certificates/{certificate_id}/archive?beta=true",
                tunnel_id=tunnel_id,
                certificate_id=certificate_id,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BetaTunnelCertificate,
        )


class CertificatesWithRawResponse:
    def __init__(self, certificates: Certificates) -> None:
        self._certificates = certificates

        self.create = _legacy_response.to_raw_response_wrapper(
            certificates.create,
        )
        self.retrieve = _legacy_response.to_raw_response_wrapper(
            certificates.retrieve,
        )
        self.list = _legacy_response.to_raw_response_wrapper(
            certificates.list,
        )
        self.archive = _legacy_response.to_raw_response_wrapper(
            certificates.archive,
        )


class AsyncCertificatesWithRawResponse:
    def __init__(self, certificates: AsyncCertificates) -> None:
        self._certificates = certificates

        self.create = _legacy_response.async_to_raw_response_wrapper(
            certificates.create,
        )
        self.retrieve = _legacy_response.async_to_raw_response_wrapper(
            certificates.retrieve,
        )
        self.list = _legacy_response.async_to_raw_response_wrapper(
            certificates.list,
        )
        self.archive = _legacy_response.async_to_raw_response_wrapper(
            certificates.archive,
        )


class CertificatesWithStreamingResponse:
    def __init__(self, certificates: Certificates) -> None:
        self._certificates = certificates

        self.create = to_streamed_response_wrapper(
            certificates.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            certificates.retrieve,
        )
        self.list = to_streamed_response_wrapper(
            certificates.list,
        )
        self.archive = to_streamed_response_wrapper(
            certificates.archive,
        )


class AsyncCertificatesWithStreamingResponse:
    def __init__(self, certificates: AsyncCertificates) -> None:
        self._certificates = certificates

        self.create = async_to_streamed_response_wrapper(
            certificates.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            certificates.retrieve,
        )
        self.list = async_to_streamed_response_wrapper(
            certificates.list,
        )
        self.archive = async_to_streamed_response_wrapper(
            certificates.archive,
        )
