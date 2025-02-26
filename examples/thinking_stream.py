import anthropic

client = anthropic.Anthropic()

with client.messages.stream(
    model="claude-3-7-sonnet-20250219",
    max_tokens=3200,
    thinking={"type": "enabled", "budget_tokens": 1600},
    messages=[{"role": "user", "content": "Create a haiku about Anthropic."}],
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
