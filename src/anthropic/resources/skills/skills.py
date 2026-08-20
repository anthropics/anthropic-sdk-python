# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Mapping, Optional, cast

import httpx2

from ...types import skill_list_params, skill_create_params
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
from .versions import (
    Versions,
    AsyncVersions,
    VersionsWithRawResponse,
    AsyncVersionsWithRawResponse,
    VersionsWithStreamingResponse,
    AsyncVersionsWithStreamingResponse,
)
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ...pagination import SyncPageCursor, AsyncPageCursor
from ...types.skill import Skill
from ..._base_client import AsyncPaginator, make_request_options
from ...types.deleted_skill import DeletedSkill

__all__ = ["Skills", "AsyncSkills"]


class Skills(SyncAPIResource):
    @cached_property
    def versions(self) -> Versions:
        return Versions(self._client)

    @cached_property
    def with_raw_response(self) -> SkillsWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#accessing-raw-response-data-eg-headers
        """
        return SkillsWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> SkillsWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#with_streaming_response
        """
        return SkillsWithStreamingResponse(self)

    def create(
        self,
        *,
        files: SequenceNotStr[FileTypes],
        display_name: Optional[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> Skill:
        """
        Create Skill

        Args:
          files: Files to upload for the skill.

              All files must be in the same top-level directory and must include a SKILL.md
              file at the root of that directory.

          display_name: Human-readable, single-line label for the Skill. Maximum 255 characters. Always
              set: derived from the SKILL.md frontmatter `name` when omitted at creation. Not
              unique.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        body = deepcopy_with_paths(
            {
                "files": files,
                "display_name": display_name,
            },
            [["files", "<array>"]],
        )
        extracted_files = extract_files(cast(Mapping[str, object], body), paths=[["files", "<array>"]])
        # It should be noted that the actual Content-Type header that will be
        # sent to the server will contain a `boundary` parameter, e.g.
        # multipart/form-data; boundary=---abc--
        extra_headers = {"Content-Type": "multipart/form-data", **(extra_headers or {})}
        return self._post(
            "/v1/skills",
            body=maybe_transform(body, skill_create_params.SkillCreateParams),
            files=extracted_files,
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Skill,
        )

    def retrieve(
        self,
        skill_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> Skill:
        """
        Get Skill

        Args:
          skill_id: Unique identifier for the skill.

              The format and length of IDs may change over time.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not skill_id:
            raise ValueError(f"Expected a non-empty value for `skill_id` but received {skill_id!r}")
        return self._get(
            path_template("/v1/skills/{skill_id}", skill_id=skill_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Skill,
        )

    def list(
        self,
        *,
        limit: int | Omit = omit,
        page: Optional[str] | Omit = omit,
        source: Optional[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> SyncPageCursor[Skill]:
        """
        List Skills

        Args:
          limit: Number of results to return per page.

              Ranges from `1` to `1000`. Defaults to `20`.

          page: Pagination token for fetching a specific page of results.

              Pass the value from a previous response's `next_page` field to get the next page
              of results.

          source: Filter skills by source.

              If provided, only skills from the specified source will be returned:

              - `"custom"`: only return user-created skills
              - `"anthropic"`: only return Anthropic-created skills

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/v1/skills",
            page=SyncPageCursor[Skill],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "limit": limit,
                        "page": page,
                        "source": source,
                    },
                    skill_list_params.SkillListParams,
                ),
            ),
            model=Skill,
        )

    def delete(
        self,
        skill_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> DeletedSkill:
        """
        Delete Skill

        Args:
          skill_id: Unique identifier for the skill.

              The format and length of IDs may change over time.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not skill_id:
            raise ValueError(f"Expected a non-empty value for `skill_id` but received {skill_id!r}")
        return self._delete(
            path_template("/v1/skills/{skill_id}", skill_id=skill_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DeletedSkill,
        )


class AsyncSkills(AsyncAPIResource):
    @cached_property
    def versions(self) -> AsyncVersions:
        return AsyncVersions(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncSkillsWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#accessing-raw-response-data-eg-headers
        """
        return AsyncSkillsWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncSkillsWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#with_streaming_response
        """
        return AsyncSkillsWithStreamingResponse(self)

    async def create(
        self,
        *,
        files: SequenceNotStr[FileTypes],
        display_name: Optional[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> Skill:
        """
        Create Skill

        Args:
          files: Files to upload for the skill.

              All files must be in the same top-level directory and must include a SKILL.md
              file at the root of that directory.

          display_name: Human-readable, single-line label for the Skill. Maximum 255 characters. Always
              set: derived from the SKILL.md frontmatter `name` when omitted at creation. Not
              unique.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        body = deepcopy_with_paths(
            {
                "files": files,
                "display_name": display_name,
            },
            [["files", "<array>"]],
        )
        extracted_files = extract_files(cast(Mapping[str, object], body), paths=[["files", "<array>"]])
        # It should be noted that the actual Content-Type header that will be
        # sent to the server will contain a `boundary` parameter, e.g.
        # multipart/form-data; boundary=---abc--
        extra_headers = {"Content-Type": "multipart/form-data", **(extra_headers or {})}
        return await self._post(
            "/v1/skills",
            body=await async_maybe_transform(body, skill_create_params.SkillCreateParams),
            files=extracted_files,
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Skill,
        )

    async def retrieve(
        self,
        skill_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> Skill:
        """
        Get Skill

        Args:
          skill_id: Unique identifier for the skill.

              The format and length of IDs may change over time.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not skill_id:
            raise ValueError(f"Expected a non-empty value for `skill_id` but received {skill_id!r}")
        return await self._get(
            path_template("/v1/skills/{skill_id}", skill_id=skill_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Skill,
        )

    def list(
        self,
        *,
        limit: int | Omit = omit,
        page: Optional[str] | Omit = omit,
        source: Optional[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> AsyncPaginator[Skill, AsyncPageCursor[Skill]]:
        """
        List Skills

        Args:
          limit: Number of results to return per page.

              Ranges from `1` to `1000`. Defaults to `20`.

          page: Pagination token for fetching a specific page of results.

              Pass the value from a previous response's `next_page` field to get the next page
              of results.

          source: Filter skills by source.

              If provided, only skills from the specified source will be returned:

              - `"custom"`: only return user-created skills
              - `"anthropic"`: only return Anthropic-created skills

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/v1/skills",
            page=AsyncPageCursor[Skill],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "limit": limit,
                        "page": page,
                        "source": source,
                    },
                    skill_list_params.SkillListParams,
                ),
            ),
            model=Skill,
        )

    async def delete(
        self,
        skill_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> DeletedSkill:
        """
        Delete Skill

        Args:
          skill_id: Unique identifier for the skill.

              The format and length of IDs may change over time.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not skill_id:
            raise ValueError(f"Expected a non-empty value for `skill_id` but received {skill_id!r}")
        return await self._delete(
            path_template("/v1/skills/{skill_id}", skill_id=skill_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DeletedSkill,
        )


class SkillsWithRawResponse:
    def __init__(self, skills: Skills) -> None:
        self._skills = skills

        self.create = to_raw_response_wrapper(
            skills.create,
        )
        self.retrieve = to_raw_response_wrapper(
            skills.retrieve,
        )
        self.list = to_raw_response_wrapper(
            skills.list,
        )
        self.delete = to_raw_response_wrapper(
            skills.delete,
        )

    @cached_property
    def versions(self) -> VersionsWithRawResponse:
        return VersionsWithRawResponse(self._skills.versions)


class AsyncSkillsWithRawResponse:
    def __init__(self, skills: AsyncSkills) -> None:
        self._skills = skills

        self.create = async_to_raw_response_wrapper(
            skills.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            skills.retrieve,
        )
        self.list = async_to_raw_response_wrapper(
            skills.list,
        )
        self.delete = async_to_raw_response_wrapper(
            skills.delete,
        )

    @cached_property
    def versions(self) -> AsyncVersionsWithRawResponse:
        return AsyncVersionsWithRawResponse(self._skills.versions)


class SkillsWithStreamingResponse:
    def __init__(self, skills: Skills) -> None:
        self._skills = skills

        self.create = to_streamed_response_wrapper(
            skills.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            skills.retrieve,
        )
        self.list = to_streamed_response_wrapper(
            skills.list,
        )
        self.delete = to_streamed_response_wrapper(
            skills.delete,
        )

    @cached_property
    def versions(self) -> VersionsWithStreamingResponse:
        return VersionsWithStreamingResponse(self._skills.versions)


class AsyncSkillsWithStreamingResponse:
    def __init__(self, skills: AsyncSkills) -> None:
        self._skills = skills

        self.create = async_to_streamed_response_wrapper(
            skills.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            skills.retrieve,
        )
        self.list = async_to_streamed_response_wrapper(
            skills.list,
        )
        self.delete = async_to_streamed_response_wrapper(
            skills.delete,
        )

    @cached_property
    def versions(self) -> AsyncVersionsWithStreamingResponse:
        return AsyncVersionsWithStreamingResponse(self._skills.versions)
