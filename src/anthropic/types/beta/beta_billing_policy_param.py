from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

from .beta_bill_to import BetaBillTo

__all__ = ["BetaBillingPolicyParam"]


class BetaBillingPolicyParam(TypedDict, total=False):
    """Declares which organization is billed for the request."""

    type: Required[Literal["billing_policy"]]

    bill_to: BetaBillTo
    """Who is billed.

    `self`, the default, bills your organization, as if `billing_policy` were
    omitted. `user_profile` bills the customer behind the user profile the request
    names; if that customer has not linked an Anthropic organization to the profile,
    or has not allowed your organization to bill it, the request is rejected rather
    than billed to you.
    """
