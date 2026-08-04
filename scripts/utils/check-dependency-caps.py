"""Ensure every production and build dependency in pyproject.toml has an upper version bound.

Unbounded requirements (e.g. `httpx>=0.25.0`) mean a future major release of a
dependency can break users at install time without us noticing, so we require an
explicit cap (e.g. `httpx>=0.25.0,<1`).
"""

from __future__ import annotations

import sys
from typing import Any
from pathlib import Path

from packaging.requirements import Requirement

if sys.version_info >= (3, 11):
    import tomllib
else:
    import tomli as tomllib

# operators that constrain the maximum installable version
UPPER_BOUND_OPERATORS = {"<", "<=", "==", "===", "~="}


def has_upper_bound(requirement: Requirement) -> bool:
    return any(spec.operator in UPPER_BOUND_OPERATORS for spec in requirement.specifier)


def main() -> None:
    pyproject_path = Path(__file__).parent.parent.parent / "pyproject.toml"
    with open(pyproject_path, "rb") as f:
        pyproject = tomllib.load(f)

    project: dict[str, Any] = pyproject["project"]
    build_system: dict[str, Any] = pyproject.get("build-system", {})

    requirement_tables: dict[str, list[str]] = {"project.dependencies": project.get("dependencies", [])}
    optional_dependencies: dict[str, list[str]] = project.get("optional-dependencies", {})
    for extra, requirements in optional_dependencies.items():
        requirement_tables[f"project.optional-dependencies.{extra}"] = requirements
    requirement_tables["build-system.requires"] = build_system.get("requires", [])

    missing_caps: list[str] = []
    for group, requirements in requirement_tables.items():
        for raw in requirements:
            requirement = Requirement(raw)
            if not has_upper_bound(requirement):
                missing_caps.append(f"  [{group}] {raw}")

    if missing_caps:
        print("The following dependencies are missing an upper version bound (e.g. `>=2, <3`):")
        print("\n".join(missing_caps))
        sys.exit(1)


if __name__ == "__main__":
    main()
