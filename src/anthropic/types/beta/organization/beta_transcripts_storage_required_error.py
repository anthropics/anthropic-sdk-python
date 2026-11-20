from typing_extensions import Literal

from ...._exceptions import BadRequestError
from .beta_transcripts_storage_required_error_details import BetaTranscriptsStorageRequiredErrorDetails

__all__ = ["BetaTranscriptsStorageRequiredError"]


class BetaTranscriptsStorageRequiredError(BadRequestError):
    """
    In an organization managed through AWS or Google Cloud, the request would leave the Workspace with `inference_data_privacy.human_review` disabled and `inference_data_privacy.transcripts_storage` not set to External Storage. With human review disabled, the organization reviews its own flagged requests, and it receives them only in that storage.
    """

    error_code: Literal["transcripts_storage_required"]  # pyright: ignore[reportIncompatibleVariableOverride]
    details: BetaTranscriptsStorageRequiredErrorDetails  # pyright: ignore[reportIncompatibleVariableOverride]
