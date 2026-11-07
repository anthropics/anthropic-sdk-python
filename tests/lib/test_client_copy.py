from __future__ import annotations

import json
import pathlib
from typing import Any, cast
from collections.abc import Callable
from typing_extensions import override

import httpx2
import pytest

import anthropic
from anthropic import CallNext, APIRequest, Middleware, APIResponse, AsyncCallNext, AsyncAPIResponse
from anthropic._utils import signature_without_evaluating_annotations
from anthropic._base_client import BaseClient, AsyncAPIClient

ClientClass = type[BaseClient[Any, Any]]

EXPORTS: list[object] = [getattr(anthropic, name) for name in dir(anthropic)]

CLIENT_CLASSES: list[ClientClass] = sorted(
    {cast(ClientClass, export) for export in EXPORTS if isinstance(export, type) and issubclass(export, BaseClient)},
    key=lambda client_class: client_class.__name__,
)

BASE_URL = "https://example.com/custom/"

PROFILE_CONFIG = {
    "authentication": {
        "type": "oidc_federation",
        "federation_rule_id": "fdrl_fake",
        "identity_token": {"source": "file", "path": "/fake/identity-token"},
    },
    "organization_id": "org_fake",
    "workspace_id": "wrkspc_fake",
}


def provide_token() -> str:
    return "fake-token"


class FakeGoogleCredentials:
    pass


GOOGLE_CREDENTIALS = FakeGoogleCredentials()

# The arguments that each sync client and its async twin have of their own. Arguments that cannot be combined are in
# separate sets. A client with the first set can send a request.
PLATFORM_ARGUMENTS: dict[str, list[dict[str, object]]] = {
    "Anthropic": [
        {"api_key": "fake-api-key", "webhook_key": "fake-webhook-key", "base_url": BASE_URL},
        {"auth_token": "fake-auth-token"},
        {"credentials": provide_token},
        {"config": PROFILE_CONFIG},
        {"profile": "fake-profile"},
    ],
    "AnthropicAWS": [
        {
            "api_key": "fake-api-key",
            "aws_region": "us-east-1",
            "workspace_id": "wrkspc_fake",
            "webhook_key": "fake-webhook-key",
            "base_url": BASE_URL,
        },
        {
            "aws_access_key": "fake-access-key",
            "aws_secret_key": "fake-secret-key",
            "aws_session_token": "fake-session-token",
            "aws_profile": "fake-profile",
            "aws_region": "us-east-1",
            "workspace_id": "wrkspc_fake",
            "auth_token": "fake-auth-token",
        },
        {"skip_auth": True, "aws_region": "us-east-1", "workspace_id": "wrkspc_fake"},
    ],
    "AnthropicBedrock": [
        {"api_key": "fake-api-key", "aws_region": "us-east-1"},
        {
            "aws_access_key": "fake-access-key",
            "aws_secret_key": "fake-secret-key",
            "aws_session_token": "fake-session-token",
            "aws_profile": "fake-profile",
            "aws_region": "us-east-1",
            "base_url": BASE_URL,
        },
    ],
    "AnthropicBedrockMantle": [
        {"api_key": "fake-api-key", "aws_region": "us-east-1"},
        {
            "aws_access_key": "fake-access-key",
            "aws_secret_key": "fake-secret-key",
            "aws_session_token": "fake-session-token",
            "aws_profile": "fake-profile",
            "aws_region": "us-east-1",
            "base_url": BASE_URL,
        },
        {"skip_auth": True, "aws_region": "us-east-1"},
    ],
    "AnthropicFoundry": [
        {"api_key": "fake-api-key", "webhook_key": "fake-webhook-key", "base_url": BASE_URL},
        {"azure_ad_token_provider": provide_token, "resource": "fake-resource"},
    ],
    "AnthropicGoogleCloud": [
        {
            "project": "fake-project",
            "location": "us-east5",
            "workspace_id": "wrkspc_fake",
            "token_provider": provide_token,
            "credentials": GOOGLE_CREDENTIALS,
            "base_url": BASE_URL,
        },
        {"skip_auth": True, "project": "fake-project", "workspace_id": "wrkspc_fake"},
    ],
    "AnthropicVertex": [
        {
            "region": "us-east5",
            "project_id": "fake-project",
            "access_token": "fake-access-token",
            "credentials": GOOGLE_CREDENTIALS,
            "base_url": BASE_URL,
        },
    ],
}

# Each client builds these for itself, out of arguments that the rest of its state holds.
BUILT_PER_CLIENT = {"_otel", "_middleware_chain", "_custom_auth", "messages", "beta"}


class PassThroughMiddleware(Middleware):
    @override
    def handle(self, request: APIRequest, call_next: CallNext) -> APIResponse[Any]:
        return call_next(request)

    @override
    async def handle_async(self, request: APIRequest, call_next: AsyncCallNext) -> AsyncAPIResponse[Any]:
        return await call_next(request)


def platform_arguments(client_class: ClientClass) -> list[dict[str, object]]:
    return PLATFORM_ARGUMENTS.get(client_class.__name__.removeprefix("Async"), [])


def http_client(
    client_class: ClientClass, transport: httpx2.MockTransport | None = None
) -> httpx2.Client | httpx2.AsyncClient:
    if issubclass(client_class, AsyncAPIClient):
        return httpx2.AsyncClient(transport=transport)
    return httpx2.Client(transport=transport)


def common_arguments(client_class: ClientClass) -> dict[str, object]:
    return {
        "timeout": 12.5,
        "max_retries": 7,
        "default_headers": {"x-kept": "yes"},
        "default_query": {"kept": "yes"},
        "open_telemetry": {"conversation_id": "conv_fake", "propagation": False},
        "http_client": http_client(client_class),
        "middleware": [PassThroughMiddleware()],
    }


def construct(client_class: ClientClass, *arguments: dict[str, object]) -> Any:
    return cast("Callable[..., Any]", client_class)(
        **{name: value for group in arguments for name, value in group.items()}
    )


def stored_state(client: object) -> dict[str, Any]:
    state = {name: value for name, value in vars(client).items() if name not in BUILT_PER_CLIENT}
    if "_creds_state" in state:
        state["_creds_state"] = state["_creds_state"].credentials
    return state


@pytest.fixture(autouse=True)
def config_dir(tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch) -> None:
    config_path = tmp_path / "configs" / "fake-profile.json"
    config_path.parent.mkdir()
    config_path.write_text(json.dumps(PROFILE_CONFIG))
    config_path.chmod(0o644)
    monkeypatch.setenv("ANTHROPIC_CONFIG_DIR", str(tmp_path))


each_client_class = pytest.mark.parametrize("client_class", CLIENT_CLASSES, ids=lambda value: value.__name__)

each_set_of_platform_arguments = pytest.mark.parametrize(
    ("client_class", "arguments"),
    [
        pytest.param(client_class, arguments, id=f"{client_class.__name__}-{next(iter(arguments))}")
        for client_class in CLIENT_CLASSES
        for arguments in platform_arguments(client_class)
    ],
)


@each_client_class
def test_every_constructor_argument_is_covered(client_class: ClientClass) -> None:
    parameters = signature_without_evaluating_annotations(client_class.__init__).parameters
    public = {name for name in parameters if name != "self" and not name.startswith("_")}

    covered = set(common_arguments(client_class)).union(*platform_arguments(client_class))

    assert covered == public, (
        f"Give each public argument of `{client_class.__name__}` a value in `PLATFORM_ARGUMENTS` or "
        "`common_arguments`, so that the tests below check that a copy keeps it."
    )


@pytest.mark.parametrize("all_arguments", [True, False], ids=["all-arguments", "platform-arguments-only"])
@each_set_of_platform_arguments
def test_copy_keeps_every_constructor_argument(
    client_class: ClientClass, arguments: dict[str, object], all_arguments: bool
) -> None:
    client = construct(client_class, arguments, common_arguments(client_class) if all_arguments else {})

    copied = client.copy()

    assert stored_state(copied) == stored_state(client)
    assert copied._client is client._client


@each_client_class
async def test_copy_sends_requests_through_the_http_client(client_class: ClientClass) -> None:
    requests: list[httpx2.Request] = []

    def respond(request: httpx2.Request) -> httpx2.Response:
        requests.append(request)
        return httpx2.Response(200, json={"id": "msg_fake"})

    client = construct(
        client_class,
        platform_arguments(client_class)[0],
        {"http_client": http_client(client_class, httpx2.MockTransport(respond))},
    )

    message = client.with_options(max_retries=0).messages.create(
        max_tokens=16, messages=[{"role": "user", "content": "Hi"}], model="claude-fake"
    )
    if issubclass(client_class, AsyncAPIClient):
        await message

    assert len(requests) == 1


@each_client_class
def test_with_options_overrides_win(client_class: ClientClass) -> None:
    client = construct(client_class, platform_arguments(client_class)[0], common_arguments(client_class))
    other_http_client = http_client(client_class)
    other_middleware = PassThroughMiddleware()

    copied = client.with_options(
        timeout=1.5,
        max_retries=1,
        default_headers={"x-added": "yes"},
        default_query={"added": "yes"},
        open_telemetry={"conversation_id": "conv_other"},
        http_client=other_http_client,
        middleware=[other_middleware],
    )

    assert copied.timeout == 1.5
    assert copied.max_retries == 1
    assert {"x-kept": "yes", "x-added": "yes"}.items() <= copied.default_headers.items()
    assert copied.default_query == {"kept": "yes", "added": "yes"}
    assert copied.open_telemetry["conversation_id"] == "conv_other"
    assert copied._client is other_http_client
    assert copied.middleware == (other_middleware,)


@each_client_class
def test_with_options_replaces_default_headers_and_query(client_class: ClientClass) -> None:
    client = construct(client_class, platform_arguments(client_class)[0], common_arguments(client_class))

    copied = client.with_options(set_default_headers={"x-only": "yes"}, set_default_query={"only": "yes"})

    assert copied.default_headers["x-only"] == "yes"
    assert "x-kept" not in copied.default_headers
    assert copied.default_query == {"only": "yes"}
    with pytest.raises(
        ValueError, match="`default_headers` and `set_default_headers` arguments are mutually exclusive"
    ):
        client.with_options(default_headers={}, set_default_headers={})
    with pytest.raises(ValueError, match="`default_query` and `set_default_query` arguments are mutually exclusive"):
        client.with_options(default_query={}, set_default_query={})
