# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Union
from typing_extensions import Annotated, TypeAlias

from .._utils import PropertyInfo
from .beta_api_error import BetaAPIError
from .beta_not_found_error import BetaNotFoundError
from .beta_overloaded_error import BetaOverloadedError
from .beta_permission_error import BetaPermissionError
from .beta_rate_limit_error import BetaRateLimitError
from .beta_authentication_error import BetaAuthenticationError
from .beta_invalid_request_error import BetaInvalidRequestError

__all__ = ["BetaError"]

BetaError: TypeAlias = Annotated[
    Union[
        BetaInvalidRequestError,
        BetaAuthenticationError,
        BetaPermissionError,
        BetaNotFoundError,
        BetaRateLimitError,
        BetaAPIError,
        BetaOverloadedError,
    ],
    PropertyInfo(discriminator="type"),
]
