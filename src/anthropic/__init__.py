# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os as _os
import typing as _t
import logging as _logging

from ._version import __title__, __version__

if _t.TYPE_CHECKING:
    from . import types as types
    from ._types import NOT_GIVEN, Omit, NoneType, NotGiven, Transport, ProxiesTypes, omit, not_given
    from ._utils import file_from_path as file_from_path
    from ._client import (
        Client as Client,
        Stream as Stream,
        Timeout as Timeout,
        Anthropic as Anthropic,
        AsyncClient as AsyncClient,
        AsyncStream as AsyncStream,
        AsyncAnthropic as AsyncAnthropic,
        RequestOptions as RequestOptions,
    )
    from ._models import BaseModel as BaseModel
    from .lib.aws import AnthropicAWS as AnthropicAWS, AsyncAnthropicAWS as AsyncAnthropicAWS
    from ._response import APIResponse as APIResponse, AsyncAPIResponse as AsyncAPIResponse
    from .lib.tools import beta_tool as beta_tool, beta_async_tool as beta_async_tool
    from ._constants import (
        AI_PROMPT as AI_PROMPT,
        HUMAN_PROMPT as HUMAN_PROMPT,
        DEFAULT_TIMEOUT as DEFAULT_TIMEOUT,
        DEFAULT_MAX_RETRIES as DEFAULT_MAX_RETRIES,
        DEFAULT_CONNECTION_LIMITS as DEFAULT_CONNECTION_LIMITS,
    )
    from .lib.vertex import AnthropicVertex as AnthropicVertex, AsyncAnthropicVertex as AsyncAnthropicVertex
    from ._exceptions import (
        APIError as APIError,
        ConflictError as ConflictError,
        NotFoundError as NotFoundError,
        AnthropicError as AnthropicError,
        APIStatusError as APIStatusError,
        RateLimitError as RateLimitError,
        APITimeoutError as APITimeoutError,
        BadRequestError as BadRequestError,
        APIConnectionError as APIConnectionError,
        AuthenticationError as AuthenticationError,
        InternalServerError as InternalServerError,
        PermissionDeniedError as PermissionDeniedError,
        UnprocessableEntityError as UnprocessableEntityError,
        APIWebhookValidationError as APIWebhookValidationError,
        APIResponseValidationError as APIResponseValidationError,
    )
    from .lib.bedrock import (
        AnthropicBedrock as AnthropicBedrock,
        AsyncAnthropicBedrock as AsyncAnthropicBedrock,
        AnthropicBedrockMantle as AnthropicBedrockMantle,
        AsyncAnthropicBedrockMantle as AsyncAnthropicBedrockMantle,
    )
    from .lib.foundry import AnthropicFoundry as AnthropicFoundry, AsyncAnthropicFoundry as AsyncAnthropicFoundry
    from ._base_client import (
        DefaultHttpxClient as DefaultHttpxClient,
        DefaultAioHttpClient as DefaultAioHttpClient,
        DefaultAsyncHttpxClient as DefaultAsyncHttpxClient,
    )
    from .lib.streaming import (
        TextEvent as TextEvent,
        BetaTextEvent as BetaTextEvent,
        MessageStream as MessageStream,
        InputJsonEvent as InputJsonEvent,
        MessageStopEvent as MessageStopEvent,
        BetaMessageStream as BetaMessageStream,
        AsyncMessageStream as AsyncMessageStream,
        BetaInputJsonEvent as BetaInputJsonEvent,
        MessageStreamEvent as MessageStreamEvent,
        ParsedBetaTextEvent as ParsedBetaTextEvent,
        MessageStreamManager as MessageStreamManager,
        ContentBlockStopEvent as ContentBlockStopEvent,
        BetaAsyncMessageStream as BetaAsyncMessageStream,
        BetaMessageStreamEvent as BetaMessageStreamEvent,
        ParsedMessageStopEvent as ParsedMessageStopEvent,
        BetaMessageStreamManager as BetaMessageStreamManager,
        ParsedMessageStreamEvent as ParsedMessageStreamEvent,
        AsyncMessageStreamManager as AsyncMessageStreamManager,
        BetaContentBlockStopEvent as BetaContentBlockStopEvent,
        ParsedBetaMessageStopEvent as ParsedBetaMessageStopEvent,
        ParsedContentBlockStopEvent as ParsedContentBlockStopEvent,
        ParsedBetaMessageStreamEvent as ParsedBetaMessageStreamEvent,
        BetaAsyncMessageStreamManager as BetaAsyncMessageStreamManager,
        ParsedBetaContentBlockStopEvent as ParsedBetaContentBlockStopEvent,
    )
    from .lib.credentials import (
        EnvToken as EnvToken,
        TokenCache as TokenCache,
        AccessToken as AccessToken,
        StaticToken as StaticToken,
        InMemoryConfig as InMemoryConfig,
        AccessTokenAuth as AccessTokenAuth,
        CredentialsFile as CredentialsFile,
        CredentialResult as CredentialResult,
        IdentityTokenFile as IdentityTokenFile,
        AccessTokenProvider as AccessTokenProvider,
        IdentityTokenProvider as IdentityTokenProvider,
        WorkloadIdentityError as WorkloadIdentityError,
        WorkloadIdentityCredentials as WorkloadIdentityCredentials,
        default_credentials as default_credentials,
        exchange_federation_assertion as exchange_federation_assertion,
    )
    from .lib._parse._transform import transform_schema as transform_schema
    from ._utils._resources_proxy import resources as resources

__all__ = [
    "types",
    "__version__",
    "__title__",
    "NoneType",
    "Transport",
    "ProxiesTypes",
    "NotGiven",
    "NOT_GIVEN",
    "not_given",
    "Omit",
    "omit",
    "AnthropicError",
    "APIError",
    "APIStatusError",
    "APITimeoutError",
    "APIConnectionError",
    "APIResponseValidationError",
    "APIWebhookValidationError",
    "BadRequestError",
    "AuthenticationError",
    "PermissionDeniedError",
    "NotFoundError",
    "ConflictError",
    "UnprocessableEntityError",
    "RateLimitError",
    "InternalServerError",
    "Timeout",
    "RequestOptions",
    "Client",
    "AsyncClient",
    "Stream",
    "AsyncStream",
    "Anthropic",
    "AsyncAnthropic",
    "file_from_path",
    "BaseModel",
    "DEFAULT_TIMEOUT",
    "DEFAULT_MAX_RETRIES",
    "DEFAULT_CONNECTION_LIMITS",
    "DefaultHttpxClient",
    "DefaultAsyncHttpxClient",
    "DefaultAioHttpClient",
    "HUMAN_PROMPT",
    "AI_PROMPT",
    "beta_tool",
    "beta_async_tool",
    "transform_schema",
]

_LAZY_ATTRS: dict[str, tuple[str, str | None]] = {
    "types": (".types", None),
    "NoneType": ("._types", "NoneType"),
    "Transport": ("._types", "Transport"),
    "ProxiesTypes": ("._types", "ProxiesTypes"),
    "NotGiven": ("._types", "NotGiven"),
    "NOT_GIVEN": ("._types", "NOT_GIVEN"),
    "not_given": ("._types", "not_given"),
    "Omit": ("._types", "Omit"),
    "omit": ("._types", "omit"),
    "Timeout": ("._client", "Timeout"),
    "RequestOptions": ("._client", "RequestOptions"),
    "Client": ("._client", "Client"),
    "AsyncClient": ("._client", "AsyncClient"),
    "Stream": ("._client", "Stream"),
    "AsyncStream": ("._client", "AsyncStream"),
    "Anthropic": ("._client", "Anthropic"),
    "AsyncAnthropic": ("._client", "AsyncAnthropic"),
    "file_from_path": ("._utils", "file_from_path"),
    "BaseModel": ("._models", "BaseModel"),
    "DEFAULT_TIMEOUT": ("._constants", "DEFAULT_TIMEOUT"),
    "DEFAULT_MAX_RETRIES": ("._constants", "DEFAULT_MAX_RETRIES"),
    "DEFAULT_CONNECTION_LIMITS": ("._constants", "DEFAULT_CONNECTION_LIMITS"),
    "HUMAN_PROMPT": ("._constants", "HUMAN_PROMPT"),
    "AI_PROMPT": ("._constants", "AI_PROMPT"),
    "AnthropicError": ("._exceptions", "AnthropicError"),
    "APIError": ("._exceptions", "APIError"),
    "APIStatusError": ("._exceptions", "APIStatusError"),
    "APITimeoutError": ("._exceptions", "APITimeoutError"),
    "APIConnectionError": ("._exceptions", "APIConnectionError"),
    "APIResponseValidationError": ("._exceptions", "APIResponseValidationError"),
    "APIWebhookValidationError": ("._exceptions", "APIWebhookValidationError"),
    "BadRequestError": ("._exceptions", "BadRequestError"),
    "AuthenticationError": ("._exceptions", "AuthenticationError"),
    "PermissionDeniedError": ("._exceptions", "PermissionDeniedError"),
    "NotFoundError": ("._exceptions", "NotFoundError"),
    "ConflictError": ("._exceptions", "ConflictError"),
    "UnprocessableEntityError": ("._exceptions", "UnprocessableEntityError"),
    "RateLimitError": ("._exceptions", "RateLimitError"),
    "InternalServerError": ("._exceptions", "InternalServerError"),
    "APIResponse": ("._response", "APIResponse"),
    "AsyncAPIResponse": ("._response", "AsyncAPIResponse"),
    "DefaultHttpxClient": ("._base_client", "DefaultHttpxClient"),
    "DefaultAsyncHttpxClient": ("._base_client", "DefaultAsyncHttpxClient"),
    "DefaultAioHttpClient": ("._base_client", "DefaultAioHttpClient"),
    "resources": ("._utils._resources_proxy", "resources"),
    "AnthropicAWS": (".lib.aws", "AnthropicAWS"),
    "AsyncAnthropicAWS": (".lib.aws", "AsyncAnthropicAWS"),
    "beta_tool": (".lib.tools", "beta_tool"),
    "beta_async_tool": (".lib.tools", "beta_async_tool"),
    "AnthropicVertex": (".lib.vertex", "AnthropicVertex"),
    "AsyncAnthropicVertex": (".lib.vertex", "AsyncAnthropicVertex"),
    "AnthropicBedrock": (".lib.bedrock", "AnthropicBedrock"),
    "AsyncAnthropicBedrock": (".lib.bedrock", "AsyncAnthropicBedrock"),
    "AnthropicBedrockMantle": (".lib.bedrock", "AnthropicBedrockMantle"),
    "AsyncAnthropicBedrockMantle": (".lib.bedrock", "AsyncAnthropicBedrockMantle"),
    "AnthropicFoundry": (".lib.foundry", "AnthropicFoundry"),
    "AsyncAnthropicFoundry": (".lib.foundry", "AsyncAnthropicFoundry"),
    "TextEvent": (".lib.streaming", "TextEvent"),
    "InputJsonEvent": (".lib.streaming", "InputJsonEvent"),
    "MessageStream": (".lib.streaming", "MessageStream"),
    "BetaTextEvent": (".lib.streaming", "BetaTextEvent"),
    "AsyncMessageStream": (".lib.streaming", "AsyncMessageStream"),
    "MessageStopEvent": (".lib.streaming", "MessageStopEvent"),
    "MessageStreamEvent": (".lib.streaming", "MessageStreamEvent"),
    "BetaInputJsonEvent": (".lib.streaming", "BetaInputJsonEvent"),
    "MessageStreamManager": (".lib.streaming", "MessageStreamManager"),
    "ContentBlockStopEvent": (".lib.streaming", "ContentBlockStopEvent"),
    "ParsedBetaTextEvent": (".lib.streaming", "ParsedBetaTextEvent"),
    "BetaMessageStream": (".lib.streaming", "BetaMessageStream"),
    "BetaAsyncMessageStream": (".lib.streaming", "BetaAsyncMessageStream"),
    "AsyncMessageStreamManager": (".lib.streaming", "AsyncMessageStreamManager"),
    "BetaMessageStreamEvent": (".lib.streaming", "BetaMessageStreamEvent"),
    "ParsedMessageStopEvent": (".lib.streaming", "ParsedMessageStopEvent"),
    "BetaMessageStreamManager": (".lib.streaming", "BetaMessageStreamManager"),
    "ParsedMessageStreamEvent": (".lib.streaming", "ParsedMessageStreamEvent"),
    "BetaContentBlockStopEvent": (".lib.streaming", "BetaContentBlockStopEvent"),
    "ParsedBetaMessageStopEvent": (".lib.streaming", "ParsedBetaMessageStopEvent"),
    "ParsedContentBlockStopEvent": (".lib.streaming", "ParsedContentBlockStopEvent"),
    "BetaAsyncMessageStreamManager": (".lib.streaming", "BetaAsyncMessageStreamManager"),
    "ParsedBetaMessageStreamEvent": (".lib.streaming", "ParsedBetaMessageStreamEvent"),
    "ParsedBetaContentBlockStopEvent": (".lib.streaming", "ParsedBetaContentBlockStopEvent"),
    "EnvToken": (".lib.credentials", "EnvToken"),
    "TokenCache": (".lib.credentials", "TokenCache"),
    "AccessToken": (".lib.credentials", "AccessToken"),
    "StaticToken": (".lib.credentials", "StaticToken"),
    "AccessTokenAuth": (".lib.credentials", "AccessTokenAuth"),
    "InMemoryConfig": (".lib.credentials", "InMemoryConfig"),
    "CredentialsFile": (".lib.credentials", "CredentialsFile"),
    "CredentialResult": (".lib.credentials", "CredentialResult"),
    "IdentityTokenFile": (".lib.credentials", "IdentityTokenFile"),
    "AccessTokenProvider": (".lib.credentials", "AccessTokenProvider"),
    "default_credentials": (".lib.credentials", "default_credentials"),
    "IdentityTokenProvider": (".lib.credentials", "IdentityTokenProvider"),
    "WorkloadIdentityError": (".lib.credentials", "WorkloadIdentityError"),
    "WorkloadIdentityCredentials": (".lib.credentials", "WorkloadIdentityCredentials"),
    "exchange_federation_assertion": (".lib.credentials", "exchange_federation_assertion"),
    "transform_schema": (".lib._parse._transform", "transform_schema"),
}


def __getattr__(name: str) -> _t.Any:
    if name not in _LAZY_ATTRS:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

    import importlib

    module_name, attr_name = _LAZY_ATTRS[name]
    module = importlib.import_module(module_name, __name__)
    attr = module if attr_name is None else getattr(module, attr_name)
    globals()[name] = attr

    try:
        attr.__module__ = "anthropic"
    except (TypeError, AttributeError):
        pass

    return attr


def _setup_logging() -> None:
    logger = _logging.getLogger("anthropic")
    httpx_logger = _logging.getLogger("httpx")

    env = _os.environ.get("ANTHROPIC_LOG")
    if env == "debug":
        _logging.basicConfig(
            format="[%(asctime)s - %(name)s:%(lineno)d - %(levelname)s] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        logger.setLevel(_logging.DEBUG)
        httpx_logger.setLevel(_logging.DEBUG)
    elif env == "info":
        _logging.basicConfig(
            format="[%(asctime)s - %(name)s:%(lineno)d - %(levelname)s] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        logger.setLevel(_logging.INFO)
        httpx_logger.setLevel(_logging.INFO)


_setup_logging()

# Update the __module__ attribute for exported symbols so that
# error messages point to this module instead of the module
# it was originally defined in, e.g.
# anthropic._exceptions.NotFoundError -> anthropic.NotFoundError
__locals = locals()
for __name in __all__:
    if not __name.startswith("__"):
        try:
            __locals[__name].__module__ = "anthropic"
        except KeyError:
            pass
        except (TypeError, AttributeError):
            # Some of our exported symbols are builtins which we can't set attributes for.
            pass
