from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["APIKeyOrganizationScope"]


class APIKeyOrganizationScope(BaseModel):
    type: Literal["organization"]
    """Scope type.

    Always `"organization"`: the API key has no Workspace. Only a principal-bound
    API key can have this scope.
    """
