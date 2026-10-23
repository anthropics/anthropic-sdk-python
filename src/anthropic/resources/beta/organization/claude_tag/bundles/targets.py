from __future__ import annotations

from typing import Any, List, cast
from itertools import chain

import httpx2

from ......_types import Body, Omit, Query, Headers, NotGiven, omit, not_given
from ......_utils import is_given, path_template, strip_not_given
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
from ......types.beta.organization.claude_tag.bundles.beta_claude_tag_bundle_target import BetaClaudeTagBundleTarget
from ......types.beta.organization.claude_tag.bundles.beta_claude_tag_deleted_bundle_target import (
    BetaClaudeTagDeletedBundleTarget,
)
from ......types.beta.organization.claude_tag.bundles.beta_claude_tag_bundle_target_create_param import (
    BetaClaudeTagBundleTargetCreateParam,
)

__all__ = ["Targets", "AsyncTargets"]


class Targets(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> TargetsWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#accessing-raw-response-data-eg-headers
        """
        return TargetsWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> TargetsWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#with_streaming_response
        """
        return TargetsWithStreamingResponse(self)

    def create(
        self,
        bundle_id: str,
        *,
        target: BetaClaudeTagBundleTargetCreateParam,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaClaudeTagBundleTarget:
        """Attach a Bundle to a Slack channel or a Slack workspace.

        A Bundle attached to a
        workspace can be used in the workspace and in every channel in it. Attaching a
        Bundle to a channel or workspace it is already attached to returns the existing
        Bundle Target. The channel or workspace must be set up: attaching never sets a
        channel up. A group direct message takes no Bundle and returns 400.

        Args:
          bundle_id: The Bundle's identifier, starting with `capp_`.

          betas: This endpoint is in beta: requests must send
              `experimental-claude-tag-2026-10-21` in this header.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not bundle_id:
            raise ValueError(f"Expected a non-empty value for `bundle_id` but received {bundle_id!r}")
        extra_headers = {
            **strip_not_given(
                {
                    "anthropic-beta": ",".join(chain((str(e) for e in betas), ["experimental-claude-tag-2026-10-21"]))
                    if is_given(betas)
                    else not_given
                }
            ),
            **(extra_headers or {}),
        }
        extra_headers = {"anthropic-beta": "experimental-claude-tag-2026-10-21", **(extra_headers or {})}
        return cast(
            BetaClaudeTagBundleTarget,
            self._post(
                path_template("/v1/organizations/claude_tag/bundles/{bundle_id}/targets", bundle_id=bundle_id),
                body=target,
                options=make_request_options(
                    extra_headers=extra_headers,
                    extra_query=extra_query,
                    extra_body=extra_body,
                    timeout=timeout,
                    qualifiers={"beta": "true"},
                    span_name="anthropic.organization.claude_tag.bundles.targets.create",
                    span_route="/v1/organizations/claude_tag/bundles/{bundle_id}/targets",
                    span_attributes={"anthropic.organization.claude_tag.bundle.id": bundle_id},
                ),
                cast_to=cast(
                    Any, BetaClaudeTagBundleTarget
                ),  # Union types cannot be passed in as arguments in the type system
            ),
        )

    def retrieve(
        self,
        target_id: str,
        *,
        bundle_id: str,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaClaudeTagBundleTarget:
        """Get one Bundle Target.

        Returns 404 when `target_id` is the identifier of another
        Bundle's Bundle Target, or the Bundle Target was detached.

        Args:
          bundle_id: The Bundle's identifier, starting with `capp_`.

          target_id: The Bundle Target's identifier, starting with `btgt_`. Attach Bundle and List
              Bundle Targets return it. It is never the identifier of the channel or
              workspace.

          betas: This endpoint is in beta: requests must send
              `experimental-claude-tag-2026-10-21` in this header.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not bundle_id:
            raise ValueError(f"Expected a non-empty value for `bundle_id` but received {bundle_id!r}")
        if not target_id:
            raise ValueError(f"Expected a non-empty value for `target_id` but received {target_id!r}")
        extra_headers = {
            **strip_not_given(
                {
                    "anthropic-beta": ",".join(chain((str(e) for e in betas), ["experimental-claude-tag-2026-10-21"]))
                    if is_given(betas)
                    else not_given
                }
            ),
            **(extra_headers or {}),
        }
        extra_headers = {"anthropic-beta": "experimental-claude-tag-2026-10-21", **(extra_headers or {})}
        return cast(
            BetaClaudeTagBundleTarget,
            self._get(
                path_template(
                    "/v1/organizations/claude_tag/bundles/{bundle_id}/targets/{target_id}",
                    bundle_id=bundle_id,
                    target_id=target_id,
                ),
                options=make_request_options(
                    extra_headers=extra_headers,
                    extra_query=extra_query,
                    extra_body=extra_body,
                    timeout=timeout,
                    qualifiers={"beta": "true"},
                    span_name="anthropic.organization.claude_tag.bundles.targets.retrieve",
                    span_route="/v1/organizations/claude_tag/bundles/{bundle_id}/targets/{target_id}",
                    span_attributes={
                        "anthropic.organization.claude_tag.bundle.id": bundle_id,
                        "anthropic.organization.claude_tag.bundle.target.id": target_id,
                    },
                ),
                cast_to=cast(
                    Any, BetaClaudeTagBundleTarget
                ),  # Union types cannot be passed in as arguments in the type system
            ),
        )

    def list(
        self,
        bundle_id: str,
        *,
        limit: int | Omit = omit,
        page: str | Omit = omit,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> SyncPageCursor[BetaClaudeTagBundleTarget]:
        """
        List the Slack channels and Slack workspaces a Bundle is attached to, newest
        first by `created_at`. Only channels and workspaces the organization owns are
        listed; a Bundle that is attached to anything else has no Bundle Target for it.

        Args:
          bundle_id: The Bundle's identifier, starting with `capp_`.

          limit: Number of items to return per page, between 1 and 100. Defaults to 20.

          page: Opaque cursor from a previous response's `next_page`.

          betas: This endpoint is in beta: requests must send
              `experimental-claude-tag-2026-10-21` in this header.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not bundle_id:
            raise ValueError(f"Expected a non-empty value for `bundle_id` but received {bundle_id!r}")
        extra_headers = {
            **strip_not_given(
                {
                    "anthropic-beta": ",".join(chain((str(e) for e in betas), ["experimental-claude-tag-2026-10-21"]))
                    if is_given(betas)
                    else not_given
                }
            ),
            **(extra_headers or {}),
        }
        extra_headers = {"anthropic-beta": "experimental-claude-tag-2026-10-21", **(extra_headers or {})}
        return self._get_api_list(
            path_template("/v1/organizations/claude_tag/bundles/{bundle_id}/targets", bundle_id=bundle_id),
            page=SyncPageCursor[BetaClaudeTagBundleTarget],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query={
                    "limit": limit,
                    "page": page,
                },
                qualifiers={"beta": "true"},
                span_name="anthropic.organization.claude_tag.bundles.targets.list",
                span_route="/v1/organizations/claude_tag/bundles/{bundle_id}/targets",
                span_attributes={"anthropic.organization.claude_tag.bundle.id": bundle_id},
            ),
            model=cast(
                Any, BetaClaudeTagBundleTarget
            ),  # Union types cannot be passed in as arguments in the type system
        )

    def delete(
        self,
        target_id: str,
        *,
        bundle_id: str,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaClaudeTagDeletedBundleTarget:
        """Detach a Bundle from a Slack channel or a Slack workspace.

        A repeated detach
        returns 404.

        Args:
          bundle_id: The Bundle's identifier, starting with `capp_`.

          target_id: The Bundle Target's identifier, starting with `btgt_`. Attach Bundle and List
              Bundle Targets return it. It is never the identifier of the channel or
              workspace.

          betas: This endpoint is in beta: requests must send
              `experimental-claude-tag-2026-10-21` in this header.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not bundle_id:
            raise ValueError(f"Expected a non-empty value for `bundle_id` but received {bundle_id!r}")
        if not target_id:
            raise ValueError(f"Expected a non-empty value for `target_id` but received {target_id!r}")
        extra_headers = {
            **strip_not_given(
                {
                    "anthropic-beta": ",".join(chain((str(e) for e in betas), ["experimental-claude-tag-2026-10-21"]))
                    if is_given(betas)
                    else not_given
                }
            ),
            **(extra_headers or {}),
        }
        extra_headers = {"anthropic-beta": "experimental-claude-tag-2026-10-21", **(extra_headers or {})}
        return self._delete(
            path_template(
                "/v1/organizations/claude_tag/bundles/{bundle_id}/targets/{target_id}",
                bundle_id=bundle_id,
                target_id=target_id,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                qualifiers={"beta": "true"},
                span_name="anthropic.organization.claude_tag.bundles.targets.delete",
                span_route="/v1/organizations/claude_tag/bundles/{bundle_id}/targets/{target_id}",
                span_attributes={
                    "anthropic.organization.claude_tag.bundle.id": bundle_id,
                    "anthropic.organization.claude_tag.bundle.target.id": target_id,
                },
            ),
            cast_to=BetaClaudeTagDeletedBundleTarget,
        )


class AsyncTargets(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncTargetsWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#accessing-raw-response-data-eg-headers
        """
        return AsyncTargetsWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncTargetsWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#with_streaming_response
        """
        return AsyncTargetsWithStreamingResponse(self)

    async def create(
        self,
        bundle_id: str,
        *,
        target: BetaClaudeTagBundleTargetCreateParam,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaClaudeTagBundleTarget:
        """Attach a Bundle to a Slack channel or a Slack workspace.

        A Bundle attached to a
        workspace can be used in the workspace and in every channel in it. Attaching a
        Bundle to a channel or workspace it is already attached to returns the existing
        Bundle Target. The channel or workspace must be set up: attaching never sets a
        channel up. A group direct message takes no Bundle and returns 400.

        Args:
          bundle_id: The Bundle's identifier, starting with `capp_`.

          betas: This endpoint is in beta: requests must send
              `experimental-claude-tag-2026-10-21` in this header.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not bundle_id:
            raise ValueError(f"Expected a non-empty value for `bundle_id` but received {bundle_id!r}")
        extra_headers = {
            **strip_not_given(
                {
                    "anthropic-beta": ",".join(chain((str(e) for e in betas), ["experimental-claude-tag-2026-10-21"]))
                    if is_given(betas)
                    else not_given
                }
            ),
            **(extra_headers or {}),
        }
        extra_headers = {"anthropic-beta": "experimental-claude-tag-2026-10-21", **(extra_headers or {})}
        return cast(
            BetaClaudeTagBundleTarget,
            await self._post(
                path_template("/v1/organizations/claude_tag/bundles/{bundle_id}/targets", bundle_id=bundle_id),
                body=target,
                options=make_request_options(
                    extra_headers=extra_headers,
                    extra_query=extra_query,
                    extra_body=extra_body,
                    timeout=timeout,
                    qualifiers={"beta": "true"},
                    span_name="anthropic.organization.claude_tag.bundles.targets.create",
                    span_route="/v1/organizations/claude_tag/bundles/{bundle_id}/targets",
                    span_attributes={"anthropic.organization.claude_tag.bundle.id": bundle_id},
                ),
                cast_to=cast(
                    Any, BetaClaudeTagBundleTarget
                ),  # Union types cannot be passed in as arguments in the type system
            ),
        )

    async def retrieve(
        self,
        target_id: str,
        *,
        bundle_id: str,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaClaudeTagBundleTarget:
        """Get one Bundle Target.

        Returns 404 when `target_id` is the identifier of another
        Bundle's Bundle Target, or the Bundle Target was detached.

        Args:
          bundle_id: The Bundle's identifier, starting with `capp_`.

          target_id: The Bundle Target's identifier, starting with `btgt_`. Attach Bundle and List
              Bundle Targets return it. It is never the identifier of the channel or
              workspace.

          betas: This endpoint is in beta: requests must send
              `experimental-claude-tag-2026-10-21` in this header.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not bundle_id:
            raise ValueError(f"Expected a non-empty value for `bundle_id` but received {bundle_id!r}")
        if not target_id:
            raise ValueError(f"Expected a non-empty value for `target_id` but received {target_id!r}")
        extra_headers = {
            **strip_not_given(
                {
                    "anthropic-beta": ",".join(chain((str(e) for e in betas), ["experimental-claude-tag-2026-10-21"]))
                    if is_given(betas)
                    else not_given
                }
            ),
            **(extra_headers or {}),
        }
        extra_headers = {"anthropic-beta": "experimental-claude-tag-2026-10-21", **(extra_headers or {})}
        return cast(
            BetaClaudeTagBundleTarget,
            await self._get(
                path_template(
                    "/v1/organizations/claude_tag/bundles/{bundle_id}/targets/{target_id}",
                    bundle_id=bundle_id,
                    target_id=target_id,
                ),
                options=make_request_options(
                    extra_headers=extra_headers,
                    extra_query=extra_query,
                    extra_body=extra_body,
                    timeout=timeout,
                    qualifiers={"beta": "true"},
                    span_name="anthropic.organization.claude_tag.bundles.targets.retrieve",
                    span_route="/v1/organizations/claude_tag/bundles/{bundle_id}/targets/{target_id}",
                    span_attributes={
                        "anthropic.organization.claude_tag.bundle.id": bundle_id,
                        "anthropic.organization.claude_tag.bundle.target.id": target_id,
                    },
                ),
                cast_to=cast(
                    Any, BetaClaudeTagBundleTarget
                ),  # Union types cannot be passed in as arguments in the type system
            ),
        )

    def list(
        self,
        bundle_id: str,
        *,
        limit: int | Omit = omit,
        page: str | Omit = omit,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> AsyncPaginator[BetaClaudeTagBundleTarget, AsyncPageCursor[BetaClaudeTagBundleTarget]]:
        """
        List the Slack channels and Slack workspaces a Bundle is attached to, newest
        first by `created_at`. Only channels and workspaces the organization owns are
        listed; a Bundle that is attached to anything else has no Bundle Target for it.

        Args:
          bundle_id: The Bundle's identifier, starting with `capp_`.

          limit: Number of items to return per page, between 1 and 100. Defaults to 20.

          page: Opaque cursor from a previous response's `next_page`.

          betas: This endpoint is in beta: requests must send
              `experimental-claude-tag-2026-10-21` in this header.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not bundle_id:
            raise ValueError(f"Expected a non-empty value for `bundle_id` but received {bundle_id!r}")
        extra_headers = {
            **strip_not_given(
                {
                    "anthropic-beta": ",".join(chain((str(e) for e in betas), ["experimental-claude-tag-2026-10-21"]))
                    if is_given(betas)
                    else not_given
                }
            ),
            **(extra_headers or {}),
        }
        extra_headers = {"anthropic-beta": "experimental-claude-tag-2026-10-21", **(extra_headers or {})}
        return self._get_api_list(
            path_template("/v1/organizations/claude_tag/bundles/{bundle_id}/targets", bundle_id=bundle_id),
            page=AsyncPageCursor[BetaClaudeTagBundleTarget],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query={
                    "limit": limit,
                    "page": page,
                },
                qualifiers={"beta": "true"},
                span_name="anthropic.organization.claude_tag.bundles.targets.list",
                span_route="/v1/organizations/claude_tag/bundles/{bundle_id}/targets",
                span_attributes={"anthropic.organization.claude_tag.bundle.id": bundle_id},
            ),
            model=cast(
                Any, BetaClaudeTagBundleTarget
            ),  # Union types cannot be passed in as arguments in the type system
        )

    async def delete(
        self,
        target_id: str,
        *,
        bundle_id: str,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaClaudeTagDeletedBundleTarget:
        """Detach a Bundle from a Slack channel or a Slack workspace.

        A repeated detach
        returns 404.

        Args:
          bundle_id: The Bundle's identifier, starting with `capp_`.

          target_id: The Bundle Target's identifier, starting with `btgt_`. Attach Bundle and List
              Bundle Targets return it. It is never the identifier of the channel or
              workspace.

          betas: This endpoint is in beta: requests must send
              `experimental-claude-tag-2026-10-21` in this header.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not bundle_id:
            raise ValueError(f"Expected a non-empty value for `bundle_id` but received {bundle_id!r}")
        if not target_id:
            raise ValueError(f"Expected a non-empty value for `target_id` but received {target_id!r}")
        extra_headers = {
            **strip_not_given(
                {
                    "anthropic-beta": ",".join(chain((str(e) for e in betas), ["experimental-claude-tag-2026-10-21"]))
                    if is_given(betas)
                    else not_given
                }
            ),
            **(extra_headers or {}),
        }
        extra_headers = {"anthropic-beta": "experimental-claude-tag-2026-10-21", **(extra_headers or {})}
        return await self._delete(
            path_template(
                "/v1/organizations/claude_tag/bundles/{bundle_id}/targets/{target_id}",
                bundle_id=bundle_id,
                target_id=target_id,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                qualifiers={"beta": "true"},
                span_name="anthropic.organization.claude_tag.bundles.targets.delete",
                span_route="/v1/organizations/claude_tag/bundles/{bundle_id}/targets/{target_id}",
                span_attributes={
                    "anthropic.organization.claude_tag.bundle.id": bundle_id,
                    "anthropic.organization.claude_tag.bundle.target.id": target_id,
                },
            ),
            cast_to=BetaClaudeTagDeletedBundleTarget,
        )


class TargetsWithRawResponse:
    def __init__(self, targets: Targets) -> None:
        self._targets = targets

        self.create = to_raw_response_wrapper(
            targets.create,
        )
        self.retrieve = to_raw_response_wrapper(
            targets.retrieve,
        )
        self.list = to_raw_response_wrapper(
            targets.list,
        )
        self.delete = to_raw_response_wrapper(
            targets.delete,
        )


class AsyncTargetsWithRawResponse:
    def __init__(self, targets: AsyncTargets) -> None:
        self._targets = targets

        self.create = async_to_raw_response_wrapper(
            targets.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            targets.retrieve,
        )
        self.list = async_to_raw_response_wrapper(
            targets.list,
        )
        self.delete = async_to_raw_response_wrapper(
            targets.delete,
        )


class TargetsWithStreamingResponse:
    def __init__(self, targets: Targets) -> None:
        self._targets = targets

        self.create = to_streamed_response_wrapper(
            targets.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            targets.retrieve,
        )
        self.list = to_streamed_response_wrapper(
            targets.list,
        )
        self.delete = to_streamed_response_wrapper(
            targets.delete,
        )


class AsyncTargetsWithStreamingResponse:
    def __init__(self, targets: AsyncTargets) -> None:
        self._targets = targets

        self.create = async_to_streamed_response_wrapper(
            targets.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            targets.retrieve,
        )
        self.list = async_to_streamed_response_wrapper(
            targets.list,
        )
        self.delete = async_to_streamed_response_wrapper(
            targets.delete,
        )
