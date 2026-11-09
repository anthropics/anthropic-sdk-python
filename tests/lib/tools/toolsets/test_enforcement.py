# ruff: noqa: ARG001, ARG005 -- stub members and hooks ignore their arguments
"""URL policy and file policy enforcement in the call pipeline: the `url_policy` hook on `navigate`, and upload and
download path handling."""

from __future__ import annotations

from typing import Any
from pathlib import Path
from typing_extensions import override

import pytest

from anthropic.tools import (
    ToolError,
    ToolsetContractError,
)
from anthropic.types.beta import BetaToolUseBlock
from anthropic.tools.browser import (
    BetaURLContext,
    BetaConfirmContext,
    BetaDialogDismissed,
    BetaLocalFilePolicy,
    BetaToolsetCallContext,
    BetaBrowserNavigateResult,
)

from ._fakes import CLICK, UPLOAD, World, FakeBrowser, AsyncFakeBrowser, texts, approve, refusal, state_block

CTX = BetaToolsetCallContext(
    tool_use=BetaToolUseBlock(type="tool_use", id="toolu_9", name="navigate", input={}, toolset_name="browser")
)


def _on(world: World, tab_id: str, url: str, *, active: bool = False) -> None:
    world.tabs[tab_id] = {"title": f"title of {url}", "url": url}
    if active:
        world.active = tab_id


# --- url_policy -----------------------------------------------------------------------------------


def test_the_policy_is_called_once_per_navigate_with_the_url_as_written_before_the_driver_runs() -> None:
    seen: list[Any] = []

    def policy(ctx: BetaURLContext, url: str) -> None:
        seen.append((ctx, url, list(world.calls)))
        if "logout" in url:
            raise ToolError("blocked: logout")

    world = World()
    browser = FakeBrowser(world, url_policy=policy)

    for written in (
        "https://example.com/",
        "example.com/path",
        " Http://Exa\tmple.COM./x ",
        "javascript:alert(1)",
        "backwards",
    ):
        browser.call(CTX, "navigate", {"url": written, "tab_id": "tab_1"})

    # once per call, with the string exactly as the model wrote it, and before the driver heard of it; the driver then
    # receives that same string
    assert [url for _, url, _ in seen] == [
        "https://example.com/",
        "example.com/path",
        " Http://Exa\tmple.COM./x ",
        "javascript:alert(1)",
        "backwards",
    ]
    assert [len(calls) for _, _, calls in seen] == [0, 1, 2, 3, 4]
    assert [i.url for i in world.inputs] == [url for _, url, _ in seen]
    assert all(ctx == BetaURLContext(member="navigate", tab_id="tab_1", tool_use_id="toolu_9") for ctx, _, _ in seen)

    # the history words are navigate's own vocabulary, not addresses: the policy is not asked, and the driver receives
    # the canonical lower-case word
    for written in ("back", " Forward ", "RELOAD"):
        browser.call(CTX, "navigate", {"url": written})
    assert len(seen) == 5 and [i.url for i in world.inputs[-3:]] == ["back", "forward", "reload"]

    # a ToolError it raises is the refusal the model reads, and the driver is not called
    assert refusal(browser, CTX, "navigate", {"url": "https://example.com/logout"}) == "blocked: logout"
    assert len(seen) == 6 and world.calls.count("navigate") == 8

    # no other member consults it, and nothing a result or a report carries does
    _on(world, "tab_2", "https://example.com/logout")
    world.results["navigate"] = BetaBrowserNavigateResult(url="https://example.com/logout", title="bye")
    for name, given in [
        ("get_page_text", {}),
        ("left_click", CLICK),
        ("list_tabs", {}),
        ("new_tab", {}),
        ("switch_tab", {"tab_id": "tab_2"}),
    ]:
        browser.call(CTX, name, given)
    assert texts(browser.call(CTX, "navigate", {"url": "https://example.com/in"}))[0] == (
        "Navigated to https://example.com/logout — bye"
    )
    assert len(seen) == 7

    # a call without a tab_id says so
    browser.call(CTX, "navigate", {"url": "https://example.com/"})
    assert seen[-1][0].tab_id is None


def test_a_policy_that_raises_something_else_refuses_with_the_sdks_text_and_logs(
    caplog: pytest.LogCaptureFixture,
) -> None:
    def policy(ctx: BetaURLContext, url: str) -> None:
        raise TypeError(f"could not parse {url}")

    browser = FakeBrowser(url_policy=policy)
    # its own message (which names the URL) goes to the log, not the model
    assert refusal(browser, CTX, "navigate", {"url": "https://example.com/oops"}) == "refused by the URL policy"
    assert "could not parse https://example.com/oops" in caplog.text
    assert browser.world.calls == []

    # a ToolsetUsageError out of the policy is the developer's and stops the run
    def misuse(ctx: BetaURLContext, url: str) -> None:
        raise ToolsetContractError("wired wrong")

    with pytest.raises(ToolsetContractError, match="wired wrong"):
        FakeBrowser(url_policy=misuse).call(CTX, "navigate", {"url": "https://example.com/"})


def test_a_predicate_shaped_or_async_policy_on_the_sync_class_is_a_contract_error() -> None:
    def predicate(ctx: BetaURLContext, url: str) -> Any:
        return False

    with pytest.raises(ToolsetContractError, match="return None to allow.*; got bool"):
        FakeBrowser(url_policy=predicate).call(CTX, "navigate", {"url": "https://example.com/"})

    async def async_policy(ctx: BetaURLContext, url: str) -> None:
        return None

    with pytest.raises(ToolsetContractError, match="url_policy is async on the synchronous toolset"):
        FakeBrowser(url_policy=async_policy)


def test_unset_checks_nothing() -> None:
    # left unset, navigate is not checked: whatever the model wrote reaches the driver as written
    browser = FakeBrowser()
    for url in ("javascript:alert(1)", "file:///etc/passwd", "http://10.0.0.5/", "chrome://settings", "not a url", ""):
        browser.call(CTX, "navigate", {"url": url})
    assert [i.url for i in browser.world.inputs] == [
        "javascript:alert(1)",
        "file:///etc/passwd",
        "http://10.0.0.5/",
        "chrome://settings",
        "not a url",
        "",
    ]

    # a URL that is not a string is the model's input error and never reaches the driver
    refusal(browser, CTX, "navigate", {"url": ["x"]})
    assert len(browser.world.calls) == 6

    # and a reported address reaches the model as the driver reported it
    for reported in ("file:///etc/passwd", "blob:null/1", "view-source:http://10.0.0.5/", "about:blank", ""):
        _on(browser.world, "tab_1", reported, active=True)
        content = browser.call(CTX, "get_page_text", {})
        assert texts(content) == ["Hello"] and state_block(content)["tabs"][0]["url"] == reported


async def test_an_explicit_none_policy_refuses_navigate_on_both_classes() -> None:
    # None is not a way to leave navigate unchecked: it is called like any other policy, the call raises, and the
    # navigate is refused with the SDK's own text before the driver hears of it.
    sync = FakeBrowser(url_policy=None)  # pyright: ignore[reportArgumentType]
    assert refusal(sync, CTX, "navigate", {"url": "file:///etc/passwd"}) == "refused by the URL policy"
    assert sync.world.calls == []

    async_browser = AsyncFakeBrowser(url_policy=None)  # pyright: ignore[reportArgumentType]
    with pytest.raises(ToolError) as caught:
        await async_browser.call(CTX, "navigate", {"url": "file:///etc/passwd"})
    assert texts(caught.value.content) == ["refused by the URL policy"] and async_browser.world.calls == []


def test_a_call_naming_a_tab_the_last_report_did_not_list_goes_to_the_driver() -> None:
    # The driver owns tab ids and answers an unknown one itself. `confirm` is asked about the call first, with no URL
    # for a tab it was never shown.
    asked: list[BetaConfirmContext] = []

    def confirm(context: BetaConfirmContext) -> bool:
        asked.append(context)
        return True

    browser = FakeBrowser(confirm=confirm)
    _on(browser.world, "tab_1", "https://example.com/", active=True)
    browser.call(CTX, "list_tabs", {})
    assert (
        refusal(browser, CTX, "navigate", {"url": "x", "tab_id": "tab_nope"}) == "No open tab with tab_id 'tab_nope'."
    )
    assert browser.world.calls[-1] == "navigate"
    assert asked[-1].tab_id == "tab_nope" and asked[-1].tab_url is None


def test_a_download_change_without_a_url_is_the_drivers_bug() -> None:
    # Built through pydantic, a download change without its url fails in the driver, or, where the model lets it
    # through, when the SDK reads the report.
    browser = FakeBrowser()
    browser.world.changes = [{"type": "download_started", "download_id": "dl_1"}]  # pyright: ignore[reportAttributeAccessIssue]
    with pytest.raises(ToolsetContractError, match="_browser_state raised"):
        browser.call(CTX, "get_page_text", {})


def test_a_long_reported_tab_url_is_cut_to_the_field_limit_and_its_controls_folded() -> None:
    browser = FakeBrowser()
    long_url = "https://" + "u" * 4090 + "@example.com/admin\n\x0bnext\u202e"
    _on(browser.world, "tab_1", "https://example.com/", active=True)
    _on(browser.world, "tab_2", long_url)

    tabs = {t["tab_id"]: t["url"] for t in state_block(browser.call(CTX, "list_tabs", {}))["tabs"]}
    assert tabs["tab_2"] == "\u2026" + long_url[:4095] and len(tabs["tab_2"]) == 4096

    _on(browser.world, "tab_2", "https://exa\nmple.com/a b\x0b)\u202e\u2028c")
    tabs = {t["tab_id"]: t["url"] for t in state_block(browser.call(CTX, "get_page_text", {}))["tabs"]}
    assert tabs["tab_2"] == "https://exa mple.com/a b ) c"


# --- file policy ----------------------------------------------------------------------------------


def test_uploads_are_refused_without_a_file_policy_and_resolved_with_one(tmp_path: Path) -> None:
    root = tmp_path / "uploads"
    root.mkdir()
    (root / "form.pdf").write_text("x")
    enable: Any = {"configs": {"file_upload": {"enabled": True}}, "confirm": approve}

    bare = FakeBrowser(**enable)
    assert (
        refusal(bare, CTX, "file_upload", {**UPLOAD, "paths": [str(root / "form.pdf")]})
        == "file_upload has no configured upload roots"
    )
    # A staged document is contained the same way: no policy, no upload; a policy lists the ids it allows.
    assert (
        refusal(bare, CTX, "file_upload", {**UPLOAD, "document_ids": ["doc_1"]})
        == "file_upload has no configured document allowlist"
    )

    policy = BetaLocalFilePolicy(upload_roots=[str(root)], upload_document_ids=["doc_1"])
    browser = FakeBrowser(file_policy=policy, **enable)
    assert texts(browser.call(CTX, "file_upload", {**UPLOAD, "paths": [str(root / "form.pdf")]})) == ["Uploaded."]
    assert browser.world.inputs[-1].paths == [str((root / "form.pdf").resolve())]
    assert texts(browser.call(CTX, "file_upload", {**UPLOAD, "document_ids": ["doc_1"]})) == ["Uploaded."]
    assert browser.world.inputs[-1].document_ids == ["doc_1"]
    assert refusal(browser, CTX, "file_upload", {**UPLOAD, "document_ids": ["doc_1", "doc_2"]}) == (
        "document not in the upload allowlist"
    )
    assert refusal(browser, CTX, "file_upload", {**UPLOAD, "paths": [str(tmp_path / "secret")]}) == (
        "file_upload path is outside the configured upload roots"
    )
    assert refusal(browser, CTX, "file_upload", {**UPLOAD, "paths": [str(root / ".." / "secret")]}) == (
        "file_upload path must not contain a '..' component"
    )
    assert refusal(browser, CTX, "file_upload", {**UPLOAD, "paths": "form.pdf"}).startswith("invalid input")
    # Only the two accepted uploads reached the driver.
    assert browser.world.calls.count("file_upload") == 2

    # an upload with no paths and no document ids names nothing to vet, so it is the driver's to answer
    assert texts(browser.call(CTX, "file_upload", dict(UPLOAD))) == ["Uploaded."]
    assert texts(bare.call(CTX, "file_upload", dict(UPLOAD))) == ["Uploaded."]


def test_a_file_policy_hook_may_return_any_iterable() -> None:
    class Lazy(BetaLocalFilePolicy):
        @override
        def resolve_upload_documents(self, context: Any, document_ids: Any) -> Any:
            return (d for d in document_ids)  # a generator: read once, handed to the driver as a list

    browser = FakeBrowser(configs={"file_upload": {"enabled": True}}, confirm=approve, file_policy=Lazy())
    assert texts(browser.call(CTX, "file_upload", {**UPLOAD, "document_ids": ["doc_9"]})) == ["Uploaded."]
    assert browser.world.inputs[-1].document_ids == ["doc_9"]


def test_download_paths_reach_the_model_only_through_an_exposing_file_policy() -> None:
    def completed(world: World) -> None:
        world.changes = [
            {
                "type": "download_completed",
                "download_id": "dl_1",
                "url": "https://example.com/a",
                "path": "/dl/x/a.bin",
            },
            {
                "type": "download_completed",
                "download_id": "dl_2",
                "url": "https://example.com/b",
                "path": "/elsewhere/b.bin",
            },
        ]

    def paths(browser: FakeBrowser) -> list[str | None]:
        completed(browser.world)
        return [c.get("path") for c in state_block(browser.call(CTX, "get_page_text", {}))["state_changes"]]

    assert paths(FakeBrowser()) == [None, None]
    assert paths(FakeBrowser(file_policy=BetaLocalFilePolicy(download_dir="/dl"))) == [None, None]
    assert paths(FakeBrowser(file_policy=BetaLocalFilePolicy(download_dir="/dl", expose_download_paths=True))) == [
        "/dl/x/a.bin",
        None,
    ]

    # A custom predicate that fails hides the path and the report still reaches the model.
    class Flaky(BetaLocalFilePolicy):
        @override
        def is_path_visible(self, path: str) -> bool:
            raise OSError("disk on fire")

    assert paths(FakeBrowser(file_policy=Flaky(download_dir="/dl", expose_download_paths=True))) == [None, None]

    # An exposed path reaches the block exactly as the driver reported it, spaces and parentheses kept. A path with a
    # line break stays hidden, because folding it to one line would name a file the policy never checked. A path too
    # long for the policy to resolve on this filesystem stays hidden too, because the policy cannot vouch for it.
    exposing = FakeBrowser(file_policy=BetaLocalFilePolicy(download_dir="/dl", expose_download_paths=True))
    exposing.world.changes = [
        {"type": "download_completed", "download_id": "dl_3", "url": "https://example.com/c", "path": "/dl/x/c\n.bin"},
        {
            "type": "download_completed",
            "download_id": "dl_4",
            "url": "https://example.com/d",
            "path": "/dl/x/" + "d" * 5000,
        },
        {"type": "download_completed", "download_id": "dl_5", "url": "https://example.com/e", "path": "/dl/x/e.bin"},
        {
            "type": "download_completed",
            "download_id": "dl_6",
            "url": "https://example.com/f",
            "path": "/dl/my file (1).pdf",
        },
    ]
    changes = state_block(exposing.call(CTX, "get_page_text", {}))["state_changes"]
    assert [(c["download_id"], c.get("path")) for c in changes] == [
        ("dl_3", None),
        ("dl_4", None),
        ("dl_5", "/dl/x/e.bin"),
        ("dl_6", "/dl/my file (1).pdf"),
    ]


def test_a_file_policy_that_fails_refuses_the_upload_and_the_call_is_still_observed(tmp_path: Path) -> None:
    class Broken(BetaLocalFilePolicy):
        @override
        def resolve_upload_paths(self, context: Any, paths: Any) -> list[str]:
            raise OSError("disk on fire")

    enable: Any = {"configs": {"file_upload": {"enabled": True}}, "confirm": approve}
    browser = FakeBrowser(file_policy=Broken(upload_roots=[str(tmp_path)]), **enable)
    assert refusal(browser, CTX, "file_upload", {**UPLOAD, "paths": [str(tmp_path / "a.pdf")]}) == (
        "the file policy could not vet the upload"
    )
    assert browser.world.calls.count("file_upload") == 0

    # a generator does its work when the SDK reads it; a failure there fails closed the same way
    class LazyBroken(BetaLocalFilePolicy):
        @override
        def resolve_upload_paths(self, context: Any, paths: Any) -> Any:
            for path in paths:
                raise FileNotFoundError(path)
                yield path

    lazy = FakeBrowser(file_policy=LazyBroken(upload_roots=[str(tmp_path)]), **enable)
    assert refusal(lazy, CTX, "file_upload", {**UPLOAD, "paths": [str(tmp_path / "a.pdf")]}) == (
        "the file policy could not vet the upload"
    )
    assert lazy.world.calls.count("file_upload") == 0


# --- error text -----------------------------------------------------------------------------------


def test_a_drivers_error_text_reaches_the_model_as_written_and_cut_to_the_field_limit() -> None:
    # The SDK does not look for local paths in a driver's text: a driver that must keep one from the model leaves it
    # out. Only the length is bounded.
    browser = FakeBrowser()
    _on(browser.world, "tab_1", "https://example.com/", active=True)
    browser.world.fail["left_click"] = ToolError("saved to /var/task/dl/f8a1.bin")
    assert refusal(browser, CTX, "left_click", CLICK) == "saved to /var/task/dl/f8a1.bin"
    browser.world.fail["left_click"] = ToolError("x" * 5000)
    assert refusal(browser, CTX, "left_click", CLICK) == "x" * 4096

    # a dialog's message and a failed download's error reach the model as written too, folded to one line
    browser.world.fail.clear()
    browser.world.changes = [
        {"type": "download_failed", "download_id": "dl_1", "url": "https://example.com/f", "error": "at /var/dl/x"},
        BetaDialogDismissed(kind="alert", message="see /var/task/secret"),
    ]
    content = browser.call(CTX, "left_click", CLICK)
    assert texts(content)[1] == 'An alert dialog "see /var/task/secret" was dismissed.'
    assert state_block(content)["state_changes"][0]["error"] == "at /var/dl/x"


def test_a_raised_exception_reads_as_its_type_and_message_only() -> None:
    class AuthFailed(Exception):
        @override
        def __str__(self) -> str:
            return "authentication failed"

    class BrokenMessage(Exception):
        @override
        def __str__(self) -> str:
            raise ValueError("no message")

    browser = FakeBrowser()
    _on(browser.world, "tab_1", "https://example.com/", active=True)

    # a constructor argument the message leaves out, such as a token, does not reach the model
    browser.world.fail["left_click"] = AuthFailed("token-123")
    assert refusal(browser, CTX, "left_click", CLICK) == "AuthFailed: authentication failed"
    # with no message, or a message that cannot be read, the model gets the type
    browser.world.fail["left_click"] = TimeoutError()
    assert refusal(browser, CTX, "left_click", CLICK) == "TimeoutError"
    browser.world.fail["left_click"] = BrokenMessage("x")
    assert refusal(browser, CTX, "left_click", CLICK) == "BrokenMessage"


# --- async parity ---------------------------------------------------------------------------------


async def test_the_async_class_takes_a_plain_or_a_coroutine_policy_and_calls_it_the_same_way() -> None:
    seen: list[Any] = []

    def plain(ctx: BetaURLContext, url: str) -> None:
        seen.append(("plain", ctx, url))
        if "internal" in url:
            raise ToolError("blocked: internal")

    async def coroutine(ctx: BetaURLContext, url: str) -> None:
        seen.append(("coroutine", ctx, url))
        if "internal" in url:
            raise ToolError("blocked: internal")

    for policy in (plain, coroutine):
        browser = AsyncFakeBrowser(url_policy=policy)
        with pytest.raises(ToolError) as caught:
            await browser.call(CTX, "navigate", {"url": "https://wiki.internal/", "tab_id": "tab_1"})
        assert texts(caught.value.content) == ["blocked: internal"] and browser.world.calls == []
        await browser.call(CTX, "navigate", {"url": " Example.COM/x "})
        await browser.call(CTX, "get_page_text", {})
        assert browser.world.calls == ["navigate", "get_page_text"] and browser.world.inputs[0].url == " Example.COM/x "

    assert [(kind, url) for kind, _, url in seen] == [
        ("plain", "https://wiki.internal/"),
        ("plain", " Example.COM/x "),
        ("coroutine", "https://wiki.internal/"),
        ("coroutine", " Example.COM/x "),
    ]
    assert seen[0][1] == BetaURLContext(member="navigate", tab_id="tab_1", tool_use_id="toolu_9")

    async def predicate(ctx: BetaURLContext, url: str) -> Any:
        return True

    with pytest.raises(ToolsetContractError, match="got bool"):
        await AsyncFakeBrowser(url_policy=predicate).call(CTX, "navigate", {"url": "https://example.com/"})

    unset = AsyncFakeBrowser()
    await unset.call(CTX, "navigate", {"url": "javascript:alert(1)"})
    assert unset.world.inputs[-1].url == "javascript:alert(1)"


async def test_the_async_class_enforces_upload_roots_too(tmp_path: Path) -> None:
    policy = BetaLocalFilePolicy(upload_roots=[str(tmp_path)])
    uploads = AsyncFakeBrowser(file_policy=policy, configs={"file_upload": {"enabled": True}}, confirm=approve)

    with pytest.raises(ToolError) as caught:
        await uploads.call(CTX, "file_upload", {**UPLOAD, "paths": ["/etc/passwd"]})
    assert texts(caught.value.content) == ["file_upload path is outside the configured upload roots"]
    assert uploads.world.calls == []


async def test_a_policy_that_raises_something_else_refuses_with_the_sdks_text_and_logs_on_the_async_class(
    caplog: pytest.LogCaptureFixture,
) -> None:
    def plain(ctx: BetaURLContext, url: str) -> None:
        raise TypeError(f"could not parse {url}")

    async def coroutine(ctx: BetaURLContext, url: str) -> None:
        raise TypeError(f"could not parse {url}")

    for policy in (plain, coroutine):
        caplog.clear()
        browser = AsyncFakeBrowser(url_policy=policy)

        with pytest.raises(ToolError) as caught:
            await browser.call(CTX, "navigate", {"url": "https://example.com/oops"})

        # its own message (which names the URL) goes to the log, not the model
        assert texts(caught.value.content) == ["refused by the URL policy"]
        assert "could not parse https://example.com/oops" in caplog.text
        assert browser.world.calls == []

    # a ToolsetUsageError out of the policy is the developer's and stops the run
    async def misuse(ctx: BetaURLContext, url: str) -> None:
        raise ToolsetContractError("wired wrong")

    with pytest.raises(ToolsetContractError, match="wired wrong"):
        await AsyncFakeBrowser(url_policy=misuse).call(CTX, "navigate", {"url": "https://example.com/"})


async def test_a_file_policy_that_fails_refuses_the_upload_on_the_async_class(tmp_path: Path) -> None:
    class Broken(BetaLocalFilePolicy):
        @override
        def resolve_upload_paths(self, context: Any, paths: Any) -> list[str]:
            raise OSError("disk on fire")

    # a generator does its work when the SDK reads it; a failure there fails closed the same way
    class LazyBroken(BetaLocalFilePolicy):
        @override
        def resolve_upload_paths(self, context: Any, paths: Any) -> Any:
            for path in paths:
                raise FileNotFoundError(path)
                yield path

    class Misused(BetaLocalFilePolicy):
        @override
        def resolve_upload_paths(self, context: Any, paths: Any) -> list[str]:
            raise ToolsetContractError("wired wrong")

    enable: Any = {"configs": {"file_upload": {"enabled": True}}, "confirm": approve}
    for policy in (Broken(upload_roots=[str(tmp_path)]), LazyBroken(upload_roots=[str(tmp_path)])):
        browser = AsyncFakeBrowser(file_policy=policy, **enable)

        with pytest.raises(ToolError) as caught:
            await browser.call(CTX, "file_upload", {**UPLOAD, "paths": [str(tmp_path / "a.pdf")]})

        assert texts(caught.value.content) == ["the file policy could not vet the upload"]
        assert browser.world.calls.count("file_upload") == 0

    # a ToolsetUsageError out of the policy is the developer's and stops the run
    misused = AsyncFakeBrowser(file_policy=Misused(upload_roots=[str(tmp_path)]), **enable)
    with pytest.raises(ToolsetContractError, match="wired wrong"):
        await misused.call(CTX, "file_upload", {**UPLOAD, "paths": [str(tmp_path / "a.pdf")]})
    assert misused.world.calls.count("file_upload") == 0


async def test_a_file_policy_hook_may_return_any_iterable_on_the_async_class() -> None:
    enable: Any = {"configs": {"file_upload": {"enabled": True}}, "confirm": approve}

    class Lazy(BetaLocalFilePolicy):
        @override
        def resolve_upload_documents(self, context: Any, document_ids: Any) -> Any:
            return (d for d in document_ids)  # a generator: read once, handed to the driver as a list

    browser = AsyncFakeBrowser(file_policy=Lazy(), **enable)
    assert texts(await browser.call(CTX, "file_upload", {**UPLOAD, "document_ids": ["doc_9"]})) == ["Uploaded."]
    assert browser.world.inputs[-1].document_ids == ["doc_9"]


async def test_download_paths_reach_the_model_only_through_an_exposing_file_policy_on_the_async_class() -> None:
    def completed(world: World) -> None:
        world.changes = [
            {
                "type": "download_completed",
                "download_id": "dl_1",
                "url": "https://example.com/a",
                "path": "/dl/x/a.bin",
            },
            {
                "type": "download_completed",
                "download_id": "dl_2",
                "url": "https://example.com/b",
                "path": "/elsewhere/b.bin",
            },
        ]

    async def paths(browser: AsyncFakeBrowser) -> list[str | None]:
        completed(browser.world)
        return [c.get("path") for c in state_block(await browser.call(CTX, "get_page_text", {}))["state_changes"]]

    assert await paths(AsyncFakeBrowser()) == [None, None]
    assert await paths(AsyncFakeBrowser(file_policy=BetaLocalFilePolicy(download_dir="/dl"))) == [None, None]
    assert await paths(
        AsyncFakeBrowser(file_policy=BetaLocalFilePolicy(download_dir="/dl", expose_download_paths=True))
    ) == ["/dl/x/a.bin", None]

    # A custom predicate that fails hides the path and the report still reaches the model.
    class Flaky(BetaLocalFilePolicy):
        @override
        def is_path_visible(self, path: str) -> bool:
            raise OSError("disk on fire")

    assert await paths(AsyncFakeBrowser(file_policy=Flaky(download_dir="/dl", expose_download_paths=True))) == [
        None,
        None,
    ]

    # An exposed path reaches the block exactly as the driver reported it, spaces and parentheses kept. A path with a
    # line break stays hidden, because folding it to one line would name a file the policy never checked. A path too
    # long for the policy to resolve on this filesystem stays hidden too, because the policy cannot vouch for it.
    exposing = AsyncFakeBrowser(file_policy=BetaLocalFilePolicy(download_dir="/dl", expose_download_paths=True))
    exposing.world.changes = [
        {"type": "download_completed", "download_id": "dl_3", "url": "https://example.com/c", "path": "/dl/x/c\n.bin"},
        {
            "type": "download_completed",
            "download_id": "dl_4",
            "url": "https://example.com/d",
            "path": "/dl/x/" + "d" * 5000,
        },
        {"type": "download_completed", "download_id": "dl_5", "url": "https://example.com/e", "path": "/dl/x/e.bin"},
        {
            "type": "download_completed",
            "download_id": "dl_6",
            "url": "https://example.com/f",
            "path": "/dl/my file (1).pdf",
        },
    ]
    changes = state_block(await exposing.call(CTX, "get_page_text", {}))["state_changes"]
    assert [(c["download_id"], c.get("path")) for c in changes] == [
        ("dl_3", None),
        ("dl_4", None),
        ("dl_5", "/dl/x/e.bin"),
        ("dl_6", "/dl/my file (1).pdf"),
    ]
