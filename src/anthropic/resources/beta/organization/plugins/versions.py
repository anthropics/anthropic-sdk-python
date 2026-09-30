from __future__ import annotations

from typing import List, Mapping, Optional, cast
from itertools import chain

import httpx2

from ....._files import deepcopy_with_paths
from ....._types import (
    Body,
    Omit,
    Query,
    Headers,
    NotGiven,
    FileTypes,
    SequenceNotStr,
    omit,
    not_given,
)
from ....._utils import is_given, extract_files, path_template, strip_not_given
from ....._compat import cached_property
from ....._resource import SyncAPIResource, AsyncAPIResource
from ....._response import (
    BinaryAPIResponse,
    AsyncBinaryAPIResponse,
    StreamedBinaryAPIResponse,
    AsyncStreamedBinaryAPIResponse,
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    to_custom_raw_response_wrapper,
    async_to_streamed_response_wrapper,
    to_custom_streamed_response_wrapper,
    async_to_custom_raw_response_wrapper,
    async_to_custom_streamed_response_wrapper,
)
from .....pagination import SyncPageCursor, AsyncPageCursor
from ....._base_client import AsyncPaginator, make_request_options
from .....types.anthropic_beta_param import AnthropicBetaParam
from .....types.beta.organization.plugins.beta_plugin_version import BetaPluginVersion

__all__ = ["Versions", "AsyncVersions"]


class Versions(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> VersionsWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#accessing-raw-response-data-eg-headers
        """
        return VersionsWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> VersionsWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#with_streaming_response
        """
        return VersionsWithStreamingResponse(self)

    def create(
        self,
        plugin_id: str,
        *,
        files: SequenceNotStr[FileTypes],
        release_notes: str | Omit = omit,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaPluginVersion:
        """
        Add a version to an organization-owned Plugin by uploading the new version's
        files; it becomes the version served to members unless the Plugin's served
        version has been pinned.

        The upload is the same `multipart/form-data` as creating a Plugin: the version's
        files (`files`, each part sent as `files[]`) and optional `release_notes`. The
        uploaded manifest's `name` must equal the Plugin's `name`. Returns the stored
        version; read the Plugin back to see which version it serves.

        Only a Plugin in a `manual` marketplace takes uploads; a Plugin synchronized
        from a repository gets its versions from the repository. When the Plugin is in
        the organization's library marketplace, a version that adds a skill with the
        name of an organization skill (a skill an administrator uploaded for the whole
        organization in claude.ai) is refused with a 409: `error_code`
        `skill_name_taken`, with that name in `details.skill_name`. A 503 with
        `error_code` `registration_pending` means the version was stored but is not yet
        usable; a later version create on the Plugin completes it.

        For a worked example, see
        [Create a version](/docs/en/manage-claude/plugins-api#create-a-version) in the
        Plugins API guide.

        **Accepted credentials:** an Admin API key with the `write:plugins` scope.

        Every request must include the beta header
        `anthropic-beta: ce-plugins-2026-09-01`. A request without it returns `404`,
        exactly as if the endpoint did not exist. The Plugins API is in beta and is
        available to Claude Enterprise organizations only. It is not available to Claude
        Platform (Claude Console) organizations, or to organizations with HIPAA
        readiness enabled.

        Args:
          plugin_id: ID of the Plugin (prefixed `plugin_`).

          files: The version's files: one part per file, the part's filename being the file's
              path within the Plugin (for example `skills/review-pr/SKILL.md`), or a single
              `.zip` or `.plugin` archive holding them all. On the wire each part is named
              `files[]`, and a part named plain `files` is not read; with cURL,
              `-F 'files[]=@SKILL.md;filename=skills/review-pr/SKILL.md'`. The files must
              include the manifest, `.claude-plugin/plugin.json`.

          release_notes: Release notes stored with the version and shown in its version history in
              claude.ai; up to 5,000 characters.

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
        body = deepcopy_with_paths(
            {
                "files": files,
                "release_notes": release_notes,
            },
            [["files", "<array>"]],
        )
        extracted_files = extract_files(cast(Mapping[str, object], body), paths=[["files", "<array>"]])
        # It should be noted that the actual Content-Type header that will be
        # sent to the server will contain a `boundary` parameter, e.g.
        # multipart/form-data; boundary=---abc--
        extra_headers["Content-Type"] = "multipart/form-data"
        return self._post(
            path_template("/v1/organizations/plugins/{plugin_id}/versions?beta=true", plugin_id=plugin_id),
            body=body,
            files=extracted_files,
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
            ),
            cast_to=BetaPluginVersion,
        )

    def retrieve(
        self,
        version: str,
        *,
        plugin_id: str,
        organization_id: Optional[str] | Omit = omit,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaPluginVersion:
        """
        Retrieve one version of a Plugin by its ID, or the Plugin's newest version.

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

          version: ID of the Plugin Version (prefixed `pluginver_`), or `latest` for the newest
              one.

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
        if not plugin_id:
            raise ValueError(f"Expected a non-empty value for `plugin_id` but received {plugin_id!r}")
        if not version:
            raise ValueError(f"Expected a non-empty value for `version` but received {version!r}")
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
                "/v1/organizations/plugins/{plugin_id}/versions/{version}?beta=true",
                plugin_id=plugin_id,
                version=version,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query={"organization_id": organization_id},
            ),
            cast_to=BetaPluginVersion,
        )

    def list(
        self,
        plugin_id: str,
        *,
        limit: int | Omit = omit,
        organization_id: Optional[str] | Omit = omit,
        page: Optional[str] | Omit = omit,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> SyncPageCursor[BetaPluginVersion]:
        """
        List a Plugin's versions, newest first.

        The first item of the first page is the version the Plugin's `latest_version_id`
        refers to.

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

              Defaults to `20`. Ranges from `1` to `1000`.

          organization_id: For a `read:org_audit` or `read:compliance_org_data` key created for all of a
              parent organization's linked organizations: a child organization of that parent
              to read instead of the organization the key was created in, given as the
              organization's UUID or its `org_`-prefixed ID. A value that is neither returns a
              400; an organization that is not a child of the key's parent, or where the
              Plugins API is not available, returns a 404. Any other key may pass only its own
              organization's ID here; another organization returns a 404.

          page: Optionally set to the `next_page` token from the previous response.

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
            path_template("/v1/organizations/plugins/{plugin_id}/versions?beta=true", plugin_id=plugin_id),
            page=SyncPageCursor[BetaPluginVersion],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query={
                    "limit": limit,
                    "organization_id": organization_id,
                    "page": page,
                },
            ),
            model=BetaPluginVersion,
        )

    def download(
        self,
        version: str,
        *,
        plugin_id: str,
        organization_id: Optional[str] | Omit = omit,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BinaryAPIResponse:
        """Download one version's `.zip` archive, exactly as stored.

        Each download of a
        Plugin from a member's personal plugin marketplace is recorded on the Compliance
        API activity feed.

        The response body is the archive (`Content-Type: application/zip`), sent as an
        attachment whose filename is derived from the Plugin's name; name saved files
        from the IDs in the request path, since that filename is not unique.

        **Accepted credentials:** an Admin API key with the `read:plugins` or
        `read:org_audit` scope, or a Compliance Access Key with the
        `read:compliance_org_data` scope.

        Every read scope above (`read:plugins`, `read:org_audit`, and
        `read:compliance_org_data`) can download the files of plugins in members'
        personal marketplaces, including files that claude.ai's admin settings do not
        show, and a `read:org_audit` or `read:compliance_org_data` key created for all
        of your parent organization's linked organizations can do this in any
        organization under it that has access to this API, by passing `organization_id`.
        Each such download records a `claude_plugin_archive_accessed` event on the
        Compliance API activity feed, identifying the key, the plugin, the version, and
        the member. Downloads of organization-owned plugins are not recorded.

        Every request must include the beta header
        `anthropic-beta: ce-plugins-2026-09-01`. A request without it returns `404`,
        exactly as if the endpoint did not exist. The Plugins API is in beta and is
        available to Claude Enterprise organizations only. It is not available to Claude
        Platform (Claude Console) organizations, or to organizations with HIPAA
        readiness enabled.

        Args:
          plugin_id: ID of the Plugin (prefixed `plugin_`).

          version: ID of the Plugin Version (prefixed `pluginver_`). `latest` is not accepted here.

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
        if not plugin_id:
            raise ValueError(f"Expected a non-empty value for `plugin_id` but received {plugin_id!r}")
        if not version:
            raise ValueError(f"Expected a non-empty value for `version` but received {version!r}")
        extra_headers = {"Accept": "application/binary", **(extra_headers or {})}
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
                "/v1/organizations/plugins/{plugin_id}/versions/{version}/content?beta=true",
                plugin_id=plugin_id,
                version=version,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query={"organization_id": organization_id},
            ),
            cast_to=BinaryAPIResponse,
        )


class AsyncVersions(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncVersionsWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#accessing-raw-response-data-eg-headers
        """
        return AsyncVersionsWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncVersionsWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#with_streaming_response
        """
        return AsyncVersionsWithStreamingResponse(self)

    async def create(
        self,
        plugin_id: str,
        *,
        files: SequenceNotStr[FileTypes],
        release_notes: str | Omit = omit,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaPluginVersion:
        """
        Add a version to an organization-owned Plugin by uploading the new version's
        files; it becomes the version served to members unless the Plugin's served
        version has been pinned.

        The upload is the same `multipart/form-data` as creating a Plugin: the version's
        files (`files`, each part sent as `files[]`) and optional `release_notes`. The
        uploaded manifest's `name` must equal the Plugin's `name`. Returns the stored
        version; read the Plugin back to see which version it serves.

        Only a Plugin in a `manual` marketplace takes uploads; a Plugin synchronized
        from a repository gets its versions from the repository. When the Plugin is in
        the organization's library marketplace, a version that adds a skill with the
        name of an organization skill (a skill an administrator uploaded for the whole
        organization in claude.ai) is refused with a 409: `error_code`
        `skill_name_taken`, with that name in `details.skill_name`. A 503 with
        `error_code` `registration_pending` means the version was stored but is not yet
        usable; a later version create on the Plugin completes it.

        For a worked example, see
        [Create a version](/docs/en/manage-claude/plugins-api#create-a-version) in the
        Plugins API guide.

        **Accepted credentials:** an Admin API key with the `write:plugins` scope.

        Every request must include the beta header
        `anthropic-beta: ce-plugins-2026-09-01`. A request without it returns `404`,
        exactly as if the endpoint did not exist. The Plugins API is in beta and is
        available to Claude Enterprise organizations only. It is not available to Claude
        Platform (Claude Console) organizations, or to organizations with HIPAA
        readiness enabled.

        Args:
          plugin_id: ID of the Plugin (prefixed `plugin_`).

          files: The version's files: one part per file, the part's filename being the file's
              path within the Plugin (for example `skills/review-pr/SKILL.md`), or a single
              `.zip` or `.plugin` archive holding them all. On the wire each part is named
              `files[]`, and a part named plain `files` is not read; with cURL,
              `-F 'files[]=@SKILL.md;filename=skills/review-pr/SKILL.md'`. The files must
              include the manifest, `.claude-plugin/plugin.json`.

          release_notes: Release notes stored with the version and shown in its version history in
              claude.ai; up to 5,000 characters.

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
        body = deepcopy_with_paths(
            {
                "files": files,
                "release_notes": release_notes,
            },
            [["files", "<array>"]],
        )
        extracted_files = extract_files(cast(Mapping[str, object], body), paths=[["files", "<array>"]])
        # It should be noted that the actual Content-Type header that will be
        # sent to the server will contain a `boundary` parameter, e.g.
        # multipart/form-data; boundary=---abc--
        extra_headers["Content-Type"] = "multipart/form-data"
        return await self._post(
            path_template("/v1/organizations/plugins/{plugin_id}/versions?beta=true", plugin_id=plugin_id),
            body=body,
            files=extracted_files,
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
            ),
            cast_to=BetaPluginVersion,
        )

    async def retrieve(
        self,
        version: str,
        *,
        plugin_id: str,
        organization_id: Optional[str] | Omit = omit,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaPluginVersion:
        """
        Retrieve one version of a Plugin by its ID, or the Plugin's newest version.

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

          version: ID of the Plugin Version (prefixed `pluginver_`), or `latest` for the newest
              one.

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
        if not plugin_id:
            raise ValueError(f"Expected a non-empty value for `plugin_id` but received {plugin_id!r}")
        if not version:
            raise ValueError(f"Expected a non-empty value for `version` but received {version!r}")
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
                "/v1/organizations/plugins/{plugin_id}/versions/{version}?beta=true",
                plugin_id=plugin_id,
                version=version,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query={"organization_id": organization_id},
            ),
            cast_to=BetaPluginVersion,
        )

    def list(
        self,
        plugin_id: str,
        *,
        limit: int | Omit = omit,
        organization_id: Optional[str] | Omit = omit,
        page: Optional[str] | Omit = omit,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> AsyncPaginator[BetaPluginVersion, AsyncPageCursor[BetaPluginVersion]]:
        """
        List a Plugin's versions, newest first.

        The first item of the first page is the version the Plugin's `latest_version_id`
        refers to.

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

              Defaults to `20`. Ranges from `1` to `1000`.

          organization_id: For a `read:org_audit` or `read:compliance_org_data` key created for all of a
              parent organization's linked organizations: a child organization of that parent
              to read instead of the organization the key was created in, given as the
              organization's UUID or its `org_`-prefixed ID. A value that is neither returns a
              400; an organization that is not a child of the key's parent, or where the
              Plugins API is not available, returns a 404. Any other key may pass only its own
              organization's ID here; another organization returns a 404.

          page: Optionally set to the `next_page` token from the previous response.

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
            path_template("/v1/organizations/plugins/{plugin_id}/versions?beta=true", plugin_id=plugin_id),
            page=AsyncPageCursor[BetaPluginVersion],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query={
                    "limit": limit,
                    "organization_id": organization_id,
                    "page": page,
                },
            ),
            model=BetaPluginVersion,
        )

    async def download(
        self,
        version: str,
        *,
        plugin_id: str,
        organization_id: Optional[str] | Omit = omit,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> AsyncBinaryAPIResponse:
        """Download one version's `.zip` archive, exactly as stored.

        Each download of a
        Plugin from a member's personal plugin marketplace is recorded on the Compliance
        API activity feed.

        The response body is the archive (`Content-Type: application/zip`), sent as an
        attachment whose filename is derived from the Plugin's name; name saved files
        from the IDs in the request path, since that filename is not unique.

        **Accepted credentials:** an Admin API key with the `read:plugins` or
        `read:org_audit` scope, or a Compliance Access Key with the
        `read:compliance_org_data` scope.

        Every read scope above (`read:plugins`, `read:org_audit`, and
        `read:compliance_org_data`) can download the files of plugins in members'
        personal marketplaces, including files that claude.ai's admin settings do not
        show, and a `read:org_audit` or `read:compliance_org_data` key created for all
        of your parent organization's linked organizations can do this in any
        organization under it that has access to this API, by passing `organization_id`.
        Each such download records a `claude_plugin_archive_accessed` event on the
        Compliance API activity feed, identifying the key, the plugin, the version, and
        the member. Downloads of organization-owned plugins are not recorded.

        Every request must include the beta header
        `anthropic-beta: ce-plugins-2026-09-01`. A request without it returns `404`,
        exactly as if the endpoint did not exist. The Plugins API is in beta and is
        available to Claude Enterprise organizations only. It is not available to Claude
        Platform (Claude Console) organizations, or to organizations with HIPAA
        readiness enabled.

        Args:
          plugin_id: ID of the Plugin (prefixed `plugin_`).

          version: ID of the Plugin Version (prefixed `pluginver_`). `latest` is not accepted here.

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
        if not plugin_id:
            raise ValueError(f"Expected a non-empty value for `plugin_id` but received {plugin_id!r}")
        if not version:
            raise ValueError(f"Expected a non-empty value for `version` but received {version!r}")
        extra_headers = {"Accept": "application/binary", **(extra_headers or {})}
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
                "/v1/organizations/plugins/{plugin_id}/versions/{version}/content?beta=true",
                plugin_id=plugin_id,
                version=version,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query={"organization_id": organization_id},
            ),
            cast_to=AsyncBinaryAPIResponse,
        )


class VersionsWithRawResponse:
    def __init__(self, versions: Versions) -> None:
        self._versions = versions

        self.create = to_raw_response_wrapper(
            versions.create,
        )
        self.retrieve = to_raw_response_wrapper(
            versions.retrieve,
        )
        self.list = to_raw_response_wrapper(
            versions.list,
        )
        self.download = to_custom_raw_response_wrapper(
            versions.download,
            BinaryAPIResponse,
        )


class AsyncVersionsWithRawResponse:
    def __init__(self, versions: AsyncVersions) -> None:
        self._versions = versions

        self.create = async_to_raw_response_wrapper(
            versions.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            versions.retrieve,
        )
        self.list = async_to_raw_response_wrapper(
            versions.list,
        )
        self.download = async_to_custom_raw_response_wrapper(
            versions.download,
            AsyncBinaryAPIResponse,
        )


class VersionsWithStreamingResponse:
    def __init__(self, versions: Versions) -> None:
        self._versions = versions

        self.create = to_streamed_response_wrapper(
            versions.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            versions.retrieve,
        )
        self.list = to_streamed_response_wrapper(
            versions.list,
        )
        self.download = to_custom_streamed_response_wrapper(
            versions.download,
            StreamedBinaryAPIResponse,
        )


class AsyncVersionsWithStreamingResponse:
    def __init__(self, versions: AsyncVersions) -> None:
        self._versions = versions

        self.create = async_to_streamed_response_wrapper(
            versions.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            versions.retrieve,
        )
        self.list = async_to_streamed_response_wrapper(
            versions.list,
        )
        self.download = async_to_custom_streamed_response_wrapper(
            versions.download,
            AsyncStreamedBinaryAPIResponse,
        )
