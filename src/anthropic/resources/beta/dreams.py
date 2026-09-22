from __future__ import annotations

from typing import List, Union, Iterable, Optional
from datetime import datetime
from itertools import chain

import httpx2

from ..._types import Body, Omit, Query, Headers, NotGiven, omit, not_given
from ..._utils import is_given, path_template, strip_not_given
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ...pagination import SyncPageCursor, AsyncPageCursor
from ...types.beta import dream_create_params
from ..._base_client import AsyncPaginator, make_request_options
from ...types.beta.beta_dream import BetaDream
from ...types.anthropic_beta_param import AnthropicBetaParam
from ...types.beta.beta_dream_status import BetaDreamStatus
from ...types.beta.beta_dream_input_param import BetaDreamInputParam
from ...types.beta.beta_output_behavior_param import BetaOutputBehaviorParam

__all__ = ["Dreams", "AsyncDreams"]


class Dreams(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> DreamsWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#accessing-raw-response-data-eg-headers
        """
        return DreamsWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> DreamsWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#with_streaming_response
        """
        return DreamsWithStreamingResponse(self)

    def create(
        self,
        *,
        inputs: Iterable[BetaDreamInputParam],
        model: dream_create_params.Model,
        instructions: Optional[str] | Omit = omit,
        output_behavior: BetaOutputBehaviorParam | Omit = omit,
        betas: List[AnthropicBetaParam] | Omit = omit,
        workspace_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaDream:
        """
        Start an asynchronous job that uses past sessions to produce a reorganized
        version of a memory store and get back the dream to poll for the result.

        By default the dream writes its result to a new memory store and doesn't change
        the input memory store. The response has `status` set to `pending` and an empty
        `outputs` array. Poll the dream until `status` is `completed`, `failed`, or
        `canceled`.

        See the
        [Dreams guide](https://platform.claude.com/docs/en/managed-agents/dreams#create-a-dream)
        to learn more about creating dreams.

        Args:
          inputs: The memory store and sessions for the dream to read, as exactly one
              `memory_store` entry and exactly one `sessions` entry.

          model: The model that runs a dream, given as a model ID or as an object with `id` and
              `speed`.

              In the object form, `speed` can only be `standard`.

              The
              [limits table in the Dreams guide](https://platform.claude.com/docs/en/managed-agents/dreams#limits)
              lists the supported models.

          instructions: Guidance that steers how the dream reads the sessions and organizes the output
              memory store, from 1 to 4,096 characters.

              See the
              [Dreams guide](https://platform.claude.com/docs/en/managed-agents/dreams#steer-with-instructions)
              for what kinds of instructions work well.

          output_behavior: Which memory store a dream writes its result to. Defaults to `create_new` when
              left out of a create request.

          betas: Optional header to specify the beta version(s) you want to use.

          workspace_id: Optional header to select the Workspace for this request. The value is a
              Workspace ID (for example, `wrkspc_011CZkZaBF1tNoB5wlCeusgy`).

              Only needed for credentials that can act on more than one Workspace. A
              credential that belongs to a specific Workspace may omit it; if sent, it must
              match that Workspace.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {
            **strip_not_given(
                {
                    "anthropic-beta": ",".join(chain((str(e) for e in betas), ["dreaming-2026-04-21"]))
                    if is_given(betas)
                    else not_given,
                    "anthropic-workspace-id": workspace_id,
                }
            ),
            **(extra_headers or {}),
        }
        extra_headers = {"anthropic-beta": "dreaming-2026-04-21", **(extra_headers or {})}
        return self._post(
            "/v1/dreams?beta=true",
            body={
                "inputs": inputs,
                "model": model,
                "instructions": instructions,
                "output_behavior": output_behavior,
            },
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BetaDream,
        )

    def retrieve(
        self,
        dream_id: str,
        *,
        betas: List[AnthropicBetaParam] | Omit = omit,
        workspace_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaDream:
        """
        Get a dream by ID to check its status, output memory store, and token usage.

        Archived dreams are returned too.

        See the
        [Dreams guide](https://platform.claude.com/docs/en/managed-agents/dreams#track-progress)
        for how to poll a dream and what each status means.

        Args:
          dream_id: The ID of the dream to get (`drm_...`).

          betas: Optional header to specify the beta version(s) you want to use.

          workspace_id: Optional header to select the Workspace for this request. The value is a
              Workspace ID (for example, `wrkspc_011CZkZaBF1tNoB5wlCeusgy`).

              Only needed for credentials that can act on more than one Workspace. A
              credential that belongs to a specific Workspace may omit it; if sent, it must
              match that Workspace.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not dream_id:
            raise ValueError(f"Expected a non-empty value for `dream_id` but received {dream_id!r}")
        extra_headers = {
            **strip_not_given(
                {
                    "anthropic-beta": ",".join(chain((str(e) for e in betas), ["dreaming-2026-04-21"]))
                    if is_given(betas)
                    else not_given,
                    "anthropic-workspace-id": workspace_id,
                }
            ),
            **(extra_headers or {}),
        }
        extra_headers = {"anthropic-beta": "dreaming-2026-04-21", **(extra_headers or {})}
        return self._get(
            path_template("/v1/dreams/{dream_id}?beta=true", dream_id=dream_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BetaDream,
        )

    def list(
        self,
        *,
        created_at_gt: Union[str, datetime] | Omit = omit,
        created_at_lt: Union[str, datetime] | Omit = omit,
        include_archived: bool | Omit = omit,
        limit: int | Omit = omit,
        page: str | Omit = omit,
        statuses: List[BetaDreamStatus] | Omit = omit,
        betas: List[AnthropicBetaParam] | Omit = omit,
        workspace_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> SyncPageCursor[BetaDream]:
        """
        List the dreams in the workspace, newest first.

        Archived dreams are left out unless `include_archived` is `true`.

        See the
        [Dreams guide](https://platform.claude.com/docs/en/managed-agents/dreams#list-dreams)
        for how to page through dreams.

        Args:
          created_at_gt: Return only dreams created after this time (exclusive), in RFC 3339.

          created_at_lt: Return only dreams created before this time (exclusive), in RFC 3339.

          include_archived: Whether to include archived dreams. Defaults to `false`.

          limit: The maximum number of dreams to return, from 1 to 100. Defaults to 20.

          page: The cursor for the page to return, taken from `next_page` in a previous
              response.

              Leave it out to get the first page.

          statuses: Return only dreams that have one of these statuses.

              Repeat the parameter to give more than one status. Leave it out to return dreams
              of every status.

          betas: Optional header to specify the beta version(s) you want to use.

          workspace_id: Optional header to select the Workspace for this request. The value is a
              Workspace ID (for example, `wrkspc_011CZkZaBF1tNoB5wlCeusgy`).

              Only needed for credentials that can act on more than one Workspace. A
              credential that belongs to a specific Workspace may omit it; if sent, it must
              match that Workspace.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {
            **strip_not_given(
                {
                    "anthropic-beta": ",".join(chain((str(e) for e in betas), ["dreaming-2026-04-21"]))
                    if is_given(betas)
                    else not_given,
                    "anthropic-workspace-id": workspace_id,
                }
            ),
            **(extra_headers or {}),
        }
        extra_headers = {"anthropic-beta": "dreaming-2026-04-21", **(extra_headers or {})}
        return self._get_api_list(
            "/v1/dreams?beta=true",
            page=SyncPageCursor[BetaDream],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query={
                    "created_at[gt]": created_at_gt,
                    "created_at[lt]": created_at_lt,
                    "include_archived": include_archived,
                    "limit": limit,
                    "page": page,
                    "statuses": statuses,
                },
            ),
            model=BetaDream,
        )

    def archive(
        self,
        dream_id: str,
        *,
        betas: List[AnthropicBetaParam] | Omit = omit,
        workspace_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaDream:
        """
        Hide a `completed`, `failed`, or `canceled` dream from the default list of
        dreams.

        Archiving a `pending` or `running` dream returns a 400 error, so cancel it
        first. Archiving an archived dream returns it unchanged. An archived dream can
        still be fetched by ID. Archiving can't be undone.

        See the
        [Dreams guide](https://platform.claude.com/docs/en/managed-agents/dreams#archive-a-dream)
        to learn more about archiving dreams.

        Args:
          dream_id: The ID of the dream to archive (`drm_...`).

          betas: Optional header to specify the beta version(s) you want to use.

          workspace_id: Optional header to select the Workspace for this request. The value is a
              Workspace ID (for example, `wrkspc_011CZkZaBF1tNoB5wlCeusgy`).

              Only needed for credentials that can act on more than one Workspace. A
              credential that belongs to a specific Workspace may omit it; if sent, it must
              match that Workspace.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not dream_id:
            raise ValueError(f"Expected a non-empty value for `dream_id` but received {dream_id!r}")
        extra_headers = {
            **strip_not_given(
                {
                    "anthropic-beta": ",".join(chain((str(e) for e in betas), ["dreaming-2026-04-21"]))
                    if is_given(betas)
                    else not_given,
                    "anthropic-workspace-id": workspace_id,
                }
            ),
            **(extra_headers or {}),
        }
        extra_headers = {"anthropic-beta": "dreaming-2026-04-21", **(extra_headers or {})}
        return self._post(
            path_template("/v1/dreams/{dream_id}/archive?beta=true", dream_id=dream_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BetaDream,
        )

    def cancel(
        self,
        dream_id: str,
        *,
        betas: List[AnthropicBetaParam] | Omit = omit,
        workspace_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaDream:
        """
        Stop a `pending` or `running` dream.

        The response shows `status` as `canceled`, unless the dream reached `completed`
        or `failed` first. `usage` can keep changing after the response. Canceling a
        `canceled` dream returns it unchanged. Canceling a `completed` or `failed` dream
        returns a 400 error.

        See the
        [Dreams guide](https://platform.claude.com/docs/en/managed-agents/dreams#cancel-a-dream)
        to learn more about canceling dreams.

        Args:
          dream_id: The ID of the dream to cancel (`drm_...`).

          betas: Optional header to specify the beta version(s) you want to use.

          workspace_id: Optional header to select the Workspace for this request. The value is a
              Workspace ID (for example, `wrkspc_011CZkZaBF1tNoB5wlCeusgy`).

              Only needed for credentials that can act on more than one Workspace. A
              credential that belongs to a specific Workspace may omit it; if sent, it must
              match that Workspace.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not dream_id:
            raise ValueError(f"Expected a non-empty value for `dream_id` but received {dream_id!r}")
        extra_headers = {
            **strip_not_given(
                {
                    "anthropic-beta": ",".join(chain((str(e) for e in betas), ["dreaming-2026-04-21"]))
                    if is_given(betas)
                    else not_given,
                    "anthropic-workspace-id": workspace_id,
                }
            ),
            **(extra_headers or {}),
        }
        extra_headers = {"anthropic-beta": "dreaming-2026-04-21", **(extra_headers or {})}
        return self._post(
            path_template("/v1/dreams/{dream_id}/cancel?beta=true", dream_id=dream_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BetaDream,
        )


class AsyncDreams(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncDreamsWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#accessing-raw-response-data-eg-headers
        """
        return AsyncDreamsWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncDreamsWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#with_streaming_response
        """
        return AsyncDreamsWithStreamingResponse(self)

    async def create(
        self,
        *,
        inputs: Iterable[BetaDreamInputParam],
        model: dream_create_params.Model,
        instructions: Optional[str] | Omit = omit,
        output_behavior: BetaOutputBehaviorParam | Omit = omit,
        betas: List[AnthropicBetaParam] | Omit = omit,
        workspace_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaDream:
        """
        Start an asynchronous job that uses past sessions to produce a reorganized
        version of a memory store and get back the dream to poll for the result.

        By default the dream writes its result to a new memory store and doesn't change
        the input memory store. The response has `status` set to `pending` and an empty
        `outputs` array. Poll the dream until `status` is `completed`, `failed`, or
        `canceled`.

        See the
        [Dreams guide](https://platform.claude.com/docs/en/managed-agents/dreams#create-a-dream)
        to learn more about creating dreams.

        Args:
          inputs: The memory store and sessions for the dream to read, as exactly one
              `memory_store` entry and exactly one `sessions` entry.

          model: The model that runs a dream, given as a model ID or as an object with `id` and
              `speed`.

              In the object form, `speed` can only be `standard`.

              The
              [limits table in the Dreams guide](https://platform.claude.com/docs/en/managed-agents/dreams#limits)
              lists the supported models.

          instructions: Guidance that steers how the dream reads the sessions and organizes the output
              memory store, from 1 to 4,096 characters.

              See the
              [Dreams guide](https://platform.claude.com/docs/en/managed-agents/dreams#steer-with-instructions)
              for what kinds of instructions work well.

          output_behavior: Which memory store a dream writes its result to. Defaults to `create_new` when
              left out of a create request.

          betas: Optional header to specify the beta version(s) you want to use.

          workspace_id: Optional header to select the Workspace for this request. The value is a
              Workspace ID (for example, `wrkspc_011CZkZaBF1tNoB5wlCeusgy`).

              Only needed for credentials that can act on more than one Workspace. A
              credential that belongs to a specific Workspace may omit it; if sent, it must
              match that Workspace.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {
            **strip_not_given(
                {
                    "anthropic-beta": ",".join(chain((str(e) for e in betas), ["dreaming-2026-04-21"]))
                    if is_given(betas)
                    else not_given,
                    "anthropic-workspace-id": workspace_id,
                }
            ),
            **(extra_headers or {}),
        }
        extra_headers = {"anthropic-beta": "dreaming-2026-04-21", **(extra_headers or {})}
        return await self._post(
            "/v1/dreams?beta=true",
            body={
                "inputs": inputs,
                "model": model,
                "instructions": instructions,
                "output_behavior": output_behavior,
            },
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BetaDream,
        )

    async def retrieve(
        self,
        dream_id: str,
        *,
        betas: List[AnthropicBetaParam] | Omit = omit,
        workspace_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaDream:
        """
        Get a dream by ID to check its status, output memory store, and token usage.

        Archived dreams are returned too.

        See the
        [Dreams guide](https://platform.claude.com/docs/en/managed-agents/dreams#track-progress)
        for how to poll a dream and what each status means.

        Args:
          dream_id: The ID of the dream to get (`drm_...`).

          betas: Optional header to specify the beta version(s) you want to use.

          workspace_id: Optional header to select the Workspace for this request. The value is a
              Workspace ID (for example, `wrkspc_011CZkZaBF1tNoB5wlCeusgy`).

              Only needed for credentials that can act on more than one Workspace. A
              credential that belongs to a specific Workspace may omit it; if sent, it must
              match that Workspace.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not dream_id:
            raise ValueError(f"Expected a non-empty value for `dream_id` but received {dream_id!r}")
        extra_headers = {
            **strip_not_given(
                {
                    "anthropic-beta": ",".join(chain((str(e) for e in betas), ["dreaming-2026-04-21"]))
                    if is_given(betas)
                    else not_given,
                    "anthropic-workspace-id": workspace_id,
                }
            ),
            **(extra_headers or {}),
        }
        extra_headers = {"anthropic-beta": "dreaming-2026-04-21", **(extra_headers or {})}
        return await self._get(
            path_template("/v1/dreams/{dream_id}?beta=true", dream_id=dream_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BetaDream,
        )

    def list(
        self,
        *,
        created_at_gt: Union[str, datetime] | Omit = omit,
        created_at_lt: Union[str, datetime] | Omit = omit,
        include_archived: bool | Omit = omit,
        limit: int | Omit = omit,
        page: str | Omit = omit,
        statuses: List[BetaDreamStatus] | Omit = omit,
        betas: List[AnthropicBetaParam] | Omit = omit,
        workspace_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> AsyncPaginator[BetaDream, AsyncPageCursor[BetaDream]]:
        """
        List the dreams in the workspace, newest first.

        Archived dreams are left out unless `include_archived` is `true`.

        See the
        [Dreams guide](https://platform.claude.com/docs/en/managed-agents/dreams#list-dreams)
        for how to page through dreams.

        Args:
          created_at_gt: Return only dreams created after this time (exclusive), in RFC 3339.

          created_at_lt: Return only dreams created before this time (exclusive), in RFC 3339.

          include_archived: Whether to include archived dreams. Defaults to `false`.

          limit: The maximum number of dreams to return, from 1 to 100. Defaults to 20.

          page: The cursor for the page to return, taken from `next_page` in a previous
              response.

              Leave it out to get the first page.

          statuses: Return only dreams that have one of these statuses.

              Repeat the parameter to give more than one status. Leave it out to return dreams
              of every status.

          betas: Optional header to specify the beta version(s) you want to use.

          workspace_id: Optional header to select the Workspace for this request. The value is a
              Workspace ID (for example, `wrkspc_011CZkZaBF1tNoB5wlCeusgy`).

              Only needed for credentials that can act on more than one Workspace. A
              credential that belongs to a specific Workspace may omit it; if sent, it must
              match that Workspace.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {
            **strip_not_given(
                {
                    "anthropic-beta": ",".join(chain((str(e) for e in betas), ["dreaming-2026-04-21"]))
                    if is_given(betas)
                    else not_given,
                    "anthropic-workspace-id": workspace_id,
                }
            ),
            **(extra_headers or {}),
        }
        extra_headers = {"anthropic-beta": "dreaming-2026-04-21", **(extra_headers or {})}
        return self._get_api_list(
            "/v1/dreams?beta=true",
            page=AsyncPageCursor[BetaDream],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query={
                    "created_at[gt]": created_at_gt,
                    "created_at[lt]": created_at_lt,
                    "include_archived": include_archived,
                    "limit": limit,
                    "page": page,
                    "statuses": statuses,
                },
            ),
            model=BetaDream,
        )

    async def archive(
        self,
        dream_id: str,
        *,
        betas: List[AnthropicBetaParam] | Omit = omit,
        workspace_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaDream:
        """
        Hide a `completed`, `failed`, or `canceled` dream from the default list of
        dreams.

        Archiving a `pending` or `running` dream returns a 400 error, so cancel it
        first. Archiving an archived dream returns it unchanged. An archived dream can
        still be fetched by ID. Archiving can't be undone.

        See the
        [Dreams guide](https://platform.claude.com/docs/en/managed-agents/dreams#archive-a-dream)
        to learn more about archiving dreams.

        Args:
          dream_id: The ID of the dream to archive (`drm_...`).

          betas: Optional header to specify the beta version(s) you want to use.

          workspace_id: Optional header to select the Workspace for this request. The value is a
              Workspace ID (for example, `wrkspc_011CZkZaBF1tNoB5wlCeusgy`).

              Only needed for credentials that can act on more than one Workspace. A
              credential that belongs to a specific Workspace may omit it; if sent, it must
              match that Workspace.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not dream_id:
            raise ValueError(f"Expected a non-empty value for `dream_id` but received {dream_id!r}")
        extra_headers = {
            **strip_not_given(
                {
                    "anthropic-beta": ",".join(chain((str(e) for e in betas), ["dreaming-2026-04-21"]))
                    if is_given(betas)
                    else not_given,
                    "anthropic-workspace-id": workspace_id,
                }
            ),
            **(extra_headers or {}),
        }
        extra_headers = {"anthropic-beta": "dreaming-2026-04-21", **(extra_headers or {})}
        return await self._post(
            path_template("/v1/dreams/{dream_id}/archive?beta=true", dream_id=dream_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BetaDream,
        )

    async def cancel(
        self,
        dream_id: str,
        *,
        betas: List[AnthropicBetaParam] | Omit = omit,
        workspace_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaDream:
        """
        Stop a `pending` or `running` dream.

        The response shows `status` as `canceled`, unless the dream reached `completed`
        or `failed` first. `usage` can keep changing after the response. Canceling a
        `canceled` dream returns it unchanged. Canceling a `completed` or `failed` dream
        returns a 400 error.

        See the
        [Dreams guide](https://platform.claude.com/docs/en/managed-agents/dreams#cancel-a-dream)
        to learn more about canceling dreams.

        Args:
          dream_id: The ID of the dream to cancel (`drm_...`).

          betas: Optional header to specify the beta version(s) you want to use.

          workspace_id: Optional header to select the Workspace for this request. The value is a
              Workspace ID (for example, `wrkspc_011CZkZaBF1tNoB5wlCeusgy`).

              Only needed for credentials that can act on more than one Workspace. A
              credential that belongs to a specific Workspace may omit it; if sent, it must
              match that Workspace.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not dream_id:
            raise ValueError(f"Expected a non-empty value for `dream_id` but received {dream_id!r}")
        extra_headers = {
            **strip_not_given(
                {
                    "anthropic-beta": ",".join(chain((str(e) for e in betas), ["dreaming-2026-04-21"]))
                    if is_given(betas)
                    else not_given,
                    "anthropic-workspace-id": workspace_id,
                }
            ),
            **(extra_headers or {}),
        }
        extra_headers = {"anthropic-beta": "dreaming-2026-04-21", **(extra_headers or {})}
        return await self._post(
            path_template("/v1/dreams/{dream_id}/cancel?beta=true", dream_id=dream_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BetaDream,
        )


class DreamsWithRawResponse:
    def __init__(self, dreams: Dreams) -> None:
        self._dreams = dreams

        self.create = to_raw_response_wrapper(
            dreams.create,
        )
        self.retrieve = to_raw_response_wrapper(
            dreams.retrieve,
        )
        self.list = to_raw_response_wrapper(
            dreams.list,
        )
        self.archive = to_raw_response_wrapper(
            dreams.archive,
        )
        self.cancel = to_raw_response_wrapper(
            dreams.cancel,
        )


class AsyncDreamsWithRawResponse:
    def __init__(self, dreams: AsyncDreams) -> None:
        self._dreams = dreams

        self.create = async_to_raw_response_wrapper(
            dreams.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            dreams.retrieve,
        )
        self.list = async_to_raw_response_wrapper(
            dreams.list,
        )
        self.archive = async_to_raw_response_wrapper(
            dreams.archive,
        )
        self.cancel = async_to_raw_response_wrapper(
            dreams.cancel,
        )


class DreamsWithStreamingResponse:
    def __init__(self, dreams: Dreams) -> None:
        self._dreams = dreams

        self.create = to_streamed_response_wrapper(
            dreams.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            dreams.retrieve,
        )
        self.list = to_streamed_response_wrapper(
            dreams.list,
        )
        self.archive = to_streamed_response_wrapper(
            dreams.archive,
        )
        self.cancel = to_streamed_response_wrapper(
            dreams.cancel,
        )


class AsyncDreamsWithStreamingResponse:
    def __init__(self, dreams: AsyncDreams) -> None:
        self._dreams = dreams

        self.create = async_to_streamed_response_wrapper(
            dreams.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            dreams.retrieve,
        )
        self.list = async_to_streamed_response_wrapper(
            dreams.list,
        )
        self.archive = async_to_streamed_response_wrapper(
            dreams.archive,
        )
        self.cancel = async_to_streamed_response_wrapper(
            dreams.cancel,
        )
