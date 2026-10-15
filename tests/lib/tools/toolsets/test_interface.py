# ruff: noqa: ARG001, ARG005 -- stub members and hooks ignore their arguments
"""Construction rules and the dispatch surface of the abstract browser toolset classes."""

from __future__ import annotations

from typing import Any, cast
from typing_extensions import override

import pytest

from anthropic.tools import (
    ToolError,
    ToolsetConfigError,
    ToolsetContractError,
)
from anthropic.types.beta import (
    BetaBrowserNavigateInput,
    BetaBrowserScreenshotInput,
    BetaBrowserGetPageTextInput,
)
from anthropic.tools.browser import (
    BetaBrowserState,
    BetaScreenshotResult,
    BetaToolsetCallContext,
    BetaBrowserNavigateResult,
    BetaAbstractBrowserToolset20260801,
    BetaAsyncAbstractBrowserToolset20260801,
)
from anthropic.lib._stainless_helpers import get_helper_tag

from ._fakes import approve

CTX = BetaToolsetCallContext()


class _Base(BetaAbstractBrowserToolset20260801):
    @override
    def _browser_state(self, context: BetaToolsetCallContext) -> BetaBrowserState:
        return BetaBrowserState(tabs=[])


class _AsyncBase(BetaAsyncAbstractBrowserToolset20260801):
    @override
    async def _browser_state(self, context: BetaToolsetCallContext) -> BetaBrowserState:
        return BetaBrowserState(tabs=[])


class TwoMembers(_Base):
    @override
    def navigate(self, context: BetaToolsetCallContext, input: BetaBrowserNavigateInput) -> BetaBrowserNavigateResult:
        return BetaBrowserNavigateResult(url=input.url, status=200, title="T")

    @override
    def screenshot(self, context: BetaToolsetCallContext, input: BetaBrowserScreenshotInput) -> BetaScreenshotResult:
        return BetaScreenshotResult(data="AAAA")


class AsyncTwoMembers(_AsyncBase):
    @override
    async def navigate(
        self, context: BetaToolsetCallContext, input: BetaBrowserNavigateInput
    ) -> BetaBrowserNavigateResult:
        return BetaBrowserNavigateResult(url=input.url, status=200, title="T")

    @override
    async def screenshot(
        self, context: BetaToolsetCallContext, input: BetaBrowserScreenshotInput
    ) -> BetaScreenshotResult:
        return BetaScreenshotResult(data="AAAA")


def _disabled(entry: Any) -> list[str]:
    configs = cast("dict[str, dict[str, object]]", entry.get("configs") or {})
    return sorted(name for name, config in configs.items() if (config or {}).get("enabled") is False)


def test_browser_state_is_abstract() -> None:
    # A driver that does not implement _browser_state cannot be constructed: the report is the model's only view of
    # the tabs, so a silently empty one would hide every driver bug behind a working-looking toolset.
    class NoState(BetaAbstractBrowserToolset20260801):
        pass

    with pytest.raises(TypeError, match="_browser_state"):
        NoState()  # pyright: ignore[reportAbstractUsage]


def test_unimplemented_members_are_sent_as_disabled_and_implemented_ones_left_to_the_api() -> None:
    entry: Any = TwoMembers().to_dict()
    assert entry["type"] == "browser_toolset_20260801"
    disabled = _disabled(entry)
    assert "navigate" not in disabled and "screenshot" not in disabled

    # Everything the subclass did not override is withheld, default-disabled members included.
    assert len(disabled) == 29 and "left_click" in disabled and "javascript_exec" in disabled

    # Nothing SDK-side leaks into the entry.
    assert set(entry) == {"type", "configs"}
    assert all(set(config) == {"enabled"} for config in entry["configs"].values())


def test_the_callers_configs_pass_through_untouched_and_are_copied() -> None:
    configs: Any = {"navigate": {"defer_loading": True}, "javascript_exec": {"enabled": False, "defer_loading": True}}
    browser = TwoMembers(configs=configs)
    entry: Any = browser.to_dict()
    assert entry["configs"]["navigate"] == {"defer_loading": True}
    assert entry["configs"]["javascript_exec"] == {"enabled": False, "defer_loading": True}

    # Enabling a member the subclass does not implement would offer the model something that can only
    # answer "not available": refused at construction.
    with pytest.raises(ToolsetConfigError, match="does not implement"):
        TwoMembers(configs={"javascript_exec": {"enabled": True}})

    configs["navigate"]["enabled"] = False
    assert browser.to_dict()["configs"]["navigate"] == {"defer_loading": True}  # pyright: ignore[reportTypedDictNotRequiredAccess, reportOptionalSubscript]
    assert browser.to_dict() is not browser.to_dict()


def test_an_execute_only_subclass_serves_every_member_and_turns_members_off_with_configs() -> None:
    class Forwarder(_Base):
        @override
        def execute(self, context: BetaToolsetCallContext, name: Any, input: Any) -> Any:
            return f"forwarded {name}"

    # A class that overrides execute serves every member, whether or not it also implements member methods: the SDK
    # cannot tell which members the override answers, so it offers them all (the wire entry disables nothing) and the
    # driver turns off what it does not serve through configs.
    entry = Forwarder().to_dict()
    assert _disabled(entry) == []
    trimmed = Forwarder(configs={"screenshot": {"enabled": False}, "zoom": {"enabled": False}}).to_dict()
    assert _disabled(trimmed) == ["screenshot", "zoom"]

    # A subclass that only overrides member methods serves only those.
    assert "zoom" in _disabled(TwoMembers().to_dict())

    # One that adds hooks around super().execute also serves every member: a member it implements runs, one it does
    # not answers from its default body inside super().execute, and configs turns off the rest.
    class Hooked(TwoMembers):
        @override
        def execute(self, context: BetaToolsetCallContext, name: Any, input: Any) -> Any:
            return super().execute(context, name, input)

    assert _disabled(Hooked().to_dict()) == []
    assert Hooked().execute(CTX, "navigate", BetaBrowserNavigateInput(url="https://example.com/")).status == 200
    with pytest.raises(ToolError, match="not available"):
        Hooked().execute(CTX, "zoom", cast(Any, {"region": [0, 0, 1, 1]}))
    assert _disabled(Hooked(configs={"zoom": {"enabled": False}}).to_dict()) == ["zoom"]


def test_a_null_configs_entry_leaves_the_member_at_its_defaults_and_goes_to_the_api_as_given() -> None:
    # The wire type spells "this member's defaults" as null as well as by leaving the key out.
    entry = cast(Any, TwoMembers(configs={"navigate": None, "screenshot": None}).to_dict())
    assert entry["configs"]["navigate"] is None and "navigate" not in _disabled(entry)
    assert TwoMembers(configs={"navigate": None}).call(CTX, "navigate", {"url": "https://example.com/"})
    # (an entry that is not a mapping, or an unknown member key, is the type checker's to catch)


def test_configs_are_gated_on_the_copy_that_is_sent() -> None:
    # A mapping that answers one thing to a lookup and another when copied cannot leave a member on that reads as
    # off: the dispatch gate reads the plain copy the wire entry carries, and an `enabled` the types do not allow
    # fails closed there (anything but True or None reads as off) rather than being re-checked at construction.
    class Shifty(dict[str, object]):
        @override
        def get(self, key: str, default: object = None) -> object:
            return False if key == "enabled" else super().get(key, default)

    shifty = TwoMembers(configs=cast(Any, {"navigate": Shifty(enabled="no")}))
    assert cast(Any, shifty.to_dict())["configs"]["navigate"] == {"enabled": "no"}  # what the API is told (and rejects)

    with pytest.raises(ToolError, match="not permitted"):
        shifty.call(CTX, "navigate", {"url": "https://example.com/"})

    off = cast(Any, TwoMembers(configs=cast(Any, {"navigate": Shifty(enabled=False)})).to_dict())
    assert off["configs"]["navigate"] == {"enabled": False} and type(off["configs"]["navigate"]) is dict

    # an entry that is not a mapping at all fails loudly rather than collapsing to {} (member left on)
    with pytest.raises(TypeError):
        TwoMembers(configs=cast(Any, {"navigate": []}))

    # a mapping that claims to be empty but iterates entries is read by its entries, not its truthiness
    class Sly(dict[str, object]):
        @override
        def __len__(self) -> int:
            return 0

    sly = cast(Any, TwoMembers(configs=cast(Any, Sly(navigate={"enabled": False}))).to_dict())
    assert sly["configs"]["navigate"] == {"enabled": False}


def test_url_policy_is_a_callable_or_unset() -> None:
    def policy(ctx: object, url: str) -> None:
        return None

    TwoMembers(url_policy=policy)
    TwoMembers()

    # (what url_policy, confirm, file_policy and tool_configs take is the type checker's to enforce)


def test_tool_configs_go_onto_the_entry_and_the_helper_tag_does_not() -> None:
    given: Any = {"cache_control": {"type": "ephemeral"}}
    browser = TwoMembers(tool_configs=given)
    assert browser.to_dict().get("cache_control") == {"type": "ephemeral"}
    assert get_helper_tag(browser) == "browser-toolset"
    assert "browser-toolset" not in str(browser.to_dict())

    # copied at construction and per call: nothing done to the dicts afterwards reaches the entry
    given["cache_control"]["type"] = "changed"
    cast(Any, browser.to_dict())["cache_control"]["ttl"] = "1h"
    assert browser.to_dict().get("cache_control") == {"type": "ephemeral"}

    with pytest.raises(ToolsetConfigError, match="tool_configs cannot set 'configs'; pass configs= instead"):
        TwoMembers(tool_configs=cast(Any, {"configs": {"navigate": {"enabled": False}}}))

    assert (
        TwoMembers(tool_configs=cast(Any, {"type": "browser_toolset_20990101"})).to_dict()["type"]
        == "browser_toolset_20260801"
    )


def test_execute_dispatches_to_the_member_method_and_refuses_unknown_names() -> None:
    browser = TwoMembers()
    result = browser.execute(CTX, "navigate", BetaBrowserNavigateInput(url="https://example.com/"))
    assert result == BetaBrowserNavigateResult(url="https://example.com/", status=200, title="T")

    with pytest.raises(ToolError) as unknown:
        browser.execute(CTX, "__init__", BetaBrowserNavigateInput(url="x"))  # pyright: ignore[reportArgumentType]
    assert str(unknown.value) == "Error: unknown browser toolset member '__init__'"

    # A member the subclass did not implement answers the model rather than raising into the runner.
    with pytest.raises(ToolError) as unavailable:
        browser.execute(CTX, "get_page_text", BetaBrowserGetPageTextInput())
    assert str(unavailable.value) == "The browser toolset member 'get_page_text' is not available in this environment."


def test_unknown_member_name_is_sanitised_in_the_refusal() -> None:
    with pytest.raises(ToolError) as caught:
        TwoMembers().execute(CTX, "x'\n\u202eevil", BetaBrowserNavigateInput(url="x"))  # pyright: ignore[reportArgumentType]
    assert str(caught.value) == "Error: unknown browser toolset member 'x evil'"  # one line, no quote, runs collapsed


def test_an_async_member_on_the_sync_class_is_a_contract_error() -> None:
    class Mixed(_Base):
        @override
        async def navigate(  # pyright: ignore[reportIncompatibleMethodOverride]
            self, context: BetaToolsetCallContext, input: BetaBrowserNavigateInput
        ) -> BetaBrowserNavigateResult:
            return BetaBrowserNavigateResult(url=input.url)

    # reported when the toolset is built, before any call
    with pytest.raises(ToolsetContractError, match="browser member 'navigate' is async on the synchronous toolset"):
        Mixed()


async def test_async_execute_awaits_async_members_and_a_sync_one_is_a_contract_error() -> None:
    class Navigates(_AsyncBase):
        @override
        async def navigate(
            self, context: BetaToolsetCallContext, input: BetaBrowserNavigateInput
        ) -> BetaBrowserNavigateResult:
            return BetaBrowserNavigateResult(url=input.url)

    browser = Navigates()
    assert await browser.execute(CTX, "navigate", BetaBrowserNavigateInput(url="u")) == BetaBrowserNavigateResult(
        url="u"
    )

    class SyncMember(Navigates):
        @override
        def get_page_text(self, context: BetaToolsetCallContext, input: BetaBrowserGetPageTextInput) -> str:  # pyright: ignore[reportIncompatibleMethodOverride]
            return "text"

    # a member written sync on the async class is a wiring mistake, reported when the toolset is built rather than
    # run on the event loop
    with pytest.raises(
        ToolsetContractError, match="browser member 'get_page_text' is sync on the asynchronous toolset"
    ):
        SyncMember()


def test_override_detection_sees_dynamic_assignment_and_intermediate_classes() -> None:
    class Middle(TwoMembers):
        pass

    class Leaf(Middle):
        @override
        def get_page_text(self, context: BetaToolsetCallContext, input: BetaBrowserGetPageTextInput) -> str:
            return "t"

    disabled = _disabled(Leaf().to_dict())
    assert {"navigate", "screenshot", "get_page_text"}.isdisjoint(disabled)

    def wait(self: Any, context: Any, input: Any) -> None:
        return None

    Patched = type("Patched", (TwoMembers,), {"wait": wait})
    assert "wait" not in _disabled(Patched().to_dict())


def test_options_do_not_leak_into_the_entry() -> None:
    entry = TwoMembers(confirm=approve, url_policy=lambda ctx, url: None).to_dict()
    assert set(entry) == {"type", "configs"}


def test_configs_is_a_read_only_copy_of_what_to_dict_sends() -> None:
    class AsyncOne(_AsyncBase):
        @override
        async def navigate(
            self, context: BetaToolsetCallContext, input: BetaBrowserNavigateInput
        ) -> BetaBrowserNavigateResult:
            return BetaBrowserNavigateResult(url=input.url)

    for browser in (TwoMembers(configs={"javascript_exec": {"enabled": False}}), AsyncOne()):
        configs: Any = browser.configs
        assert configs is not None and configs == cast(Any, browser.to_dict())["configs"]
        assert configs["left_click"] == {"enabled": False}  # not implemented, so withheld from the model
        configs["left_click"] = {"enabled": True}  # a copy: nothing the toolset holds changes
        assert cast(Any, browser.configs)["left_click"] == {"enabled": False}
        assert browser.configs is not browser.configs
        with pytest.raises(AttributeError):
            browser.configs = {}  # pyright: ignore[reportAttributeAccessIssue]


def test_async_unimplemented_members_are_sent_as_disabled_and_implemented_ones_left_to_the_api() -> None:
    entry: Any = AsyncTwoMembers().to_dict()
    assert entry["type"] == "browser_toolset_20260801"
    disabled = _disabled(entry)
    assert "navigate" not in disabled and "screenshot" not in disabled

    # Everything the subclass did not override is withheld, default-disabled members included.
    assert len(disabled) == 29 and "left_click" in disabled and "javascript_exec" in disabled

    # Nothing SDK-side leaks into the entry.
    assert set(entry) == {"type", "configs"}
    assert all(set(config) == {"enabled"} for config in entry["configs"].values())


async def test_async_execute_dispatches_to_the_member_method_and_refuses_unknown_names() -> None:
    browser = AsyncTwoMembers()
    result = await browser.execute(CTX, "navigate", BetaBrowserNavigateInput(url="https://example.com/"))
    assert result == BetaBrowserNavigateResult(url="https://example.com/", status=200, title="T")

    with pytest.raises(ToolError) as unknown:
        await browser.execute(CTX, "__init__", BetaBrowserNavigateInput(url="x"))  # pyright: ignore[reportArgumentType]
    assert str(unknown.value) == "Error: unknown browser toolset member '__init__'"

    # A member the subclass did not implement answers the model rather than raising into the runner.
    with pytest.raises(ToolError) as unavailable:
        await browser.execute(CTX, "get_page_text", BetaBrowserGetPageTextInput())
    assert str(unavailable.value) == "The browser toolset member 'get_page_text' is not available in this environment."


async def test_async_unknown_member_name_is_sanitised_in_the_refusal() -> None:
    with pytest.raises(ToolError) as caught:
        await AsyncTwoMembers().execute(CTX, "x'\n\u202eevil", BetaBrowserNavigateInput(url="x"))  # pyright: ignore[reportArgumentType]
    assert str(caught.value) == "Error: unknown browser toolset member 'x evil'"


async def test_an_async_execute_override_serves_every_member_and_turns_members_off_with_configs() -> None:
    class Forwarder(_AsyncBase):
        @override
        async def execute(self, context: BetaToolsetCallContext, name: Any, input: Any) -> Any:
            return f"forwarded {name}"

    # A class that overrides execute serves every member, so the wire entry disables nothing and the driver turns off
    # what it does not serve through configs.
    assert _disabled(Forwarder().to_dict()) == []
    trimmed = Forwarder(configs={"screenshot": {"enabled": False}, "zoom": {"enabled": False}}).to_dict()
    assert _disabled(trimmed) == ["screenshot", "zoom"]
    # A subclass that only overrides member methods serves only those.
    assert "zoom" in _disabled(AsyncTwoMembers().to_dict())

    # One that adds hooks around super().execute also serves every member: a member it implements runs, one it does
    # not answers from its default body inside super().execute, and configs turns off the rest.
    class Hooked(AsyncTwoMembers):
        @override
        async def execute(self, context: BetaToolsetCallContext, name: Any, input: Any) -> Any:
            return await super().execute(context, name, input)

    assert _disabled(Hooked().to_dict()) == []
    assert (await Hooked().execute(CTX, "navigate", BetaBrowserNavigateInput(url="https://example.com/"))).status == 200
    with pytest.raises(ToolError, match="not available"):
        await Hooked().execute(CTX, "zoom", cast(Any, {"region": [0, 0, 1, 1]}))
    assert _disabled(Hooked(configs={"zoom": {"enabled": False}}).to_dict()) == ["zoom"]
