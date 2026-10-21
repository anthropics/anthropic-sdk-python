from __future__ import annotations

from typing import Dict, List, Union, Optional
from datetime import datetime
from itertools import chain

import httpx2

from .memories import (
    Memories,
    AsyncMemories,
    MemoriesWithRawResponse,
    AsyncMemoriesWithRawResponse,
    MemoriesWithStreamingResponse,
    AsyncMemoriesWithStreamingResponse,
)
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
from .memory_versions import (
    MemoryVersions,
    AsyncMemoryVersions,
    MemoryVersionsWithRawResponse,
    AsyncMemoryVersionsWithRawResponse,
    MemoryVersionsWithStreamingResponse,
    AsyncMemoryVersionsWithStreamingResponse,
)
from ....types.anthropic_beta_param import AnthropicBetaParam
from ....types.beta.beta_managed_agents_memory_store import BetaManagedAgentsMemoryStore
from ....types.beta.beta_managed_agents_deleted_memory_store import BetaManagedAgentsDeletedMemoryStore

__all__ = ["MemoryStores", "AsyncMemoryStores"]


class MemoryStores(SyncAPIResource):
    @cached_property
    def memories(self) -> Memories:
        return Memories(self._client)

    @cached_property
    def memory_versions(self) -> MemoryVersions:
        return MemoryVersions(self._client)

    @cached_property
    def with_raw_response(self) -> MemoryStoresWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#accessing-raw-response-data-eg-headers
        """
        return MemoryStoresWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> MemoryStoresWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#with_streaming_response
        """
        return MemoryStoresWithStreamingResponse(self)

    def create(
        self,
        *,
        name: str,
        description: str | Omit = omit,
        metadata: Dict[str, str] | Omit = omit,
        betas: List[AnthropicBetaParam] | Omit = omit,
        workspace_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaManagedAgentsMemoryStore:
        """
        Create a Memory Store

        Args:
          name: The name of the memory store, 1 to 255 characters long, without control
              characters. Names don't have to be unique in a workspace.

              In a session, the store's directory under `/mnt/memory/` is based on this name.
              The name is lowercased and every run of characters other than ASCII letters and
              digits becomes one hyphen. The session's memory store resource gives the exact
              path in `mount_path`.

              See the
              [memory guide](https://platform.claude.com/docs/en/managed-agents/memory#how-the-agent-accesses-memory)
              to learn more about how agents access memory stores.

          description: Free-text description of what the store contains, up to 1,024 characters.
              Included in the agent's system prompt when the store is attached, so word it to
              be useful to the agent.

          metadata: Key-value pairs for your own use, such as the end user that the store belongs
              to. The agent doesn't see them.

              A store has at most 16 pairs. Keys are 1 to 64 characters long and values at
              most 512 characters.

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
            "/v1/memory_stores?beta=true",
            body={
                "name": name,
                "description": description,
                "metadata": metadata,
            },
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                span_name="anthropic.memory_stores.create",
                span_route="/v1/memory_stores",
                span_created_id="gen_ai.memory.store.id",
            ),
            cast_to=BetaManagedAgentsMemoryStore,
        )

    def retrieve(
        self,
        memory_store_id: str,
        *,
        betas: List[AnthropicBetaParam] | Omit = omit,
        workspace_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaManagedAgentsMemoryStore:
        """
        Retrieve a Memory Store

        Args:
          memory_store_id: The ID of the memory store to retrieve (`memstore_...`).

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
        return self._get(
            path_template("/v1/memory_stores/{memory_store_id}?beta=true", memory_store_id=memory_store_id),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                span_name="anthropic.memory_stores.retrieve",
                span_route="/v1/memory_stores/{memory_store_id}",
                span_attributes={"gen_ai.memory.store.id": memory_store_id},
            ),
            cast_to=BetaManagedAgentsMemoryStore,
        )

    def update(
        self,
        memory_store_id: str,
        *,
        description: Optional[str] | Omit = omit,
        metadata: Optional[Dict[str, Optional[str]]] | Omit = omit,
        name: Optional[str] | Omit = omit,
        betas: List[AnthropicBetaParam] | Omit = omit,
        workspace_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaManagedAgentsMemoryStore:
        """
        Update a Memory Store

        Args:
          memory_store_id: The ID of the memory store to update (`memstore_...`).

              The request fails with HTTP status 400 if the store is archived.

          description: New description for the store, up to 1,024 characters. Pass an empty string to
              clear it.

          metadata: Changes to apply to the memory store's metadata. Keys you leave out keep their
              values.

              Set a key to a string to add or replace it, or to `null` to remove it. After the
              change, the metadata can hold at most 16 key-value pairs. Keys are 1 to 64
              characters long and values at most 512 characters.

          name: The new name of the memory store, 1 to 255 characters long, without control
              characters.

              Sessions created after the change use the new name for the store's directory
              under `/mnt/memory/`.

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
            path_template("/v1/memory_stores/{memory_store_id}?beta=true", memory_store_id=memory_store_id),
            body={
                "description": description,
                "metadata": metadata,
                "name": name,
            },
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                span_name="anthropic.memory_stores.update",
                span_route="/v1/memory_stores/{memory_store_id}",
                span_attributes={"gen_ai.memory.store.id": memory_store_id},
            ),
            cast_to=BetaManagedAgentsMemoryStore,
        )

    def list(
        self,
        *,
        created_at_gte: Union[str, datetime] | Omit = omit,
        created_at_lte: Union[str, datetime] | Omit = omit,
        include_archived: bool | Omit = omit,
        limit: int | Omit = omit,
        page: str | Omit = omit,
        betas: List[AnthropicBetaParam] | Omit = omit,
        workspace_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> SyncPageCursor[BetaManagedAgentsMemoryStore]:
        """
        List Memory Stores

        Args:
          created_at_gte: Return only memory stores created at or after this time (inclusive).

          created_at_lte: Return only memory stores created at or before this time (inclusive).

          include_archived: When `true`, archived stores are included in the results. Defaults to `false`
              (archived stores are excluded).

          limit: Maximum number of stores to return per page. Must be between 1 and 100. Defaults
              to 20 when omitted.

          page: The `next_page` value from a previous response, to get the next page. Omit it to
              get the first page.

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
            "/v1/memory_stores?beta=true",
            page=SyncPageCursor[BetaManagedAgentsMemoryStore],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query={
                    "created_at[gte]": created_at_gte,
                    "created_at[lte]": created_at_lte,
                    "include_archived": include_archived,
                    "limit": limit,
                    "page": page,
                },
                span_name="anthropic.memory_stores.list",
                span_route="/v1/memory_stores",
            ),
            model=BetaManagedAgentsMemoryStore,
        )

    def delete(
        self,
        memory_store_id: str,
        *,
        betas: List[AnthropicBetaParam] | Omit = omit,
        workspace_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaManagedAgentsDeletedMemoryStore:
        """
        Delete a Memory Store

        Args:
          memory_store_id: The ID of the memory store to delete (`memstore_...`).

              Deleting a store also deletes all its memories and memory versions. It can't be
              undone.

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
        return self._delete(
            path_template("/v1/memory_stores/{memory_store_id}?beta=true", memory_store_id=memory_store_id),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                span_name="anthropic.memory_stores.delete",
                span_route="/v1/memory_stores/{memory_store_id}",
                span_attributes={"gen_ai.memory.store.id": memory_store_id},
            ),
            cast_to=BetaManagedAgentsDeletedMemoryStore,
        )

    def archive(
        self,
        memory_store_id: str,
        *,
        betas: List[AnthropicBetaParam] | Omit = omit,
        workspace_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaManagedAgentsMemoryStore:
        """
        Archive a Memory Store

        Args:
          memory_store_id: The ID of the memory store to archive (`memstore_...`).

              Archiving can't be undone. Archiving a store that is already archived returns it
              unchanged.

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
            path_template("/v1/memory_stores/{memory_store_id}/archive?beta=true", memory_store_id=memory_store_id),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                span_name="anthropic.memory_stores.archive",
                span_route="/v1/memory_stores/{memory_store_id}/archive",
                span_attributes={"gen_ai.memory.store.id": memory_store_id},
            ),
            cast_to=BetaManagedAgentsMemoryStore,
        )


class AsyncMemoryStores(AsyncAPIResource):
    @cached_property
    def memories(self) -> AsyncMemories:
        return AsyncMemories(self._client)

    @cached_property
    def memory_versions(self) -> AsyncMemoryVersions:
        return AsyncMemoryVersions(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncMemoryStoresWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#accessing-raw-response-data-eg-headers
        """
        return AsyncMemoryStoresWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncMemoryStoresWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#with_streaming_response
        """
        return AsyncMemoryStoresWithStreamingResponse(self)

    async def create(
        self,
        *,
        name: str,
        description: str | Omit = omit,
        metadata: Dict[str, str] | Omit = omit,
        betas: List[AnthropicBetaParam] | Omit = omit,
        workspace_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaManagedAgentsMemoryStore:
        """
        Create a Memory Store

        Args:
          name: The name of the memory store, 1 to 255 characters long, without control
              characters. Names don't have to be unique in a workspace.

              In a session, the store's directory under `/mnt/memory/` is based on this name.
              The name is lowercased and every run of characters other than ASCII letters and
              digits becomes one hyphen. The session's memory store resource gives the exact
              path in `mount_path`.

              See the
              [memory guide](https://platform.claude.com/docs/en/managed-agents/memory#how-the-agent-accesses-memory)
              to learn more about how agents access memory stores.

          description: Free-text description of what the store contains, up to 1,024 characters.
              Included in the agent's system prompt when the store is attached, so word it to
              be useful to the agent.

          metadata: Key-value pairs for your own use, such as the end user that the store belongs
              to. The agent doesn't see them.

              A store has at most 16 pairs. Keys are 1 to 64 characters long and values at
              most 512 characters.

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
            "/v1/memory_stores?beta=true",
            body={
                "name": name,
                "description": description,
                "metadata": metadata,
            },
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                span_name="anthropic.memory_stores.create",
                span_route="/v1/memory_stores",
                span_created_id="gen_ai.memory.store.id",
            ),
            cast_to=BetaManagedAgentsMemoryStore,
        )

    async def retrieve(
        self,
        memory_store_id: str,
        *,
        betas: List[AnthropicBetaParam] | Omit = omit,
        workspace_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaManagedAgentsMemoryStore:
        """
        Retrieve a Memory Store

        Args:
          memory_store_id: The ID of the memory store to retrieve (`memstore_...`).

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
        return await self._get(
            path_template("/v1/memory_stores/{memory_store_id}?beta=true", memory_store_id=memory_store_id),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                span_name="anthropic.memory_stores.retrieve",
                span_route="/v1/memory_stores/{memory_store_id}",
                span_attributes={"gen_ai.memory.store.id": memory_store_id},
            ),
            cast_to=BetaManagedAgentsMemoryStore,
        )

    async def update(
        self,
        memory_store_id: str,
        *,
        description: Optional[str] | Omit = omit,
        metadata: Optional[Dict[str, Optional[str]]] | Omit = omit,
        name: Optional[str] | Omit = omit,
        betas: List[AnthropicBetaParam] | Omit = omit,
        workspace_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaManagedAgentsMemoryStore:
        """
        Update a Memory Store

        Args:
          memory_store_id: The ID of the memory store to update (`memstore_...`).

              The request fails with HTTP status 400 if the store is archived.

          description: New description for the store, up to 1,024 characters. Pass an empty string to
              clear it.

          metadata: Changes to apply to the memory store's metadata. Keys you leave out keep their
              values.

              Set a key to a string to add or replace it, or to `null` to remove it. After the
              change, the metadata can hold at most 16 key-value pairs. Keys are 1 to 64
              characters long and values at most 512 characters.

          name: The new name of the memory store, 1 to 255 characters long, without control
              characters.

              Sessions created after the change use the new name for the store's directory
              under `/mnt/memory/`.

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
            path_template("/v1/memory_stores/{memory_store_id}?beta=true", memory_store_id=memory_store_id),
            body={
                "description": description,
                "metadata": metadata,
                "name": name,
            },
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                span_name="anthropic.memory_stores.update",
                span_route="/v1/memory_stores/{memory_store_id}",
                span_attributes={"gen_ai.memory.store.id": memory_store_id},
            ),
            cast_to=BetaManagedAgentsMemoryStore,
        )

    def list(
        self,
        *,
        created_at_gte: Union[str, datetime] | Omit = omit,
        created_at_lte: Union[str, datetime] | Omit = omit,
        include_archived: bool | Omit = omit,
        limit: int | Omit = omit,
        page: str | Omit = omit,
        betas: List[AnthropicBetaParam] | Omit = omit,
        workspace_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> AsyncPaginator[BetaManagedAgentsMemoryStore, AsyncPageCursor[BetaManagedAgentsMemoryStore]]:
        """
        List Memory Stores

        Args:
          created_at_gte: Return only memory stores created at or after this time (inclusive).

          created_at_lte: Return only memory stores created at or before this time (inclusive).

          include_archived: When `true`, archived stores are included in the results. Defaults to `false`
              (archived stores are excluded).

          limit: Maximum number of stores to return per page. Must be between 1 and 100. Defaults
              to 20 when omitted.

          page: The `next_page` value from a previous response, to get the next page. Omit it to
              get the first page.

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
            "/v1/memory_stores?beta=true",
            page=AsyncPageCursor[BetaManagedAgentsMemoryStore],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query={
                    "created_at[gte]": created_at_gte,
                    "created_at[lte]": created_at_lte,
                    "include_archived": include_archived,
                    "limit": limit,
                    "page": page,
                },
                span_name="anthropic.memory_stores.list",
                span_route="/v1/memory_stores",
            ),
            model=BetaManagedAgentsMemoryStore,
        )

    async def delete(
        self,
        memory_store_id: str,
        *,
        betas: List[AnthropicBetaParam] | Omit = omit,
        workspace_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaManagedAgentsDeletedMemoryStore:
        """
        Delete a Memory Store

        Args:
          memory_store_id: The ID of the memory store to delete (`memstore_...`).

              Deleting a store also deletes all its memories and memory versions. It can't be
              undone.

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
        return await self._delete(
            path_template("/v1/memory_stores/{memory_store_id}?beta=true", memory_store_id=memory_store_id),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                span_name="anthropic.memory_stores.delete",
                span_route="/v1/memory_stores/{memory_store_id}",
                span_attributes={"gen_ai.memory.store.id": memory_store_id},
            ),
            cast_to=BetaManagedAgentsDeletedMemoryStore,
        )

    async def archive(
        self,
        memory_store_id: str,
        *,
        betas: List[AnthropicBetaParam] | Omit = omit,
        workspace_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaManagedAgentsMemoryStore:
        """
        Archive a Memory Store

        Args:
          memory_store_id: The ID of the memory store to archive (`memstore_...`).

              Archiving can't be undone. Archiving a store that is already archived returns it
              unchanged.

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
            path_template("/v1/memory_stores/{memory_store_id}/archive?beta=true", memory_store_id=memory_store_id),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                span_name="anthropic.memory_stores.archive",
                span_route="/v1/memory_stores/{memory_store_id}/archive",
                span_attributes={"gen_ai.memory.store.id": memory_store_id},
            ),
            cast_to=BetaManagedAgentsMemoryStore,
        )


class MemoryStoresWithRawResponse:
    def __init__(self, memory_stores: MemoryStores) -> None:
        self._memory_stores = memory_stores

        self.create = to_raw_response_wrapper(
            memory_stores.create,
        )
        self.retrieve = to_raw_response_wrapper(
            memory_stores.retrieve,
        )
        self.update = to_raw_response_wrapper(
            memory_stores.update,
        )
        self.list = to_raw_response_wrapper(
            memory_stores.list,
        )
        self.delete = to_raw_response_wrapper(
            memory_stores.delete,
        )
        self.archive = to_raw_response_wrapper(
            memory_stores.archive,
        )

    @cached_property
    def memories(self) -> MemoriesWithRawResponse:
        return MemoriesWithRawResponse(self._memory_stores.memories)

    @cached_property
    def memory_versions(self) -> MemoryVersionsWithRawResponse:
        return MemoryVersionsWithRawResponse(self._memory_stores.memory_versions)


class AsyncMemoryStoresWithRawResponse:
    def __init__(self, memory_stores: AsyncMemoryStores) -> None:
        self._memory_stores = memory_stores

        self.create = async_to_raw_response_wrapper(
            memory_stores.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            memory_stores.retrieve,
        )
        self.update = async_to_raw_response_wrapper(
            memory_stores.update,
        )
        self.list = async_to_raw_response_wrapper(
            memory_stores.list,
        )
        self.delete = async_to_raw_response_wrapper(
            memory_stores.delete,
        )
        self.archive = async_to_raw_response_wrapper(
            memory_stores.archive,
        )

    @cached_property
    def memories(self) -> AsyncMemoriesWithRawResponse:
        return AsyncMemoriesWithRawResponse(self._memory_stores.memories)

    @cached_property
    def memory_versions(self) -> AsyncMemoryVersionsWithRawResponse:
        return AsyncMemoryVersionsWithRawResponse(self._memory_stores.memory_versions)


class MemoryStoresWithStreamingResponse:
    def __init__(self, memory_stores: MemoryStores) -> None:
        self._memory_stores = memory_stores

        self.create = to_streamed_response_wrapper(
            memory_stores.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            memory_stores.retrieve,
        )
        self.update = to_streamed_response_wrapper(
            memory_stores.update,
        )
        self.list = to_streamed_response_wrapper(
            memory_stores.list,
        )
        self.delete = to_streamed_response_wrapper(
            memory_stores.delete,
        )
        self.archive = to_streamed_response_wrapper(
            memory_stores.archive,
        )

    @cached_property
    def memories(self) -> MemoriesWithStreamingResponse:
        return MemoriesWithStreamingResponse(self._memory_stores.memories)

    @cached_property
    def memory_versions(self) -> MemoryVersionsWithStreamingResponse:
        return MemoryVersionsWithStreamingResponse(self._memory_stores.memory_versions)


class AsyncMemoryStoresWithStreamingResponse:
    def __init__(self, memory_stores: AsyncMemoryStores) -> None:
        self._memory_stores = memory_stores

        self.create = async_to_streamed_response_wrapper(
            memory_stores.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            memory_stores.retrieve,
        )
        self.update = async_to_streamed_response_wrapper(
            memory_stores.update,
        )
        self.list = async_to_streamed_response_wrapper(
            memory_stores.list,
        )
        self.delete = async_to_streamed_response_wrapper(
            memory_stores.delete,
        )
        self.archive = async_to_streamed_response_wrapper(
            memory_stores.archive,
        )

    @cached_property
    def memories(self) -> AsyncMemoriesWithStreamingResponse:
        return AsyncMemoriesWithStreamingResponse(self._memory_stores.memories)

    @cached_property
    def memory_versions(self) -> AsyncMemoryVersionsWithStreamingResponse:
        return AsyncMemoryVersionsWithStreamingResponse(self._memory_stores.memory_versions)
