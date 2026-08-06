# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

from .beta_currency import BetaCurrency

__all__ = ["BetaMonetaryAmountParam"]


class BetaMonetaryAmountParam(TypedDict, total=False):
    """A monetary amount in a specific currency."""

    amount: Required[str]
    """
    Amount in minor units of the currency, as an integer decimal string with no
    leading zeros: "2500" is $25.00 and "50" is fifty cents. A string rather than a
    number so no float rounding is ever applied.
    """

    currency: Required[BetaCurrency]
    """Uppercase ISO-4217 currency code.

    `USD` is the only currency currently supported; the accepted set is closed and
    grows only when a new currency is priced.
    """
