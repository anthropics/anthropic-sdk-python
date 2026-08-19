# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union
from typing_extensions import TypeAlias

from .beta_browser_state_change_tab_opened_param import BetaBrowserStateChangeTabOpenedParam
from .beta_browser_state_change_download_failed_param import BetaBrowserStateChangeDownloadFailedParam
from .beta_browser_state_change_download_started_param import BetaBrowserStateChangeDownloadStartedParam
from .beta_browser_state_change_download_completed_param import BetaBrowserStateChangeDownloadCompletedParam

__all__ = ["BetaBrowserStateChangeParam"]

BetaBrowserStateChangeParam: TypeAlias = Union[
    BetaBrowserStateChangeTabOpenedParam,
    BetaBrowserStateChangeDownloadStartedParam,
    BetaBrowserStateChangeDownloadCompletedParam,
    BetaBrowserStateChangeDownloadFailedParam,
]
