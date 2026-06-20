#!/usr/bin/env -S uv run python

import os
from pathlib import Path

from anthropic import Anthropic


def main() -> None:
    anthropic = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

    # Create an environment
    environment = anthropic.beta.environments.create(
        name="files-example-environment",
    )
    print("Created environment:", environment.id)

    # Create an agent with the built-in toolset and an always-allow permission policy
    agent = anthropic.beta.agents.create(
        name="files-example-agent",
        model="claude-sonnet-4-6",
        tools=[
            {
                "type": "agent_toolset_20260401",
                "default_config": {
                    "enabled": True,
                    "permission_policy": {"type": "always_allow"},
                },
            }
        ],
    )
    print("Created agent:", agent.id)

    # Upload a file
    file = anthropic.beta.files.upload(
        file=Path(__file__).parent / "data.csv",
    )
    print("Uploaded file:", file.id)

    # Create a session with the file mounted as a resource
    session = anthropic.beta.sessions.create(
        environment_id=environment.id,
        agent={"type": "agent", "id": agent.id, "version": agent.version},
        resources=[
            {
                "type": "file",
                "file_id": file.id,
                "mount_path": "data.csv",
            }
        ],
    )
    print("Created session:", session.id)

    resources = anthropic.beta.sessions.resources.list(session.id)
    print("Listed session resources:", resources.data)

    # Send a prompt asking the agent to read the mounted file and stream events
    print("Streaming events:")
    anthropic.beta.sessions.events.send(
        session.id,
        events=[
            {
                "type": "user.message",
                "content": [
                    {
                        "type": "text",
                        "text": "Read /uploads/data.csv and tell me the column names.",
                    }
                ],
            }
        ],
    )

    with anthropic.beta.sessions.events.stream(session.id) as stream:
        for event in stream:
            print(event.to_json(indent=2))
            if event.type == "session.status_idle":
                break


if __name__ == "__main__":
    main()
