# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["BetaDreamMemoryStoreInputParam"]


class BetaDreamMemoryStoreInputParam(TypedDict, total=False):
    """An input memory store the dream reads from.

    The dream never mutates this store unless it is also the destination: with output_behavior {type: "update_existing"} the job consolidates this store in place.
    """

    memory_store_id: Required[str]

    type: Required[Literal["memory_store"]]
