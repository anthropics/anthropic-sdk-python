from datetime import datetime
from typing_extensions import Literal

from ......_models import BaseModel
from .beta_google_managed_cmek_control import BetaGoogleManagedCMEKControl
from .beta_google_managed_storage_control import BetaGoogleManagedStorageControl

__all__ = ["BetaGoogleManagedDataControls"]


class BetaGoogleManagedDataControls(BaseModel):
    """
    A user profile's encryption key and storage bucket settings for Claude on Google Cloud's Agent Platform. Every user profile has one of these objects. You can read and update it, but not create or delete it. Keys and buckets are set for each region. A request's region depends on the Google endpoint it is sent to: `us` is the US multi-region endpoint and the regional endpoint of every location whose name starts with `us-`, `eu` is the EU multi-region endpoint and the regional endpoint of every location whose name starts with `europe-`, `sg` is the `asia-southeast1` regional endpoint, and `global` is the global endpoint, wherever Google serves the request. Anthropic may add regions.
    """

    bucket_label_value: str
    """The label value that every bucket set up for this profile must have.

    It never changes.
    """

    cmek: BetaGoogleManagedCMEKControl
    """
    The customer-managed encryption key control: the key in the end customer's
    Google Cloud KMS that is set for each region.
    """

    storage: BetaGoogleManagedStorageControl
    """
    The customer-owned storage control: the end customer's Cloud Storage bucket that
    is set for each region.
    """

    type: Literal["google_managed_data_controls"]
    """Object type. Always `google_managed_data_controls`."""

    updated_at: datetime
    """
    When an update last changed a control, or a region's status last changed, in RFC
    3339 format. A region that starts or stops reading `suspended`, a change to
    `last_checked_at` alone, and the removal of a retired entry do not count.
    """

    user_profile_id: str
    """The ID of the user profile that these controls belong to (`uprof_...`)."""
