# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Optional

import httpx2

from ....._types import Body, Omit, Query, Headers, NotGiven, omit, not_given
from ....._utils import is_given, path_template, maybe_transform, strip_not_given, async_maybe_transform
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
from .....types.beta.organization.federation import issuer_list_params, issuer_create_params, issuer_update_params
from .....types.beta.organization.federation.beta_federation_issuer import BetaFederationIssuer

__all__ = ["Issuers", "AsyncIssuers"]


class Issuers(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> IssuersWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#accessing-raw-response-data-eg-headers
        """
        return IssuersWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> IssuersWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#with_streaming_response
        """
        return IssuersWithStreamingResponse(self)

    def create(
        self,
        *,
        issuer_url: str,
        name: str,
        check_jti: Optional[bool] | Omit = omit,
        jwks: issuer_create_params.JWKS | Omit = omit,
        max_jwt_lifetime_seconds: Optional[int] | Omit = omit,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaFederationIssuer:
        """
        **Requires an OAuth access token with the `org:admin` scope**, from
        `ant auth login --scope org:admin` or a workload identity federation rule; Admin
        API keys are not accepted. See
        [Manage WIF with the Admin API](/docs/en/manage-claude/wif-admin-api).

        Register an OIDC issuer that Anthropic will trust for workload identity
        federation in your organization.

        The `jwks` field controls how the issuer's signing keys are obtained and takes
        one of three shapes selected by `type`: `discovery` (resolve keys through OIDC
        discovery), `explicit_url` (fetch keys from a fixed JWKS URL), or `inline`
        (provide a static key set). When `jwks.type` is `discovery` and no
        `discovery_base` is set, the issuer URL must be publicly reachable over HTTPS so
        Anthropic can fetch the discovery document; for `explicit_url` and `inline`
        modes the issuer URL is only matched as the JWT's `iss` claim and is not
        fetched.

        Args:
          issuer_url: The `iss` claim value to match against.

          name: Slug identifier (lowercase, digits, hyphens). Unique within the organization; a
              duplicate name returns 409.

          check_jti: Whether the jwt-bearer exchange enforces JTI single-use (replay protection) for
              tokens from this issuer. Defaults to true. Applies only to assertions carrying a
              `jti` claim; tokens without one are accepted without single-use enforcement.

          jwks: How signing keys are obtained. Defaults to OIDC discovery.

          max_jwt_lifetime_seconds: Maximum allowed iat→exp spread for assertions from this issuer (1-176400
              seconds, i.e. up to 49h). Defaults to 3600 (1h). Assertions must carry both
              `iat` and `exp`; a missing `iat` is rejected.

          betas: Optional header to specify the beta version(s) you want to use.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {
            **strip_not_given({"anthropic-beta": ",".join(str(e) for e in betas) if is_given(betas) else not_given}),
            **(extra_headers or {}),
        }
        return self._post(
            "/v1/organizations/federation_issuers?beta=true",
            body=maybe_transform(
                {
                    "issuer_url": issuer_url,
                    "name": name,
                    "check_jti": check_jti,
                    "jwks": jwks,
                    "max_jwt_lifetime_seconds": max_jwt_lifetime_seconds,
                },
                issuer_create_params.IssuerCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BetaFederationIssuer,
        )

    def retrieve(
        self,
        federation_issuer_id: str,
        *,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaFederationIssuer:
        """
        **Requires an OAuth access token with the `org:admin` scope**, from
        `ant auth login --scope org:admin` or a workload identity federation rule; Admin
        API keys are not accepted. See
        [Manage WIF with the Admin API](/docs/en/manage-claude/wif-admin-api).

        Retrieve a federation issuer by its ID (`fdis_...`).

        Args:
          federation_issuer_id: ID of the federation issuer.

          betas: Optional header to specify the beta version(s) you want to use.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not federation_issuer_id:
            raise ValueError(
                f"Expected a non-empty value for `federation_issuer_id` but received {federation_issuer_id!r}"
            )
        extra_headers = {
            **strip_not_given({"anthropic-beta": ",".join(str(e) for e in betas) if is_given(betas) else not_given}),
            **(extra_headers or {}),
        }
        return self._get(
            path_template(
                "/v1/organizations/federation_issuers/{federation_issuer_id}?beta=true",
                federation_issuer_id=federation_issuer_id,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BetaFederationIssuer,
        )

    def update(
        self,
        federation_issuer_id: str,
        *,
        check_jti: Optional[bool] | Omit = omit,
        issuer_url: Optional[str] | Omit = omit,
        jwks: Optional[issuer_update_params.JWKS] | Omit = omit,
        jwks_polling_disabled: Optional[bool] | Omit = omit,
        max_jwt_lifetime_seconds: Optional[int] | Omit = omit,
        name: Optional[str] | Omit = omit,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaFederationIssuer:
        """
        **Requires an OAuth access token with the `org:admin` scope**, from
        `ant auth login --scope org:admin` or a workload identity federation rule; Admin
        API keys are not accepted. See
        [Manage WIF with the Admin API](/docs/en/manage-claude/wif-admin-api).

        Partially update a federation issuer.

        Setting `jwks` replaces the full JWKS shape at once. Archived issuers cannot be
        updated; this returns 400. Create a new issuer instead.

        Updating an issuer that backs a rule with a scope outside `workspace:developer`
        or `workspace:inference` requires a Console session.

        Args:
          federation_issuer_id: ID of the federation issuer to update.

          check_jti: Whether the jwt-bearer exchange enforces JTI single-use (replay protection) for
              tokens from this issuer. Applies only to assertions carrying a `jti` claim;
              tokens without one are accepted without single-use enforcement.

          issuer_url: Replaces the `iss` claim value to match against. For discovery-mode issuers
              without a `discovery_base`, this is also the URL Anthropic fetches the OIDC
              discovery document and signing keys from, so changing it repoints the JWKS
              source. Changing the issuer URL to a well-known shared platform is rejected
              while any live rule under this issuer would not constrain tenant identity.

          jwks: Replaces the entire JWKS configuration.

          jwks_polling_disabled: Only `false` is accepted, to re-enable polling after the system pauses it.
              Polling is paused automatically; sending `true` is rejected.

          max_jwt_lifetime_seconds: Maximum allowed iat→exp spread for assertions from this issuer (1-176400
              seconds, i.e. up to 49h). Assertions must carry both `iat` and `exp`; a missing
              `iat` is rejected.

          name: Replaces the slug identifier (lowercase, digits, hyphens). Unique within the
              organization; a duplicate name returns 409.

          betas: Optional header to specify the beta version(s) you want to use.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not federation_issuer_id:
            raise ValueError(
                f"Expected a non-empty value for `federation_issuer_id` but received {federation_issuer_id!r}"
            )
        extra_headers = {
            **strip_not_given({"anthropic-beta": ",".join(str(e) for e in betas) if is_given(betas) else not_given}),
            **(extra_headers or {}),
        }
        return self._post(
            path_template(
                "/v1/organizations/federation_issuers/{federation_issuer_id}?beta=true",
                federation_issuer_id=federation_issuer_id,
            ),
            body=maybe_transform(
                {
                    "check_jti": check_jti,
                    "issuer_url": issuer_url,
                    "jwks": jwks,
                    "jwks_polling_disabled": jwks_polling_disabled,
                    "max_jwt_lifetime_seconds": max_jwt_lifetime_seconds,
                    "name": name,
                },
                issuer_update_params.IssuerUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BetaFederationIssuer,
        )

    def list(
        self,
        *,
        include_archived: bool | Omit = omit,
        limit: int | Omit = omit,
        page: Optional[str] | Omit = omit,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> SyncPageCursor[BetaFederationIssuer]:
        """
        **Requires an OAuth access token with the `org:admin` scope**, from
        `ant auth login --scope org:admin` or a workload identity federation rule; Admin
        API keys are not accepted. See
        [Manage WIF with the Admin API](/docs/en/manage-claude/wif-admin-api).

        List federation issuers in your organization.

        Archived issuers are excluded unless `include_archived=true`.

        Args:
          include_archived: Include archived resources. Defaults to false.

          limit: Number of results per page.

          page: Opaque cursor from a previous response's `next_page`.

          betas: Optional header to specify the beta version(s) you want to use.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {
            **strip_not_given({"anthropic-beta": ",".join(str(e) for e in betas) if is_given(betas) else not_given}),
            **(extra_headers or {}),
        }
        return self._get_api_list(
            "/v1/organizations/federation_issuers?beta=true",
            page=SyncPageCursor[BetaFederationIssuer],
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
                    issuer_list_params.IssuerListParams,
                ),
            ),
            model=BetaFederationIssuer,
        )

    def archive(
        self,
        federation_issuer_id: str,
        *,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaFederationIssuer:
        """
        **Requires an OAuth access token with the `org:admin` scope**, from
        `ant auth login --scope org:admin` or a workload identity federation rule; Admin
        API keys are not accepted. See
        [Manage WIF with the Admin API](/docs/en/manage-claude/wif-admin-api).

        Archive a federation issuer.

        Idempotent; re-archiving returns the issuer with its original `archived_at`.
        Rejected with 400 if any live (non-archived) federation rule still references
        the issuer; archive those rules first (a rule's issuer cannot be changed), or
        recreate them against another issuer.

        Args:
          federation_issuer_id: ID of the federation issuer to archive.

          betas: Optional header to specify the beta version(s) you want to use.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not federation_issuer_id:
            raise ValueError(
                f"Expected a non-empty value for `federation_issuer_id` but received {federation_issuer_id!r}"
            )
        extra_headers = {
            **strip_not_given({"anthropic-beta": ",".join(str(e) for e in betas) if is_given(betas) else not_given}),
            **(extra_headers or {}),
        }
        return self._post(
            path_template(
                "/v1/organizations/federation_issuers/{federation_issuer_id}/archive?beta=true",
                federation_issuer_id=federation_issuer_id,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BetaFederationIssuer,
        )


class AsyncIssuers(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncIssuersWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#accessing-raw-response-data-eg-headers
        """
        return AsyncIssuersWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncIssuersWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#with_streaming_response
        """
        return AsyncIssuersWithStreamingResponse(self)

    async def create(
        self,
        *,
        issuer_url: str,
        name: str,
        check_jti: Optional[bool] | Omit = omit,
        jwks: issuer_create_params.JWKS | Omit = omit,
        max_jwt_lifetime_seconds: Optional[int] | Omit = omit,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaFederationIssuer:
        """
        **Requires an OAuth access token with the `org:admin` scope**, from
        `ant auth login --scope org:admin` or a workload identity federation rule; Admin
        API keys are not accepted. See
        [Manage WIF with the Admin API](/docs/en/manage-claude/wif-admin-api).

        Register an OIDC issuer that Anthropic will trust for workload identity
        federation in your organization.

        The `jwks` field controls how the issuer's signing keys are obtained and takes
        one of three shapes selected by `type`: `discovery` (resolve keys through OIDC
        discovery), `explicit_url` (fetch keys from a fixed JWKS URL), or `inline`
        (provide a static key set). When `jwks.type` is `discovery` and no
        `discovery_base` is set, the issuer URL must be publicly reachable over HTTPS so
        Anthropic can fetch the discovery document; for `explicit_url` and `inline`
        modes the issuer URL is only matched as the JWT's `iss` claim and is not
        fetched.

        Args:
          issuer_url: The `iss` claim value to match against.

          name: Slug identifier (lowercase, digits, hyphens). Unique within the organization; a
              duplicate name returns 409.

          check_jti: Whether the jwt-bearer exchange enforces JTI single-use (replay protection) for
              tokens from this issuer. Defaults to true. Applies only to assertions carrying a
              `jti` claim; tokens without one are accepted without single-use enforcement.

          jwks: How signing keys are obtained. Defaults to OIDC discovery.

          max_jwt_lifetime_seconds: Maximum allowed iat→exp spread for assertions from this issuer (1-176400
              seconds, i.e. up to 49h). Defaults to 3600 (1h). Assertions must carry both
              `iat` and `exp`; a missing `iat` is rejected.

          betas: Optional header to specify the beta version(s) you want to use.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {
            **strip_not_given({"anthropic-beta": ",".join(str(e) for e in betas) if is_given(betas) else not_given}),
            **(extra_headers or {}),
        }
        return await self._post(
            "/v1/organizations/federation_issuers?beta=true",
            body=await async_maybe_transform(
                {
                    "issuer_url": issuer_url,
                    "name": name,
                    "check_jti": check_jti,
                    "jwks": jwks,
                    "max_jwt_lifetime_seconds": max_jwt_lifetime_seconds,
                },
                issuer_create_params.IssuerCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BetaFederationIssuer,
        )

    async def retrieve(
        self,
        federation_issuer_id: str,
        *,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaFederationIssuer:
        """
        **Requires an OAuth access token with the `org:admin` scope**, from
        `ant auth login --scope org:admin` or a workload identity federation rule; Admin
        API keys are not accepted. See
        [Manage WIF with the Admin API](/docs/en/manage-claude/wif-admin-api).

        Retrieve a federation issuer by its ID (`fdis_...`).

        Args:
          federation_issuer_id: ID of the federation issuer.

          betas: Optional header to specify the beta version(s) you want to use.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not federation_issuer_id:
            raise ValueError(
                f"Expected a non-empty value for `federation_issuer_id` but received {federation_issuer_id!r}"
            )
        extra_headers = {
            **strip_not_given({"anthropic-beta": ",".join(str(e) for e in betas) if is_given(betas) else not_given}),
            **(extra_headers or {}),
        }
        return await self._get(
            path_template(
                "/v1/organizations/federation_issuers/{federation_issuer_id}?beta=true",
                federation_issuer_id=federation_issuer_id,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BetaFederationIssuer,
        )

    async def update(
        self,
        federation_issuer_id: str,
        *,
        check_jti: Optional[bool] | Omit = omit,
        issuer_url: Optional[str] | Omit = omit,
        jwks: Optional[issuer_update_params.JWKS] | Omit = omit,
        jwks_polling_disabled: Optional[bool] | Omit = omit,
        max_jwt_lifetime_seconds: Optional[int] | Omit = omit,
        name: Optional[str] | Omit = omit,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaFederationIssuer:
        """
        **Requires an OAuth access token with the `org:admin` scope**, from
        `ant auth login --scope org:admin` or a workload identity federation rule; Admin
        API keys are not accepted. See
        [Manage WIF with the Admin API](/docs/en/manage-claude/wif-admin-api).

        Partially update a federation issuer.

        Setting `jwks` replaces the full JWKS shape at once. Archived issuers cannot be
        updated; this returns 400. Create a new issuer instead.

        Updating an issuer that backs a rule with a scope outside `workspace:developer`
        or `workspace:inference` requires a Console session.

        Args:
          federation_issuer_id: ID of the federation issuer to update.

          check_jti: Whether the jwt-bearer exchange enforces JTI single-use (replay protection) for
              tokens from this issuer. Applies only to assertions carrying a `jti` claim;
              tokens without one are accepted without single-use enforcement.

          issuer_url: Replaces the `iss` claim value to match against. For discovery-mode issuers
              without a `discovery_base`, this is also the URL Anthropic fetches the OIDC
              discovery document and signing keys from, so changing it repoints the JWKS
              source. Changing the issuer URL to a well-known shared platform is rejected
              while any live rule under this issuer would not constrain tenant identity.

          jwks: Replaces the entire JWKS configuration.

          jwks_polling_disabled: Only `false` is accepted, to re-enable polling after the system pauses it.
              Polling is paused automatically; sending `true` is rejected.

          max_jwt_lifetime_seconds: Maximum allowed iat→exp spread for assertions from this issuer (1-176400
              seconds, i.e. up to 49h). Assertions must carry both `iat` and `exp`; a missing
              `iat` is rejected.

          name: Replaces the slug identifier (lowercase, digits, hyphens). Unique within the
              organization; a duplicate name returns 409.

          betas: Optional header to specify the beta version(s) you want to use.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not federation_issuer_id:
            raise ValueError(
                f"Expected a non-empty value for `federation_issuer_id` but received {federation_issuer_id!r}"
            )
        extra_headers = {
            **strip_not_given({"anthropic-beta": ",".join(str(e) for e in betas) if is_given(betas) else not_given}),
            **(extra_headers or {}),
        }
        return await self._post(
            path_template(
                "/v1/organizations/federation_issuers/{federation_issuer_id}?beta=true",
                federation_issuer_id=federation_issuer_id,
            ),
            body=await async_maybe_transform(
                {
                    "check_jti": check_jti,
                    "issuer_url": issuer_url,
                    "jwks": jwks,
                    "jwks_polling_disabled": jwks_polling_disabled,
                    "max_jwt_lifetime_seconds": max_jwt_lifetime_seconds,
                    "name": name,
                },
                issuer_update_params.IssuerUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BetaFederationIssuer,
        )

    def list(
        self,
        *,
        include_archived: bool | Omit = omit,
        limit: int | Omit = omit,
        page: Optional[str] | Omit = omit,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> AsyncPaginator[BetaFederationIssuer, AsyncPageCursor[BetaFederationIssuer]]:
        """
        **Requires an OAuth access token with the `org:admin` scope**, from
        `ant auth login --scope org:admin` or a workload identity federation rule; Admin
        API keys are not accepted. See
        [Manage WIF with the Admin API](/docs/en/manage-claude/wif-admin-api).

        List federation issuers in your organization.

        Archived issuers are excluded unless `include_archived=true`.

        Args:
          include_archived: Include archived resources. Defaults to false.

          limit: Number of results per page.

          page: Opaque cursor from a previous response's `next_page`.

          betas: Optional header to specify the beta version(s) you want to use.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {
            **strip_not_given({"anthropic-beta": ",".join(str(e) for e in betas) if is_given(betas) else not_given}),
            **(extra_headers or {}),
        }
        return self._get_api_list(
            "/v1/organizations/federation_issuers?beta=true",
            page=AsyncPageCursor[BetaFederationIssuer],
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
                    issuer_list_params.IssuerListParams,
                ),
            ),
            model=BetaFederationIssuer,
        )

    async def archive(
        self,
        federation_issuer_id: str,
        *,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaFederationIssuer:
        """
        **Requires an OAuth access token with the `org:admin` scope**, from
        `ant auth login --scope org:admin` or a workload identity federation rule; Admin
        API keys are not accepted. See
        [Manage WIF with the Admin API](/docs/en/manage-claude/wif-admin-api).

        Archive a federation issuer.

        Idempotent; re-archiving returns the issuer with its original `archived_at`.
        Rejected with 400 if any live (non-archived) federation rule still references
        the issuer; archive those rules first (a rule's issuer cannot be changed), or
        recreate them against another issuer.

        Args:
          federation_issuer_id: ID of the federation issuer to archive.

          betas: Optional header to specify the beta version(s) you want to use.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not federation_issuer_id:
            raise ValueError(
                f"Expected a non-empty value for `federation_issuer_id` but received {federation_issuer_id!r}"
            )
        extra_headers = {
            **strip_not_given({"anthropic-beta": ",".join(str(e) for e in betas) if is_given(betas) else not_given}),
            **(extra_headers or {}),
        }
        return await self._post(
            path_template(
                "/v1/organizations/federation_issuers/{federation_issuer_id}/archive?beta=true",
                federation_issuer_id=federation_issuer_id,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BetaFederationIssuer,
        )


class IssuersWithRawResponse:
    def __init__(self, issuers: Issuers) -> None:
        self._issuers = issuers

        self.create = to_raw_response_wrapper(
            issuers.create,
        )
        self.retrieve = to_raw_response_wrapper(
            issuers.retrieve,
        )
        self.update = to_raw_response_wrapper(
            issuers.update,
        )
        self.list = to_raw_response_wrapper(
            issuers.list,
        )
        self.archive = to_raw_response_wrapper(
            issuers.archive,
        )


class AsyncIssuersWithRawResponse:
    def __init__(self, issuers: AsyncIssuers) -> None:
        self._issuers = issuers

        self.create = async_to_raw_response_wrapper(
            issuers.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            issuers.retrieve,
        )
        self.update = async_to_raw_response_wrapper(
            issuers.update,
        )
        self.list = async_to_raw_response_wrapper(
            issuers.list,
        )
        self.archive = async_to_raw_response_wrapper(
            issuers.archive,
        )


class IssuersWithStreamingResponse:
    def __init__(self, issuers: Issuers) -> None:
        self._issuers = issuers

        self.create = to_streamed_response_wrapper(
            issuers.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            issuers.retrieve,
        )
        self.update = to_streamed_response_wrapper(
            issuers.update,
        )
        self.list = to_streamed_response_wrapper(
            issuers.list,
        )
        self.archive = to_streamed_response_wrapper(
            issuers.archive,
        )


class AsyncIssuersWithStreamingResponse:
    def __init__(self, issuers: AsyncIssuers) -> None:
        self._issuers = issuers

        self.create = async_to_streamed_response_wrapper(
            issuers.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            issuers.retrieve,
        )
        self.update = async_to_streamed_response_wrapper(
            issuers.update,
        )
        self.list = async_to_streamed_response_wrapper(
            issuers.list,
        )
        self.archive = async_to_streamed_response_wrapper(
            issuers.archive,
        )
