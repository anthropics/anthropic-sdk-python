#!/usr/bin/env -S poetry run python

# Note: you must have installed `anthropic` with the `bedrock` extra
# e.g. `pip install -U anthropic[bedrock]`

from anthropic import AnthropicBedrock

# Note: this assumes you have AWS credentials configured.
#
# https://boto3.amazonaws.com/v1/documentation/api/latest/guide/credentials.html
client = AnthropicBedrock()

print("------ standard response ------")
message = client.messages.create(
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": "Hello!",
        }
    ],
    model="anthropic.claude-3-sonnet-20240229-v1:0",
)
print(message.model_dump_json(indent=2))

print("------ streamed response ------")

with client.messages.stream(
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": "Say hello there!",
        }
    ],
    model="anthropic.claude-3-sonnet-20240229-v1:0",
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)
    print()

    # you can still get the accumulated final message outside of
    # the context manager, as long as the entire stream was consumed
    # inside of the context manager
    accumulated = stream.get_final_message()
    print("accumulated message: ", accumulated.model_dump_json(indent=2))
