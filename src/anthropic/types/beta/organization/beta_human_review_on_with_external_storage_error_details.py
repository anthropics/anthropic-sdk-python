from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaHumanReviewOnWithExternalStorageErrorDetails"]


class BetaHumanReviewOnWithExternalStorageErrorDetails(BaseModel):
    """
    The request would leave the Workspace with `inference_data_privacy.safeguards_storage` set to External Storage and `inference_data_privacy.human_review` enabled. Anthropic doesn't offer human review of data in a customer's own storage. Set `human_review` to `disabled`, or `safeguards_storage` to `internal`.
    """

    error_code: Literal["human_review_on_with_external_storage"]
