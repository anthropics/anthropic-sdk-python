from __future__ import annotations

from typing import List, Mapping, Optional, cast
from itertools import chain
from typing_extensions import Literal

import httpx2

from ...._files import deepcopy_with_paths
from ...._types import Body, Omit, Query, Headers, NotGiven, FileTypes, omit, not_given
from ...._utils import is_given, extract_files, path_template, strip_not_given
from ...._compat import cached_property
from ...._resource import SyncAPIResource, AsyncAPIResource
from ...._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ....pagination import SyncPageCursor, AsyncPageCursor
from ...._base_client import AsyncPaginator, make_request_options
from ....types.anthropic_beta_param import AnthropicBetaParam
from ....types.beta.organization.beta_plugin_marketplace import BetaPluginMarketplace
from ....types.beta.organization.beta_plugin_marketplace_validation_report import BetaPluginMarketplaceValidationReport

__all__ = ["PluginMarketplaces", "AsyncPluginMarketplaces"]


class PluginMarketplaces(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> PluginMarketplacesWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#accessing-raw-response-data-eg-headers
        """
        return PluginMarketplacesWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> PluginMarketplacesWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#with_streaming_response
        """
        return PluginMarketplacesWithStreamingResponse(self)

    def retrieve(
        self,
        marketplace_id: str,
        *,
        organization_id: Optional[str] | Omit = omit,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaPluginMarketplace:
        """
        Retrieve a plugin marketplace by ID.

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
          marketplace_id: ID of the plugin marketplace (prefixed `marketplace_`).

          organization_id: For a `read:org_audit` or `read:compliance_org_data` key created for all of a
              parent organization's linked organizations: a child organization of that parent
              to read instead of the organization the key was created in, given as the
              organization's UUID or its `org_`-prefixed ID. A value that is neither returns a
              400; an organization that is not a child of the key's parent, or where the
              Plugins API is not available, returns a 404. Any other key may pass only its own
              organization's ID here; another organization returns a 404.

          betas: This endpoint is in beta: requests must send `ce-plugins-2026-09-01` in this
              header.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not marketplace_id:
            raise ValueError(f"Expected a non-empty value for `marketplace_id` but received {marketplace_id!r}")
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
        return self._get(
            path_template(
                "/v1/organizations/plugin_marketplaces/{marketplace_id}?beta=true", marketplace_id=marketplace_id
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query={"organization_id": organization_id},
            ),
            cast_to=BetaPluginMarketplace,
        )

    def update(
        self,
        marketplace_id: str,
        *,
        default_installation_preference: Literal["auto_install", "available", "not_available", "required"],
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaPluginMarketplace:
        """
        Set the default installation setting of one of the organization's own plugin
        marketplaces. Every Plugin in it without a setting of its own gets this default
        as its organization-wide setting, including Plugins added later.

        Pass it as `default_installation_preference`. A member's personal marketplace
        cannot be updated here (403).

        **Accepted credentials:** an Admin API key with the `write:plugins` scope.

        Every request must include the beta header
        `anthropic-beta: ce-plugins-2026-09-01`. A request without it returns `404`,
        exactly as if the endpoint did not exist. The Plugins API is in beta and is
        available to Claude Enterprise organizations only. It is not available to Claude
        Platform (Claude Console) organizations, or to organizations with HIPAA
        readiness enabled.

        Args:
          marketplace_id: ID of the plugin marketplace (prefixed `marketplace_`).

          default_installation_preference: The organization-wide installation setting every Plugin in the marketplace
              without one of its own gets: one of `required`, `auto_install`, `available`,
              `not_available`. Once set it can be changed but not removed.

          betas: This endpoint is in beta: requests must send `ce-plugins-2026-09-01` in this
              header.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not marketplace_id:
            raise ValueError(f"Expected a non-empty value for `marketplace_id` but received {marketplace_id!r}")
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
        return self._post(
            path_template(
                "/v1/organizations/plugin_marketplaces/{marketplace_id}?beta=true", marketplace_id=marketplace_id
            ),
            body={"default_installation_preference": default_installation_preference},
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
            ),
            cast_to=BetaPluginMarketplace,
        )

    def list(
        self,
        *,
        limit: int | Omit = omit,
        organization_id: Optional[str] | Omit = omit,
        owner_type: Optional[Literal["organization", "user"]] | Omit = omit,
        page: Optional[str] | Omit = omit,
        source: Optional[Literal["directory", "github", "gitlab", "manual", "public_git"]] | Omit = omit,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> SyncPageCursor[BetaPluginMarketplace]:
        """
        List the plugin marketplaces Plugins live in, newest first: the organization's
        own and its members' personal ones.

        Plugin marketplaces are created, connected to a repository and deleted in
        claude.ai, not through this API. The organization's library marketplace, the
        organization-owned `manual` marketplace that uploads go to when no marketplace
        is named, is created the first time something is put in it and is listed from
        then on.

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
          limit: Number of items to return per page.

              Defaults to `20`. Ranges from `1` to `1000`.

          organization_id: For a `read:org_audit` or `read:compliance_org_data` key created for all of a
              parent organization's linked organizations: a child organization of that parent
              to read instead of the organization the key was created in, given as the
              organization's UUID or its `org_`-prefixed ID. A value that is neither returns a
              400; an organization that is not a child of the key's parent, or where the
              Plugins API is not available, returns a 404. Any other key may pass only its own
              organization's ID here; another organization returns a 404.

          owner_type: `organization` for the organization's plugin marketplaces, `user` for members'
              personal plugin marketplaces.

          page: Optionally set to the `next_page` token from the previous response.

          source: Only plugin marketplaces with this `source`: `manual` for those whose Plugins
              are uploaded; `github`, `gitlab` or `public_git` for those synchronized from a
              Git repository. `directory` (Anthropic's catalog) is never listed here.

          betas: This endpoint is in beta: requests must send `ce-plugins-2026-09-01` in this
              header.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
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
            "/v1/organizations/plugin_marketplaces?beta=true",
            page=SyncPageCursor[BetaPluginMarketplace],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query={
                    "limit": limit,
                    "organization_id": organization_id,
                    "owner_type": owner_type,
                    "page": page,
                    "source": source,
                },
            ),
            model=BetaPluginMarketplace,
        )

    def validate_archive(
        self,
        *,
        archive: FileTypes,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaPluginMarketplaceValidationReport:
        """
        Check whether a plugin marketplace, uploaded as a `.zip` of the marketplace
        directory, would synchronize into claude.ai, without connecting or storing it.

        To check a public GitHub repository instead, use Validate Plugin Marketplace
        Repository.

        The report says whether `marketplace.json` is well-formed, which plugins a
        synchronization would skip and why, and which plugins would synchronize only in
        part, with some files left out. An archive that cannot be read as a marketplace
        is reported, not refused: the response is a report with `valid: false`. Plugin
        sources outside the marketplace are fetched anonymously from GitHub, so a
        private one is reported as not found; a source on any other host is not fetched
        here, and the report notes that it will be checked when the marketplace actually
        synchronizes.

        Nothing is recorded on the Compliance API activity feed.

        For a worked example, see
        [Validate marketplace content](/docs/en/manage-claude/plugins-api#validate-marketplace-content)
        in the Plugins API guide.

        **Accepted credentials:** an Admin API key with the `read:plugins` or
        `write:plugins` scope; `read:org_audit` and `read:compliance_org_data` do not
        grant it.

        Every request must include the beta header
        `anthropic-beta: ce-plugins-2026-09-01`. A request without it returns `404`,
        exactly as if the endpoint did not exist. The Plugins API is in beta and is
        available to Claude Enterprise organizations only. It is not available to Claude
        Platform (Claude Console) organizations, or to organizations with HIPAA
        readiness enabled.

        Args:
          archive: A .zip of the marketplace directory (its contents at the root, or wrapped in one
              folder as a Git host's download produces), sent as a file part with a filename;
              DEFLATE- or STORE-compressed, at most 32 MB. A part sent without a filename, a
              second archive part, or any other form field is a 400; a larger archive is
              a 413.

          betas: This endpoint is in beta: requests must send `ce-plugins-2026-09-01` in this
              header.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
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
        body = deepcopy_with_paths({"archive": archive}, [["archive"]])
        files = extract_files(cast(Mapping[str, object], body), paths=[["archive"]])
        # It should be noted that the actual Content-Type header that will be
        # sent to the server will contain a `boundary` parameter, e.g.
        # multipart/form-data; boundary=---abc--
        extra_headers["Content-Type"] = "multipart/form-data"
        return self._post(
            "/v1/organizations/plugin_marketplaces/validate_archive?beta=true",
            body=body,
            files=files,
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
            ),
            cast_to=BetaPluginMarketplaceValidationReport,
        )

    def validate_repository(
        self,
        *,
        repository_url: str,
        ref: Optional[str] | Omit = omit,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaPluginMarketplaceValidationReport:
        """
        Check whether a plugin marketplace held in a public GitHub repository would
        synchronize into claude.ai, without connecting or storing it.

        To check a `.zip` of the marketplace directory instead, use Validate Plugin
        Marketplace Archive.

        The report says whether `marketplace.json` is well-formed, which plugins a
        synchronization would skip and why, and which plugins would synchronize only in
        part, with some files left out. A repository that is missing, private, or has no
        such branch or commit is reported, not refused: the response is a report with
        `valid: false`. Plugin sources outside the marketplace are fetched anonymously
        from GitHub, so a private one is reported as not found; a source on any other
        host is not fetched here, and the report notes that it will be checked when the
        marketplace actually synchronizes.

        Nothing is recorded on the Compliance API activity feed.

        For a worked example, see
        [Validate marketplace content](/docs/en/manage-claude/plugins-api#validate-marketplace-content)
        in the Plugins API guide.

        **Accepted credentials:** an Admin API key with the `read:plugins` or
        `write:plugins` scope; `read:org_audit` and `read:compliance_org_data` do not
        grant it.

        Every request must include the beta header
        `anthropic-beta: ce-plugins-2026-09-01`. A request without it returns `404`,
        exactly as if the endpoint did not exist. The Plugins API is in beta and is
        available to Claude Enterprise organizations only. It is not available to Claude
        Platform (Claude Console) organizations, or to organizations with HIPAA
        readiness enabled.

        Args:
          repository_url: The `https://` URL of a public repository on github.com that holds the
              marketplace. Any other host, a URL with credentials in it, or one that does not
              name a repository is a 400.

          ref: The branch to validate the tip of, or the full 40-character SHA of the commit to
              validate. When omitted, the branch a synchronization would read (usually the
              repository's default branch); if that is not the default branch, the report's
              `ref` says which branch was read. An empty string, or a value that is neither a
              branch name nor a 40-character SHA, is a 400.

          betas: This endpoint is in beta: requests must send `ce-plugins-2026-09-01` in this
              header.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
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
        return self._post(
            "/v1/organizations/plugin_marketplaces/validate_repository?beta=true",
            body={
                "repository_url": repository_url,
                "ref": ref,
            },
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
            ),
            cast_to=BetaPluginMarketplaceValidationReport,
        )


class AsyncPluginMarketplaces(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncPluginMarketplacesWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#accessing-raw-response-data-eg-headers
        """
        return AsyncPluginMarketplacesWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncPluginMarketplacesWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#with_streaming_response
        """
        return AsyncPluginMarketplacesWithStreamingResponse(self)

    async def retrieve(
        self,
        marketplace_id: str,
        *,
        organization_id: Optional[str] | Omit = omit,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaPluginMarketplace:
        """
        Retrieve a plugin marketplace by ID.

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
          marketplace_id: ID of the plugin marketplace (prefixed `marketplace_`).

          organization_id: For a `read:org_audit` or `read:compliance_org_data` key created for all of a
              parent organization's linked organizations: a child organization of that parent
              to read instead of the organization the key was created in, given as the
              organization's UUID or its `org_`-prefixed ID. A value that is neither returns a
              400; an organization that is not a child of the key's parent, or where the
              Plugins API is not available, returns a 404. Any other key may pass only its own
              organization's ID here; another organization returns a 404.

          betas: This endpoint is in beta: requests must send `ce-plugins-2026-09-01` in this
              header.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not marketplace_id:
            raise ValueError(f"Expected a non-empty value for `marketplace_id` but received {marketplace_id!r}")
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
        return await self._get(
            path_template(
                "/v1/organizations/plugin_marketplaces/{marketplace_id}?beta=true", marketplace_id=marketplace_id
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query={"organization_id": organization_id},
            ),
            cast_to=BetaPluginMarketplace,
        )

    async def update(
        self,
        marketplace_id: str,
        *,
        default_installation_preference: Literal["auto_install", "available", "not_available", "required"],
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaPluginMarketplace:
        """
        Set the default installation setting of one of the organization's own plugin
        marketplaces. Every Plugin in it without a setting of its own gets this default
        as its organization-wide setting, including Plugins added later.

        Pass it as `default_installation_preference`. A member's personal marketplace
        cannot be updated here (403).

        **Accepted credentials:** an Admin API key with the `write:plugins` scope.

        Every request must include the beta header
        `anthropic-beta: ce-plugins-2026-09-01`. A request without it returns `404`,
        exactly as if the endpoint did not exist. The Plugins API is in beta and is
        available to Claude Enterprise organizations only. It is not available to Claude
        Platform (Claude Console) organizations, or to organizations with HIPAA
        readiness enabled.

        Args:
          marketplace_id: ID of the plugin marketplace (prefixed `marketplace_`).

          default_installation_preference: The organization-wide installation setting every Plugin in the marketplace
              without one of its own gets: one of `required`, `auto_install`, `available`,
              `not_available`. Once set it can be changed but not removed.

          betas: This endpoint is in beta: requests must send `ce-plugins-2026-09-01` in this
              header.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not marketplace_id:
            raise ValueError(f"Expected a non-empty value for `marketplace_id` but received {marketplace_id!r}")
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
        return await self._post(
            path_template(
                "/v1/organizations/plugin_marketplaces/{marketplace_id}?beta=true", marketplace_id=marketplace_id
            ),
            body={"default_installation_preference": default_installation_preference},
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
            ),
            cast_to=BetaPluginMarketplace,
        )

    def list(
        self,
        *,
        limit: int | Omit = omit,
        organization_id: Optional[str] | Omit = omit,
        owner_type: Optional[Literal["organization", "user"]] | Omit = omit,
        page: Optional[str] | Omit = omit,
        source: Optional[Literal["directory", "github", "gitlab", "manual", "public_git"]] | Omit = omit,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> AsyncPaginator[BetaPluginMarketplace, AsyncPageCursor[BetaPluginMarketplace]]:
        """
        List the plugin marketplaces Plugins live in, newest first: the organization's
        own and its members' personal ones.

        Plugin marketplaces are created, connected to a repository and deleted in
        claude.ai, not through this API. The organization's library marketplace, the
        organization-owned `manual` marketplace that uploads go to when no marketplace
        is named, is created the first time something is put in it and is listed from
        then on.

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
          limit: Number of items to return per page.

              Defaults to `20`. Ranges from `1` to `1000`.

          organization_id: For a `read:org_audit` or `read:compliance_org_data` key created for all of a
              parent organization's linked organizations: a child organization of that parent
              to read instead of the organization the key was created in, given as the
              organization's UUID or its `org_`-prefixed ID. A value that is neither returns a
              400; an organization that is not a child of the key's parent, or where the
              Plugins API is not available, returns a 404. Any other key may pass only its own
              organization's ID here; another organization returns a 404.

          owner_type: `organization` for the organization's plugin marketplaces, `user` for members'
              personal plugin marketplaces.

          page: Optionally set to the `next_page` token from the previous response.

          source: Only plugin marketplaces with this `source`: `manual` for those whose Plugins
              are uploaded; `github`, `gitlab` or `public_git` for those synchronized from a
              Git repository. `directory` (Anthropic's catalog) is never listed here.

          betas: This endpoint is in beta: requests must send `ce-plugins-2026-09-01` in this
              header.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
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
            "/v1/organizations/plugin_marketplaces?beta=true",
            page=AsyncPageCursor[BetaPluginMarketplace],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query={
                    "limit": limit,
                    "organization_id": organization_id,
                    "owner_type": owner_type,
                    "page": page,
                    "source": source,
                },
            ),
            model=BetaPluginMarketplace,
        )

    async def validate_archive(
        self,
        *,
        archive: FileTypes,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaPluginMarketplaceValidationReport:
        """
        Check whether a plugin marketplace, uploaded as a `.zip` of the marketplace
        directory, would synchronize into claude.ai, without connecting or storing it.

        To check a public GitHub repository instead, use Validate Plugin Marketplace
        Repository.

        The report says whether `marketplace.json` is well-formed, which plugins a
        synchronization would skip and why, and which plugins would synchronize only in
        part, with some files left out. An archive that cannot be read as a marketplace
        is reported, not refused: the response is a report with `valid: false`. Plugin
        sources outside the marketplace are fetched anonymously from GitHub, so a
        private one is reported as not found; a source on any other host is not fetched
        here, and the report notes that it will be checked when the marketplace actually
        synchronizes.

        Nothing is recorded on the Compliance API activity feed.

        For a worked example, see
        [Validate marketplace content](/docs/en/manage-claude/plugins-api#validate-marketplace-content)
        in the Plugins API guide.

        **Accepted credentials:** an Admin API key with the `read:plugins` or
        `write:plugins` scope; `read:org_audit` and `read:compliance_org_data` do not
        grant it.

        Every request must include the beta header
        `anthropic-beta: ce-plugins-2026-09-01`. A request without it returns `404`,
        exactly as if the endpoint did not exist. The Plugins API is in beta and is
        available to Claude Enterprise organizations only. It is not available to Claude
        Platform (Claude Console) organizations, or to organizations with HIPAA
        readiness enabled.

        Args:
          archive: A .zip of the marketplace directory (its contents at the root, or wrapped in one
              folder as a Git host's download produces), sent as a file part with a filename;
              DEFLATE- or STORE-compressed, at most 32 MB. A part sent without a filename, a
              second archive part, or any other form field is a 400; a larger archive is
              a 413.

          betas: This endpoint is in beta: requests must send `ce-plugins-2026-09-01` in this
              header.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
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
        body = deepcopy_with_paths({"archive": archive}, [["archive"]])
        files = extract_files(cast(Mapping[str, object], body), paths=[["archive"]])
        # It should be noted that the actual Content-Type header that will be
        # sent to the server will contain a `boundary` parameter, e.g.
        # multipart/form-data; boundary=---abc--
        extra_headers["Content-Type"] = "multipart/form-data"
        return await self._post(
            "/v1/organizations/plugin_marketplaces/validate_archive?beta=true",
            body=body,
            files=files,
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
            ),
            cast_to=BetaPluginMarketplaceValidationReport,
        )

    async def validate_repository(
        self,
        *,
        repository_url: str,
        ref: Optional[str] | Omit = omit,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaPluginMarketplaceValidationReport:
        """
        Check whether a plugin marketplace held in a public GitHub repository would
        synchronize into claude.ai, without connecting or storing it.

        To check a `.zip` of the marketplace directory instead, use Validate Plugin
        Marketplace Archive.

        The report says whether `marketplace.json` is well-formed, which plugins a
        synchronization would skip and why, and which plugins would synchronize only in
        part, with some files left out. A repository that is missing, private, or has no
        such branch or commit is reported, not refused: the response is a report with
        `valid: false`. Plugin sources outside the marketplace are fetched anonymously
        from GitHub, so a private one is reported as not found; a source on any other
        host is not fetched here, and the report notes that it will be checked when the
        marketplace actually synchronizes.

        Nothing is recorded on the Compliance API activity feed.

        For a worked example, see
        [Validate marketplace content](/docs/en/manage-claude/plugins-api#validate-marketplace-content)
        in the Plugins API guide.

        **Accepted credentials:** an Admin API key with the `read:plugins` or
        `write:plugins` scope; `read:org_audit` and `read:compliance_org_data` do not
        grant it.

        Every request must include the beta header
        `anthropic-beta: ce-plugins-2026-09-01`. A request without it returns `404`,
        exactly as if the endpoint did not exist. The Plugins API is in beta and is
        available to Claude Enterprise organizations only. It is not available to Claude
        Platform (Claude Console) organizations, or to organizations with HIPAA
        readiness enabled.

        Args:
          repository_url: The `https://` URL of a public repository on github.com that holds the
              marketplace. Any other host, a URL with credentials in it, or one that does not
              name a repository is a 400.

          ref: The branch to validate the tip of, or the full 40-character SHA of the commit to
              validate. When omitted, the branch a synchronization would read (usually the
              repository's default branch); if that is not the default branch, the report's
              `ref` says which branch was read. An empty string, or a value that is neither a
              branch name nor a 40-character SHA, is a 400.

          betas: This endpoint is in beta: requests must send `ce-plugins-2026-09-01` in this
              header.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
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
        return await self._post(
            "/v1/organizations/plugin_marketplaces/validate_repository?beta=true",
            body={
                "repository_url": repository_url,
                "ref": ref,
            },
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
            ),
            cast_to=BetaPluginMarketplaceValidationReport,
        )


class PluginMarketplacesWithRawResponse:
    def __init__(self, plugin_marketplaces: PluginMarketplaces) -> None:
        self._plugin_marketplaces = plugin_marketplaces

        self.retrieve = to_raw_response_wrapper(
            plugin_marketplaces.retrieve,
        )
        self.update = to_raw_response_wrapper(
            plugin_marketplaces.update,
        )
        self.list = to_raw_response_wrapper(
            plugin_marketplaces.list,
        )
        self.validate_archive = to_raw_response_wrapper(
            plugin_marketplaces.validate_archive,
        )
        self.validate_repository = to_raw_response_wrapper(
            plugin_marketplaces.validate_repository,
        )


class AsyncPluginMarketplacesWithRawResponse:
    def __init__(self, plugin_marketplaces: AsyncPluginMarketplaces) -> None:
        self._plugin_marketplaces = plugin_marketplaces

        self.retrieve = async_to_raw_response_wrapper(
            plugin_marketplaces.retrieve,
        )
        self.update = async_to_raw_response_wrapper(
            plugin_marketplaces.update,
        )
        self.list = async_to_raw_response_wrapper(
            plugin_marketplaces.list,
        )
        self.validate_archive = async_to_raw_response_wrapper(
            plugin_marketplaces.validate_archive,
        )
        self.validate_repository = async_to_raw_response_wrapper(
            plugin_marketplaces.validate_repository,
        )


class PluginMarketplacesWithStreamingResponse:
    def __init__(self, plugin_marketplaces: PluginMarketplaces) -> None:
        self._plugin_marketplaces = plugin_marketplaces

        self.retrieve = to_streamed_response_wrapper(
            plugin_marketplaces.retrieve,
        )
        self.update = to_streamed_response_wrapper(
            plugin_marketplaces.update,
        )
        self.list = to_streamed_response_wrapper(
            plugin_marketplaces.list,
        )
        self.validate_archive = to_streamed_response_wrapper(
            plugin_marketplaces.validate_archive,
        )
        self.validate_repository = to_streamed_response_wrapper(
            plugin_marketplaces.validate_repository,
        )


class AsyncPluginMarketplacesWithStreamingResponse:
    def __init__(self, plugin_marketplaces: AsyncPluginMarketplaces) -> None:
        self._plugin_marketplaces = plugin_marketplaces

        self.retrieve = async_to_streamed_response_wrapper(
            plugin_marketplaces.retrieve,
        )
        self.update = async_to_streamed_response_wrapper(
            plugin_marketplaces.update,
        )
        self.list = async_to_streamed_response_wrapper(
            plugin_marketplaces.list,
        )
        self.validate_archive = async_to_streamed_response_wrapper(
            plugin_marketplaces.validate_archive,
        )
        self.validate_repository = async_to_streamed_response_wrapper(
            plugin_marketplaces.validate_repository,
        )
