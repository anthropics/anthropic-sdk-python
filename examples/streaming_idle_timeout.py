"""Give a streaming call a bound that keepalives cannot reset.

`timeout=` bounds one socket read. A server that sends `: ping` comments, or `ping` events, resets
that timer without ever sending part of the answer, so a stalled stream looks exactly like a slow
one. This example puts a second bound on the same stream: no content for N seconds raises
`APITimeoutError`, whatever the keepalives are doing.

Run against a real endpoint:
    ANTHROPIC_API_KEY=... python examples/streaming_idle_timeout.py
The window here is short so the example finishes quickly; pick yours from the slowest legitimate gap
between content events, not from the total length of a response.
"""

import os

from anthropic import Anthropic, APITimeoutError
from anthropic.lib.streaming._idle_timeout import guard_stream

client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

stream = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Write a paragraph about river deltas."}],
    stream=True,
)
guard_stream(stream, seconds=30.0)

try:
    for event in stream:
        if event.type == "content_block_delta" and event.delta.type == "text_delta":
            print(event.delta.text, end="", flush=True)
except APITimeoutError:
    # Distinguishable from a short answer: this means the server went quiet, not that it finished.
    print("\n[stream went quiet for 30s with no content — treat as a stall]")
