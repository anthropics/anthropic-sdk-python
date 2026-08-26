# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, List, Optional

import httpx2

from .workspaces import (
    Workspaces,
    AsyncWorkspaces,
    WorkspacesWithRawResponse,
    AsyncWorkspacesWithRawResponse,
    WorkspacesWithStreamingResponse,
    AsyncWorkspacesWithStreamingResponse,
)
from ......_types import Body, Omit, Query, Headers, NotGiven, omit, not_given
from ......_utils import is_given, path_template, maybe_transform, strip_not_given, async_maybe_transform
from ......_compat import cached_property
from ......_resource import SyncAPIResource, AsyncAPIResource
from ......_response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ......pagination import SyncPageCursor, AsyncPageCursor
from ......_base_client import AsyncPaginator, make_request_options
from ......types.anthropic_beta_param import AnthropicBetaParam
from ......types.beta.organization.federation import (
    rule_list_params,
    rule_create_params,
    rule_update_params,
)
from ......types.beta.organization.federation.beta_federation_rule import BetaFederationRule
from ......types.beta.organization.federation.beta_federation_rule_match_param import BetaFederationRuleMatchParam
from ......types.beta.organization.federation.beta_service_account_target_param import BetaServiceAccountTargetParam

__all__ = ["Rules", "AsyncRules"]


class Rules(SyncAPIResource):
    @cached_property
    def workspaces(self) -> Workspaces:
        return Workspaces(self._client)

    @cached_property
    def with_raw_response(self) -> RulesWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#accessing-raw-response-data-eg-headers
        """
        return RulesWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> RulesWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#with_streaming_response
        """
        return RulesWithStreamingResponse(self)

    def create(
        self,
        *,
        issuer_id: str,
        match: BetaFederationRuleMatchParam,
        name: str,
        oauth_scope: str,
        target: BetaServiceAccountTargetParam,
        applies_to_all_workspaces: bool | Omit = omit,
        attributes: Optional[Dict[str, str]] | Omit = omit,
        description: Optional[str] | Omit = omit,
        token_lifetime_seconds: int | Omit = omit,
        workspace_id: Optional[str] | Omit = omit,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaFederationRule:
        """
        **Requires an OAuth access token with the `org:admin` scope**, from
        `ant auth login --scope org:admin` or a workload identity federation rule; Admin
        API keys are not accepted. See
        [Manage WIF with the Admin API](/docs/en/manage-claude/wif-admin-api).

        Create a federation rule owned by your organization.

        The referenced issuer and the target service account must already exist in the
        same organization; invalid references are rejected with a 400 error. The
        workspace reference is validated. Membership is not checked at rule creation:
        token exchange resolves a single enabled workspace per call and is rejected
        unless the target service account is a member of that workspace (it is
        implicitly a member of the default workspace). Rules on well-known shared
        issuers (GitHub Actions, GitLab, Buildkite, Terraform Cloud, Google) must
        constrain tenant identity via an identity-bearing claim, a tenant-pinning
        subject prefix (such as `repo:YOUR_ORG/...`), or a CEL condition referencing one
        of those identity claims (e.g. `claims.repository_owner`). OAuth callers may
        only manage rules whose `oauth_scope` is `workspace:developer` or
        `workspace:inference`; other scopes require a Console session.

        Args:
          issuer_id: Tagged ID of the federation issuer.

          match: Conditions the verified JWT must satisfy for this rule to apply. At least one of
              `subject_prefix` (other than a wildcard-only value like `*`), `claims`, or
              `condition` is required; `audience` alone is not sufficient.

          name: Slug identifier (lowercase, digits, hyphens). Unique within the organization; a
              duplicate name returns 409.

          oauth_scope: Space-separated OAuth scopes. OAuth callers may only set `workspace:developer`
              or `workspace:inference`; other scopes (such as `org:admin`) require a Console
              session.

          target: Identity that tokens minted via this rule act as. Currently always a
              `service_account` target.

          applies_to_all_workspaces: When true, enable this rule for every workspace in the org (including workspaces
              created later).

          attributes: CEL expressions `{name: expr}` extracting named values from claims. Not yet
              supported; any non-empty value is rejected with 400.

          description: Optional free-text description.

          token_lifetime_seconds: Lifetime in seconds for access tokens minted via this rule (60-86400). Defaults
              to 3600 (1h). Minted tokens are capped at
              `max(60, min(this value, 2 × remaining assertion validity))` seconds.

          workspace_id: Tagged ID of the workspace to enable this rule for. Required unless
              `applies_to_all_workspaces` is true. Additional workspaces can be added via the
              `/federation_rules/{federation_rule_id}/workspaces` sub-resource.

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
            "/v1/organizations/federation_rules?beta=true",
            body=maybe_transform(
                {
                    "issuer_id": issuer_id,
                    "match": match,
                    "name": name,
                    "oauth_scope": oauth_scope,
                    "target": target,
                    "applies_to_all_workspaces": applies_to_all_workspaces,
                    "attributes": attributes,
                    "description": description,
                    "token_lifetime_seconds": token_lifetime_seconds,
                    "workspace_id": workspace_id,
                },
                rule_create_params.RuleCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BetaFederationRule,
        )

    def retrieve(
        self,
        federation_rule_id: str,
        *,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaFederationRule:
        """
        **Requires an OAuth access token with the `org:admin` scope**, from
        `ant auth login --scope org:admin` or a workload identity federation rule; Admin
        API keys are not accepted. See
        [Manage WIF with the Admin API](/docs/en/manage-claude/wif-admin-api).

        Retrieve a federation rule by its ID (`fdrl_...`).

        Args:
          federation_rule_id: ID of the federation rule.

          betas: Optional header to specify the beta version(s) you want to use.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not federation_rule_id:
            raise ValueError(f"Expected a non-empty value for `federation_rule_id` but received {federation_rule_id!r}")
        extra_headers = {
            **strip_not_given({"anthropic-beta": ",".join(str(e) for e in betas) if is_given(betas) else not_given}),
            **(extra_headers or {}),
        }
        return self._get(
            path_template(
                "/v1/organizations/federation_rules/{federation_rule_id}?beta=true",
                federation_rule_id=federation_rule_id,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BetaFederationRule,
        )

    def update(
        self,
        federation_rule_id: str,
        *,
        applies_to_all_workspaces: Optional[bool] | Omit = omit,
        attributes: Optional[Dict[str, str]] | Omit = omit,
        description: Optional[str] | Omit = omit,
        match: Optional[BetaFederationRuleMatchParam] | Omit = omit,
        name: Optional[str] | Omit = omit,
        oauth_scope: Optional[str] | Omit = omit,
        target: Optional[BetaServiceAccountTargetParam] | Omit = omit,
        token_lifetime_seconds: Optional[int] | Omit = omit,
        workspace_id: Optional[str] | Omit = omit,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaFederationRule:
        """
        **Requires an OAuth access token with the `org:admin` scope**, from
        `ant auth login --scope org:admin` or a workload identity federation rule; Admin
        API keys are not accepted. See
        [Manage WIF with the Admin API](/docs/en/manage-claude/wif-admin-api).

        Partially update a federation rule.

        `issuer_id` is immutable. `match` and `target` are replaced as whole objects
        when set. Referenced service accounts and workspaces must exist in your
        organization; invalid references are rejected with a 400 error. Archived rules
        cannot be updated; this returns 400. Create a new rule instead. Rules on
        well-known shared issuers (GitHub Actions, GitLab, Buildkite, Terraform Cloud,
        Google) must constrain tenant identity via an identity-bearing claim, a
        tenant-pinning subject prefix (such as `repo:YOUR_ORG/...`), or a CEL condition
        referencing one of those identity claims (e.g. `claims.repository_owner`). On
        these issuers the requirement is re-checked on every update; if an existing
        rule's stored match does not yet constrain tenant identity, any update (even a
        rename or description change) must also supply a conforming `match` in the same
        request. OAuth callers may only manage rules whose `oauth_scope` is
        `workspace:developer` or `workspace:inference`; other scopes require a Console
        session.

        Args:
          federation_rule_id: ID of the federation rule to update.

          applies_to_all_workspaces: When true, enables this rule for every workspace in the org (including
              workspaces created later). Setting `false` is rejected with 400 if no workspace
              would remain enabled; a rule with only a legacy `workspace_id` binding continues
              to mint.

          attributes: Replaces the CEL expressions `{name: expr}` extracting named values from claims.
              Send null to clear them. Not yet supported; any non-empty value is rejected
              with 400.

          description: Replaces the description. Omit to leave unchanged; send `null` to clear (the
              field is stored as an empty string).

          match: Does the incoming JWT qualify?

              All populated fields must pass; omitted fields are skipped. At least one of
              `subject_prefix` (other than a wildcard-only value like `*`), `claims`, or
              `condition` is required; `audience` alone is not sufficient.

          name: Replaces the slug identifier (lowercase, digits, hyphens). Unique within the
              organization; a duplicate name returns 409.

          oauth_scope: Replaces the space-separated OAuth scopes granted on minted tokens. OAuth
              callers may only set `workspace:developer` or `workspace:inference`; other
              scopes (such as `org:admin`) require a Console session.

          target: Bind to a fixed service account by ID.

          token_lifetime_seconds: Replaces the lifetime in seconds for access tokens minted via this rule
              (60-86400). Minted tokens are capped at
              `max(60, min(this value, 2 × remaining assertion validity))` seconds.

          workspace_id: Replaces the existing single workspace enablement (the previous one is removed).
              Rejected with 400 if the rule is enabled for more than one workspace; use the
              `/federation_rules/{federation_rule_id}/workspaces` sub-resource instead.

          betas: Optional header to specify the beta version(s) you want to use.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not federation_rule_id:
            raise ValueError(f"Expected a non-empty value for `federation_rule_id` but received {federation_rule_id!r}")
        extra_headers = {
            **strip_not_given({"anthropic-beta": ",".join(str(e) for e in betas) if is_given(betas) else not_given}),
            **(extra_headers or {}),
        }
        return self._post(
            path_template(
                "/v1/organizations/federation_rules/{federation_rule_id}?beta=true",
                federation_rule_id=federation_rule_id,
            ),
            body=maybe_transform(
                {
                    "applies_to_all_workspaces": applies_to_all_workspaces,
                    "attributes": attributes,
                    "description": description,
                    "match": match,
                    "name": name,
                    "oauth_scope": oauth_scope,
                    "target": target,
                    "token_lifetime_seconds": token_lifetime_seconds,
                    "workspace_id": workspace_id,
                },
                rule_update_params.RuleUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BetaFederationRule,
        )

    def list(
        self,
        *,
        include_archived: bool | Omit = omit,
        issuer_id: Optional[str] | Omit = omit,
        limit: int | Omit = omit,
        page: Optional[str] | Omit = omit,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> SyncPageCursor[BetaFederationRule]:
        """
        **Requires an OAuth access token with the `org:admin` scope**, from
        `ant auth login --scope org:admin` or a workload identity federation rule; Admin
        API keys are not accepted. See
        [Manage WIF with the Admin API](/docs/en/manage-claude/wif-admin-api).

        List federation rules in your organization.

        Optionally filter by issuer with `issuer_id`. Archived rules are excluded unless
        `include_archived=true`.

        Args:
          include_archived: Include archived resources. Defaults to false.

          issuer_id: Filter to rules referencing this federation issuer.

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
            "/v1/organizations/federation_rules?beta=true",
            page=SyncPageCursor[BetaFederationRule],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "include_archived": include_archived,
                        "issuer_id": issuer_id,
                        "limit": limit,
                        "page": page,
                    },
                    rule_list_params.RuleListParams,
                ),
            ),
            model=BetaFederationRule,
        )

    def archive(
        self,
        federation_rule_id: str,
        *,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaFederationRule:
        """
        **Requires an OAuth access token with the `org:admin` scope**, from
        `ant auth login --scope org:admin` or a workload identity federation rule; Admin
        API keys are not accepted. See
        [Manage WIF with the Admin API](/docs/en/manage-claude/wif-admin-api).

        Archive a federation rule.

        Token exchange through this rule stops immediately. Idempotent; re-archiving
        returns the rule with its original `archived_at`. Archiving clears the rule's
        workspace targeting (`workspace_id` and `workspace_ids` are emptied). Tokens
        already minted before archive remain valid until they expire. OAuth callers may
        only manage rules whose `oauth_scope` is `workspace:developer` or
        `workspace:inference`; other scopes require a Console session.

        Args:
          federation_rule_id: ID of the federation rule to archive.

          betas: Optional header to specify the beta version(s) you want to use.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not federation_rule_id:
            raise ValueError(f"Expected a non-empty value for `federation_rule_id` but received {federation_rule_id!r}")
        extra_headers = {
            **strip_not_given({"anthropic-beta": ",".join(str(e) for e in betas) if is_given(betas) else not_given}),
            **(extra_headers or {}),
        }
        return self._post(
            path_template(
                "/v1/organizations/federation_rules/{federation_rule_id}/archive?beta=true",
                federation_rule_id=federation_rule_id,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BetaFederationRule,
        )


class AsyncRules(AsyncAPIResource):
    @cached_property
    def workspaces(self) -> AsyncWorkspaces:
        return AsyncWorkspaces(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncRulesWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#accessing-raw-response-data-eg-headers
        """
        return AsyncRulesWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncRulesWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#with_streaming_response
        """
        return AsyncRulesWithStreamingResponse(self)

    async def create(
        self,
        *,
        issuer_id: str,
        match: BetaFederationRuleMatchParam,
        name: str,
        oauth_scope: str,
        target: BetaServiceAccountTargetParam,
        applies_to_all_workspaces: bool | Omit = omit,
        attributes: Optional[Dict[str, str]] | Omit = omit,
        description: Optional[str] | Omit = omit,
        token_lifetime_seconds: int | Omit = omit,
        workspace_id: Optional[str] | Omit = omit,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaFederationRule:
        """
        **Requires an OAuth access token with the `org:admin` scope**, from
        `ant auth login --scope org:admin` or a workload identity federation rule; Admin
        API keys are not accepted. See
        [Manage WIF with the Admin API](/docs/en/manage-claude/wif-admin-api).

        Create a federation rule owned by your organization.

        The referenced issuer and the target service account must already exist in the
        same organization; invalid references are rejected with a 400 error. The
        workspace reference is validated. Membership is not checked at rule creation:
        token exchange resolves a single enabled workspace per call and is rejected
        unless the target service account is a member of that workspace (it is
        implicitly a member of the default workspace). Rules on well-known shared
        issuers (GitHub Actions, GitLab, Buildkite, Terraform Cloud, Google) must
        constrain tenant identity via an identity-bearing claim, a tenant-pinning
        subject prefix (such as `repo:YOUR_ORG/...`), or a CEL condition referencing one
        of those identity claims (e.g. `claims.repository_owner`). OAuth callers may
        only manage rules whose `oauth_scope` is `workspace:developer` or
        `workspace:inference`; other scopes require a Console session.

        Args:
          issuer_id: Tagged ID of the federation issuer.

          match: Conditions the verified JWT must satisfy for this rule to apply. At least one of
              `subject_prefix` (other than a wildcard-only value like `*`), `claims`, or
              `condition` is required; `audience` alone is not sufficient.

          name: Slug identifier (lowercase, digits, hyphens). Unique within the organization; a
              duplicate name returns 409.

          oauth_scope: Space-separated OAuth scopes. OAuth callers may only set `workspace:developer`
              or `workspace:inference`; other scopes (such as `org:admin`) require a Console
              session.

          target: Identity that tokens minted via this rule act as. Currently always a
              `service_account` target.

          applies_to_all_workspaces: When true, enable this rule for every workspace in the org (including workspaces
              created later).

          attributes: CEL expressions `{name: expr}` extracting named values from claims. Not yet
              supported; any non-empty value is rejected with 400.

          description: Optional free-text description.

          token_lifetime_seconds: Lifetime in seconds for access tokens minted via this rule (60-86400). Defaults
              to 3600 (1h). Minted tokens are capped at
              `max(60, min(this value, 2 × remaining assertion validity))` seconds.

          workspace_id: Tagged ID of the workspace to enable this rule for. Required unless
              `applies_to_all_workspaces` is true. Additional workspaces can be added via the
              `/federation_rules/{federation_rule_id}/workspaces` sub-resource.

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
            "/v1/organizations/federation_rules?beta=true",
            body=await async_maybe_transform(
                {
                    "issuer_id": issuer_id,
                    "match": match,
                    "name": name,
                    "oauth_scope": oauth_scope,
                    "target": target,
                    "applies_to_all_workspaces": applies_to_all_workspaces,
                    "attributes": attributes,
                    "description": description,
                    "token_lifetime_seconds": token_lifetime_seconds,
                    "workspace_id": workspace_id,
                },
                rule_create_params.RuleCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BetaFederationRule,
        )

    async def retrieve(
        self,
        federation_rule_id: str,
        *,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaFederationRule:
        """
        **Requires an OAuth access token with the `org:admin` scope**, from
        `ant auth login --scope org:admin` or a workload identity federation rule; Admin
        API keys are not accepted. See
        [Manage WIF with the Admin API](/docs/en/manage-claude/wif-admin-api).

        Retrieve a federation rule by its ID (`fdrl_...`).

        Args:
          federation_rule_id: ID of the federation rule.

          betas: Optional header to specify the beta version(s) you want to use.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not federation_rule_id:
            raise ValueError(f"Expected a non-empty value for `federation_rule_id` but received {federation_rule_id!r}")
        extra_headers = {
            **strip_not_given({"anthropic-beta": ",".join(str(e) for e in betas) if is_given(betas) else not_given}),
            **(extra_headers or {}),
        }
        return await self._get(
            path_template(
                "/v1/organizations/federation_rules/{federation_rule_id}?beta=true",
                federation_rule_id=federation_rule_id,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BetaFederationRule,
        )

    async def update(
        self,
        federation_rule_id: str,
        *,
        applies_to_all_workspaces: Optional[bool] | Omit = omit,
        attributes: Optional[Dict[str, str]] | Omit = omit,
        description: Optional[str] | Omit = omit,
        match: Optional[BetaFederationRuleMatchParam] | Omit = omit,
        name: Optional[str] | Omit = omit,
        oauth_scope: Optional[str] | Omit = omit,
        target: Optional[BetaServiceAccountTargetParam] | Omit = omit,
        token_lifetime_seconds: Optional[int] | Omit = omit,
        workspace_id: Optional[str] | Omit = omit,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaFederationRule:
        """
        **Requires an OAuth access token with the `org:admin` scope**, from
        `ant auth login --scope org:admin` or a workload identity federation rule; Admin
        API keys are not accepted. See
        [Manage WIF with the Admin API](/docs/en/manage-claude/wif-admin-api).

        Partially update a federation rule.

        `issuer_id` is immutable. `match` and `target` are replaced as whole objects
        when set. Referenced service accounts and workspaces must exist in your
        organization; invalid references are rejected with a 400 error. Archived rules
        cannot be updated; this returns 400. Create a new rule instead. Rules on
        well-known shared issuers (GitHub Actions, GitLab, Buildkite, Terraform Cloud,
        Google) must constrain tenant identity via an identity-bearing claim, a
        tenant-pinning subject prefix (such as `repo:YOUR_ORG/...`), or a CEL condition
        referencing one of those identity claims (e.g. `claims.repository_owner`). On
        these issuers the requirement is re-checked on every update; if an existing
        rule's stored match does not yet constrain tenant identity, any update (even a
        rename or description change) must also supply a conforming `match` in the same
        request. OAuth callers may only manage rules whose `oauth_scope` is
        `workspace:developer` or `workspace:inference`; other scopes require a Console
        session.

        Args:
          federation_rule_id: ID of the federation rule to update.

          applies_to_all_workspaces: When true, enables this rule for every workspace in the org (including
              workspaces created later). Setting `false` is rejected with 400 if no workspace
              would remain enabled; a rule with only a legacy `workspace_id` binding continues
              to mint.

          attributes: Replaces the CEL expressions `{name: expr}` extracting named values from claims.
              Send null to clear them. Not yet supported; any non-empty value is rejected
              with 400.

          description: Replaces the description. Omit to leave unchanged; send `null` to clear (the
              field is stored as an empty string).

          match: Does the incoming JWT qualify?

              All populated fields must pass; omitted fields are skipped. At least one of
              `subject_prefix` (other than a wildcard-only value like `*`), `claims`, or
              `condition` is required; `audience` alone is not sufficient.

          name: Replaces the slug identifier (lowercase, digits, hyphens). Unique within the
              organization; a duplicate name returns 409.

          oauth_scope: Replaces the space-separated OAuth scopes granted on minted tokens. OAuth
              callers may only set `workspace:developer` or `workspace:inference`; other
              scopes (such as `org:admin`) require a Console session.

          target: Bind to a fixed service account by ID.

          token_lifetime_seconds: Replaces the lifetime in seconds for access tokens minted via this rule
              (60-86400). Minted tokens are capped at
              `max(60, min(this value, 2 × remaining assertion validity))` seconds.

          workspace_id: Replaces the existing single workspace enablement (the previous one is removed).
              Rejected with 400 if the rule is enabled for more than one workspace; use the
              `/federation_rules/{federation_rule_id}/workspaces` sub-resource instead.

          betas: Optional header to specify the beta version(s) you want to use.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not federation_rule_id:
            raise ValueError(f"Expected a non-empty value for `federation_rule_id` but received {federation_rule_id!r}")
        extra_headers = {
            **strip_not_given({"anthropic-beta": ",".join(str(e) for e in betas) if is_given(betas) else not_given}),
            **(extra_headers or {}),
        }
        return await self._post(
            path_template(
                "/v1/organizations/federation_rules/{federation_rule_id}?beta=true",
                federation_rule_id=federation_rule_id,
            ),
            body=await async_maybe_transform(
                {
                    "applies_to_all_workspaces": applies_to_all_workspaces,
                    "attributes": attributes,
                    "description": description,
                    "match": match,
                    "name": name,
                    "oauth_scope": oauth_scope,
                    "target": target,
                    "token_lifetime_seconds": token_lifetime_seconds,
                    "workspace_id": workspace_id,
                },
                rule_update_params.RuleUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BetaFederationRule,
        )

    def list(
        self,
        *,
        include_archived: bool | Omit = omit,
        issuer_id: Optional[str] | Omit = omit,
        limit: int | Omit = omit,
        page: Optional[str] | Omit = omit,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> AsyncPaginator[BetaFederationRule, AsyncPageCursor[BetaFederationRule]]:
        """
        **Requires an OAuth access token with the `org:admin` scope**, from
        `ant auth login --scope org:admin` or a workload identity federation rule; Admin
        API keys are not accepted. See
        [Manage WIF with the Admin API](/docs/en/manage-claude/wif-admin-api).

        List federation rules in your organization.

        Optionally filter by issuer with `issuer_id`. Archived rules are excluded unless
        `include_archived=true`.

        Args:
          include_archived: Include archived resources. Defaults to false.

          issuer_id: Filter to rules referencing this federation issuer.

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
            "/v1/organizations/federation_rules?beta=true",
            page=AsyncPageCursor[BetaFederationRule],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "include_archived": include_archived,
                        "issuer_id": issuer_id,
                        "limit": limit,
                        "page": page,
                    },
                    rule_list_params.RuleListParams,
                ),
            ),
            model=BetaFederationRule,
        )

    async def archive(
        self,
        federation_rule_id: str,
        *,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaFederationRule:
        """
        **Requires an OAuth access token with the `org:admin` scope**, from
        `ant auth login --scope org:admin` or a workload identity federation rule; Admin
        API keys are not accepted. See
        [Manage WIF with the Admin API](/docs/en/manage-claude/wif-admin-api).

        Archive a federation rule.

        Token exchange through this rule stops immediately. Idempotent; re-archiving
        returns the rule with its original `archived_at`. Archiving clears the rule's
        workspace targeting (`workspace_id` and `workspace_ids` are emptied). Tokens
        already minted before archive remain valid until they expire. OAuth callers may
        only manage rules whose `oauth_scope` is `workspace:developer` or
        `workspace:inference`; other scopes require a Console session.

        Args:
          federation_rule_id: ID of the federation rule to archive.

          betas: Optional header to specify the beta version(s) you want to use.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not federation_rule_id:
            raise ValueError(f"Expected a non-empty value for `federation_rule_id` but received {federation_rule_id!r}")
        extra_headers = {
            **strip_not_given({"anthropic-beta": ",".join(str(e) for e in betas) if is_given(betas) else not_given}),
            **(extra_headers or {}),
        }
        return await self._post(
            path_template(
                "/v1/organizations/federation_rules/{federation_rule_id}/archive?beta=true",
                federation_rule_id=federation_rule_id,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BetaFederationRule,
        )


class RulesWithRawResponse:
    def __init__(self, rules: Rules) -> None:
        self._rules = rules

        self.create = to_raw_response_wrapper(
            rules.create,
        )
        self.retrieve = to_raw_response_wrapper(
            rules.retrieve,
        )
        self.update = to_raw_response_wrapper(
            rules.update,
        )
        self.list = to_raw_response_wrapper(
            rules.list,
        )
        self.archive = to_raw_response_wrapper(
            rules.archive,
        )

    @cached_property
    def workspaces(self) -> WorkspacesWithRawResponse:
        return WorkspacesWithRawResponse(self._rules.workspaces)


class AsyncRulesWithRawResponse:
    def __init__(self, rules: AsyncRules) -> None:
        self._rules = rules

        self.create = async_to_raw_response_wrapper(
            rules.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            rules.retrieve,
        )
        self.update = async_to_raw_response_wrapper(
            rules.update,
        )
        self.list = async_to_raw_response_wrapper(
            rules.list,
        )
        self.archive = async_to_raw_response_wrapper(
            rules.archive,
        )

    @cached_property
    def workspaces(self) -> AsyncWorkspacesWithRawResponse:
        return AsyncWorkspacesWithRawResponse(self._rules.workspaces)


class RulesWithStreamingResponse:
    def __init__(self, rules: Rules) -> None:
        self._rules = rules

        self.create = to_streamed_response_wrapper(
            rules.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            rules.retrieve,
        )
        self.update = to_streamed_response_wrapper(
            rules.update,
        )
        self.list = to_streamed_response_wrapper(
            rules.list,
        )
        self.archive = to_streamed_response_wrapper(
            rules.archive,
        )

    @cached_property
    def workspaces(self) -> WorkspacesWithStreamingResponse:
        return WorkspacesWithStreamingResponse(self._rules.workspaces)


class AsyncRulesWithStreamingResponse:
    def __init__(self, rules: AsyncRules) -> None:
        self._rules = rules

        self.create = async_to_streamed_response_wrapper(
            rules.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            rules.retrieve,
        )
        self.update = async_to_streamed_response_wrapper(
            rules.update,
        )
        self.list = async_to_streamed_response_wrapper(
            rules.list,
        )
        self.archive = async_to_streamed_response_wrapper(
            rules.archive,
        )

    @cached_property
    def workspaces(self) -> AsyncWorkspacesWithStreamingResponse:
        return AsyncWorkspacesWithStreamingResponse(self._rules.workspaces)
