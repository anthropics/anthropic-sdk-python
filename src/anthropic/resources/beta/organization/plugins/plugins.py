from __future__ import annotations

from typing import List, Union, Mapping, Optional, cast
from datetime import datetime
from itertools import chain
from typing_extensions import Literal

import httpx2

from .shares import (
    Shares,
    AsyncShares,
    SharesWithRawResponse,
    AsyncSharesWithRawResponse,
    SharesWithStreamingResponse,
    AsyncSharesWithStreamingResponse,
)
from .versions import (
    Versions,
    AsyncVersions,
    VersionsWithRawResponse,
    AsyncVersionsWithRawResponse,
    VersionsWithStreamingResponse,
    AsyncVersionsWithStreamingResponse,
)
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
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from .....pagination import SyncPageCursor, AsyncPageCursor
from ....._base_client import AsyncPaginator, make_request_options
from .installation_settings import (
    InstallationSettings,
    AsyncInstallationSettings,
    InstallationSettingsWithRawResponse,
    AsyncInstallationSettingsWithRawResponse,
    InstallationSettingsWithStreamingResponse,
    AsyncInstallationSettingsWithStreamingResponse,
)
from .....types.anthropic_beta_param import AnthropicBetaParam
from .....types.beta.organization.beta_plugin import BetaPlugin
from .....types.beta.organization.beta_deleted_plugin import BetaDeletedPlugin

__all__ = ["Plugins", "AsyncPlugins"]


class Plugins(SyncAPIResource):
    @cached_property
    def versions(self) -> Versions:
        return Versions(self._client)

    @cached_property
    def installation_settings(self) -> InstallationSettings:
        return InstallationSettings(self._client)

    @cached_property
    def shares(self) -> Shares:
        return Shares(self._client)

    @cached_property
    def with_raw_response(self) -> PluginsWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#accessing-raw-response-data-eg-headers
        """
        return PluginsWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> PluginsWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#with_streaming_response
        """
        return PluginsWithStreamingResponse(self)

    def create(
        self,
        *,
        files: SequenceNotStr[FileTypes],
        marketplace_id: str | Omit = omit,
        release_notes: str | Omit = omit,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaPlugin:
        """
        Create an organization-owned Plugin and its first version by uploading the
        version's files.

        The upload is `multipart/form-data`: the version's files (`files`, each part
        sent as `files[]`), with an optional `marketplace_id` and `release_notes`. The
        manifest's `name` becomes the Plugin's `name`, and `display_name`, `description`
        and `manifest_version` come from the manifest too.

        `name` may contain lowercase letters (from any alphabet), digits, and hyphens,
        up to 64 characters. Uppercase letters, spaces, underscores, and other
        punctuation are rejected.

        The `name` must be unique within the marketplace: a name already taken returns a
        409 with `error_code` `plugin_name_taken` and, when a Plugin holds it, that
        Plugin's ID in `details.plugin_id`. A Plugin going into the organization's
        library marketplace is also refused with a 409 when one of its skills has the
        name of an organization skill (a skill an administrator uploaded for the whole
        organization in claude.ai): `error_code` `skill_name_taken`, with that name in
        `details.skill_name`; rename the skill, or remove the organization skill in
        claude.ai. A 503 with `error_code` `registration_pending` means the Plugin and
        its version were stored (their IDs are in `details`) but are not yet usable in
        claude.ai: do not retry the create (the retry would return `plugin_name_taken`);
        create a version on the stored Plugin instead, which completes it.

        For a worked example, see
        [Create a plugin](/docs/en/manage-claude/plugins-api#create-a-plugin) in the
        Plugins API guide.

        **Accepted credentials:** an Admin API key with the `write:plugins` scope.

        Every request must include the beta header
        `anthropic-beta: ce-plugins-2026-09-01`. A request without it returns `404`,
        exactly as if the endpoint did not exist. The Plugins API is in beta and is
        available to Claude Enterprise organizations only. It is not available to Claude
        Platform (Claude Console) organizations, or to organizations with HIPAA
        readiness enabled.

        Args:
          files: The version's files: one part per file, the part's filename being the file's
              path within the Plugin (for example `skills/review-pr/SKILL.md`), or a single
              `.zip` or `.plugin` archive holding them all. On the wire each part is named
              `files[]`, and a part named plain `files` is not read; with cURL,
              `-F 'files[]=@SKILL.md;filename=skills/review-pr/SKILL.md'`. The files must
              include the manifest, `.claude-plugin/plugin.json`.

          marketplace_id: ID of the organization-owned plugin marketplace to create the Plugin in
              (prefixed `marketplace_`). It must be a `manual` marketplace, one whose Plugins
              are uploaded rather than synchronized from a repository. When omitted, the
              Plugin is created in the organization's library marketplace, an
              organization-owned `manual` marketplace created on first use.

          release_notes: Release notes stored with the version and shown in its version history in
              claude.ai; up to 5,000 characters.

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
        body = deepcopy_with_paths(
            {
                "files": files,
                "marketplace_id": marketplace_id,
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
            "/v1/organizations/plugins?beta=true",
            body=body,
            files=extracted_files,
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
            ),
            cast_to=BetaPlugin,
        )

    def retrieve(
        self,
        plugin_id: str,
        *,
        organization_id: Optional[str] | Omit = omit,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaPlugin:
        """
        Retrieve a Plugin by ID.

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
            path_template("/v1/organizations/plugins/{plugin_id}?beta=true", plugin_id=plugin_id),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query={"organization_id": organization_id},
            ),
            cast_to=BetaPlugin,
        )

    def update(
        self,
        plugin_id: str,
        *,
        served_version_id: str,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaPlugin:
        """
        Change which stored version of an organization-owned Plugin is served to
        members, for example to roll back to an earlier one. This pins the served
        version: later uploads are stored but no longer change what is served, and
        pinning cannot currently be undone, here or in claude.ai.

        Pass the version as `served_version_id`: an earlier one to roll back, a later
        one to start serving a version that was stored without being served, or the one
        already served to pin it without changing what is served. No new version is
        created.

        When the organization has content scanning enabled, a version whose scan is
        still running is refused with a 409 (`error_code` `scan_pending`; retry once the
        scan finishes) and one whose scan failed, errored or reached no verdict with a
        400 (`scan_failed`; a `warn` is accepted). When the Plugin is in the
        organization's library marketplace, a version other than the one served is also
        refused with a 409 when one of its skills has a name that an organization skill
        (one an administrator uploaded for the whole organization in claude.ai) has
        since taken: `error_code` `skill_name_taken`, with that name in
        `details.skill_name`. A member-owned Plugin cannot be updated here (403).

        This endpoint does not write installation settings; they are written at
        `/v1/organizations/plugins/{plugin_id}/installation_settings/{target}`.

        **Accepted credentials:** an Admin API key with the `write:plugins` scope.

        Every request must include the beta header
        `anthropic-beta: ce-plugins-2026-09-01`. A request without it returns `404`,
        exactly as if the endpoint did not exist. The Plugins API is in beta and is
        available to Claude Enterprise organizations only. It is not available to Claude
        Platform (Claude Console) organizations, or to organizations with HIPAA
        readiness enabled.

        Args:
          plugin_id: ID of the Plugin (prefixed `plugin_`).

          served_version_id: Serve this version of the Plugin (prefixed `pluginver_`) and pin the served
              version to it; `latest` is not accepted.

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
        return self._post(
            path_template("/v1/organizations/plugins/{plugin_id}?beta=true", plugin_id=plugin_id),
            body={"served_version_id": served_version_id},
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
            ),
            cast_to=BetaPlugin,
        )

    def list(
        self,
        *,
        created_at_gt: Union[str, datetime, None] | Omit = omit,
        created_at_gte: Union[str, datetime, None] | Omit = omit,
        created_at_lt: Union[str, datetime, None] | Omit = omit,
        created_at_lte: Union[str, datetime, None] | Omit = omit,
        limit: int | Omit = omit,
        marketplace_id: Optional[str] | Omit = omit,
        organization_id: Optional[str] | Omit = omit,
        owner_type: Optional[Literal["organization", "user"]] | Omit = omit,
        owner_user_id: Optional[str] | Omit = omit,
        page: Optional[str] | Omit = omit,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> SyncPageCursor[BetaPlugin]:
        """
        List the Plugins created under the organization, newest first: those in the
        organization's own plugin marketplaces and those in members' personal plugin
        marketplaces.

        Plugins in members' personal marketplaces are listed with the same detail as the
        organization's own, and their files can be downloaded through the version
        archive endpoint, which records each such download on the Compliance API
        activity feed.

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
          created_at_gt: RFC 3339 timestamp bound; combine [gte], [gt], [lte], [lt].

          created_at_gte: RFC 3339 timestamp bound; combine [gte], [gt], [lte], [lt].

          created_at_lt: RFC 3339 timestamp bound; combine [gte], [gt], [lte], [lt].

          created_at_lte: RFC 3339 timestamp bound; combine [gte], [gt], [lte], [lt].

          limit: Number of items to return per page.

              Defaults to `20`. Ranges from `1` to `100`.

          marketplace_id: Only Plugins in this plugin marketplace (prefixed `marketplace_`).

          organization_id: For a `read:org_audit` or `read:compliance_org_data` key created for all of a
              parent organization's linked organizations: a child organization of that parent
              to read instead of the organization the key was created in, given as the
              organization's UUID or its `org_`-prefixed ID. A value that is neither returns a
              400; an organization that is not a child of the key's parent, or where the
              Plugins API is not available, returns a 404. Any other key may pass only its own
              organization's ID here; another organization returns a 404.

          owner_type: `organization` for Plugins in the organization's plugin marketplaces, `user` for
              Plugins in members' personal plugin marketplaces.

          owner_user_id: Only Plugins in this member's personal plugin marketplaces (prefixed `user_`); a
              removed member's ID is accepted.

          page: Optionally set to the `next_page` token from the previous response.

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
            "/v1/organizations/plugins?beta=true",
            page=SyncPageCursor[BetaPlugin],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query={
                    "created_at[gt]": created_at_gt,
                    "created_at[gte]": created_at_gte,
                    "created_at[lt]": created_at_lt,
                    "created_at[lte]": created_at_lte,
                    "limit": limit,
                    "marketplace_id": marketplace_id,
                    "organization_id": organization_id,
                    "owner_type": owner_type,
                    "owner_user_id": owner_user_id,
                    "page": page,
                },
            ),
            model=BetaPlugin,
        )

    def delete(
        self,
        plugin_id: str,
        *,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaDeletedPlugin:
        """
        Permanently delete a Plugin and every version it holds, exactly as when an
        administrator deletes it in claude.ai. The Plugin may belong to the organization
        or to a member, including a member who has since left the organization.

        An organization-owned Plugin's installation settings go with it; a member-owned
        Plugin's shares are withdrawn and its owner no longer has it.

        To take an organization-owned Plugin out of use reversibly, set its
        organization-wide installation setting to `not_available` instead (and remove or
        change any group settings, which override it for their members). Only a Plugin
        in a `manual` marketplace can be deleted here; one synchronized from a
        repository is removed by removing it from the repository (400).

        **Accepted credentials:** an Admin API key with the `write:plugins` scope.

        Every request must include the beta header
        `anthropic-beta: ce-plugins-2026-09-01`. A request without it returns `404`,
        exactly as if the endpoint did not exist. The Plugins API is in beta and is
        available to Claude Enterprise organizations only. It is not available to Claude
        Platform (Claude Console) organizations, or to organizations with HIPAA
        readiness enabled.

        Args:
          plugin_id: ID of the Plugin (prefixed `plugin_`).

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
        return self._delete(
            path_template("/v1/organizations/plugins/{plugin_id}?beta=true", plugin_id=plugin_id),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
            ),
            cast_to=BetaDeletedPlugin,
        )


class AsyncPlugins(AsyncAPIResource):
    @cached_property
    def versions(self) -> AsyncVersions:
        return AsyncVersions(self._client)

    @cached_property
    def installation_settings(self) -> AsyncInstallationSettings:
        return AsyncInstallationSettings(self._client)

    @cached_property
    def shares(self) -> AsyncShares:
        return AsyncShares(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncPluginsWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#accessing-raw-response-data-eg-headers
        """
        return AsyncPluginsWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncPluginsWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#with_streaming_response
        """
        return AsyncPluginsWithStreamingResponse(self)

    async def create(
        self,
        *,
        files: SequenceNotStr[FileTypes],
        marketplace_id: str | Omit = omit,
        release_notes: str | Omit = omit,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaPlugin:
        """
        Create an organization-owned Plugin and its first version by uploading the
        version's files.

        The upload is `multipart/form-data`: the version's files (`files`, each part
        sent as `files[]`), with an optional `marketplace_id` and `release_notes`. The
        manifest's `name` becomes the Plugin's `name`, and `display_name`, `description`
        and `manifest_version` come from the manifest too.

        `name` may contain lowercase letters (from any alphabet), digits, and hyphens,
        up to 64 characters. Uppercase letters, spaces, underscores, and other
        punctuation are rejected.

        The `name` must be unique within the marketplace: a name already taken returns a
        409 with `error_code` `plugin_name_taken` and, when a Plugin holds it, that
        Plugin's ID in `details.plugin_id`. A Plugin going into the organization's
        library marketplace is also refused with a 409 when one of its skills has the
        name of an organization skill (a skill an administrator uploaded for the whole
        organization in claude.ai): `error_code` `skill_name_taken`, with that name in
        `details.skill_name`; rename the skill, or remove the organization skill in
        claude.ai. A 503 with `error_code` `registration_pending` means the Plugin and
        its version were stored (their IDs are in `details`) but are not yet usable in
        claude.ai: do not retry the create (the retry would return `plugin_name_taken`);
        create a version on the stored Plugin instead, which completes it.

        For a worked example, see
        [Create a plugin](/docs/en/manage-claude/plugins-api#create-a-plugin) in the
        Plugins API guide.

        **Accepted credentials:** an Admin API key with the `write:plugins` scope.

        Every request must include the beta header
        `anthropic-beta: ce-plugins-2026-09-01`. A request without it returns `404`,
        exactly as if the endpoint did not exist. The Plugins API is in beta and is
        available to Claude Enterprise organizations only. It is not available to Claude
        Platform (Claude Console) organizations, or to organizations with HIPAA
        readiness enabled.

        Args:
          files: The version's files: one part per file, the part's filename being the file's
              path within the Plugin (for example `skills/review-pr/SKILL.md`), or a single
              `.zip` or `.plugin` archive holding them all. On the wire each part is named
              `files[]`, and a part named plain `files` is not read; with cURL,
              `-F 'files[]=@SKILL.md;filename=skills/review-pr/SKILL.md'`. The files must
              include the manifest, `.claude-plugin/plugin.json`.

          marketplace_id: ID of the organization-owned plugin marketplace to create the Plugin in
              (prefixed `marketplace_`). It must be a `manual` marketplace, one whose Plugins
              are uploaded rather than synchronized from a repository. When omitted, the
              Plugin is created in the organization's library marketplace, an
              organization-owned `manual` marketplace created on first use.

          release_notes: Release notes stored with the version and shown in its version history in
              claude.ai; up to 5,000 characters.

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
        body = deepcopy_with_paths(
            {
                "files": files,
                "marketplace_id": marketplace_id,
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
            "/v1/organizations/plugins?beta=true",
            body=body,
            files=extracted_files,
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
            ),
            cast_to=BetaPlugin,
        )

    async def retrieve(
        self,
        plugin_id: str,
        *,
        organization_id: Optional[str] | Omit = omit,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaPlugin:
        """
        Retrieve a Plugin by ID.

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
            path_template("/v1/organizations/plugins/{plugin_id}?beta=true", plugin_id=plugin_id),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query={"organization_id": organization_id},
            ),
            cast_to=BetaPlugin,
        )

    async def update(
        self,
        plugin_id: str,
        *,
        served_version_id: str,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaPlugin:
        """
        Change which stored version of an organization-owned Plugin is served to
        members, for example to roll back to an earlier one. This pins the served
        version: later uploads are stored but no longer change what is served, and
        pinning cannot currently be undone, here or in claude.ai.

        Pass the version as `served_version_id`: an earlier one to roll back, a later
        one to start serving a version that was stored without being served, or the one
        already served to pin it without changing what is served. No new version is
        created.

        When the organization has content scanning enabled, a version whose scan is
        still running is refused with a 409 (`error_code` `scan_pending`; retry once the
        scan finishes) and one whose scan failed, errored or reached no verdict with a
        400 (`scan_failed`; a `warn` is accepted). When the Plugin is in the
        organization's library marketplace, a version other than the one served is also
        refused with a 409 when one of its skills has a name that an organization skill
        (one an administrator uploaded for the whole organization in claude.ai) has
        since taken: `error_code` `skill_name_taken`, with that name in
        `details.skill_name`. A member-owned Plugin cannot be updated here (403).

        This endpoint does not write installation settings; they are written at
        `/v1/organizations/plugins/{plugin_id}/installation_settings/{target}`.

        **Accepted credentials:** an Admin API key with the `write:plugins` scope.

        Every request must include the beta header
        `anthropic-beta: ce-plugins-2026-09-01`. A request without it returns `404`,
        exactly as if the endpoint did not exist. The Plugins API is in beta and is
        available to Claude Enterprise organizations only. It is not available to Claude
        Platform (Claude Console) organizations, or to organizations with HIPAA
        readiness enabled.

        Args:
          plugin_id: ID of the Plugin (prefixed `plugin_`).

          served_version_id: Serve this version of the Plugin (prefixed `pluginver_`) and pin the served
              version to it; `latest` is not accepted.

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
        return await self._post(
            path_template("/v1/organizations/plugins/{plugin_id}?beta=true", plugin_id=plugin_id),
            body={"served_version_id": served_version_id},
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
            ),
            cast_to=BetaPlugin,
        )

    def list(
        self,
        *,
        created_at_gt: Union[str, datetime, None] | Omit = omit,
        created_at_gte: Union[str, datetime, None] | Omit = omit,
        created_at_lt: Union[str, datetime, None] | Omit = omit,
        created_at_lte: Union[str, datetime, None] | Omit = omit,
        limit: int | Omit = omit,
        marketplace_id: Optional[str] | Omit = omit,
        organization_id: Optional[str] | Omit = omit,
        owner_type: Optional[Literal["organization", "user"]] | Omit = omit,
        owner_user_id: Optional[str] | Omit = omit,
        page: Optional[str] | Omit = omit,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> AsyncPaginator[BetaPlugin, AsyncPageCursor[BetaPlugin]]:
        """
        List the Plugins created under the organization, newest first: those in the
        organization's own plugin marketplaces and those in members' personal plugin
        marketplaces.

        Plugins in members' personal marketplaces are listed with the same detail as the
        organization's own, and their files can be downloaded through the version
        archive endpoint, which records each such download on the Compliance API
        activity feed.

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
          created_at_gt: RFC 3339 timestamp bound; combine [gte], [gt], [lte], [lt].

          created_at_gte: RFC 3339 timestamp bound; combine [gte], [gt], [lte], [lt].

          created_at_lt: RFC 3339 timestamp bound; combine [gte], [gt], [lte], [lt].

          created_at_lte: RFC 3339 timestamp bound; combine [gte], [gt], [lte], [lt].

          limit: Number of items to return per page.

              Defaults to `20`. Ranges from `1` to `100`.

          marketplace_id: Only Plugins in this plugin marketplace (prefixed `marketplace_`).

          organization_id: For a `read:org_audit` or `read:compliance_org_data` key created for all of a
              parent organization's linked organizations: a child organization of that parent
              to read instead of the organization the key was created in, given as the
              organization's UUID or its `org_`-prefixed ID. A value that is neither returns a
              400; an organization that is not a child of the key's parent, or where the
              Plugins API is not available, returns a 404. Any other key may pass only its own
              organization's ID here; another organization returns a 404.

          owner_type: `organization` for Plugins in the organization's plugin marketplaces, `user` for
              Plugins in members' personal plugin marketplaces.

          owner_user_id: Only Plugins in this member's personal plugin marketplaces (prefixed `user_`); a
              removed member's ID is accepted.

          page: Optionally set to the `next_page` token from the previous response.

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
            "/v1/organizations/plugins?beta=true",
            page=AsyncPageCursor[BetaPlugin],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query={
                    "created_at[gt]": created_at_gt,
                    "created_at[gte]": created_at_gte,
                    "created_at[lt]": created_at_lt,
                    "created_at[lte]": created_at_lte,
                    "limit": limit,
                    "marketplace_id": marketplace_id,
                    "organization_id": organization_id,
                    "owner_type": owner_type,
                    "owner_user_id": owner_user_id,
                    "page": page,
                },
            ),
            model=BetaPlugin,
        )

    async def delete(
        self,
        plugin_id: str,
        *,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaDeletedPlugin:
        """
        Permanently delete a Plugin and every version it holds, exactly as when an
        administrator deletes it in claude.ai. The Plugin may belong to the organization
        or to a member, including a member who has since left the organization.

        An organization-owned Plugin's installation settings go with it; a member-owned
        Plugin's shares are withdrawn and its owner no longer has it.

        To take an organization-owned Plugin out of use reversibly, set its
        organization-wide installation setting to `not_available` instead (and remove or
        change any group settings, which override it for their members). Only a Plugin
        in a `manual` marketplace can be deleted here; one synchronized from a
        repository is removed by removing it from the repository (400).

        **Accepted credentials:** an Admin API key with the `write:plugins` scope.

        Every request must include the beta header
        `anthropic-beta: ce-plugins-2026-09-01`. A request without it returns `404`,
        exactly as if the endpoint did not exist. The Plugins API is in beta and is
        available to Claude Enterprise organizations only. It is not available to Claude
        Platform (Claude Console) organizations, or to organizations with HIPAA
        readiness enabled.

        Args:
          plugin_id: ID of the Plugin (prefixed `plugin_`).

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
        return await self._delete(
            path_template("/v1/organizations/plugins/{plugin_id}?beta=true", plugin_id=plugin_id),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
            ),
            cast_to=BetaDeletedPlugin,
        )


class PluginsWithRawResponse:
    def __init__(self, plugins: Plugins) -> None:
        self._plugins = plugins

        self.create = to_raw_response_wrapper(
            plugins.create,
        )
        self.retrieve = to_raw_response_wrapper(
            plugins.retrieve,
        )
        self.update = to_raw_response_wrapper(
            plugins.update,
        )
        self.list = to_raw_response_wrapper(
            plugins.list,
        )
        self.delete = to_raw_response_wrapper(
            plugins.delete,
        )

    @cached_property
    def versions(self) -> VersionsWithRawResponse:
        return VersionsWithRawResponse(self._plugins.versions)

    @cached_property
    def installation_settings(self) -> InstallationSettingsWithRawResponse:
        return InstallationSettingsWithRawResponse(self._plugins.installation_settings)

    @cached_property
    def shares(self) -> SharesWithRawResponse:
        return SharesWithRawResponse(self._plugins.shares)


class AsyncPluginsWithRawResponse:
    def __init__(self, plugins: AsyncPlugins) -> None:
        self._plugins = plugins

        self.create = async_to_raw_response_wrapper(
            plugins.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            plugins.retrieve,
        )
        self.update = async_to_raw_response_wrapper(
            plugins.update,
        )
        self.list = async_to_raw_response_wrapper(
            plugins.list,
        )
        self.delete = async_to_raw_response_wrapper(
            plugins.delete,
        )

    @cached_property
    def versions(self) -> AsyncVersionsWithRawResponse:
        return AsyncVersionsWithRawResponse(self._plugins.versions)

    @cached_property
    def installation_settings(self) -> AsyncInstallationSettingsWithRawResponse:
        return AsyncInstallationSettingsWithRawResponse(self._plugins.installation_settings)

    @cached_property
    def shares(self) -> AsyncSharesWithRawResponse:
        return AsyncSharesWithRawResponse(self._plugins.shares)


class PluginsWithStreamingResponse:
    def __init__(self, plugins: Plugins) -> None:
        self._plugins = plugins

        self.create = to_streamed_response_wrapper(
            plugins.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            plugins.retrieve,
        )
        self.update = to_streamed_response_wrapper(
            plugins.update,
        )
        self.list = to_streamed_response_wrapper(
            plugins.list,
        )
        self.delete = to_streamed_response_wrapper(
            plugins.delete,
        )

    @cached_property
    def versions(self) -> VersionsWithStreamingResponse:
        return VersionsWithStreamingResponse(self._plugins.versions)

    @cached_property
    def installation_settings(self) -> InstallationSettingsWithStreamingResponse:
        return InstallationSettingsWithStreamingResponse(self._plugins.installation_settings)

    @cached_property
    def shares(self) -> SharesWithStreamingResponse:
        return SharesWithStreamingResponse(self._plugins.shares)


class AsyncPluginsWithStreamingResponse:
    def __init__(self, plugins: AsyncPlugins) -> None:
        self._plugins = plugins

        self.create = async_to_streamed_response_wrapper(
            plugins.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            plugins.retrieve,
        )
        self.update = async_to_streamed_response_wrapper(
            plugins.update,
        )
        self.list = async_to_streamed_response_wrapper(
            plugins.list,
        )
        self.delete = async_to_streamed_response_wrapper(
            plugins.delete,
        )

    @cached_property
    def versions(self) -> AsyncVersionsWithStreamingResponse:
        return AsyncVersionsWithStreamingResponse(self._plugins.versions)

    @cached_property
    def installation_settings(self) -> AsyncInstallationSettingsWithStreamingResponse:
        return AsyncInstallationSettingsWithStreamingResponse(self._plugins.installation_settings)

    @cached_property
    def shares(self) -> AsyncSharesWithStreamingResponse:
        return AsyncSharesWithStreamingResponse(self._plugins.shares)
