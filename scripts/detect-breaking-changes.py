from __future__ import annotations

import sys
from typing import Iterator
from pathlib import Path

import griffe
from rich.text import Text
from rich.style import Style
from rich.console import Console


def resolve_assignment_alias(obj: griffe.Object | griffe.Alias) -> griffe.Object | griffe.Alias:
    # griffe models `Foo = Bar` (a deprecated alias for a renamed class) as an attribute
    # with no members, so compare against the class it points to instead. Aliases can be
    # chained (`Foo = Bar`, `Bar = Baz`), so keep following them until we reach a class.
    target: griffe.Object | griffe.Alias | None = obj
    seen: set[str] = set()
    while isinstance(target, griffe.Attribute) and isinstance(target.value, griffe.ExprName):
        if target.path in seen:  # `A = B; B = A`
            return obj
        seen.add(target.path)
        try:
            # annotated as `Module | Class` upstream, but a re-exported name resolves to an `Alias`
            resolved: griffe.Object | griffe.Alias | None = target.value.resolved
            if isinstance(resolved, griffe.Alias):
                resolved = resolved.final_target
            target = resolved
        except Exception:
            return obj

    return target if isinstance(target, griffe.Class) else obj


def resolve_import(obj: griffe.Object | griffe.Alias) -> griffe.Object | griffe.Alias:
    if not isinstance(obj, griffe.Alias) or not obj.runtime:  # `if TYPE_CHECKING:` imports are gone at runtime
        return obj

    try:
        target = obj.final_target
    except griffe.GriffeError:
        return obj

    # `import pkg.name` stops working when a module is replaced by an import of another module
    return obj if isinstance(target, griffe.Module) else target


def public_members(obj: griffe.Object | griffe.Alias) -> dict[str, griffe.Object | griffe.Alias]:
    obj = resolve_assignment_alias(obj)
    if isinstance(obj, griffe.Alias):
        # an import we didn't follow has no members to compare. Imports are technically part
        # of the public API, but we don't have good preventative measures in place to prevent
        # changing them
        return {}

    return {name: value for name, value in obj.all_members.items() if not name.startswith("_")}


def find_breaking_changes(
    new_obj: griffe.Object | griffe.Alias,
    old_obj: griffe.Object | griffe.Alias,
    *,
    path: list[str],
) -> Iterator[Text | str]:
    # a class that moved and is imported from its new module is still public. Old-side
    # imports aren't followed, so a class imported at the baseline has no members checked
    new_members = public_members(resolve_import(new_obj))
    old_members = public_members(old_obj)

    for name, old_member in old_members.items():
        if isinstance(old_member, griffe.Alias) and len(path) > 2:
            # ignore imports in `/types/` for now, they're technically part of the public API
            # but we don't have good preventative measures in place to prevent changing them
            continue

        new_member = new_members.get(name)
        if new_member is None:
            cls_name = old_member.__class__.__name__
            yield Text(f"({cls_name})", style=Style(color="rgb(119, 119, 119)"))
            yield from [" " for _ in range(10 - len(cls_name))]
            yield f" {'.'.join(path)}.{name}"
            yield "\n"
            continue

        yield from find_breaking_changes(new_member, old_member, path=[*path, name])


def main() -> None:
    try:
        against_ref = sys.argv[1]
    except IndexError as err:
        raise RuntimeError("You must specify a base ref to run breaking change detection against") from err

    package = griffe.load(
        "anthropic",
        search_paths=[Path(__file__).parent.parent.joinpath("src")],
    )
    old_package = griffe.load_git(
        "anthropic",
        ref=against_ref,
        search_paths=["src"],
    )
    assert isinstance(package, griffe.Module)
    assert isinstance(old_package, griffe.Module)

    output = list(find_breaking_changes(package, old_package, path=["anthropic"]))
    if output:
        # soft_wrap: CI stdout is not a TTY, so rich would otherwise hard-wrap long symbol paths at 80 columns
        console = Console(soft_wrap=True)
        console.print(Text("Breaking changes detected!", style=Style(color="rgb(165, 79, 87)")))
        console.print()

        for text in output:
            console.print(text, end="")

        sys.exit(1)


main()
