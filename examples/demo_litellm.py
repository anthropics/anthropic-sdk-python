#!/usr/bin/env -S poetry run python

import asyncio
from litellm import completion

def main() -> None:
    messages = [
        { "content": "You are a helpful assistant","role": "system"}
        { "content": "how does a court case get to the Supreme Court?","role": "user"},
    ]
    result = completion(model="claude-2", max_tokens=1000))
    print(result)


main()
