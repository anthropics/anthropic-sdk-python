from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["BetaGCPExternalStorageConfigParam"]


class BetaGCPExternalStorageConfigParam(TypedDict, total=False):
    """A Google Cloud Storage bucket."""

    bucket_name: Required[str]
    """
    The bucket's name, without `gs://`: 3 to 63 lower-case letters, digits and
    hyphens, starting and ending with a letter or digit. It can't start with `goog`
    or contain `google`.
    """

    project_number: Required[str]
    """
    Project number, not project ID, of the Google Cloud project that holds the
    bucket.
    """

    region: Required[str]
    """
    The bucket's Google Cloud region, such as `us-east5`: one of the single regions
    that the setup guide lists. Dual-regions and multi-regions aren't supported.
    """

    type: Required[Literal["gcp"]]
