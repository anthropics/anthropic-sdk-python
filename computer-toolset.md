# Computer toolset

`computer_toolset_20260801` is one `tools[]` entry that gives the model a family of desktop tools (`screenshot`, `left_click`, `type`, …), which the SDK's identifiers call *members*. The SDK ships no desktop driver: you subclass `BetaAbstractComputerToolset20260801` and implement the tools your backend supports.

## Quick start

```py
from anthropic import Anthropic
from my_desktop import MyDesktop, confirm  # both shown below

with MyDesktop(backend, confirm=confirm) as desktop:
    runner = Anthropic().beta.messages.tool_runner(
        model="claude-sonnet-5",
        max_tokens=1024,
        tools=[desktop],
        messages=[{"role": "user", "content": "Open the calculator and compute 17 * 23."}],
    )
    for message in runner:
        print(message)
```

- You close the desktop. The runner ([tools.md](tools.md#tool-runner)) never does.
- The runner runs a turn's computer actions in order and stops at the first one that fails or is refused. Other tools in the turn still run.

Without the runner, pass `desktop` in the `tools` of `client.beta.messages.create()` and answer each computer `tool_use` in the reply (`message` below) with `desktop.tool_result(tool_use)`. A refusal or failure comes back as an `is_error` result, and your loop must not run the turn's later computer actions:

```py
from anthropic.types.beta import BetaToolResultBlockParam

uses = [b for b in message.content if b.type == "tool_use" and b.toolset_name == desktop.toolset_name]
results: list[BetaToolResultBlockParam] = []
for use in uses:
    if results and results[-1].get("is_error"):  # a skipped tool_use still needs a result
        results.append({
            "type": "tool_result", "tool_use_id": use.id, "toolset_name": use.toolset_name, "is_error": True,
            "content": "Not executed: an earlier computer action in this turn failed.",
        })
    else:
        results.append(desktop.tool_result(use))
```

## Implement a driver

```py
from anthropic.tools.computer import BetaAbstractComputerToolset20260801, BetaScreenshotResult, BetaToolsetCallContext
from anthropic.types.beta import BetaComputerLeftClickInput, BetaComputerScreenshotInput, BetaComputerTypeInput

class MyDesktop(BetaAbstractComputerToolset20260801):
    def __init__(self, backend, **options):
        super().__init__(**options)
        self.backend = backend  # whatever reaches your desktop: a VNC client, a remote-desktop API, xdotool

    def screenshot(self, context: BetaToolsetCallContext, input: BetaComputerScreenshotInput) -> BetaScreenshotResult:
        return BetaScreenshotResult(data=self.backend.png_base64())

    def left_click(self, context: BetaToolsetCallContext, input: BetaComputerLeftClickInput) -> None:
        self.backend.click(input.coordinate, input.text)  # see Coordinates

    def type(self, context: BetaToolsetCallContext, input: BetaComputerTypeInput) -> None:
        self.backend.type(input.text)

    def close(self) -> None:
        super().close()  # first: it waits for calls in flight
        self.backend.close()
```

Override the tools your backend supports: `key`, `hold_key`, `type`, `cursor_position`, `mouse_move`, `left_mouse_down`, `left_mouse_up`, `left_click`, `left_click_drag`, `right_click`, `middle_click`, `double_click`, `triple_click`, `scroll`, `wait`, `screenshot`, `zoom`. `input` is the parsed `BetaComputer<Tool>Input` from `anthropic.types.beta`, and its docstring is the tool's contract. A tool you don't override is sent to the API as `enabled: false`. For `AsyncAnthropic`, subclass `BetaAsyncAbstractComputerToolset20260801`, whose tools and `close` are `async def`.

- **Results.** `screenshot` and `zoom` return a `BetaScreenshotResult`, and `cursor_position` a `BetaComputerCursorPositionResult`. Every other tool returns nothing, or one line of text for the model. The SDK never resizes an image, and the API rejects one over [the model's image limits](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool#handle-coordinate-scaling-for-higher-resolutions). Capture a `zoom` region at display resolution, not from the scaled screenshot.
- **Coordinates.** Every coordinate the model sends is in pixels of the full screenshot, not of the display or a `zoom` image. Your driver scales them to display pixels, reports `cursor_position` back in screenshot pixels (rounded to `int`), and keeps the capture size fixed for the session.
- **Input values.** The SDK checks the types in `input`, not the values. Raise `ToolError` for a coordinate outside the display (don't clamp it) and for a `duration`, `repeat` or `scroll_amount` your backend should not honor.
- **Errors.** When a tool raises `ToolError` (from `anthropic.tools`) or any other exception, the model reads its text, unredacted, and the run continues. Keep error text to fixed phrases: an exception's message can carry screen content, a host name or a session token. A `ToolsetUsageError`, a mistake in your code or options, propagates and stops the run.
- **Try it without the API.** Pass a hand-built `BetaToolUseBlock` (from `anthropic.types.beta`) to `tool_result()`: `desktop.tool_result(BetaToolUseBlock(type="tool_use", id="toolu_1", toolset_name="computer", name="left_click", input={"coordinate": [640, 360]}))`.

## Options

- `configs={"zoom": {"enabled": False}}` turns a tool off.
- `tool_configs={"cache_control": {"type": "ephemeral"}}` sets `cache_control` on the `tools[]` entry.
- `confirm=confirm` is asked before each call runs, and only `True` approves: any other answer refuses the call, and so does an exception (raise `ToolError` to word the refusal). Without one, nothing is asked, clicks included. The constructor requires one while `type`, `key` or `hold_key` is enabled. Show the approver the tool and its input, with every invisible character escaped: the model may be relaying screen content, and what the approver reads must be what runs.

```py
import json
from anthropic.tools.computer import BetaComputerConfirmContext

def confirm(context: BetaComputerConfirmContext) -> bool:
    if context.member not in {"type", "key", "hold_key"}:
        return True
    # json.dumps escapes every non-ASCII and control character
    return ask_user(f"Allow {context.member}?\n{json.dumps(context.input.to_dict(), indent=2)}")
```

**Hooks.** Override `execute(context, name, input)` and call `super().execute(...)` to run code around every call, or skip `super()` to forward every call to a remote desktop. It runs after `confirm`, so nothing checks an input you change there. Overriding `execute` marks every tool as served, so the model is offered all of them: turn off the ones you don't serve in `configs`.

## Running a computer toolset safely

What is on the screen steers the model: a page, a document or a message can try to make it type into the wrong window or trigger consequential actions. Before you run a driver against anything but a throwaway machine:

1. **Isolate the desktop.** Run it in one container or VM per session, with no credentials or host mounts and egress only to the hosts the task needs. Keep the model loop, the toolset and the API key outside it.
2. **Gate consequential actions with `confirm`.** It sees the tool and its input, not what a click does on the screen. If the desktop has applications that can send, pay or delete, have a person approve clicks too. With a terminal, a run dialog or a launcher focused, whatever is typed runs as a command.
3. **Treat the screen as untrusted.** Never execute, store as trusted or forward screen contents, window titles or clipboard text unchecked.
