from __future__ import annotations

from typing import Iterable
from typing_extensions import Required, TypedDict

from ..message_create_params import MessageCreateParamsNonStreaming

__all__ = ["BatchCreateParams", "Request"]


class BatchCreateParams(TypedDict, total=False):
    requests: Required[Iterable[Request]]
    """List of requests for prompt completion.

    Each is an individual request to create a Message.
    """

    user_profile_id: str
    """The user profile ID to attribute the requests in this batch to.

    Use when acting on behalf of a party other than your organization. Requires the
    `user-profiles` beta header. Applies to every request in the batch; an
    individual request whose `user_profile_id` body field conflicts with this header
    is errored.
    """

    workspace_id: str
    """Optional header to select the Workspace for this request.

    The value is a Workspace ID (for example, `wrkspc_011CZkZaBF1tNoB5wlCeusgy`).

    Only needed for credentials that can act on more than one Workspace. A
    credential that belongs to a specific Workspace may omit it; if sent, it must
    match that Workspace.
    """


class Request(TypedDict, total=False):
    custom_id: Required[str]
    """Developer-provided ID created for each request in a Message Batch.

    Useful for matching results to requests, as results may be given out of request
    order.

    Must be unique for each request within the Message Batch.
    """

    params: Required[MessageCreateParamsNonStreaming]
    """Messages API creation parameters for the individual request.

    See the
    [Messages API reference](https://platform.claude.com/docs/en/api/messages) for
    full documentation on available parameters.
    """
