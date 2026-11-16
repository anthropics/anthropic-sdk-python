from typing import Union
from typing_extensions import Annotated, TypeAlias

from ..._models import UnionDiscriminator
from .api_error_object import APIErrorObject
from .billing_error_object import BillingErrorObject
from .not_found_error_object import NotFoundErrorObject
from .overloaded_error_object import OverloadedErrorObject
from .permission_error_object import PermissionErrorObject
from .rate_limit_error_object import RateLimitErrorObject
from .authentication_error_object import AuthenticationErrorObject
from .gateway_timeout_error_object import GatewayTimeoutErrorObject
from .invalid_request_error_object import InvalidRequestErrorObject

__all__ = ["ErrorObject"]

ErrorObject: TypeAlias = Annotated[
    Union[
        InvalidRequestErrorObject,
        AuthenticationErrorObject,
        BillingErrorObject,
        PermissionErrorObject,
        NotFoundErrorObject,
        RateLimitErrorObject,
        GatewayTimeoutErrorObject,
        APIErrorObject,
        OverloadedErrorObject,
    ],
    UnionDiscriminator("type"),
]
