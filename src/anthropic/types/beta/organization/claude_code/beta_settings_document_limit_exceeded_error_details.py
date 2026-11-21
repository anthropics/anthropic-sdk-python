from typing_extensions import Literal

from ....._models import BaseModel

__all__ = ["BetaSettingsDocumentLimitExceededErrorDetails"]


class BetaSettingsDocumentLimitExceededErrorDetails(BaseModel):
    """
    The organization has reached its limit of settings documents, counting unused ones. An owner can remove unused documents in claude.ai. Deleting a group's settings or clearing the default settings also frees a document, if nothing else uses it. None of these works once the organization has also reached its settings history limit.
    """

    error_code: Literal["settings_document_limit_exceeded"]
