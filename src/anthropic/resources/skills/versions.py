# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Mapping, Optional, cast

import httpx2

from ..._files import deepcopy_with_paths
from ..._types import (
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
from ..._utils import extract_files, path_template, maybe_transform, async_maybe_transform
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ...pagination import SyncPageCursor, AsyncPageCursor
from ..._base_client import AsyncPaginator, make_request_options
from ...types.skills import version_list_params, version_create_params
from ...types.skills.skill_version import SkillVersion
from ...types.skills.deleted_skill_version import DeletedSkillVersion

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
        skill_id: str,
        *,
        files: SequenceNotStr[FileTypes],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> SkillVersion:
        """
        Create Skill Version

        Args:
          skill_id: Unique identifier for the skill.

              The format and length of IDs may change over time.

          files: Files to upload for the skill.

              All files must be in the same top-level directory and must include a SKILL.md
              file at the root of that directory.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not skill_id:
            raise ValueError(f"Expected a non-empty value for `skill_id` but received {skill_id!r}")
        body = deepcopy_with_paths({"files": files}, [["files", "<array>"]])
        extracted_files = extract_files(cast(Mapping[str, object], body), paths=[["files", "<array>"]])
        # It should be noted that the actual Content-Type header that will be
        # sent to the server will contain a `boundary` parameter, e.g.
        # multipart/form-data; boundary=---abc--
        extra_headers = {"Content-Type": "multipart/form-data", **(extra_headers or {})}
        return self._post(
            path_template("/v1/skills/{skill_id}/versions", skill_id=skill_id),
            body=maybe_transform(body, version_create_params.VersionCreateParams),
            files=extracted_files,
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SkillVersion,
        )

    def retrieve(
        self,
        version: str,
        *,
        skill_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> SkillVersion:
        """
        Get Skill Version

        Args:
          skill_id: Unique identifier for the skill.

              The format and length of IDs may change over time.

          version: Identifies the skill version: a version ID, or — where the endpoint accepts it —
              the literal `latest` for the skill's most recent version.

              Requests carrying the `skills-2025-10-02` beta header address versions by their
              Unix epoch timestamp instead (e.g., "1759178010641129").

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not skill_id:
            raise ValueError(f"Expected a non-empty value for `skill_id` but received {skill_id!r}")
        if not version:
            raise ValueError(f"Expected a non-empty value for `version` but received {version!r}")
        return self._get(
            path_template("/v1/skills/{skill_id}/versions/{version}", skill_id=skill_id, version=version),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SkillVersion,
        )

    def list(
        self,
        skill_id: str,
        *,
        limit: Optional[int] | Omit = omit,
        page: Optional[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> SyncPageCursor[SkillVersion]:
        """
        List Skill Versions

        Args:
          skill_id: Unique identifier for the skill.

              The format and length of IDs may change over time.

          limit: Number of results to return per page.

              Ranges from `1` to `1000`. Defaults to `20`.

          page: Optionally set to the `next_page` token from the previous response.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not skill_id:
            raise ValueError(f"Expected a non-empty value for `skill_id` but received {skill_id!r}")
        return self._get_api_list(
            path_template("/v1/skills/{skill_id}/versions", skill_id=skill_id),
            page=SyncPageCursor[SkillVersion],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "limit": limit,
                        "page": page,
                    },
                    version_list_params.VersionListParams,
                ),
            ),
            model=SkillVersion,
        )

    def delete(
        self,
        version: str,
        *,
        skill_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> DeletedSkillVersion:
        """
        Delete Skill Version

        Args:
          skill_id: Unique identifier for the skill.

              The format and length of IDs may change over time.

          version: Identifies the skill version: a version ID, or — where the endpoint accepts it —
              the literal `latest` for the skill's most recent version.

              Requests carrying the `skills-2025-10-02` beta header address versions by their
              Unix epoch timestamp instead (e.g., "1759178010641129").

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not skill_id:
            raise ValueError(f"Expected a non-empty value for `skill_id` but received {skill_id!r}")
        if not version:
            raise ValueError(f"Expected a non-empty value for `version` but received {version!r}")
        return self._delete(
            path_template("/v1/skills/{skill_id}/versions/{version}", skill_id=skill_id, version=version),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DeletedSkillVersion,
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
        skill_id: str,
        *,
        files: SequenceNotStr[FileTypes],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> SkillVersion:
        """
        Create Skill Version

        Args:
          skill_id: Unique identifier for the skill.

              The format and length of IDs may change over time.

          files: Files to upload for the skill.

              All files must be in the same top-level directory and must include a SKILL.md
              file at the root of that directory.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not skill_id:
            raise ValueError(f"Expected a non-empty value for `skill_id` but received {skill_id!r}")
        body = deepcopy_with_paths({"files": files}, [["files", "<array>"]])
        extracted_files = extract_files(cast(Mapping[str, object], body), paths=[["files", "<array>"]])
        # It should be noted that the actual Content-Type header that will be
        # sent to the server will contain a `boundary` parameter, e.g.
        # multipart/form-data; boundary=---abc--
        extra_headers = {"Content-Type": "multipart/form-data", **(extra_headers or {})}
        return await self._post(
            path_template("/v1/skills/{skill_id}/versions", skill_id=skill_id),
            body=await async_maybe_transform(body, version_create_params.VersionCreateParams),
            files=extracted_files,
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SkillVersion,
        )

    async def retrieve(
        self,
        version: str,
        *,
        skill_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> SkillVersion:
        """
        Get Skill Version

        Args:
          skill_id: Unique identifier for the skill.

              The format and length of IDs may change over time.

          version: Identifies the skill version: a version ID, or — where the endpoint accepts it —
              the literal `latest` for the skill's most recent version.

              Requests carrying the `skills-2025-10-02` beta header address versions by their
              Unix epoch timestamp instead (e.g., "1759178010641129").

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not skill_id:
            raise ValueError(f"Expected a non-empty value for `skill_id` but received {skill_id!r}")
        if not version:
            raise ValueError(f"Expected a non-empty value for `version` but received {version!r}")
        return await self._get(
            path_template("/v1/skills/{skill_id}/versions/{version}", skill_id=skill_id, version=version),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SkillVersion,
        )

    def list(
        self,
        skill_id: str,
        *,
        limit: Optional[int] | Omit = omit,
        page: Optional[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> AsyncPaginator[SkillVersion, AsyncPageCursor[SkillVersion]]:
        """
        List Skill Versions

        Args:
          skill_id: Unique identifier for the skill.

              The format and length of IDs may change over time.

          limit: Number of results to return per page.

              Ranges from `1` to `1000`. Defaults to `20`.

          page: Optionally set to the `next_page` token from the previous response.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not skill_id:
            raise ValueError(f"Expected a non-empty value for `skill_id` but received {skill_id!r}")
        return self._get_api_list(
            path_template("/v1/skills/{skill_id}/versions", skill_id=skill_id),
            page=AsyncPageCursor[SkillVersion],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "limit": limit,
                        "page": page,
                    },
                    version_list_params.VersionListParams,
                ),
            ),
            model=SkillVersion,
        )

    async def delete(
        self,
        version: str,
        *,
        skill_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> DeletedSkillVersion:
        """
        Delete Skill Version

        Args:
          skill_id: Unique identifier for the skill.

              The format and length of IDs may change over time.

          version: Identifies the skill version: a version ID, or — where the endpoint accepts it —
              the literal `latest` for the skill's most recent version.

              Requests carrying the `skills-2025-10-02` beta header address versions by their
              Unix epoch timestamp instead (e.g., "1759178010641129").

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not skill_id:
            raise ValueError(f"Expected a non-empty value for `skill_id` but received {skill_id!r}")
        if not version:
            raise ValueError(f"Expected a non-empty value for `version` but received {version!r}")
        return await self._delete(
            path_template("/v1/skills/{skill_id}/versions/{version}", skill_id=skill_id, version=version),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DeletedSkillVersion,
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
        self.delete = to_raw_response_wrapper(
            versions.delete,
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
        self.delete = async_to_raw_response_wrapper(
            versions.delete,
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
        self.delete = to_streamed_response_wrapper(
            versions.delete,
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
        self.delete = async_to_streamed_response_wrapper(
            versions.delete,
        )
