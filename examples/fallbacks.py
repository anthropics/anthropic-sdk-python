#!/usr/bin/env -S uv run python
from anthropic import Anthropic, BetaFallbackState, BetaRefusalFallbackMiddleware
from anthropic.types.beta import BetaMessageParam


def main() -> None:
    # Server-side fallbacks (preferred): the API retries a refusal itself — one
    # request, a plain client, no client-side logic. Use this when talking to
    # the API directly.
    client = Anthropic()
    message = client.beta.messages.create(
        max_tokens=1024,
        model="claude-fable-5",
        messages=[{"role": "user", "content": "Some prompt that triggers a refusal"}],
        fallbacks=[{"model": "claude-opus-4-8"}],
        betas=["server-side-fallback-2026-06-01"],
    )
    print("server-side:", message.model)

    # If your provider doesn't support server-side fallbacks, register the
    # client-side middleware instead:
    fallback_client = Anthropic(
        middleware=[BetaRefusalFallbackMiddleware([{"model": "claude-opus-4-8"}])],
    )
    state = BetaFallbackState()  # pins follow-ups to the model that accepted

    # Streaming: on a refusal the middleware retries and splices the fallback's
    # events onto the open stream — one continuous message, with a `fallback`
    # content block marking the model boundary.
    messages: list[BetaMessageParam] = [{"role": "user", "content": "Some prompt that triggers a refusal"}]
    with state, fallback_client.beta.messages.stream(
        max_tokens=1024,
        model="claude-fable-5",
        messages=messages,
    ) as stream:
        for event in stream:
            if event.type == "text":
                print(event.text, end="", flush=True)
            elif event.type == "content_block_start" and event.content_block.type == "fallback":
                block = event.content_block
                print(f"\n--- fell back: {block.from_.model} -> {block.to.model} ---")
        streamed = stream.get_final_message()
    print("\nstreaming:", streamed.model)
    messages.append({"role": "assistant", "content": streamed.content})

    # Non-streaming: reusing the state keeps the conversation pinned.
    messages.append({"role": "user", "content": "what did I just ask you?"})
    with state:
        follow_up = fallback_client.beta.messages.create(
            max_tokens=1024,
            model="claude-fable-5",
            messages=messages,
        )
    print("non-streaming:", follow_up.model)


main()
