import time
import shutil
import threading
from typing import List, Optional, cast
from pathlib import Path
from typing_extensions import override

from pydantic import TypeAdapter

from anthropic import Anthropic
from anthropic.lib.tools import BetaAbstractMemoryTool
from anthropic.types.beta import (
    BetaMessageParam,
    BetaContentBlockParam,
    BetaMemoryTool20250818Command,
    BetaContextManagementConfigParam,
    BetaMemoryTool20250818ViewCommand,
    BetaMemoryTool20250818CreateCommand,
    BetaMemoryTool20250818DeleteCommand,
    BetaMemoryTool20250818InsertCommand,
    BetaMemoryTool20250818RenameCommand,
    BetaMemoryTool20250818StrReplaceCommand,
)

MEMORY_SYSTEM_PROMPT = """- ***DO NOT just store the conversation history**
        - No need to mention your memory tool or what you are writting in it to the user, unless they ask
        - Store facts about the user and their preferences
        - Before responding, check memory to adjust technical depth and response style appropriately
        - Keep memories up-to-date - remove outdated info, add new details as you learn them
        - Use an xml format like <xml><name>John Doe</name></user></xml>"""


# Context management automatically clears old tool results to stay within token limits
# Triggers when input exceeds 20k tokens, clears down to 10k tokens
CONTEXT_MANAGEMENT = {
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


class LocalFilesystemMemoryTool(BetaAbstractMemoryTool):
    """File-based memory storage implementation for Claude conversations"""

    def __init__(self, base_path: str = "./memory"):
        super().__init__()
        self.base_path = Path(base_path)
        self.memory_root = self.base_path / "memories"
        self.memory_root.mkdir(parents=True, exist_ok=True)

    def _validate_path(self, path: str) -> Path:
        """Validate and resolve memory paths"""
        if not path.startswith("/memories"):
            raise ValueError(f"Path must start with /memories, got: {path}")

        relative_path = path[len("/memories") :].lstrip("/")
        full_path = self.memory_root / relative_path if relative_path else self.memory_root

        try:
            full_path.resolve().relative_to(self.memory_root.resolve())
        except ValueError as e:
            raise ValueError(f"Path {path} would escape /memories directory") from e

        return full_path

    @override
    def view(self, command: BetaMemoryTool20250818ViewCommand) -> str:
        full_path = self._validate_path(command.path)

        if full_path.is_dir():
            items: List[str] = []
            try:
                for item in sorted(full_path.iterdir()):
                    if item.name.startswith("."):
                        continue
                    items.append(f"{item.name}/" if item.is_dir() else item.name)
                return f"Directory: {command.path}" + "\n".join([f"- {item}" for item in items])
            except Exception as e:
                raise RuntimeError(f"Cannot read directory {command.path}: {e}") from e

        elif full_path.is_file():
            try:
                content = full_path.read_text(encoding="utf-8")
                lines = content.splitlines()
                view_range = command.view_range
                if view_range:
                    start_line = max(1, view_range[0]) - 1
                    end_line = len(lines) if view_range[1] == -1 else view_range[1]
                    lines = lines[start_line:end_line]
                    start_num = start_line + 1
                else:
                    start_num = 1

                numbered_lines = [f"{i + start_num:4d}: {line}" for i, line in enumerate(lines)]
                return "\n".join(numbered_lines)
            except Exception as e:
                raise RuntimeError(f"Cannot read file {command.path}: {e}") from e
        else:
            raise RuntimeError(f"Path not found: {command.path}")

    @override
    def create(self, command: BetaMemoryTool20250818CreateCommand) -> str:
        full_path = self._validate_path(command.path)
        full_path.parent.mkdir(parents=True, exist_ok=True)
        full_path.write_text(command.file_text, encoding="utf-8")
        return f"File created successfully at {command.path}"

    @override
    def str_replace(self, command: BetaMemoryTool20250818StrReplaceCommand) -> str:
        full_path = self._validate_path(command.path)

        if not full_path.is_file():
            raise FileNotFoundError(f"File not found: {command.path}")

        content = full_path.read_text(encoding="utf-8")
        count = content.count(command.old_str)
        if count == 0:
            raise ValueError(f"Text not found in {command.path}")
        elif count > 1:
            raise ValueError(f"Text appears {count} times in {command.path}. Must be unique.")

        new_content = content.replace(command.old_str, command.new_str)
        full_path.write_text(new_content, encoding="utf-8")
        return f"File {command.path} has been edited"

    @override
    def insert(self, command: BetaMemoryTool20250818InsertCommand) -> str:
        full_path = self._validate_path(command.path)
        insert_line = command.insert_line
        insert_text = command.insert_text

        if not full_path.is_file():
            raise FileNotFoundError(f"File not found: {command.path}")

        lines = full_path.read_text(encoding="utf-8").splitlines()
        if insert_line < 0 or insert_line > len(lines):
            raise ValueError(f"Invalid insert_line {insert_line}. Must be 0-{len(lines)}")

        lines.insert(insert_line, insert_text.rstrip("\n"))
        full_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        return f"Text inserted at line {insert_line} in {command.path}"

    @override
    def delete(self, command: BetaMemoryTool20250818DeleteCommand) -> str:
        full_path = self._validate_path(command.path)

        if command.path == "/memories":
            raise ValueError("Cannot delete the /memories directory itself")

        if full_path.is_file():
            full_path.unlink()
            return f"File deleted: {command.path}"
        elif full_path.is_dir():
            shutil.rmtree(full_path)
            return f"Directory deleted: {command.path}"
        else:
            raise FileNotFoundError(f"Path not found: {command.path}")

    @override
    def rename(self, command: BetaMemoryTool20250818RenameCommand) -> str:
        old_full_path = self._validate_path(command.old_path)
        new_full_path = self._validate_path(command.new_path)

        if not old_full_path.exists():
            raise FileNotFoundError(f"Source path not found: {command.old_path}")
        if new_full_path.exists():
            raise ValueError(f"Destination already exists: {command.new_path}")

        new_full_path.parent.mkdir(parents=True, exist_ok=True)
        old_full_path.rename(new_full_path)
        return f"Renamed {command.old_path} to {command.new_path}"

    @override
    def clear_all_memory(self) -> str:
        """Override the base implementation to provide file system clearing."""
        if self.memory_root.exists():
            shutil.rmtree(self.memory_root)
        self.memory_root.mkdir(parents=True, exist_ok=True)
        return "All memory cleared"


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
    memory = LocalFilesystemMemoryTool()

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

                threshold = CONTEXT_MANAGEMENT["edits"][0]["trigger"]["value"]  # type: ignore
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
                system=MEMORY_SYSTEM_PROMPT,
                messages=messages,
                tools=[memory],
                context_management=cast(BetaContextManagementConfigParam, CONTEXT_MANAGEMENT),
            )
        except Exception:
            spinner.stop()
            raise

        # Process all messages from the runner
        assistant_content: list[BetaContentBlockParam] = []
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

            # Generate tool response automatically
            tool_response = runner.generate_tool_call_response()
            if tool_response and tool_response["content"]:
                # Add tool results to messages
                messages.append({"role": "user", "content": tool_response["content"]})

                for result in tool_response["content"]:
                    if isinstance(result, dict) and result.get("type") == "tool_result":
                        print(f"[Tool result processed]")

        # Store assistant message
        if assistant_content:
            messages.append({"role": "assistant", "content": assistant_content})

        print()


if __name__ == "__main__":
    conversation_loop()
