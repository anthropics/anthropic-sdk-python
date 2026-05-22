#!/usr/bin/env -S uv run python

import os
import json
import time

from anthropic import Anthropic
from anthropic.lib.tools import beta_tool

MCP_SERVER_NAME = "github"
MCP_SERVER_URL = "https://api.githubcopilot.com/mcp/"

PROMPT = (
    "Hi! List every tool and skill you have access to, grouped by where they "
    "came from (built-in toolset, custom tool, MCP server, skills)."
)


# A custom tool — executed by this client rather than the agent. `custom=True`
# makes `to_dict()` emit the managed-agents custom-tool param for
# `agents.create(...)`, while the decorated function stays runnable so we can
# answer the `agent.custom_tool_use` event below by calling it directly.
@beta_tool(custom=True)
def get_weather(city: str) -> str:  # noqa: ARG001
    """Look up the current weather for a city."""
    return json.dumps({"temperature_c": 14})


def main() -> None:
    anthropic = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

    github_token = os.environ.get("GITHUB_TOKEN")
    if not github_token:
        raise RuntimeError(
            "GITHUB_TOKEN is required (use a fine-grained PAT with public-repo read only)"
        )

    # Create an environment
    environment = anthropic.beta.environments.create(
        name="comprehensive-example-environment",
    )
    print("Created environment:", environment.id)

    # Create a vault and store the MCP server credential in it
    vault = anthropic.beta.vaults.create(display_name="comprehensive-example-vault")
    print("Created vault:", vault.id)

    credential = anthropic.beta.vaults.credentials.create(
        vault.id,
        display_name="github-mcp",
        auth={
            "type": "static_bearer",
            "mcp_server_url": MCP_SERVER_URL,
            "token": github_token,
        },
    )
    print("Created credential:", credential.id)

    # Upload a custom skill
    skill_md_path = os.path.join(os.path.dirname(__file__), "greeting-SKILL.md")
    with open(skill_md_path, "rb") as skill_file:
        skill = anthropic.beta.skills.create(
            display_title=f"comprehensive-greeting-{int(time.time() * 1000)}",
            files=[("greeting/SKILL.md", skill_file, "text/markdown")],
        )
    print("Created skill:", skill.id)

    # Create v1 of the agent with the built-in toolset, an MCP server, and a custom tool
    agent_v1 = anthropic.beta.agents.create(
        name="comprehensive-example-agent",
        model="claude-sonnet-4-6",
        system="You are a helpful assistant.",
        mcp_servers=[{"type": "url", "name": MCP_SERVER_NAME, "url": MCP_SERVER_URL}],
        tools=[
            {"type": "agent_toolset_20260401"},
            {"type": "mcp_toolset", "mcp_server_name": MCP_SERVER_NAME},
            get_weather.to_dict(),
        ],
    )
    print("Created agent v1:", agent_v1.id)

    # Patch the agent to v2 by adding skills; each update bumps the version
    agent = anthropic.beta.agents.update(
        agent_v1.id,
        version=agent_v1.version,
        skills=[
            {"type": "custom", "skill_id": skill.id},
            {"type": "anthropic", "skill_id": "xlsx"},
        ],
    )
    print("Patched agent to v2:", agent.id)

    versions = anthropic.beta.agents.versions.list(agent.id)
    print("Agent versions:", versions.data)

    # Create a session pinned to v2; the vault supplies the MCP credential
    session = anthropic.beta.sessions.create(
        environment_id=environment.id,
        agent={"type": "agent", "id": agent.id, "version": agent.version},
        vault_ids=[vault.id],
    )
    print("Created session:", session.id)

    # Send a prompt and stream events, answering the custom tool if called
    print("Streaming events:")
    anthropic.beta.sessions.events.send(
        session.id,
        events=[
            {"type": "user.message", "content": [{"type": "text", "text": PROMPT}]}
        ],
    )

    with anthropic.beta.sessions.events.stream(session.id) as stream:
        for event in stream:
            print(event.to_json(indent=2))
            # `get_weather` is a custom (non-builtin) tool, so the agent emits an
            # `agent.custom_tool_use` event and expects a `user.custom_tool_result`.
            if event.type == "agent.custom_tool_use" and event.name == get_weather.name:
                # Answer the custom tool by running our local implementation.
                result = get_weather.call(event.input)
                assert isinstance(result, str)
                anthropic.beta.sessions.events.send(
                    session.id,
                    events=[
                        {
                            "type": "user.custom_tool_result",
                            "custom_tool_use_id": event.id,
                            "content": [{"type": "text", "text": result}],
                        }
                    ],
                )
            if (
                event.type == "session.status_idle"
                and event.stop_reason
                and event.stop_reason.type == "end_turn"
            ):
                break


if __name__ == "__main__":
    main()
