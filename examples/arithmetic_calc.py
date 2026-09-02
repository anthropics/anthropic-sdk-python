from __future__ import annotations

from anthropic import Anthropic
from anthropic.types import MessageParam, ToolParam

client = Anthropic()

_AB_SCHEMA = {
    "type": "object",
    "properties": {"a": {"type": "number"}, "b": {"type": "number"}},
    "required": ["a", "b"],
}

TOOLS: list[ToolParam] = [
    {"name": "add", "description": "Add two numbers", "input_schema": _AB_SCHEMA},
    {"name": "subtract", "description": "Subtract b from a", "input_schema": _AB_SCHEMA},
    {"name": "multiply", "description": "Multiply two numbers", "input_schema": _AB_SCHEMA},
    {
        "name": "divide",
        "description": "Divide a by b",
        "input_schema": {
            "type": "object",
            "properties": {
                "a": {"type": "number"},
                "b": {"type": "number", "description": "Must be non-zero"},
            },
            "required": ["a", "b"],
        },
    },
]

_OPS = {
    "add": lambda a, b: a + b,
    "subtract": lambda a, b: a - b,
    "multiply": lambda a, b: a * b,
}


def _run_tool(name: str, inputs: dict) -> str:
    a, b = inputs["a"], inputs["b"]
    if name == "divide":
        if b == 0:
            return "Error: division by zero"
        return str(a / b)
    if name in _OPS:
        return str(_OPS[name](a, b))
    return f"Error: unknown tool '{name}'"


def calculate(expression: str) -> str:
    messages: list[MessageParam] = [{"role": "user", "content": expression}]

    while True:
        response = client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=1024,
            tools=TOOLS,
            messages=messages,
        )

        if response.stop_reason != "tool_use":
            return next((b.text for b in response.content if b.type == "text"), "")

        tool_uses = [b for b in response.content if b.type == "tool_use"]
        messages.append({"role": "assistant", "content": response.content})
        messages.append({
            "role": "user",
            "content": [
                {
                    "type": "tool_result",
                    "tool_use_id": t.id,
                    "content": _run_tool(t.name, t.input),
                }
                for t in tool_uses
            ],
        })


if __name__ == "__main__":
    print(calculate("What is 1 + 1?"))
    print(calculate("What is (10 + 5) * 3 - 8 / 2?"))
