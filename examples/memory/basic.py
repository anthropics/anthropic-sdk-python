import time
import threading
from typing import Optional

from pydantic import TypeAdapter

from anthropic import Anthropic
from anthropic.tools import BetaLocalFilesystemMemoryTool
from anthropic.types.beta import (
    BetaMessageParam,
    BetaContentBlockParam,
    BetaMemoryTool20250818Command,
    BetaMemoryTool20250818ViewCommand,
)
from anthropic.types.beta.beta_context_management_config_param import BetaContextManagementConfigParam

# Context management automatically clears old tool results to stay within token limits
# Triggers when input exceeds 30k tokens, keeps 3 tool uses after clearing
DEFAULT_CONTEXT_MANAGEMENT: BetaContextManagementConfigParam = {
    "edits": [
        {
            "type": "clear_tool_uses_20250919",
            # The below parameters are OPTIONAL:
            # Trigger clearing when threshold is exceeded
            "trigger": {"type": "input_tokens", "value": 30000},
            # Number of tool uses to keep after clearing
            "keep": {"type": "tool_uses", "value": 3},
            # Optional: Clear at least this many tokens
            "clear_at_least": {"type": "input_tokens", "value": 5000},
            # Exclude these tools uses from being cleared
            "exclude_tools": ["web_search"],
        }
    ]
}

DEFAULT_MEMORY_SYSTEM_PROMPT = """- ***DO NOT just store the conversation history**
        - No need to mention your memory tool or what you are writing in it to the user, unless they ask
        - Store facts about the user and their preferences
        - Before responding, check memory to adjust technical depth and response style appropriately
        - Keep memories up-to-date - remove outdated info, add new details as you learn them
        - Use an xml format like <xml><name>John Doe</name></user></xml>"""


class Spinner:
    def __init__(self, message: str = "Thinking"):
        self.message = message
        self.spinning = False
        self.thread = None

    def start(self):
        self.spinning = True
        self.thread = threading.Thread(target=self._spin)
        self.thread.start()

    def stop(self):
        self.spinning = False
        if self.thread:
            self.thread.join()
        print("\r" + " " * (len(self.message) + 10) + "\r", end="", flush=True)

    def _spin(self):
        chars = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"
        i = 0
        while self.spinning:
            print(f"\r{self.message} {chars[i % len(chars)]}", end="", flush=True)
            i += 1
            time.sleep(0.1)


def conversation_loop():
    client = Anthropic()
    memory = BetaLocalFilesystemMemoryTool()

    messages: list[BetaMessageParam] = []

    # Initialize tracking for debug
    last_response_id: Optional[str] = None
    last_usage = None

    print("🧠 Claude with Memory & Web Search - Interactive Session")
    print("Commands:")
    print("  /quit or /exit - Exit the session")
    print("  /clear - Start fresh conversation")
    print("  /memory_view - See all memory files")
    print("  /memory_clear - Delete all memory")
    print("  /debug - View conversation history and token usage")

    # Display context management settings
    print(f"\n🧹 Context Management")
    print("=" * 60)

    while True:
        try:
            user_input = input("\nYou: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if user_input.lower() in ["/quit", "/exit"]:
            print("Goodbye!")
            break
        elif user_input.lower() == "/clear":
            messages = []
            print("Conversation cleared!")
            continue
        elif user_input.lower() == "/memory_view":
            result = memory.execute(BetaMemoryTool20250818ViewCommand(command="view", path="/memories"))
            print("\n📁 Memory contents:")
            print(result)
            continue
        elif user_input.lower() == "/memory_clear":
            result = memory.clear_all_memory()
            print(f"🗑️ {result}")
            continue
        elif user_input.lower() == "/debug":
            print("\n🔍 Conversation history:")

            # Show last response ID if available
            if last_response_id:
                print(f"📌 Last response ID: {last_response_id}")

            # Show token usage if available
            if last_usage:
                usage = last_usage
                input_tokens = usage.get("input_tokens", 0)
                cached_tokens = usage.get("cache_read_input_tokens", 0)
                uncached_tokens = input_tokens - cached_tokens

                print(f"📊 Last API call tokens:")
                print(f"   Total input: {input_tokens:,} tokens")
                print(f"   Cached: {cached_tokens:,} tokens")
                print(f"   Uncached: {uncached_tokens:,} tokens")

                threshold = DEFAULT_CONTEXT_MANAGEMENT["edits"][0]["trigger"]["value"]  # type: ignore
                print(f"   Context clearing threshold: {threshold:,} tokens")
                if input_tokens >= threshold:
                    print(f"   🧹 Context clearing should trigger soon!")
                elif input_tokens >= threshold * 0.8:  # 80% of threshold #type: ignore
                    print(f"   ⚠️  Approaching context clearing threshold!")

            print("=" * 80)

            for i, message in enumerate(messages):
                role = message["role"].upper()
                print(f"\n[{i + 1}] {role}:")
                print("-" * 40)

                content = message["content"]
                if isinstance(content, str):
                    print(content[:500] + "..." if len(content) > 500 else content)
                elif isinstance(content, list):
                    for block in content:
                        if isinstance(block, dict):
                            if block.get("type") in ["tool_use", "server_tool_use"]:
                                print(f"Tool: {block.get('name', 'unknown')}")
                            elif block.get("type") == "tool_result":
                                print(f"Tool Result: [content]")
                            elif block.get("type") == "text":
                                text = block.get("text", "")
                                print(f"Text: {text[:200]}..." if len(text) > 200 else f"Text: {text}")
            print("=" * 80)
            continue
        elif not user_input:
            continue

        messages.append({"role": "user", "content": user_input})

        print("\nClaude: ", end="", flush=True)

        spinner = Spinner("Thinking")
        spinner.start()

        # Use tool_runner with memory tool
        try:
            runner = client.beta.messages.tool_runner(
                betas=["context-management-2025-06-27"],
                model="claude-sonnet-4-20250514",
                max_tokens=2048,
                system=DEFAULT_MEMORY_SYSTEM_PROMPT,
                messages=messages,
                tools=[memory],
                context_management=DEFAULT_CONTEXT_MANAGEMENT,
            )
        except Exception:
            spinner.stop()
            raise

        # Process all messages from the runner
        for message in runner:
            spinner.stop()

            # Store response ID and usage for debug display
            last_response_id = message.id

            if hasattr(message, "usage") and message.usage:
                last_usage = message.usage.model_dump() if hasattr(message.usage, "model_dump") else dict(message.usage)

            # Check for context management actions
            if message.context_management:
                for edit in message.context_management.applied_edits:
                    print(f"\n🧹 [Context Management: {edit.type} applied]")

            # Process content blocks
            assistant_content: list[BetaContentBlockParam] = []
            for content in message.content:
                if content.type == "text":
                    print(content.text, end="", flush=True)
                    assistant_content.append({"type": "text", "text": content.text})

                elif content.type == "tool_use" and content.name == "memory":
                    tool_input = TypeAdapter[BetaMemoryTool20250818Command](
                        BetaMemoryTool20250818Command
                    ).validate_python(content.input)

                    print(f"\n[Memory tool called: {tool_input.command}]")
                    assistant_content.append(
                        {
                            "type": "tool_use",
                            "id": content.id,
                            "name": content.name,
                            "input": content.input,
                        }
                    )

            # Store assistant message
            if assistant_content:
                messages.append({"role": "assistant", "content": assistant_content})

            # Generate tool response automatically
            tool_response = runner.generate_tool_call_response()
            if tool_response and tool_response["content"]:
                # Add tool results to messages
                messages.append({"role": "user", "content": tool_response["content"]})

                for result in tool_response["content"]:
                    if isinstance(result, dict) and result.get("type") == "tool_result":
                        print(f"[Tool result processed]")

        print()


if __name__ == "__main__":
    conversation_loop()
