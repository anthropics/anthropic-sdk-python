# ruff: noqa: ARG001 -- stub hooks ignore their arguments
"""The SDK's own refusals are `ToolError` subclasses: each site raises its class, the model reads the same text as
ever, and the `ToolError` that `call` raises names the refusal as its cause."""

from __future__ import annotations

from typing import Any, cast
from pathlib import Path
from typing_extensions import override

import pytest

from anthropic.tools import (
    ToolError,
    ConfirmFailedError,
    UnknownMemberError,
    DisabledMemberError,
    ConfirmDeclinedError,
    UnavailableMemberError,
    InvalidMemberInputError,
)
from anthropic.tools.browser import (
    BetaURLContext,
    URLRefusedError,
    BetaConfirmContext,
    UploadRefusedError,
    BetaLocalFilePolicy,
    BetaToolsetCallContext,
    beta_check_upload_path,
)

from ._fakes import CLICK, UPLOAD, FakeBrowser, AsyncFakeBrowser, texts, approve

CTX = BetaToolsetCallContext()


async def _async_refusal(browser: AsyncFakeBrowser, name: str, input: Any) -> ToolError:
    """The same as `_refusal`, for a call on the async class."""
    with pytest.raises(ToolError) as caught:
        await browser.call(CTX, name, input)
    cause = caught.value.__cause__
    assert isinstance(cause, ToolError)
    assert texts(caught.value.content)[0] == str(cause)
    return cause


def _refusal(browser: FakeBrowser, name: str, input: Any) -> ToolError:
    """The refusal behind the `ToolError` a call raises: its cause, whose own text is what the model reads."""
    with pytest.raises(ToolError) as caught:
        browser.call(CTX, name, input)
    cause = caught.value.__cause__
    assert isinstance(cause, ToolError)
    assert texts(caught.value.content)[0] == str(cause)
    return cause


def test_member_resolution_and_input_refusals() -> None:
    browser = FakeBrowser(configs={"scroll": {"enabled": False}})

    unknown = _refusal(browser, "teleport", {})
    assert isinstance(unknown, UnknownMemberError)
    assert str(unknown) == "Error: unknown browser toolset member 'teleport'"

    disabled = _refusal(browser, "scroll", {"scroll_direction": "down", **CLICK})
    assert isinstance(disabled, DisabledMemberError)
    assert str(disabled) == (
        "The 'scroll' action is not permitted by this application's permissions and cannot be used in this session."
    )

    unavailable = _refusal(browser, "hover", CLICK)  # the fake does not implement hover
    assert isinstance(unavailable, UnavailableMemberError)
    assert str(unavailable) == "The browser toolset member 'hover' is not available in this environment."

    invalid = _refusal(browser, "left_click", {})
    assert isinstance(invalid, InvalidMemberInputError)
    assert str(invalid).startswith("invalid input for browser member 'left_click': target: ")
    assert str(InvalidMemberInputError("wait", "duration: too long", family="browser")) == (
        "invalid input for browser member 'wait': duration: too long"
    )
    # family has no default, so none of the three can fall back to the browser's wording
    for refusal, args in (
        (UnknownMemberError, ("x",)),
        (UnavailableMemberError, ("x",)),
        (InvalidMemberInputError, ("x", "y")),
    ):
        with pytest.raises(TypeError):
            cast(Any, refusal)(*args)

    assert browser.world.calls == []


def test_url_refusals() -> None:
    def no_logout(context: BetaURLContext, url: str) -> None:
        if "logout" in url:
            raise ToolError("blocked: logout")

    browser = FakeBrowser(url_policy=no_logout)
    own = _refusal(browser, "navigate", {"url": "https://example.com/logout"})
    assert type(own) is ToolError and str(own) == "blocked: logout"  # the policy's own ToolError, as raised

    # a custom policy that raised something other than a ToolError refused too, with the SDK's text
    def broken(context: BetaURLContext, url: str) -> None:
        raise RuntimeError(url)

    fallback = _refusal(FakeBrowser(url_policy=broken), "navigate", {"url": "https://example.com/"})
    assert isinstance(fallback, URLRefusedError) and str(fallback) == "refused by the URL policy"

    # the reason is one bounded line
    assert str(URLRefusedError("blocked: " + "x" * 500)) == ("blocked: " + "x" * 500)[:200]

    assert browser.world.calls == []


def test_confirm_refusals() -> None:
    def deny(context: BetaConfirmContext) -> bool:
        return False

    declined = _refusal(FakeBrowser(confirm=deny), "left_click", CLICK)
    assert isinstance(declined, ConfirmDeclinedError)
    assert str(declined) == (
        "The user did not grant permission to run 'left_click'. Do not retry it unless the user asks you to."
    )

    def broken(context: BetaConfirmContext) -> bool:
        raise RuntimeError("tty closed")

    failed = _refusal(FakeBrowser(confirm=broken), "left_click", CLICK)
    assert isinstance(failed, ConfirmFailedError)
    assert str(failed) == (
        "Permission to run 'left_click' could not be obtained (the confirmation prompt failed). "
        "Do not retry it unless the user asks you to."
    )


def test_a_hook_refusal_is_cut_to_the_field_limit_and_stays_the_cause() -> None:
    def echo(context: BetaURLContext, url: str) -> None:
        raise ToolError(f"blocked: {url}")

    def refuse(context: BetaConfirmContext) -> bool:
        raise ToolError("declined: " + "c" * 5000)

    url = "https://example.com/" + "a" * 5000
    cases: list[tuple[FakeBrowser, str, Any, str]] = [
        (FakeBrowser(url_policy=echo), "navigate", {"url": url}, f"blocked: {url}"),
        (FakeBrowser(confirm=refuse), "left_click", CLICK, "declined: " + "c" * 5000),
    ]
    for browser, name, input, text in cases:
        with pytest.raises(ToolError) as caught:
            browser.call(CTX, name, input)
        assert texts(caught.value.content)[0] == text[:4096]
        assert str(caught.value.__cause__) == text  # the refusal as raised, uncut


def test_upload_refusals(tmp_path: Path) -> None:
    root = tmp_path / "uploads"
    root.mkdir()
    (root / "form.pdf").write_text("x")
    enable: Any = {"configs": {"file_upload": {"enabled": True}}, "confirm": approve}
    bare = FakeBrowser(**enable)

    no_roots = _refusal(bare, "file_upload", {**UPLOAD, "paths": [str(root / "form.pdf")]})
    assert isinstance(no_roots, UploadRefusedError) and str(no_roots) == "file_upload has no configured upload roots"

    no_documents = _refusal(bare, "file_upload", {**UPLOAD, "document_ids": ["doc_1"]})
    assert isinstance(no_documents, UploadRefusedError)

    policy = BetaLocalFilePolicy(upload_roots=[str(root)], upload_document_ids=["doc_1"])
    browser = FakeBrowser(file_policy=policy, **enable)

    outside = _refusal(browser, "file_upload", {**UPLOAD, "paths": [str(tmp_path / "secret")]})
    assert isinstance(outside, UploadRefusedError)
    assert str(outside) == "file_upload path is outside the configured upload roots"

    unlisted = _refusal(browser, "file_upload", {**UPLOAD, "document_ids": ["doc_2"]})
    assert isinstance(unlisted, UploadRefusedError) and str(unlisted) == "document not in the upload allowlist"

    class Crashing(BetaLocalFilePolicy):
        @override
        def resolve_upload_paths(self, context: Any, paths: Any) -> list[str]:
            raise RuntimeError(paths)

    crashed = _refusal(FakeBrowser(file_policy=Crashing(), **enable), "file_upload", {**UPLOAD, "paths": ["/f"]})
    assert isinstance(crashed, UploadRefusedError)
    assert str(crashed) == "the file policy could not vet the upload"

    with pytest.raises(UploadRefusedError, match="outside the configured upload roots"):
        beta_check_upload_path(str(tmp_path / "secret"), [str(root)])

    assert bare.world.calls == [] and browser.world.calls == []


async def test_the_async_class_names_its_refusals_the_same_way() -> None:
    def broken(context: BetaURLContext, url: str) -> None:
        raise RuntimeError(url)

    browser = AsyncFakeBrowser(url_policy=broken)

    with pytest.raises(ToolError) as caught:
        await browser.call(CTX, "navigate", {"url": "http://10.0.0.5/"})
    assert isinstance(caught.value.__cause__, URLRefusedError)

    def echo(context: BetaURLContext, url: str) -> None:
        raise ToolError(f"blocked: {url}")

    url = "https://example.com/" + "a" * 5000
    with pytest.raises(ToolError) as cut:
        await AsyncFakeBrowser(url_policy=echo).call(CTX, "navigate", {"url": url})
    assert texts(cut.value.content)[0] == f"blocked: {url}"[:4096] and str(cut.value.__cause__) == f"blocked: {url}"


async def test_the_async_class_names_its_confirm_refusals_the_same_way() -> None:
    async def deny(context: BetaConfirmContext) -> bool:
        return False

    declined = await _async_refusal(AsyncFakeBrowser(confirm=deny), "left_click", CLICK)
    assert isinstance(declined, ConfirmDeclinedError)
    assert (
        str(declined)
        == "The user did not grant permission to run 'left_click'. Do not retry it unless the user asks you to."
    )

    async def broken(context: BetaConfirmContext) -> bool:
        raise RuntimeError("tty closed")

    failed = await _async_refusal(AsyncFakeBrowser(confirm=broken), "left_click", CLICK)
    assert isinstance(failed, ConfirmFailedError)
    assert str(failed) == (
        "Permission to run 'left_click' could not be obtained (the confirmation prompt failed). "
        "Do not retry it unless the user asks you to."
    )


async def test_the_async_class_names_its_upload_refusals_the_same_way(tmp_path: Path) -> None:
    enable: Any = {"configs": {"file_upload": {"enabled": True}}, "confirm": approve}
    bare = AsyncFakeBrowser(**enable)
    no_roots = await _async_refusal(bare, "file_upload", {**UPLOAD, "paths": [str(tmp_path / "form.pdf")]})
    assert isinstance(no_roots, UploadRefusedError) and str(no_roots) == "file_upload has no configured upload roots"

    class Crashing(BetaLocalFilePolicy):
        @override
        def resolve_upload_paths(self, context: Any, paths: Any) -> list[str]:
            raise RuntimeError(paths)

    crashed = await _async_refusal(
        AsyncFakeBrowser(file_policy=Crashing(), **enable), "file_upload", {**UPLOAD, "paths": ["/f"]}
    )
    assert isinstance(crashed, UploadRefusedError)
    assert str(crashed) == "the file policy could not vet the upload"

    policy = BetaLocalFilePolicy(upload_roots=[str(tmp_path / "uploads")], upload_document_ids=["doc_1"])
    browser = AsyncFakeBrowser(file_policy=policy, **enable)
    outside = await _async_refusal(browser, "file_upload", {**UPLOAD, "paths": [str(tmp_path / "secret")]})
    assert isinstance(outside, UploadRefusedError)
    assert str(outside) == "file_upload path is outside the configured upload roots"

    unlisted = await _async_refusal(browser, "file_upload", {**UPLOAD, "document_ids": ["doc_2"]})
    assert isinstance(unlisted, UploadRefusedError) and str(unlisted) == "document not in the upload allowlist"
    assert bare.world.calls == [] and browser.world.calls == []
