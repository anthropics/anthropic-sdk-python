from typing import Union
from typing_extensions import Annotated, TypeAlias

from .._models import UnionDiscriminator
from .beta_api_error_object import BetaAPIErrorObject
from .beta_billing_error_object import BetaBillingErrorObject
from .beta_not_found_error_object import BetaNotFoundErrorObject
from .beta_overloaded_error_object import BetaOverloadedErrorObject
from .beta_permission_error_object import BetaPermissionErrorObject
from .beta_rate_limit_error_object import BetaRateLimitErrorObject
from .beta_authentication_error_object import BetaAuthenticationErrorObject
from .beta_gateway_timeout_error_object import BetaGatewayTimeoutErrorObject
from .beta_invalid_request_error_object import BetaInvalidRequestErrorObject

__all__ = ["BetaErrorObject"]

BetaErrorObject: TypeAlias = Annotated[
    Union[
        BetaInvalidRequestErrorObject,
        BetaAuthenticationErrorObject,
        BetaBillingErrorObject,
        BetaPermissionErrorObject,
        BetaNotFoundErrorObject,
        BetaRateLimitErrorObject,
        BetaGatewayTimeoutErrorObject,
        BetaAPIErrorObject,
        BetaOverloadedErrorObject,
    ],
    UnionDiscriminator("type"),
]
