from typing_extensions import Literal, TypeAlias

__all__ = ["BetaManagedAgentsCredentialValidationStatus"]

BetaManagedAgentsCredentialValidationStatus: TypeAlias = Literal["valid", "invalid", "unknown"]
"""Overall verdict of a credential validation probe.

- `valid` - The credential successfully authenticated against its MCP server.
- `invalid` - The probe reached the MCP server and the server rejected the credential, or no access token is stored. A refresh, if one was tried, didn't recover it. Usually the end user needs to authorize again.
- `unknown` - The probe couldn't tell whether the credential works, for example because of a network error or because a refresh succeeded but the new access token wasn't tested. Validate the credential again to find out.
"""
