"""Show the full summary content after compaction"""

import json

from anthropic import Anthropic
from anthropic.lib.tools import beta_tool


@beta_tool
def search(query: str) -> str:
    """Search for information."""
    return json.dumps(
        {
            "results": [
                {"title": f"Result for {query}", "content": "Lorem ipsum " * 100},
                {"title": f"More on {query}", "content": "Detailed info " * 100},
            ]
        }
    )


@beta_tool
def done(summary: str) -> str:  # noqa: ARG001
    """Call when finished."""
    return "Complete"


client = Anthropic()

runner = client.beta.messages.tool_runner(
    model="claude-sonnet-4-20250514",
    max_tokens=4096,
    tools=[search, done],
    messages=[
        {
            "role": "user",
            "content": "You MUST search for EACH of these animals ONE BY ONE: dogs, cats, birds, fish, horses, elephants, lions, tigers, bears, wolves. After searching for ALL of them, call done.",
        }
    ],
    compaction_control={
        "enabled": True,
        "context_token_threshold": 3000,  # Even lower threshold
    },
)

prev_msg_count = 0
for i, message in enumerate(runner):
    curr_msg_count = len(list(runner._params["messages"]))
    print(f"Turn {i + 1}: {message.usage.input_tokens} input tokens, {curr_msg_count} messages")

    if curr_msg_count < prev_msg_count:
        print("=" * 70)
        print("🔄 COMPACTION OCCURRED!")
        print("=" * 70)
        print(f"Messages went from {prev_msg_count} → {curr_msg_count}")
        print(f"Input tokens: {message.usage.input_tokens}")
        print("\nNEW MESSAGES LIST:")
        print("-" * 70)

        for msg in runner._params["messages"]:
            role = msg.get("role", "?")
            content = msg.get("content", "")

            if isinstance(content, list):
                for block in content:
                    if isinstance(block, dict) and block.get("type") == "text":
                        print(f"\n[{role}] TEXT BLOCK:")
                        print(block.get("text", ""))
            elif isinstance(content, str):
                print(f"\n[{role}]:")
                print(content)

        print("-" * 70)

    prev_msg_count = curr_msg_count

print("\n✅ Done!")
