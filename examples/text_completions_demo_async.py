#!/usr/bin/env -S poetry run python

import asyncio

import anthropic
from anthropic import AsyncAnthropic


async def main() -> None:
    client = AsyncAnthropic()

    res = await client.completions.create(
        model="claude-2.1",
        prompt=f"{anthropic.HUMAN_PROMPT} how does a court case get to the Supreme Court? {anthropic.AI_PROMPT}",
        max_tokens_to_sample=1000,
    )
    print(res.completion)


asyncio.run(main())
