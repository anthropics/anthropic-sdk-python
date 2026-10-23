from __future__ import annotations

from typing import Any, List, Optional, cast
from itertools import chain

import httpx2

from ...._types import Body, Omit, Query, Headers, NotGiven, omit, not_given
from ...._utils import is_given, path_template, strip_not_given
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
from ....types.beta.memory_stores import (
    BetaManagedAgentsMemoryView,
)
from ....types.anthropic_beta_param import AnthropicBetaParam
from ....types.beta.memory_stores.beta_managed_agents_memory import BetaManagedAgentsMemory
from ....types.beta.memory_stores.beta_managed_agents_memory_view import BetaManagedAgentsMemoryView
from ....types.beta.memory_stores.beta_managed_agents_deleted_memory import BetaManagedAgentsDeletedMemory
from ....types.beta.memory_stores.beta_managed_agents_memory_list_item import BetaManagedAgentsMemoryListItem
from ....types.beta.memory_stores.beta_managed_agents_precondition_param import BetaManagedAgentsPreconditionParam

__all__ = ["Memories", "AsyncMemories"]


class Memories(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> MemoriesWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#accessing-raw-response-data-eg-headers
        """
        return MemoriesWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> MemoriesWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#with_streaming_response
        """
        return MemoriesWithStreamingResponse(self)

    def create(
        self,
        memory_store_id: str,
        *,
        content: Optional[str],
        path: str,
        view: BetaManagedAgentsMemoryView | Omit = omit,
        betas: List[AnthropicBetaParam] | Omit = omit,
        workspace_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaManagedAgentsMemory:
        """
        Create a Memory

        Args:
          memory_store_id: The ID of the memory store to create the memory in (`memstore_...`).

          content: The UTF-8 text content of the new memory. Pass `""` to create an empty memory.

              The maximum size is 100 kB (102,400 bytes).

          path: The path of the new memory, such as `/projects/foo/notes.md`. Paths are
              case-sensitive.

              A path starts with `/` and has 1 to 20 segments. A segment can't be empty and
              can't be `.` or `..`. A path can't contain control characters, format
              characters, or the line and paragraph separators U+2028 and U+2029. It must be
              in Unicode Normalization Form C and at most 1,024 bytes long.

          view: Whether a `memory` or `memory_version` in the response includes its `content`.
              Defaults to `full` on retrieve operations and to `basic` on list, create, and
              update operations.

              With `full`, list operations return at most 20 items per page.

          betas: This endpoint is in beta: requests must send `agent-memory-2026-07-22` or
              `managed-agents-2026-04-01` in this header.

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
        if not memory_store_id:
            raise ValueError(f"Expected a non-empty value for `memory_store_id` but received {memory_store_id!r}")
        extra_headers = {
            **strip_not_given(
                {
                    "anthropic-beta": ",".join(chain((str(e) for e in betas), ["agent-memory-2026-07-22"]))
                    if is_given(betas)
                    else not_given,
                    "anthropic-workspace-id": workspace_id,
                }
            ),
            **(extra_headers or {}),
        }
        extra_headers = {"anthropic-beta": "agent-memory-2026-07-22", **(extra_headers or {})}
        return self._post(
            path_template("/v1/memory_stores/{memory_store_id}/memories", memory_store_id=memory_store_id),
            body={
                "content": content,
                "path": path,
            },
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query={"view": view},
                qualifiers={"beta": "true"},
                span_name="anthropic.memory_stores.memories.create",
                span_route="/v1/memory_stores/{memory_store_id}/memories",
                span_attributes={"gen_ai.memory.store.id": memory_store_id},
                span_created_id="gen_ai.memory.record.id",
            ),
            cast_to=BetaManagedAgentsMemory,
        )

    def retrieve(
        self,
        memory_id: str,
        *,
        memory_store_id: str,
        view: BetaManagedAgentsMemoryView | Omit = omit,
        betas: List[AnthropicBetaParam] | Omit = omit,
        workspace_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaManagedAgentsMemory:
        """
        Retrieve a Memory

        Args:
          memory_store_id: The ID of the memory store that holds the memory (`memstore_...`).

          memory_id: The ID of the memory to retrieve (`mem_...`).

          view: Whether a `memory` or `memory_version` in the response includes its `content`.
              Defaults to `full` on retrieve operations and to `basic` on list, create, and
              update operations.

              With `full`, list operations return at most 20 items per page.

          betas: This endpoint is in beta: requests must send `agent-memory-2026-07-22` or
              `managed-agents-2026-04-01` in this header.

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
        if not memory_store_id:
            raise ValueError(f"Expected a non-empty value for `memory_store_id` but received {memory_store_id!r}")
        if not memory_id:
            raise ValueError(f"Expected a non-empty value for `memory_id` but received {memory_id!r}")
        extra_headers = {
            **strip_not_given(
                {
                    "anthropic-beta": ",".join(chain((str(e) for e in betas), ["agent-memory-2026-07-22"]))
                    if is_given(betas)
                    else not_given,
                    "anthropic-workspace-id": workspace_id,
                }
            ),
            **(extra_headers or {}),
        }
        extra_headers = {"anthropic-beta": "agent-memory-2026-07-22", **(extra_headers or {})}
        return self._get(
            path_template(
                "/v1/memory_stores/{memory_store_id}/memories/{memory_id}",
                memory_store_id=memory_store_id,
                memory_id=memory_id,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query={"view": view},
                qualifiers={"beta": "true"},
                span_name="anthropic.memory_stores.memories.retrieve",
                span_route="/v1/memory_stores/{memory_store_id}/memories/{memory_id}",
                span_attributes={"gen_ai.memory.store.id": memory_store_id, "gen_ai.memory.record.id": memory_id},
            ),
            cast_to=BetaManagedAgentsMemory,
        )

    def update(
        self,
        memory_id: str,
        *,
        memory_store_id: str,
        view: BetaManagedAgentsMemoryView | Omit = omit,
        content: Optional[str] | Omit = omit,
        path: Optional[str] | Omit = omit,
        precondition: BetaManagedAgentsPreconditionParam | Omit = omit,
        betas: List[AnthropicBetaParam] | Omit = omit,
        workspace_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaManagedAgentsMemory:
        """
        Update a Memory

        Args:
          memory_store_id: The ID of the memory store that holds the memory (`memstore_...`).

          memory_id: The ID of the memory to update (`mem_...`).

          view: Whether a `memory` or `memory_version` in the response includes its `content`.
              Defaults to `full` on retrieve operations and to `basic` on list, create, and
              update operations.

              With `full`, list operations return at most 20 items per page.

          content: New UTF-8 text content for the memory. Maximum 100 kB (102,400 bytes). Omit to
              leave the content unchanged (e.g., for a rename-only update).

          path: The new path of the memory, which renames it. Omit it to keep the current path.

              The memory keeps its `id`. A path starts with `/` and has 1 to 20 segments. A
              segment can't be empty and can't be `.` or `..`. A path can't contain control
              characters, format characters, or the line and paragraph separators U+2028 and
              U+2029. It must be in Unicode Normalization Form C and at most 1,024 bytes long.
              Paths are case-sensitive.

          precondition: The condition that the memory must meet for the update to apply. Omit it to
              update unconditionally.

              If the condition fails, the request fails with HTTP status 409.

          betas: This endpoint is in beta: requests must send `agent-memory-2026-07-22` or
              `managed-agents-2026-04-01` in this header.

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
        if not memory_store_id:
            raise ValueError(f"Expected a non-empty value for `memory_store_id` but received {memory_store_id!r}")
        if not memory_id:
            raise ValueError(f"Expected a non-empty value for `memory_id` but received {memory_id!r}")
        extra_headers = {
            **strip_not_given(
                {
                    "anthropic-beta": ",".join(chain((str(e) for e in betas), ["agent-memory-2026-07-22"]))
                    if is_given(betas)
                    else not_given,
                    "anthropic-workspace-id": workspace_id,
                }
            ),
            **(extra_headers or {}),
        }
        extra_headers = {"anthropic-beta": "agent-memory-2026-07-22", **(extra_headers or {})}
        return self._post(
            path_template(
                "/v1/memory_stores/{memory_store_id}/memories/{memory_id}",
                memory_store_id=memory_store_id,
                memory_id=memory_id,
            ),
            body={
                "content": content,
                "path": path,
                "precondition": precondition,
            },
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query={"view": view},
                qualifiers={"beta": "true"},
                span_name="anthropic.memory_stores.memories.update",
                span_route="/v1/memory_stores/{memory_store_id}/memories/{memory_id}",
                span_attributes={"gen_ai.memory.store.id": memory_store_id, "gen_ai.memory.record.id": memory_id},
            ),
            cast_to=BetaManagedAgentsMemory,
        )

    def list(
        self,
        memory_store_id: str,
        *,
        depth: int | Omit = omit,
        limit: int | Omit = omit,
        page: str | Omit = omit,
        path_prefix: str | Omit = omit,
        view: BetaManagedAgentsMemoryView | Omit = omit,
        betas: List[AnthropicBetaParam] | Omit = omit,
        workspace_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> SyncPageCursor[BetaManagedAgentsMemoryListItem]:
        """
        List Memories

        Args:
          memory_store_id: The ID of the memory store to list memories from (`memstore_...`).

          depth: How far below `path_prefix` to list. Defaults to `0`, which lists every memory
              below the prefix.

              Pass `1` to list only the direct children. Deeper memories are then grouped into
              `memory_prefix` items.

          limit: The maximum number of items to return per page, from 1 to 100. Defaults to 20.

              With `view=full`, a page holds at most 20 items. `memory` and `memory_prefix`
              items both count toward the limit.

          page: The `next_page` value from a previous response, to get the next page. Omit it to
              get the first page.

          path_prefix: Return only memories whose path starts with this prefix, such as `/notes/`. This
              value appears in request URLs. Do not include secrets or personally identifiable
              information.

              Omit it to list the whole store. The prefix must end with `/` and matches whole
              segments, so `/notes/` matches `/notes/todo.md` but not
              `/notes-archive/todo.md`.

          view: Whether each memory in the response includes `content`. Defaults to `basic`,
              which sets it to `null`.

              With `full`, a page holds at most 20 items.

          betas: This endpoint is in beta: requests must send `agent-memory-2026-07-22` or
              `managed-agents-2026-04-01` in this header.

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
        if not memory_store_id:
            raise ValueError(f"Expected a non-empty value for `memory_store_id` but received {memory_store_id!r}")
        extra_headers = {
            **strip_not_given(
                {
                    "anthropic-beta": ",".join(chain((str(e) for e in betas), ["agent-memory-2026-07-22"]))
                    if is_given(betas)
                    else not_given,
                    "anthropic-workspace-id": workspace_id,
                }
            ),
            **(extra_headers or {}),
        }
        extra_headers = {"anthropic-beta": "agent-memory-2026-07-22", **(extra_headers or {})}
        return self._get_api_list(
            path_template("/v1/memory_stores/{memory_store_id}/memories", memory_store_id=memory_store_id),
            page=SyncPageCursor[BetaManagedAgentsMemoryListItem],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query={
                    "depth": depth,
                    "limit": limit,
                    "page": page,
                    "path_prefix": path_prefix,
                    "view": view,
                },
                qualifiers={"beta": "true"},
                span_name="anthropic.memory_stores.memories.list",
                span_route="/v1/memory_stores/{memory_store_id}/memories",
                span_content_query_params=("page",),
                span_attributes={"gen_ai.memory.store.id": memory_store_id},
            ),
            model=cast(
                Any, BetaManagedAgentsMemoryListItem
            ),  # Union types cannot be passed in as arguments in the type system
        )

    def delete(
        self,
        memory_id: str,
        *,
        memory_store_id: str,
        expected_content_sha256: str | Omit = omit,
        betas: List[AnthropicBetaParam] | Omit = omit,
        workspace_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaManagedAgentsDeletedMemory:
        """
        Delete a Memory

        Args:
          memory_store_id: The ID of the memory store that holds the memory (`memstore_...`).

          memory_id: The ID of the memory to delete (`mem_...`).

          expected_content_sha256: Delete the memory only if its current `content_sha256` equals this value, given
              as 64 lowercase hexadecimal characters. Omit it to delete unconditionally.

              If the hashes differ, the request fails with HTTP status 409 and nothing is
              deleted.

          betas: This endpoint is in beta: requests must send `agent-memory-2026-07-22` or
              `managed-agents-2026-04-01` in this header.

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
        if not memory_store_id:
            raise ValueError(f"Expected a non-empty value for `memory_store_id` but received {memory_store_id!r}")
        if not memory_id:
            raise ValueError(f"Expected a non-empty value for `memory_id` but received {memory_id!r}")
        extra_headers = {
            **strip_not_given(
                {
                    "anthropic-beta": ",".join(chain((str(e) for e in betas), ["agent-memory-2026-07-22"]))
                    if is_given(betas)
                    else not_given,
                    "anthropic-workspace-id": workspace_id,
                }
            ),
            **(extra_headers or {}),
        }
        extra_headers = {"anthropic-beta": "agent-memory-2026-07-22", **(extra_headers or {})}
        return self._delete(
            path_template(
                "/v1/memory_stores/{memory_store_id}/memories/{memory_id}",
                memory_store_id=memory_store_id,
                memory_id=memory_id,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query={"expected_content_sha256": expected_content_sha256},
                qualifiers={"beta": "true"},
                span_name="anthropic.memory_stores.memories.delete",
                span_route="/v1/memory_stores/{memory_store_id}/memories/{memory_id}",
                span_attributes={"gen_ai.memory.store.id": memory_store_id, "gen_ai.memory.record.id": memory_id},
            ),
            cast_to=BetaManagedAgentsDeletedMemory,
        )


class AsyncMemories(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncMemoriesWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#accessing-raw-response-data-eg-headers
        """
        return AsyncMemoriesWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncMemoriesWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#with_streaming_response
        """
        return AsyncMemoriesWithStreamingResponse(self)

    async def create(
        self,
        memory_store_id: str,
        *,
        content: Optional[str],
        path: str,
        view: BetaManagedAgentsMemoryView | Omit = omit,
        betas: List[AnthropicBetaParam] | Omit = omit,
        workspace_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaManagedAgentsMemory:
        """
        Create a Memory

        Args:
          memory_store_id: The ID of the memory store to create the memory in (`memstore_...`).

          content: The UTF-8 text content of the new memory. Pass `""` to create an empty memory.

              The maximum size is 100 kB (102,400 bytes).

          path: The path of the new memory, such as `/projects/foo/notes.md`. Paths are
              case-sensitive.

              A path starts with `/` and has 1 to 20 segments. A segment can't be empty and
              can't be `.` or `..`. A path can't contain control characters, format
              characters, or the line and paragraph separators U+2028 and U+2029. It must be
              in Unicode Normalization Form C and at most 1,024 bytes long.

          view: Whether a `memory` or `memory_version` in the response includes its `content`.
              Defaults to `full` on retrieve operations and to `basic` on list, create, and
              update operations.

              With `full`, list operations return at most 20 items per page.

          betas: This endpoint is in beta: requests must send `agent-memory-2026-07-22` or
              `managed-agents-2026-04-01` in this header.

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
        if not memory_store_id:
            raise ValueError(f"Expected a non-empty value for `memory_store_id` but received {memory_store_id!r}")
        extra_headers = {
            **strip_not_given(
                {
                    "anthropic-beta": ",".join(chain((str(e) for e in betas), ["agent-memory-2026-07-22"]))
                    if is_given(betas)
                    else not_given,
                    "anthropic-workspace-id": workspace_id,
                }
            ),
            **(extra_headers or {}),
        }
        extra_headers = {"anthropic-beta": "agent-memory-2026-07-22", **(extra_headers or {})}
        return await self._post(
            path_template("/v1/memory_stores/{memory_store_id}/memories", memory_store_id=memory_store_id),
            body={
                "content": content,
                "path": path,
            },
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query={"view": view},
                qualifiers={"beta": "true"},
                span_name="anthropic.memory_stores.memories.create",
                span_route="/v1/memory_stores/{memory_store_id}/memories",
                span_attributes={"gen_ai.memory.store.id": memory_store_id},
                span_created_id="gen_ai.memory.record.id",
            ),
            cast_to=BetaManagedAgentsMemory,
        )

    async def retrieve(
        self,
        memory_id: str,
        *,
        memory_store_id: str,
        view: BetaManagedAgentsMemoryView | Omit = omit,
        betas: List[AnthropicBetaParam] | Omit = omit,
        workspace_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaManagedAgentsMemory:
        """
        Retrieve a Memory

        Args:
          memory_store_id: The ID of the memory store that holds the memory (`memstore_...`).

          memory_id: The ID of the memory to retrieve (`mem_...`).

          view: Whether a `memory` or `memory_version` in the response includes its `content`.
              Defaults to `full` on retrieve operations and to `basic` on list, create, and
              update operations.

              With `full`, list operations return at most 20 items per page.

          betas: This endpoint is in beta: requests must send `agent-memory-2026-07-22` or
              `managed-agents-2026-04-01` in this header.

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
        if not memory_store_id:
            raise ValueError(f"Expected a non-empty value for `memory_store_id` but received {memory_store_id!r}")
        if not memory_id:
            raise ValueError(f"Expected a non-empty value for `memory_id` but received {memory_id!r}")
        extra_headers = {
            **strip_not_given(
                {
                    "anthropic-beta": ",".join(chain((str(e) for e in betas), ["agent-memory-2026-07-22"]))
                    if is_given(betas)
                    else not_given,
                    "anthropic-workspace-id": workspace_id,
                }
            ),
            **(extra_headers or {}),
        }
        extra_headers = {"anthropic-beta": "agent-memory-2026-07-22", **(extra_headers or {})}
        return await self._get(
            path_template(
                "/v1/memory_stores/{memory_store_id}/memories/{memory_id}",
                memory_store_id=memory_store_id,
                memory_id=memory_id,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query={"view": view},
                qualifiers={"beta": "true"},
                span_name="anthropic.memory_stores.memories.retrieve",
                span_route="/v1/memory_stores/{memory_store_id}/memories/{memory_id}",
                span_attributes={"gen_ai.memory.store.id": memory_store_id, "gen_ai.memory.record.id": memory_id},
            ),
            cast_to=BetaManagedAgentsMemory,
        )

    async def update(
        self,
        memory_id: str,
        *,
        memory_store_id: str,
        view: BetaManagedAgentsMemoryView | Omit = omit,
        content: Optional[str] | Omit = omit,
        path: Optional[str] | Omit = omit,
        precondition: BetaManagedAgentsPreconditionParam | Omit = omit,
        betas: List[AnthropicBetaParam] | Omit = omit,
        workspace_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaManagedAgentsMemory:
        """
        Update a Memory

        Args:
          memory_store_id: The ID of the memory store that holds the memory (`memstore_...`).

          memory_id: The ID of the memory to update (`mem_...`).

          view: Whether a `memory` or `memory_version` in the response includes its `content`.
              Defaults to `full` on retrieve operations and to `basic` on list, create, and
              update operations.

              With `full`, list operations return at most 20 items per page.

          content: New UTF-8 text content for the memory. Maximum 100 kB (102,400 bytes). Omit to
              leave the content unchanged (e.g., for a rename-only update).

          path: The new path of the memory, which renames it. Omit it to keep the current path.

              The memory keeps its `id`. A path starts with `/` and has 1 to 20 segments. A
              segment can't be empty and can't be `.` or `..`. A path can't contain control
              characters, format characters, or the line and paragraph separators U+2028 and
              U+2029. It must be in Unicode Normalization Form C and at most 1,024 bytes long.
              Paths are case-sensitive.

          precondition: The condition that the memory must meet for the update to apply. Omit it to
              update unconditionally.

              If the condition fails, the request fails with HTTP status 409.

          betas: This endpoint is in beta: requests must send `agent-memory-2026-07-22` or
              `managed-agents-2026-04-01` in this header.

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
        if not memory_store_id:
            raise ValueError(f"Expected a non-empty value for `memory_store_id` but received {memory_store_id!r}")
        if not memory_id:
            raise ValueError(f"Expected a non-empty value for `memory_id` but received {memory_id!r}")
        extra_headers = {
            **strip_not_given(
                {
                    "anthropic-beta": ",".join(chain((str(e) for e in betas), ["agent-memory-2026-07-22"]))
                    if is_given(betas)
                    else not_given,
                    "anthropic-workspace-id": workspace_id,
                }
            ),
            **(extra_headers or {}),
        }
        extra_headers = {"anthropic-beta": "agent-memory-2026-07-22", **(extra_headers or {})}
        return await self._post(
            path_template(
                "/v1/memory_stores/{memory_store_id}/memories/{memory_id}",
                memory_store_id=memory_store_id,
                memory_id=memory_id,
            ),
            body={
                "content": content,
                "path": path,
                "precondition": precondition,
            },
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query={"view": view},
                qualifiers={"beta": "true"},
                span_name="anthropic.memory_stores.memories.update",
                span_route="/v1/memory_stores/{memory_store_id}/memories/{memory_id}",
                span_attributes={"gen_ai.memory.store.id": memory_store_id, "gen_ai.memory.record.id": memory_id},
            ),
            cast_to=BetaManagedAgentsMemory,
        )

    def list(
        self,
        memory_store_id: str,
        *,
        depth: int | Omit = omit,
        limit: int | Omit = omit,
        page: str | Omit = omit,
        path_prefix: str | Omit = omit,
        view: BetaManagedAgentsMemoryView | Omit = omit,
        betas: List[AnthropicBetaParam] | Omit = omit,
        workspace_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> AsyncPaginator[BetaManagedAgentsMemoryListItem, AsyncPageCursor[BetaManagedAgentsMemoryListItem]]:
        """
        List Memories

        Args:
          memory_store_id: The ID of the memory store to list memories from (`memstore_...`).

          depth: How far below `path_prefix` to list. Defaults to `0`, which lists every memory
              below the prefix.

              Pass `1` to list only the direct children. Deeper memories are then grouped into
              `memory_prefix` items.

          limit: The maximum number of items to return per page, from 1 to 100. Defaults to 20.

              With `view=full`, a page holds at most 20 items. `memory` and `memory_prefix`
              items both count toward the limit.

          page: The `next_page` value from a previous response, to get the next page. Omit it to
              get the first page.

          path_prefix: Return only memories whose path starts with this prefix, such as `/notes/`. This
              value appears in request URLs. Do not include secrets or personally identifiable
              information.

              Omit it to list the whole store. The prefix must end with `/` and matches whole
              segments, so `/notes/` matches `/notes/todo.md` but not
              `/notes-archive/todo.md`.

          view: Whether each memory in the response includes `content`. Defaults to `basic`,
              which sets it to `null`.

              With `full`, a page holds at most 20 items.

          betas: This endpoint is in beta: requests must send `agent-memory-2026-07-22` or
              `managed-agents-2026-04-01` in this header.

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
        if not memory_store_id:
            raise ValueError(f"Expected a non-empty value for `memory_store_id` but received {memory_store_id!r}")
        extra_headers = {
            **strip_not_given(
                {
                    "anthropic-beta": ",".join(chain((str(e) for e in betas), ["agent-memory-2026-07-22"]))
                    if is_given(betas)
                    else not_given,
                    "anthropic-workspace-id": workspace_id,
                }
            ),
            **(extra_headers or {}),
        }
        extra_headers = {"anthropic-beta": "agent-memory-2026-07-22", **(extra_headers or {})}
        return self._get_api_list(
            path_template("/v1/memory_stores/{memory_store_id}/memories", memory_store_id=memory_store_id),
            page=AsyncPageCursor[BetaManagedAgentsMemoryListItem],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query={
                    "depth": depth,
                    "limit": limit,
                    "page": page,
                    "path_prefix": path_prefix,
                    "view": view,
                },
                qualifiers={"beta": "true"},
                span_name="anthropic.memory_stores.memories.list",
                span_route="/v1/memory_stores/{memory_store_id}/memories",
                span_content_query_params=("page",),
                span_attributes={"gen_ai.memory.store.id": memory_store_id},
            ),
            model=cast(
                Any, BetaManagedAgentsMemoryListItem
            ),  # Union types cannot be passed in as arguments in the type system
        )

    async def delete(
        self,
        memory_id: str,
        *,
        memory_store_id: str,
        expected_content_sha256: str | Omit = omit,
        betas: List[AnthropicBetaParam] | Omit = omit,
        workspace_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaManagedAgentsDeletedMemory:
        """
        Delete a Memory

        Args:
          memory_store_id: The ID of the memory store that holds the memory (`memstore_...`).

          memory_id: The ID of the memory to delete (`mem_...`).

          expected_content_sha256: Delete the memory only if its current `content_sha256` equals this value, given
              as 64 lowercase hexadecimal characters. Omit it to delete unconditionally.

              If the hashes differ, the request fails with HTTP status 409 and nothing is
              deleted.

          betas: This endpoint is in beta: requests must send `agent-memory-2026-07-22` or
              `managed-agents-2026-04-01` in this header.

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
        if not memory_store_id:
            raise ValueError(f"Expected a non-empty value for `memory_store_id` but received {memory_store_id!r}")
        if not memory_id:
            raise ValueError(f"Expected a non-empty value for `memory_id` but received {memory_id!r}")
        extra_headers = {
            **strip_not_given(
                {
                    "anthropic-beta": ",".join(chain((str(e) for e in betas), ["agent-memory-2026-07-22"]))
                    if is_given(betas)
                    else not_given,
                    "anthropic-workspace-id": workspace_id,
                }
            ),
            **(extra_headers or {}),
        }
        extra_headers = {"anthropic-beta": "agent-memory-2026-07-22", **(extra_headers or {})}
        return await self._delete(
            path_template(
                "/v1/memory_stores/{memory_store_id}/memories/{memory_id}",
                memory_store_id=memory_store_id,
                memory_id=memory_id,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query={"expected_content_sha256": expected_content_sha256},
                qualifiers={"beta": "true"},
                span_name="anthropic.memory_stores.memories.delete",
                span_route="/v1/memory_stores/{memory_store_id}/memories/{memory_id}",
                span_attributes={"gen_ai.memory.store.id": memory_store_id, "gen_ai.memory.record.id": memory_id},
            ),
            cast_to=BetaManagedAgentsDeletedMemory,
        )


class MemoriesWithRawResponse:
    def __init__(self, memories: Memories) -> None:
        self._memories = memories

        self.create = to_raw_response_wrapper(
            memories.create,
        )
        self.retrieve = to_raw_response_wrapper(
            memories.retrieve,
        )
        self.update = to_raw_response_wrapper(
            memories.update,
        )
        self.list = to_raw_response_wrapper(
            memories.list,
        )
        self.delete = to_raw_response_wrapper(
            memories.delete,
        )


class AsyncMemoriesWithRawResponse:
    def __init__(self, memories: AsyncMemories) -> None:
        self._memories = memories

        self.create = async_to_raw_response_wrapper(
            memories.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            memories.retrieve,
        )
        self.update = async_to_raw_response_wrapper(
            memories.update,
        )
        self.list = async_to_raw_response_wrapper(
            memories.list,
        )
        self.delete = async_to_raw_response_wrapper(
            memories.delete,
        )


class MemoriesWithStreamingResponse:
    def __init__(self, memories: Memories) -> None:
        self._memories = memories

        self.create = to_streamed_response_wrapper(
            memories.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            memories.retrieve,
        )
        self.update = to_streamed_response_wrapper(
            memories.update,
        )
        self.list = to_streamed_response_wrapper(
            memories.list,
        )
        self.delete = to_streamed_response_wrapper(
            memories.delete,
        )


class AsyncMemoriesWithStreamingResponse:
    def __init__(self, memories: AsyncMemories) -> None:
        self._memories = memories

        self.create = async_to_streamed_response_wrapper(
            memories.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            memories.retrieve,
        )
        self.update = async_to_streamed_response_wrapper(
            memories.update,
        )
        self.list = async_to_streamed_response_wrapper(
            memories.list,
        )
        self.delete = async_to_streamed_response_wrapper(
            memories.delete,
        )
