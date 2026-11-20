from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaGCPExternalStorageConfig"]


class BetaGCPExternalStorageConfig(BaseModel):
    """A Google Cloud Storage bucket."""

    bucket_name: str
    """The bucket's name, without `gs://`."""

    project_number: str
    """Number of the Google Cloud project that holds the bucket."""

    region: str
    """The bucket's Google Cloud region."""

    type: Literal["gcp"]
