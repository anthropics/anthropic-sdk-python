#!/usr/bin/env -S poetry run python

import asyncio

from anthropic import AI_PROMPT, HUMAN_PROMPT, Anthropic, APIStatusError, AsyncAnthropic

client = Anthropic()
async_client = AsyncAnthropic()

question = """
Hey Claude! How can I recursively list all files in a directory in Python?
"""


def sync_stream() -> None:
    stream = client.completions.create(
        prompt=f"{HUMAN_PROMPT} {question}{AI_PROMPT}",
        model="claude-2.1",
        stream=True,
        max_tokens_to_sample=300,
    )

    for completion in stream:
        print(completion.completion, end="", flush=True)

    print()


async def async_stream() -> None:
    stream = await async_client.completions.create(
        prompt=f"{HUMAN_PROMPT} {question}{AI_PROMPT}",
        model="claude-2.1",
        stream=True,
        max_tokens_to_sample=300,
    )

    async for completion in stream:
        print(completion.completion, end="", flush=True)

    print()


def stream_error() -> None:
    try:
        client.completions.create(
            prompt=f"{HUMAN_PROMPT} {question}{AI_PROMPT}",
            model="claude-unknown-model",
            stream=True,
            max_tokens_to_sample=300,
        )
    except APIStatusError as err:
        print(f"Caught API status error with response body: {err.response.text}")


sync_stream()
asyncio.run(async_stream())
stream_error()
