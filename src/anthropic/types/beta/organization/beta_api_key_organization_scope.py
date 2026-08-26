# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaAPIKeyOrganizationScope"]


class BetaAPIKeyOrganizationScope(BaseModel):
    type: Literal["organization"]
    """Scope type.

    Always `"organization"`: the API key has no Workspace. Only a principal-bound
    API key can have this scope.
    """
