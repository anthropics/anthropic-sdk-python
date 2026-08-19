# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union
from typing_extensions import TypeAlias

from .browser_state_change_tab_opened_param import BrowserStateChangeTabOpenedParam
from .browser_state_change_download_failed_param import BrowserStateChangeDownloadFailedParam
from .browser_state_change_download_started_param import BrowserStateChangeDownloadStartedParam
from .browser_state_change_download_completed_param import BrowserStateChangeDownloadCompletedParam

__all__ = ["BrowserStateChangeParam"]

BrowserStateChangeParam: TypeAlias = Union[
    BrowserStateChangeTabOpenedParam,
    BrowserStateChangeDownloadStartedParam,
    BrowserStateChangeDownloadCompletedParam,
    BrowserStateChangeDownloadFailedParam,
]
