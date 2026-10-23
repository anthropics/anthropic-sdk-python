import rich

from anthropic import Anthropic, beta_tool

client = Anthropic()


@beta_tool
def lookup_order(order_id: str) -> str:
    """Look up the shipping status of an order.

    Args:
        order_id: The order number, e.g. 4821
    """
    return f"Order {order_id} shipped two days ago and arrives tomorrow."


def main() -> None:
    thread = client.beta.messages.thread(
        model="claude-sonnet-5",
        max_tokens=1024,
        system="You are a support agent for Acme. Keep replies short.",
        tools=[lookup_order],
    )

    # Each turn sends only the new messages; the server holds the rest of the conversation.
    first = thread.send({"role": "user", "content": "Hi! I have a question about an order."})
    rich.print(first.content)

    # `stream()` sends a turn the same way and streams the reply as it arrives.
    with thread.stream(
        {"role": "user", "content": "Before I find the order number: how long does standard shipping usually take?"}
    ) as stream:
        for text in stream.text_stream:
            print(text, end="", flush=True)
        print()

    # A turn that may call `lookup_order` goes through the tool runner, which continues the same thread and answers
    # the tool calls.
    thread.append({"role": "user", "content": "It's order #4821 and it hasn't arrived. Can you check where it is?"})
    final = thread.tool_runner().until_done()
    rich.print(final.content)

    # The streaming runner yields one stream per turn and still answers any tool calls in between.
    thread.append({"role": "user", "content": "Thanks. What should I do if it isn't here by then?"})
    for stream in thread.tool_runner(stream=True):
        for text in stream.text_stream:
            print(text, end="", flush=True)
        print()

    # `fork()` copies the thread. The fork's first turn starts a new server-side thread from the same history, and the
    # two continue independently from then on.
    cancellation = thread.fork()
    cancellation.append({"role": "user", "content": "Actually, I'd rather cancel the order and get a refund."})
    rich.print(cancellation.tool_runner().until_done().content)
    rich.print(thread.send({"role": "user", "content": "Great, I'll wait for it. Thanks!"}).content)

    # `model`, `system`, `tools`, ... are fixed for a thread's lifetime; start a new one from the history to change them.
    escalation = client.beta.messages.thread(
        model="claude-sonnet-5",
        max_tokens=1024,
        system="You are a senior support agent for Acme. Decide whether to refund, and say why in one sentence.",
        tools=[lookup_order],
        messages=cancellation.messages,
    )
    decision = escalation.send({"role": "user", "content": "Can you approve the refund?"})
    rich.print(decision.content)


main()
