# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["UserUpdateParams"]


class UserUpdateParams(TypedDict, total=False):
    role: Required[Literal["billing", "claude_code_user", "developer", "managed", "user"]]
    """New role for the User.

    The accepted values depend on the organization type. Console and API
    organizations accept `user`, `developer`, `billing`, and `claude_code_user`;
    `admin` cannot be assigned through the API. Claude Enterprise organizations
    accept `user` and `managed`.
    """
