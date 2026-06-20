# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["BetaManagedAgentsPreconditionParam"]


class BetaManagedAgentsPreconditionParam(TypedDict, total=False):
    """
    Optimistic-concurrency precondition: the update applies only if the memory's stored `content_sha256` equals the supplied value. On mismatch, the request returns `memory_precondition_failed_error` (HTTP 409); re-read the memory and retry against the fresh state. If the precondition fails but the stored state already exactly matches the requested `content` and `path`, the server returns 200 instead of 409.
    """

    type: Required[Literal["content_sha256"]]

    content_sha256: str
    """
    Expected `content_sha256` of the stored memory (64 lowercase hexadecimal
    characters). Typically the `content_sha256` returned by a prior read or list
    call. Because the server applies no content normalization, clients can also
    compute this locally as the SHA-256 of the UTF-8 content bytes.
    """
