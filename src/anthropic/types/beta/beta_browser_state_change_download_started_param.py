# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["BetaBrowserStateChangeDownloadStartedParam"]


class BetaBrowserStateChangeDownloadStartedParam(TypedDict, total=False):
    """A file download that started during this call."""

    download_id: Required[str]
    """
    The caller-assigned identifier for this download, stable across the state
    changes reporting it.
    """

    type: Required[Literal["download_started"]]

    url: Required[str]
    """The final post-redirect URL the download was served from."""
