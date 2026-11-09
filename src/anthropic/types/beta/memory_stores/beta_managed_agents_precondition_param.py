from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["BetaManagedAgentsPreconditionParam"]


class BetaManagedAgentsPreconditionParam(TypedDict, total=False):
    """Optional condition that must hold for an update to apply.

    When omitted, the update is unconditional. Asserts the current state of the memory being updated. When an update changes `path`, the precondition still refers to the memory's current content, not the destination path. Currently the only supported variant is `content_sha256`.
    """

    type: Required[Literal["content_sha256"]]

    content_sha256: str
    """
    Expected `content_sha256` of the stored memory (64 lowercase hexadecimal
    characters). Typically the `content_sha256` returned by a prior read or list
    call. Because the server applies no content normalization, clients can also
    compute this locally as the SHA-256 of the UTF-8 content bytes.
    """
