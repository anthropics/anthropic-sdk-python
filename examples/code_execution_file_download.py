#!/usr/bin/env -S uv run python
from __future__ import annotations

from anthropic import Anthropic

client = Anthropic()


def main() -> None:
    # Ask Claude to generate a CSV file using the code execution server tool.
    message = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=4096,
        messages=[
            {
                "role": "user",
                "content": (
                    "Use Python to create a CSV file at /output/report.csv. "
                    "Include a header row (name,age,city) and 3 sample rows of "
                    "data, then print 'Done' when finished."
                ),
            }
        ],
        tools=[{"type": "code_execution_20250825", "name": "code_execution"}],
    )

    # Show every block type that came back for reference.
    print("Response block types:")
    for block in message.content:
        print(f"  {block.type}")

    # Extract the file_id from the code execution result.
    #
    # NOTE — the following pattern shown in some documentation is INCORRECT
    # and will never match when using server-side tools like code_execution:
    #
    #   if block.type == "tool_use" and block.name == "code_execution":
    #       for result_block in block.content:
    #           file_id = result_block.file_id          # never reached
    #
    # Server-side tools (code_execution, web_search, etc.) produce a
    # "server_tool_use" block for the invocation, not "tool_use".
    # The generated file arrives in a separate block:
    #
    #   block                            type = "bash_code_execution_tool_result"
    #     .content                       BashCodeExecutionResultBlock
    #       .content[i]                  BashCodeExecutionOutputBlock
    #         .type == "bash_code_execution_output"
    #         .file_id                   <-- the ID to pass to files.download()

    file_id: str | None = None

    for block in message.content:
        if block.type == "bash_code_execution_tool_result":
            result = block.content  # BashCodeExecutionResultBlock | BashCodeExecutionToolResultError
            if result.type == "bash_code_execution_result":
                for output in result.content:  # List[BashCodeExecutionOutputBlock]
                    if output.type == "bash_code_execution_output" and output.file_id:
                        file_id = output.file_id
                        break
            break

    if file_id is None:
        print("\nNo file output found in the response.")
        return

    print(f"\nFound file_id: {file_id}")

    # Download the generated file and save it locally.
    file_data = client.beta.files.download(file_id)
    output_path = "report.csv"
    with open(output_path, "wb") as f:
        f.write(file_data.read())

    print(f"Saved to '{output_path}'.")


if __name__ == "__main__":
    main()
