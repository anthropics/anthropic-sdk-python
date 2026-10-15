from __future__ import annotations

from typing import Union, Optional
from datetime import date
from typing_extensions import Required, TypedDict

from ....._types import SequenceNotStr

__all__ = ["SummaryListParams"]


class SummaryListParams(TypedDict, total=False):
    starting_date: Required[Union[str, date]]
    """UTC date in YYYY-MM-DD format.

    Start of the date range (inclusive). Data is typically available with a 1-day
    lag (varies by query; the error for a too-recent date names the latest available
    day) and may be revised by a few percent over the following days. No earlier
    than 2026-01-01.
    """

    ending_date: Union[str, date, None]
    """UTC date in YYYY-MM-DD format.

    End of the date range (exclusive). Data is typically available with a 1-day lag,
    so this can be at most today — which is also the default when omitted, making
    the last entry cover the most recent available day. Data may be revised by a few
    percent over the following days. The range may span at most 366 days.
    """

    filter: Optional[SequenceNotStr[str]]
    """Filters as `dimension:value`.

    Only `rbac_group_id` is supported (e.g. `filter[]=rbac_group_id:{id}`); repeat
    the param to OR across groups. Scopes the whole day series to members of the
    matching group(s), re-aggregated from member-level activity — org-wide
    seat/invite fields and the adoption rates derived from them are null on scoped
    rows. `rbac_group_id` accepts the tagged id (`rbac_group_...`, as emitted in
    responses and by the spend-limits API) or a bare group UUID, and matches users
    who held the group at any point during each UTC day (time-of-usage attribution).
    At most 100 entries.
    """

    limit: Optional[int]
    """Number of results per page (1-1000, default 100).

    The day series (at most 366 entries) is currently returned in full in a single
    page, so `limit` does not yet shorten it.
    """

    page: Optional[str]
    """Opaque cursor from a previous response's `next_page` field.

    `next_page` is currently always null, so there is never a cursor to send.
    """
