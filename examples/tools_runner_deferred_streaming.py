from anthropic import Anthropic, beta_tool

client = Anthropic()


@beta_tool
def list_files(directory: str) -> str:
    """List the files in a directory.

    Args:
        directory: The directory to list.
    """
    return f"{directory}/app.log\n{directory}/notes.txt"


@beta_tool
def delete_file(path: str) -> str:
    """Delete a file.

    Args:
        path: The file to delete.
    """
    return f"Deleted {path}."


def main() -> None:
    runner = client.beta.messages.tool_runner(
        model="claude-sonnet-5",
        max_tokens=1024,
        max_iterations=10,
        tools=[list_files, delete_file],
        messages=[{"role": "user", "content": "List the files in /tmp/demo, then delete the ones that end in .log."}],
        stream=True,
        run_tools_eagerly=True,
    )

    for stream in runner:
        # `list_files` runs while the reply is still streaming. A `delete_file` call waits for the answer below.
        for event in stream:
            if event.type == "content_block_start" and event.content_block.type == "tool_use":
                if event.content_block.name == "delete_file":
                    runner.defer_tool_call(event.content_block)
            elif event.type == "text":
                print(event.text, end="", flush=True)

        held = runner.deferred_tool_calls
        if not held:
            continue

        print("\nThe model wants to run:")
        for tool_use in held:
            print(f"  {tool_use.name}({tool_use.input})")
        if input("Allow? [y/N] ").strip().lower() != "y":
            print("Stopped before running them.")
            break
        # The held calls run when this loop body ends.


main()
