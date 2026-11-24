from datetime import datetime
from typing_extensions import Literal

from ......._models import BaseModel
from .beta_google_managed_project_cmek_control import BetaGoogleManagedProjectCMEKControl
from .beta_google_managed_project_storage_control import BetaGoogleManagedProjectStorageControl

__all__ = ["BetaGoogleManagedProjectDataControls"]


class BetaGoogleManagedProjectDataControls(BaseModel):
    """
    A Google Cloud project's encryption key and storage bucket settings for Claude on Google Cloud's Agent Platform. Your organization has one of these objects for each Google Cloud project that it has proved it owns. You can read and update it, but not create or delete it. Keys and buckets are set for each region. A request's region depends on the Google endpoint it is sent to: `us` is the US multi-region endpoint and the regional endpoint of every location whose name starts with `us-`, `eu` is the EU multi-region endpoint and the regional endpoint of every location whose name starts with `europe-`, `sg` is the `asia-southeast1` regional endpoint, and `global` is the global endpoint, wherever Google serves the request. Anthropic may add regions.
    """

    cmek: BetaGoogleManagedProjectCMEKControl
    """
    The customer-managed encryption key control: the key in your Google Cloud KMS
    that is set for each region. It covers the project's requests that name no user
    profile, or a user profile that has no key of its own for the project.
    """

    project_number: str
    """
    The number of the Google Cloud project that these controls belong to, in
    decimal.
    """

    storage: BetaGoogleManagedProjectStorageControl
    """
    The customer-owned storage control: your Cloud Storage bucket that is set for
    each region. It covers the project's requests that name no user profile, or a
    user profile that has no bucket of its own for the project.
    """

    type: Literal["google_managed_project_data_controls"]
    """Object type. Always `google_managed_project_data_controls`."""

    updated_at: datetime
    """
    When an update last changed a control, or a region's status last changed, in RFC
    3339 format. A region that starts or stops reading `suspended`, a change to
    `last_checked_at` alone, and the removal of a retired entry do not count.
    """
