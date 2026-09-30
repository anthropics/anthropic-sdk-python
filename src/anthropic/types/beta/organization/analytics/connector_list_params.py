from __future__ import annotations

import datetime
from typing import List, Union, Optional
from typing_extensions import Literal, TypedDict

from ....._types import SequenceNotStr

__all__ = ["ConnectorListParams"]


class ConnectorListParams(TypedDict, total=False):
    date: Union[str, datetime.date, None]
    """UTC date in YYYY-MM-DD format.

    The day to get connector usage for. Data is typically available with a 1-day lag
    (varies by query; the error for a too-recent date names the latest available
    day) and may be revised by a few percent over the following days. No earlier
    than 2026-01-01.
    """

    ending_date: Union[str, datetime.date, None]
    """UTC date in YYYY-MM-DD format.

    End of the date range (exclusive); only valid with `starting_date`. Data is
    typically available with a 1-day lag (varies by query; the error for a
    too-recent date names the latest available day), so this can be at most today —
    which is also the default when omitted, resolved once when the first page is
    served and reused for the rest of the pagination sequence. At most 366 days
    after `starting_date`.
    """

    filter: Optional[SequenceNotStr[str]]
    """Filters as `dimension:value`, e.g.

    `filter[]=rbac_group_id:{id}`. Repeat the param for OR within a dimension and
    across dimensions for AND. Supported dimensions on this endpoint:
    `connector_name`, `product`, `rbac_group_id`, `user_id`. Value forms:
    `connector_name` matches case-insensitively, a display name such as 'GitHub MCP'
    also matches its normalized stored form ('github'), and for rows whose
    `connector_name` is an opaque connector id the connector's display name
    (`connector_display_name`) also matches; `product` is one of `chat`,
    `claude_code`, `cowork`, or `office_agent`; `rbac_group_id` takes the tagged id
    (`rbac_group_...`, as emitted in responses and by the spend-limits API) or a
    bare group UUID, and matches users who held the group at any point during each
    covered UTC day (time-of-usage attribution); `user_id` takes a tagged user id
    (`user_...`), as emitted in responses. An unsupported dimension returns 400. At
    most 100 entries.
    """

    group_by: Optional[List[Literal["product", "rbac_group_id", "user_id"]]]
    """Dimensions to break results out by (e.g.

    `group_by[]=user_id`). Supported on this endpoint: `product`, `rbac_group_id`,
    `user_id`. Grouped rows carry the requested dimension values as additional
    fields and paginate like ungrouped responses via `next_page`; an unsupported
    dimension returns 400. `rbac_group_id` attributes a user to every group they
    held at any point during each covered UTC day, so grouped rows are not an
    exclusive partition and can sum above org-level totals. At most 100 entries.
    """

    limit: Optional[int]
    """Number of results per page (1-1000, default 100)."""

    order: Optional[Literal["asc", "desc"]]
    """Sort direction: `asc` or `desc`.

    Defaults to `asc` for the endpoint's sort column and to `desc` when `order_by`
    names a metric (a top-N ranking). Applies to `order_by`, or to the endpoint's
    default sort field when `order_by` is omitted.
    """

    order_by: Optional[str]
    """Sort field.

    Restricted to the endpoint's sort column plus its rankable metrics (metrics
    default to descending; a few metrics rank in date-range mode only, per the
    endpoint's documented orderable set).
    """

    page: Optional[str]
    """Opaque cursor from a previous response's `next_page` field."""

    starting_date: Union[str, datetime.date, None]
    """UTC date in YYYY-MM-DD format.

    Start of a date range (inclusive). Enables rollup mode: one row per entity
    aggregated over the whole range — addable counters are summed across days, and a
    distinct count is never summed where summing could double-count (a field's range
    value is recomputed exactly over the window, approximate via HLL with typical
    error under 2%, null, or — for the creation-event counts, whose per-day values
    cannot overlap — a per-day sum that is itself exact; each field's own
    description says which). Use either `date` or `starting_date`, not both. Data is
    typically available with a 1-day lag (varies by query; the error for a
    too-recent date names the latest available day) and may be revised by a few
    percent over the following days. No earlier than 2026-01-01.
    """
