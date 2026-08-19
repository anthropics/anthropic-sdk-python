# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import Literal, Required, TypedDict

__all__ = ["BetaBrowserStateChangeDownloadCompletedParam"]


class BetaBrowserStateChangeDownloadCompletedParam(TypedDict, total=False):
    """
    A file download that finished during this call, reported with the
    same `download_id` as its `download_started` — or without a prior
    `download_started`, when the download finished during the call that
    started it (at most one state change per `download_id` per result).
    """

    download_id: Required[str]
    """
    The caller-assigned identifier for this download, stable across the state
    changes reporting it.
    """

    type: Required[Literal["download_completed"]]

    url: Required[str]
    """The final post-redirect URL the download was served from."""

    path: Optional[str]
    """Where the executor saved the file, on the executor's filesystem.

    Only included when another tool in the same environment can read the file at
    that path.
    """

    size_bytes: Optional[int]
    """The completed download's size."""
