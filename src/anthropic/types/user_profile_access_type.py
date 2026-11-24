from typing_extensions import Literal, TypeAlias

__all__ = ["UserProfileAccessType"]

UserProfileAccessType: TypeAlias = Literal["application", "passthrough"]
"""How the platform uses the API on behalf of the entity this profile represents.

`application`: the platform sells a product that uses the API behind the scenes, and the profile represents an individual end-user of that product. `passthrough`: the platform resells raw inference, and the profile identifies the resold-to company.

- `application` - The user profile represents an individual end-user of a product that the platform builds on the API. New profiles get this value by default.
- `passthrough` - The user profile represents a company that the platform resells Claude access to.
"""
