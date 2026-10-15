"""What the toolset families share: the member registry, the options resolved at construction, the stages of a
member call that every family runs, and the serialized sync and async call loops.

A family module (`_browser`, `_computer`) supplies its registry and its two abstract classes; the pipeline stages
that are its own (the browser's URL and file policies, its state report) sit beside them in its own modules.
"""

from __future__ import annotations

import copy
import inspect
import functools
import threading
from abc import abstractmethod
from typing import Any, Generic, TypeVar, ClassVar, cast
from collections.abc import Mapping, Callable, Iterable, Sequence
from typing_extensions import Literal, TypeAlias, TypedDict, final, get_args, override

import anyio
import pydantic

from ._errors import (
    ConfirmFailedError,
    ToolsetConfigError,
    UnknownMemberError,
    DisabledMemberError,
    ConfirmDeclinedError,
    ToolsetContractError,
    UnavailableMemberError,
    InvalidMemberInputError,
)
from ._runnable import (
    ToolsetFamily,
    BetaToolsetContent,
    BaseRunnableToolset,
    BetaRunnableToolset,
    BetaToolsetCallContext,
    BetaAsyncRunnableToolset,
    hook_refusal,
)
from ._sanitize import FIELD_MAX, error_text_content
from ...._compat import field_outer_type, get_model_fields
from ...._models import BaseModel, GenericModel, validate_type
from ....types.beta import BetaTextBlockParam, BetaCacheControlEphemeralParam
from .._beta_functions import ToolError
from ..._stainless_helpers import StainlessHelperHeaderValue, tag_helper

__all__ = [
    "BetaToolConfigs",
    "BetaScreenshotResult",
    "ResultKind",
    "Member",
    "Registry",
    "BaseToolsetOptions",
    "BaseToolset",
    "BaseSyncToolset",
    "BaseAsyncToolset",
    "NestedCallError",
    "AsyncOnSyncToolsetError",
    "SyncOnAsyncToolsetError",
    "check_sync_hook",
    "members_from_union",
    "overridden",
    "build_wire_configs",
    "parse_input",
    "input_problem",
    "confirm_outcome",
    "error_content",
    "checked_error",
    "bounded_error",
]

_NameT = TypeVar("_NameT", bound=str, covariant=True)
_InputT = TypeVar("_InputT", bound=BaseModel, covariant=True)
_ConfirmT = TypeVar("_ConfirmT", bound="Callable[..., object]")

ABSENT = object()


class BetaToolConfigs(TypedDict, total=False):
    """Fields set on the toolset's `tools[]` entry itself rather than on a member."""

    cache_control: BetaCacheControlEphemeralParam | None


class BetaScreenshotResult(BaseModel):
    """A screenshot or zoom image from a browser or computer toolset, rendered as one image block. The image must
    already fit the model's image limits: the API rejects an oversized one rather than scaling it down."""

    data: str
    """Base64 image bytes, without a `data:` prefix."""

    media_type: Literal["image/png", "image/jpeg", "image/gif", "image/webp"] = "image/png"


ResultKind: TypeAlias = Literal["navigate", "screenshot", "point", "text", "tab", "tabs", "none"]
"""What a member returns: a navigation result, a screenshot, a cursor position, a string, one tab entry, the tab
list, or nothing (a pure action, rendered from its confirmation template followed by the one line of text it may
return)."""


class Member(GenericModel, Generic[_NameT, _InputT]):
    """One member of a toolset: the model its `tool_use.input` is parsed into, its result kind, the confirmation the
    model reads after a pure action (`{field}` placeholders are filled from the input, `{ref}` reads the browser's
    `target.ref`, and a line the action returned follows it), and whether it is on by default."""

    name: _NameT
    input: type[_InputT]
    result: ResultKind
    text: str | None = None
    enabled_by_default: bool = True


class Registry(Generic[_NameT, _InputT]):
    """One family's members by name, in the API's order, with what the family is called on the wire."""

    def __init__(
        self,
        *,
        family: ToolsetFamily,
        helper_tag: StainlessHelperHeaderValue,
        members: Mapping[str, Member[_NameT, _InputT]],
    ) -> None:
        self.family: ToolsetFamily = family
        self.helper_tag: StainlessHelperHeaderValue = helper_tag
        """The `x-stainless-helper` value a toolset of this family sends."""
        self.members = members
        self.names: list[_NameT] = [member.name for member in members.values()]
        self.default_disabled: frozenset[str] = frozenset(
            name for name, member in members.items() if not member.enabled_by_default
        )
        """Members the API withholds unless `configs` enables them."""

    def member_enabled(self, name: str, configs: Mapping[str, object] | None) -> bool:
        """Whether `configs` leave `name` enabled, failing closed when the answer is unclear.

        Only a real boolean `enabled` turns a member on or off. Any other value fails closed, so a
        malformed entry can never turn on a member that is off by default.
        """
        entry = configs.get(name) if configs else None
        if isinstance(entry, Mapping):
            enabled: object = entry.get("enabled")  # pyright: ignore[reportUnknownMemberType, reportUnknownVariableType]
            if enabled is True:
                return True
            if enabled is not None:
                return False
        elif entry is not None:
            return False  # an entry that is neither a mapping nor None (`{"navigate": False}`) reads as off, not as default
        return name not in self.default_disabled


class NestedCallError(ToolsetContractError):
    def __init__(self) -> None:
        super().__init__(
            "call() was invoked from inside a member; a member that composes other members calls their methods directly"
        )


class AsyncOnSyncToolsetError(ToolsetContractError):
    def __init__(self, what: str, *, twin: str) -> None:
        super().__init__(f"{what} is async on the synchronous toolset; define it with def, or subclass {twin}")


class SyncOnAsyncToolsetError(ToolsetContractError):
    def __init__(self, what: str, *, twin: str) -> None:
        super().__init__(f"{what} is sync on the asynchronous toolset; define it with async def, or subclass {twin}")


class BaseToolsetOptions(Generic[_NameT, _InputT, _ConfirmT]):
    """The constructor options every family has, validated and resolved once at construction. A mistake in them
    raises `ToolsetConfigError` here, and a member, an `execute` or a `confirm` written for the other flavour
    (`async def` on the synchronous class, a plain `def` member on the asynchronous one) raises
    `ToolsetContractError`.

    - `wire_configs` is what the `tools[]` entry sends: the caller's `configs` plus `enabled: false` for every member
      `cls` does not serve.
    - `served` is the members a sampled call may reach (the implemented ones, or all of them for a class that
      overrides `execute`).
    - `configured` is the members present in the caller's own `configs`.

    A family with more options subclasses this and validates them after `super().__init__`."""

    def __init__(
        self,
        cls: type[BaseToolset[Any, Any, Any]],
        *,
        registry: Registry[_NameT, _InputT],
        default_bodies: frozenset[object],
        configs: Mapping[str, object] | None,
        confirm: _ConfirmT | None,
        tool_configs: BetaToolConfigs | None,
        family_methods: Sequence[str] = (),
    ) -> None:
        self.registry = registry
        implemented = overridden(cls, registry.names, default_bodies)
        check_flavour(cls, [*sorted(implemented), "execute", *family_methods], registry=registry)
        self.served = frozenset(registry.names) if overridden(cls, ["execute"], default_bodies) else implemented
        self.wire_configs = build_wire_configs(configs, self.served, registry.names)
        self.configured = frozenset(() if configs is None else configs)

        if confirm is not None:
            check_sync_hook(cls, "confirm", confirm)
        self.confirm = confirm

        if "configs" in (tool_configs or {}):
            raise ToolsetConfigError("tool_configs cannot set 'configs'; pass configs= instead")
        self.tool_configs: Mapping[str, object] = copy.deepcopy(dict(tool_configs or {}))

    def is_enabled(self, name: str) -> bool:
        """Whether the member is offered to the model and may be dispatched."""
        return self.registry.member_enabled(name, self.wire_configs)

    def resolve(self, name: str) -> Member[_NameT, _InputT]:
        """Stage one of a call: the registry row for `name`, or the refusal the model reads (an
        unknown name, a member this application disabled, or one the driver does not implement)."""
        member = self.registry.members.get(name)
        if member is None:
            raise UnknownMemberError(name, family=self.registry.family)
        if not self.is_enabled(member.name):
            if member.name not in self.served and member.name not in self.configured:
                raise UnavailableMemberError(member.name, family=self.registry.family)
            raise DisabledMemberError(member.name)
        return member


class BaseToolset(BaseRunnableToolset, Generic[_NameT, _InputT, _ConfirmT]):
    """What every toolset class shares below its family: the options resolved at construction and the registry
    lookup that keeps model output away from the instance's other attributes."""

    _toolset_twin: ClassVar[str]
    """The name of the class with the other calling convention (the async class's sync twin and vice versa), for the
    contract error that tells a driver which class its `def` or `async def` members belong on."""

    def __init__(self, options: BaseToolsetOptions[_NameT, _InputT, _ConfirmT]) -> None:
        self._toolset_options = options
        tag_helper(self, options.registry.helper_tag)

    def _toolset_member_method(self, name: str) -> Callable[..., Any]:
        """Resolve `name` through the registry before touching the instance: `getattr(self, name)`
        on raw model output would reach `__init__` or any other attribute."""
        if name not in self._toolset_options.registry.members:
            raise UnknownMemberError(name, family=self._toolset_options.registry.family)
        method: Callable[..., Any] = getattr(self, name)
        return method


class BaseSyncToolset(BaseToolset[_NameT, _InputT, _ConfirmT], BetaRunnableToolset):
    """The synchronous call loop: member calls run one at a time, `close` waits for the calls in flight, and the
    family's `_toolset_run` does the work of one call under the lock."""

    def __init__(self, options: BaseToolsetOptions[_NameT, _InputT, _ConfirmT]) -> None:
        super().__init__(options)

        # One member call runs at a time: `__lock` serialises them, and `__lock_holder` records the thread inside it
        # so a nested `call()` or a `close()` from within a member is recognised.
        self.__lock = threading.Lock()
        self.__lock_holder: int | None = None

        # `close()` waits on `__settled` until `__pending` (the calls accepted and not yet finished, running or queued)
        # drops to zero.
        self.__pending = 0
        self.__settled = threading.Condition()

    @final
    @override
    def call(self, context: BetaToolsetCallContext, name: str, input: Mapping[str, object]) -> BetaToolsetContent:
        """The entry point the tool runner and `tool_result` use: runs one member call through the
        pipeline and returns its `tool_result` content.

        A refusal or failure is raised as a `ToolError` that carries the `tool_result` content. Its `__cause__` is the
        specific refusal (`DisabledMemberError`, …) or, when a member raised something other than `ToolError`, the
        `ToolError` that wraps it.

        Calls run one at a time (no order promised).

        Not an extension point (override `execute` or a member method) and not for use from inside a member: a member
        that composes others calls their methods directly."""
        if self.__lock_holder == threading.get_ident():
            raise NestedCallError()

        with self.__settled:
            self._toolset_refuse_if_closed()
            self.__pending += 1

        try:
            with self.__lock:
                self.__lock_holder = threading.get_ident()
                try:
                    return self._toolset_run(context, name, input)
                finally:
                    self.__lock_holder = None
        finally:
            with self.__settled:
                self.__pending -= 1
                if not self.__pending:
                    self.__settled.notify_all()

    @override
    def close(self) -> None:
        """Release what the toolset holds when you are done. The tool runner never calls this, so one instance can
        serve several runs, and a `with` block calls it for you.

        Marks the toolset closed (a call that arrives afterwards raises `ToolsetClosedError`), then waits for the
        calls already accepted, in flight or queued, to settle, so an override that calls `super().close()` first
        tears the backend down with nothing still using it.

        Called from inside a member, `close` returns without waiting: that member's own call is the one in flight."""
        super().close()

        if self.__lock_holder == threading.get_ident():
            return  # the caller is the call in flight

        with self.__settled:
            while self.__pending:
                self.__settled.wait()

    @abstractmethod
    def _toolset_run(
        self, context: BetaToolsetCallContext, name: str, input: Mapping[str, object]
    ) -> BetaToolsetContent:
        """One member call, under the lock: the family's pipeline from the raw `tool_use.input` to the content."""
        ...

    def _toolset_confirm(self, name: str, shown: BetaToolsetCallContext) -> None:
        """The approval gate: every call about to run is shown to `confirm` first, inside the pipeline
        and under the lock, so no override of `execute` or of the member can skip it."""
        confirm = self._toolset_options.confirm
        if confirm is None:
            return

        returned: object = None
        raised: Exception | None = None
        try:
            returned = confirm(shown)
        except Exception as exc:
            raised = exc

        confirm_outcome(name, returned, raised)


class BaseAsyncToolset(BaseToolset[_NameT, _InputT, _ConfirmT], BetaAsyncRunnableToolset):
    """The asynchronous call loop; see `BaseSyncToolset`."""

    def __init__(self, options: BaseToolsetOptions[_NameT, _InputT, _ConfirmT]) -> None:
        super().__init__(options)

        # One member call runs at a time: `__lock` (created on first use, so the toolset can be constructed outside an
        # event loop) serialises them, and `__lock_holder` records the task inside it so a nested `call()` is
        # recognised.
        self.__lock: anyio.Lock | None = None
        self.__lock_holder: object = None

        # `close()` waits on `__settled` until `__pending` (the calls accepted and not yet finished) drops to zero. A
        # fresh event is armed whenever a call arrives with none pending.
        self.__pending = 0
        self.__settled: anyio.Event | None = None

    @final
    @override
    async def call(self, context: BetaToolsetCallContext, name: str, input: Mapping[str, object]) -> BetaToolsetContent:
        """The entry point the tool runner and `tool_result` use. See the synchronous class's
        `call`. A cancelled task raises out of here at the member's own `await` and the lock is
        released."""
        self._toolset_refuse_if_closed()

        if self.__lock is None:
            self.__lock = anyio.Lock()
        current = anyio.get_current_task()
        if self.__lock_holder == current:
            raise NestedCallError()

        lock = self.__lock
        if not self.__pending:
            self.__settled = anyio.Event()
        self.__pending += 1

        try:
            async with lock:
                self.__lock_holder = current
                try:
                    return await self._toolset_run(context, name, input)
                finally:
                    self.__lock_holder = None
        finally:
            self.__pending -= 1
            if not self.__pending and self.__settled is not None:
                self.__settled.set()

    @override
    async def close(self) -> None:
        """Release what the toolset holds when you are done. See the synchronous class's `close`. Marks the toolset
        closed, then waits for the calls already accepted to settle. An override awaits `super().close()` first.
        Called from inside a member it returns without waiting."""
        await super().close()

        if self.__lock is None or self.__lock_holder == anyio.get_current_task():
            return  # no call was ever accepted, or the caller is the call in flight

        while self.__pending and self.__settled is not None:
            await self.__settled.wait()

    @abstractmethod
    async def _toolset_run(
        self, context: BetaToolsetCallContext, name: str, input: Mapping[str, object]
    ) -> BetaToolsetContent: ...

    async def _toolset_confirm(self, name: str, shown: BetaToolsetCallContext) -> None:
        confirm = self._toolset_options.confirm
        if confirm is None:
            return

        returned: object = None
        raised: Exception | None = None
        try:
            returned = confirm(shown)
            if inspect.isawaitable(returned):
                returned = await returned
        except Exception as exc:
            raised = exc

        confirm_outcome(name, returned, raised)


def members_from_union(
    block_union: object, stand_ins: Mapping[str, type[BaseModel]]
) -> list[tuple[str, type[BaseModel]]]:
    """One `(name, input model)` per variant of a generated `tool_use` union, in its order. A variant whose `input`
    is typed as a bare object (a member that takes none) gets its model from `stand_ins`."""
    annotated = get_args(block_union)  # (Union[...], discriminator)
    members: list[tuple[str, type[BaseModel]]] = []
    for variant in cast("tuple[type[BaseModel], ...]", get_args(annotated[0])):
        fields = get_model_fields(variant)
        (name,) = cast("tuple[str]", get_args(field_outer_type(fields["name"])))
        generated = field_outer_type(fields["input"])
        members.append((name, stand_ins[name] if generated is object else cast("type[BaseModel]", generated)))
    return members


def overridden(cls: type, names: Sequence[str], default_bodies: frozenset[object]) -> frozenset[str]:
    """Those of `names` that `cls` overrides, by method identity against the family's abstract classes (their own
    member and `execute` bodies are `default_bodies`). Nothing is called."""
    return frozenset(name for name in names if getattr(cls, name) not in default_bodies)


def is_async_callable(obj: object) -> bool:
    """Whether calling `obj` returns a coroutine: an `async def` function, an object whose `__call__` is one, or a
    `functools.partial` of either."""
    while isinstance(obj, functools.partial):
        obj = obj.func
    return inspect.iscoroutinefunction(obj) or inspect.iscoroutinefunction(getattr(obj, "__call__", None))  # noqa: B004


def check_flavour(cls: type[BaseToolset[Any, Any, Any]], names: Iterable[str], *, registry: Registry[Any, Any]) -> None:
    """Raise when one of toolset class `cls`'s methods `names` is written for the other flavour: `async def` on the
    synchronous toolset, where nothing would await it, or a plain `def` on the asynchronous one, where it would run
    blocking I/O on the event loop."""
    is_async = issubclass(cls, BetaAsyncRunnableToolset)
    for name in names:
        if is_async_callable(getattr(cls, name)) == is_async:
            continue
        what = f"{registry.family} member {name!r}" if name in registry.members else name
        error = SyncOnAsyncToolsetError if is_async else AsyncOnSyncToolsetError
        raise error(what, twin=cls._toolset_twin)


def check_sync_hook(cls: type[BaseToolset[Any, Any, Any]], what: str, hook: object) -> None:
    """Raise when `hook` (`confirm`, or a family's own hook) is async and `cls` is a synchronous toolset. The
    asynchronous classes take either kind."""
    if not issubclass(cls, BetaAsyncRunnableToolset) and is_async_callable(hook):
        raise AsyncOnSyncToolsetError(what, twin=cls._toolset_twin)


def build_wire_configs(
    configs: Mapping[str, object] | None, served: frozenset[str], names: Sequence[str]
) -> dict[str, dict[str, object] | None] | None:
    """The caller's `configs`, deep-copied, with `enabled: false` added for every member that is
    not served. Enabling such a member is a configuration error."""
    # This copy is what the dispatch gate reads and what the request sends. None means "this member's defaults". A
    # malformed entry fails closed (member_enabled reads it as off, the API rejects it), and one that is not a mapping
    # raises here.
    wire: dict[str, dict[str, object] | None] = {
        name: None if given is None else copy.deepcopy({**cast("Mapping[str, object]", given)})
        for name, given in (configs.items() if configs is not None else ())
    }

    unserved = [name for name in names if name not in served and (wire.get(name) or {}).get("enabled") is True]
    if unserved:  # the model would be offered a member that can only ever answer "not available"
        raise ToolsetConfigError(
            f"configs enables member(s) this toolset does not implement: {sorted(unserved)!r} "
            "(override the member method; a subclass that overrides only execute() serves every member)"
        )

    for name in names:
        if name in served:
            continue
        wire[name] = {**(wire.get(name) or {}), "enabled": False}
    return wire if wire else None


def parse_input(member: Member[_NameT, _InputT], raw: Mapping[str, object], *, family: ToolsetFamily) -> _InputT:
    """Parse the model's `tool_use.input` into the member's input model.

    A mistyped field is the model's mistake, so it comes back as a `ToolError` the model can read
    and correct rather than an exception that ends the loop. The value is not echoed. A key the schema
    does not declare stays on the parsed input, so the driver and `confirm` read what the model sent, except an
    undeclared key named after an attribute of the model, which is removed before validation."""
    fields = get_model_fields(member.input)
    declared = {*fields, *(field.alias for field in fields.values() if field.alias)}
    # On pydantic v1 an extra field becomes an instance attribute, so a key named after an attribute of the model class,
    # such as `to_dict`, would replace it. `getattr_static` avoids reading `__fields__`, which warns on pydantic v2.
    raw = {
        key: value
        for key, value in raw.items()
        if key in declared or inspect.getattr_static(member.input, key, ABSENT) is ABSENT
    }

    try:
        return validate_type(type_=member.input, value=raw)
    except pydantic.ValidationError as exc:
        # every failed field, so the model can correct them in one round trip
        problems = "; ".join(input_problem(error["loc"], error["msg"]) for error in exc.errors()) or "invalid input"
        raise InvalidMemberInputError(member.name, problems, family=family) from None


def input_problem(loc: Sequence[int | str], msg: str) -> str:
    """One pydantic error as `loc: message` (the value is not echoed)."""
    where = ".".join(str(part) for part in loc)
    first = msg.splitlines()[0] if msg else "invalid input"
    return f"{where}: {first}" if where else first


def confirm_outcome(name: str, returned: object, raised: Exception | None) -> None:
    """Turn what the `confirm` callable did into the gate's decision: return to proceed, or raise the
    refusal the model reads.

    A `ToolError` that `confirm` raised is relayed as-is. Any other exception means the prompt failed: the call is
    refused and the run continues. Any answer other than `True` declines the call."""
    if raised is not None:
        raise hook_refusal(raised, ConfirmFailedError(name))
    if returned is not True:
        if inspect.iscoroutine(returned):
            returned.close()  # from a confirm that returns a coroutine: declined, with no "never awaited" warning
        raise ConfirmDeclinedError(name)


def error_content(error: ToolError) -> list[BetaTextBlockParam]:
    content = error_text_content(error.content)
    return [{"type": "text", "text": content}] if isinstance(content, str) else content


def checked_error(error: ToolError, check: Callable[[str], str]) -> ToolError:
    """`error` with each text block run through `check` and then bounded, or the same object when nothing changed.
    The bound comes after the check, so the check reads the driver's text whole."""
    content = error_content(error)
    checked: list[BetaTextBlockParam] = []
    for block in content:
        block = copy.copy(block)
        block["text"] = check(block["text"])[:FIELD_MAX]
        checked.append(block)
    if checked == content:
        return error
    return ToolError(checked)


def bounded_error(error: ToolError) -> ToolError:
    """`checked_error` with no check: each text block cut to the field limit, for a family with nothing to redact."""
    return checked_error(error, lambda text: text)
