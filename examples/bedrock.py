#!/usr/bin/env -S poetry run python

# Note: you must have installed `anthropic` with the `bedrock` extra
# e.g. `pip install -U anthropic[bedrock]`

from anthropic import AI_PROMPT, HUMAN_PROMPT, AnthropicBedrock

# Note: this assumes you have AWS credentials configured.
#
# https://boto3.amazonaws.com/v1/documentation/api/latest/guide/credentials.html
client = AnthropicBedrock()

print("------ standard response ------")
completion = client.completions.create(
    model="anthropic.claude-instant-v1",
    prompt=f"{HUMAN_PROMPT} hey!{AI_PROMPT}",
    stop_sequences=[HUMAN_PROMPT],
    max_tokens_to_sample=500,
    temperature=0.5,
    top_k=250,
    top_p=0.5,
)
print(completion.completion)


question = """
Hey Claude! How can I recursively list all files in a directory in Python?
"""

print("------ streamed response ------")
stream = client.completions.create(
    model="anthropic.claude-instant-v1",
    prompt=f"{HUMAN_PROMPT} {question}{AI_PROMPT}",
    max_tokens_to_sample=500,
    stream=True,
)
for item in stream:
    print(item.completion, end="")
print()
