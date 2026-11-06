from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["BetaUserProfileEnrollEndUserActionParam"]


class BetaUserProfileEnrollEndUserActionParam(TypedDict, total=False):
    """The end-user that the profile represents enrolls in a program."""

    type: Required[Literal["enroll_end_user"]]
