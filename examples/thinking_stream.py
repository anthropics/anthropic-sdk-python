import anthropic

client = anthropic.Anthropic()

with client.messages.stream(
    model="claude-sonnet-5",
    max_tokens=16000,
    thinking={"type": "adaptive", "display": "summarized"},
    output_config={"effort": "high"},
    messages=[
        {
            "role": "user",
            "content": "Create a haiku about Anthropic. Think carefully about syllable counts before answering.",
        }
    ],
) as stream:
    thinking = "not-started"

    for event in stream:
        if event.type == "thinking":
            if thinking == "not-started":
                print("Thinking:\n---------")
                thinking = "started"

            print(event.thinking, end="", flush=True)
        elif event.type == "text":
            if thinking != "finished":
                print("\n\nText:\n-----")
                thinking = "finished"

            print(event.text, end="", flush=True)
