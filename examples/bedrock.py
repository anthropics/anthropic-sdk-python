#!/usr/bin/env -S poetry run python

# Note: you must have installed `anthropic` with the `bedrock` extra
# e.g. `pip install -U anthropic[bedrock]`

from anthropic import AnthropicBedrock

# Note: this assumes you have AWS credentials configured.
#
# https://boto3.amazonaws.com/v1/documentation/api/latest/guide/credentials.html
client = AnthropicBedrock()

# Some Amazon Bedrock models must be invoked with an inference profile ID or
# inference profile ARN for on-demand throughput. If a direct model ID returns
# an error like "on-demand throughput isn't supported", use the ID from Bedrock
# Cross-region inference, for example:
#
# model = "us.anthropic.claude-sonnet-4-5-20250929-v1:0"
#
# Inference profile ARNs can also be used, for example:
#
# model = "arn:aws:bedrock:us-east-1:123456789012:inference-profile/us.anthropic.claude-sonnet-4-5-20250929-v1:0"
MODEL = "us.anthropic.claude-sonnet-4-5-20250929-v1:0"

print("------ standard response ------")
message = client.messages.create(
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": "Hello!",
        }
    ],
    model=MODEL,
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
    model=MODEL,
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)
    print()

    # you can still get the accumulated final message outside of
    # the context manager, as long as the entire stream was consumed
    # inside of the context manager
    accumulated = stream.get_final_message()
    print("accumulated message: ", accumulated.model_dump_json(indent=2))
