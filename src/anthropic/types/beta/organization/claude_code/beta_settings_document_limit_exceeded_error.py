from typing_extensions import Literal

from ....._exceptions import BadRequestError
from .beta_settings_document_limit_exceeded_error_details import BetaSettingsDocumentLimitExceededErrorDetails

__all__ = ["BetaSettingsDocumentLimitExceededError"]


class BetaSettingsDocumentLimitExceededError(BadRequestError):
    """
    The organization has reached its limit of settings documents, counting unused ones. An owner can remove unused documents in claude.ai. Deleting a group's settings or clearing the default settings also frees a document, if nothing else uses it. None of these works once the organization has also reached its settings history limit.
    """

    error_code: Literal["settings_document_limit_exceeded"]  # pyright: ignore[reportIncompatibleVariableOverride]
    details: BetaSettingsDocumentLimitExceededErrorDetails  # pyright: ignore[reportIncompatibleVariableOverride]
