# Browser toolset

`browser_toolset_20260801` is a *toolset*: one `tools[]` entry that declares a family of member tools (`navigate`, `screenshot`, `left_click`, …). Each call arrives as a `tool_use` block whose `name` is the member and whose `toolset_name` is `"browser"`.

The SDK ships no browser driver and no URL policy. It ships the abstract class a driver subclasses. Before a call reaches the driver, the SDK runs your `url_policy` (on `navigate`), your `file_policy` (on `file_upload`) and then your `confirm` (on every call). An example driver for the Chrome DevTools Protocol is in [claude-quickstarts](https://github.com/anthropics/claude-quickstarts).

## Quick start

```py
from anthropic import Anthropic
from my_browser import MyBrowser, example_policy  # your driver and your URL policy, both shown below

with MyBrowser(backend, url_policy=example_policy(["example.com", "iana.org"])) as browser:
    runner = Anthropic().beta.messages.tool_runner(
        model="claude-sonnet-5",
        max_tokens=1024,
        tools=[browser],
        messages=[{"role": "user", "content": "Open example.com and tell me the page heading."}],
    )
    for message in runner:
        print(message)
```

- You close the browser. The runner ([tools.md](tools.md#tool-runner)) never does, so one instance can serve several runs.
- The runner runs a turn's browser actions in order and stops at the first one that fails or is refused. Other tools in the turn still run.
- Before you deploy a driver, read [Running a browser toolset safely](#running-a-browser-toolset-safely).

Without the runner, pass `browser` in the `tools` of `client.beta.messages.create()` and answer each browser `tool_use` in the reply (`message` below) with `browser.tool_result(tool_use)`. A refusal or failure comes back as an `is_error` result, and your loop must not run the turn's later browser actions:

```py
from anthropic.types.beta import BetaToolResultBlockParam

uses = [b for b in message.content if b.type == "tool_use" and b.toolset_name == browser.toolset_name]
results: list[BetaToolResultBlockParam] = []
for use in uses:
    if results and results[-1].get("is_error"):  # a skipped tool_use still needs a result
        results.append({
            "type": "tool_result", "tool_use_id": use.id, "toolset_name": use.toolset_name, "is_error": True,
            "content": "Not executed: an earlier action in this turn failed.",
        })
    else:
        results.append(browser.tool_result(use))
```

## Implement a driver

```py
from anthropic.tools.browser import (
    BetaAbstractBrowserToolset20260801, BetaBrowserNavigateResult, BetaBrowserState,
    BetaScreenshotResult, BetaToolsetCallContext,
)
from anthropic.types.beta import BetaBrowserLeftClickInput, BetaBrowserNavigateInput, BetaBrowserScreenshotInput

class MyBrowser(BetaAbstractBrowserToolset20260801):
    def __init__(self, backend, **options):
        super().__init__(**options)
        self.backend = backend  # whatever reaches your browser: a DevTools client, a hosted browser's API

    def _browser_state(self, context: BetaToolsetCallContext) -> BetaBrowserState:
        return BetaBrowserState(
            tabs=[{"tab_id": t.id, "title": t.title, "url": t.url, "active": t.active} for t in self.backend.tabs()],
            state_changes=self.backend.drain_changes(),
        )

    def navigate(self, context: BetaToolsetCallContext, input: BetaBrowserNavigateInput) -> BetaBrowserNavigateResult:
        page = self.backend.goto(input.url, input.tab_id)  # as the model wrote it: see Addresses
        return BetaBrowserNavigateResult(url=page.url, status=page.status, title=page.title)

    def screenshot(self, context: BetaToolsetCallContext, input: BetaBrowserScreenshotInput) -> BetaScreenshotResult:
        return BetaScreenshotResult(data=self.backend.png_base64(input.tab_id))

    def left_click(self, context: BetaToolsetCallContext, input: BetaBrowserLeftClickInput) -> None:
        self.backend.click(input.target, input.tab_id)

    def close(self) -> None:
        super().close()  # first: it waits for calls in flight
        self.backend.close()
```

Override the members your backend supports. A member you don't override is sent to the API as `enabled: false`. `input` is the parsed `BetaBrowser<Member>Input`, and its docstring is the member's contract. For `AsyncAnthropic`, subclass `BetaAsyncAbstractBrowserToolset20260801`, whose members, `_browser_state` and `close` are `async def`. Import the names in this guide from `anthropic.tools.browser`, the errors from `anthropic.tools`, and the generated inputs, blocks and `*Param` types from `anthropic.types.beta`.

Members: `navigate`, `list_tabs`, `new_tab`, `switch_tab`, `close_tab`, `read_page`, `get_page_text`, `read_console`, `read_network`, `find`, `form_input`, `file_upload`, `scroll_to`, `screenshot`, `zoom`, `left_click`, `right_click`, `middle_click`, `double_click`, `triple_click`, `hover`, `left_click_drag`, `left_mouse_down`, `left_mouse_up`, `mouse_move`, `scroll`, `type`, `key`, `hold_key`, `wait`, `javascript_exec`.

- **State.** Every driver implements `_browser_state(context)`, its report of the browser. The SDK calls it after every call, failed and refused ones included. Return every open tab and drain your state changes: tabs opened and downloads (the generated `BetaBrowserStateChange*Param` types), and a `BetaDialogDismissed(kind=..., message=...)` for every native dialog you dismiss, since no member answers a dialog. Catch failures inside it: an exception from it stops the run.
- **Tabs.** Mark exactly one tab `active`, truthfully, and honor `tab_id` in every member that takes one: `confirm` is shown the tab URL from your last report, not from the browser. After `new_tab`, the new tab must be the only active one, or the call fails.
- **Results.** Each member's signature in the base class gives its return type. A string is text for the model: at most one line from an action such as a click. The SDK sends the text of a reading member such as `get_page_text` uncut, so bound its length. The model does not see what `new_tab`, `switch_tab` and `list_tabs` return: it reads the `browser_state` block.
- **Addresses.** `navigate` receives `input.url` as the model wrote it, or the word `back`, `forward` or `reload`. Read the address the way your `url_policy` does: add `https://` when it has no scheme, and refuse every other scheme you don't mean to open, such as `javascript:`, `view-source:`, `data:` and `file:`.
- **Coordinates.** Coordinates are viewport pixels, in the frame of a full-viewport screenshot. Capture the viewport, not the full page, at device scale factor 1, or scale the coordinates yourself. The SDK never resizes an image, and the API rejects one over [the model's image limits](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool#handle-coordinate-scaling-for-higher-resolutions).
- **Input values.** The SDK checks the types in `input`, not the values. Raise `ToolError` for a `wait` or `hold_key` `duration` longer than you support.
- **Errors.** When a member raises `ToolError` or any other exception, the model reads its text, unredacted, and the run continues. Keep paths and URLs out of it and use fixed phrases, in `download_failed.error` too: never `str(exc)`. A `ToolsetUsageError`, a mistake in your code or options, propagates and stops the run.
- **Try it without the API.** Pass a hand-built `BetaToolUseBlock` to `tool_result()`, which runs the policies and `confirm` too: `browser.tool_result(BetaToolUseBlock(type="tool_use", id="toolu_1", toolset_name="browser", name="navigate", input={"url": "example.com"}))`.

## Options

To change an option, build a new toolset and a new runner. An exception from `url_policy`, `file_policy` or `confirm` refuses the call.

| option | what it is | left unset |
|---|---|---|
| `configs` | `{"<member>": {"enabled": bool}}`, which turns a member on or off | `file_upload`, `read_console`, `read_network` and `javascript_exec` stay off |
| `url_policy` | `(context, url) -> None`, your check on the address of each `navigate` | `navigate` is not checked |
| `file_policy` | a `BetaFilePolicy`, such as `BetaLocalFilePolicy` | uploads are refused, and download paths stay hidden |
| `confirm` | `(context) -> bool`, asked before every call | nothing is asked |
| `tool_configs` | other fields of the `tools[]` entry, such as `{"cache_control": {"type": "ephemeral"}}` | none are sent |

**Approval.** Only `True` from `confirm(context)` approves: any other answer refuses the call (raise `ToolError` to word the refusal). Return `True` for the members you don't gate. `javascript_exec` and `file_upload` cannot be enabled without a `confirm`.

`context.tab_url` is the target tab's URL in the driver's last report. The page may have moved since, and the approved call runs wherever the tab is by then. `None` (the first call, a tab the report does not list) means the page is unknown, not that the tab is empty. If you remember approvals per site, ask again whenever the URL is missing or has no host (`about:blank`, a browser error page).

Show the approver the member, the page and the input, with every invisible character escaped (in `tab_url` too): the model may be relaying page content, and what the approver reads must be what runs.

```py
import json
from anthropic.tools.browser import BetaConfirmContext

def confirm(context: BetaConfirmContext) -> bool:
    if context.member not in {"javascript_exec", "file_upload"}:
        return True
    # json.dumps escapes every non-ASCII and control character; ask_user is how you ask a person
    page = json.dumps(context.tab_url) if context.tab_url else "an unknown page"
    return ask_user(f"Allow {context.member} on {page}?\n{json.dumps(context.input.to_dict(), indent=2)}")
```

**Hooks.** Override `execute(context, name, input)` and call `super().execute(...)` to run code around every call, or skip `super()` to forward every call to a remote browser. It runs after the policies and `confirm`, so nothing checks an input you change there. Overriding `execute` marks every member as served, so the model is offered every member that is on by default: turn off the ones you don't serve in `configs`.

## Running a browser toolset safely

The pages the model visits steer its actions: a page can try to point the browser at internal services, pull files off the host or trigger consequential actions. Do all of this before you run a driver against anything but a throwaway profile.

1. **Pass a `url_policy`.** Left unset, `navigate` is not checked. See [URL policy](#url-policy).
2. **Intercept requests in the driver.** The policy sees only the address the model asks for: not a redirect, a subresource or a navigation a page starts. The toolset does not expose the policy, so keep it (`self._policy = options.get("url_policy")`) and call it from your request handler as `self._policy(BetaURLContext(), url)`. An async policy refuses nothing unless you await it. Abort the request on any exception, and report a page-started navigation you refuse as a `BetaNavigationRefused()` state change.
3. **Put egress rules on the browser's container.** Allow only the hosts the task needs. This is the backstop: interception does not see every request. An open DevTools port is unauthenticated full control of the browser and bypasses the policies and `confirm`, so let only the model loop's host reach it.
4. **Pass a `file_policy`, or leave `file_upload` off.** `file_upload` lets the page the model is browsing read files from the browser host. See [File policy](#file-policy).
5. **Gate consequential members with `confirm`.** It sees the member, its input and the tab's URL, not what a click does. Ask a person for `javascript_exec` and `file_upload` everywhere, and for clicks, `type`, `key` and `form_input` on sites where purchases, messages or accepting terms can happen.
6. **Isolate the browser.** Run it in one container or VM per session, with a fresh profile, no credentials, no mounts beyond the upload roots and the download directory, and no filesystem shared with other tools the model can call. Keep the model loop, the toolset and the API key outside it.
7. **Treat everything a page returns as untrusted.** That includes titles, URLs, file names and downloaded files: never execute, store as trusted or forward them unchecked. URLs reach the model and `confirm` unredacted, with any credentials and `data:` bodies.

**Hosted browsers.** Egress rules and isolation (3, 6) are the provider's, so a request your interception misses can reach whatever the provider's network can. A hosted browser cannot mount your upload roots: refuse path uploads and use `document_ids`, or check paths where the browser runs.

### URL policy

`url_policy(context, url)` returns `None` to allow and raises `ToolError` to refuse. `url` is the string exactly as the model wrote it: not trimmed, not normalized, no scheme added. `back`, `forward` and `reload` are not put to the policy.

```py
import re
from urllib.parse import urlsplit
from anthropic.tools import ToolError
from anthropic.tools.browser import BetaURLContext, BetaURLPolicy

def example_policy(allowed_hosts: list[str]) -> BetaURLPolicy:
    """An example, not a production policy: http(s) pages on the allowed hosts or their subdomains."""
    hosts = [host for host in (entry.strip().lower().rstrip(".") for entry in allowed_hosts) if host]

    def policy(_context: BetaURLContext, url: str) -> None:
        # A browser, or a strip() in your driver, drops these before the scheme is read: " file:" would pass below.
        if re.search(r"[\s\x00-\x1f\x7f]", url):
            raise ToolError("blocked: the address contains whitespace or a control character")
        # Judge what the browser will open: no scheme means https://, and a backslash reads as a slash.
        with_scheme = url if re.match(r"[a-z][a-z0-9+.-]*:", url, re.I) else f"https://{url}"
        parts = urlsplit(with_scheme.replace("\\", "/"))  # a parse error raises, which also refuses
        host = (parts.hostname or "").lower()
        if parts.scheme not in ("http", "https") or not any(host == h or host.endswith("." + h) for h in hosts):
            raise ToolError(f"blocked: {url} is not on an allowed host")

    return policy
```

A production policy needs more: parse the address the way a browser reads it, and account for the many spellings one host or IP address has. This one reads a bare `localhost:3000` as a scheme and refuses it.

### File policy

`BetaLocalFilePolicy` is the `file_policy` the SDK ships. It judges paths on the machine that runs the SDK, so mount the upload roots at the same path in the browser's container. To write your own, implement `BetaFilePolicy` and build on `beta_check_upload_path(path, roots)`.

```py
from anthropic.tools.browser import BetaLocalFilePolicy

browser = MyBrowser(
    backend,
    configs={"file_upload": {"enabled": True}},  # MyBrowser must also implement file_upload
    confirm=confirm,
    file_policy=BetaLocalFilePolicy(
        upload_roots=["/task/uploads"],
        upload_document_ids=["file_011CNha8iCJcU1wXNR6q4V8w"],  # Files API documents the model may attach
        download_dir="/task/downloads",
    ),
)
```

- Create the upload roots first: a missing root grants nothing. Let nothing the model can reach write to them, because the check runs once, before the driver opens the file.
- Point the driver at one dedicated download directory, outside every upload root and out of reach of the model's other tools. `download_dir` does not move downloads: it bounds the paths the model may see, and only with `expose_download_paths=True`.
