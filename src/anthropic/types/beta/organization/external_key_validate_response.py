# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["ExternalKeyValidateResponse"]


class ExternalKeyValidateResponse(BaseModel):
    """Result of a validation roundtrip against the customer's KMS.

    HTTP 200 for both outcomes — the operation completed; `status` says
    whether the key works.
    """

    error: Optional[str] = None
    """Error message when status is `failure`. Null otherwise."""

    status: Literal["failure", "success"]
    """`success` — encrypt/decrypt roundtrip succeeded.

    `failure` — the roundtrip failed or timed out; see `error`.
    """

    type: Literal["external_key_validation"]
