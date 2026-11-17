from __future__ import annotations

import os
import sys
import shutil
import subprocess
from pathlib import Path

import pytest

SCRIPT = Path(__file__).parent.parent / "scripts" / "detect-breaking-changes.py"
PACKAGE = "anthropic"
PACKAGE_DIR = Path("src/anthropic")

FOO = """\
class Foo:
    def bar(self) -> int:
        return 1

    def baz(self) -> int:
        return 2
"""
FOO_WITHOUT_BAZ = """\
class Foo:
    def bar(self) -> int:
        return 1
"""
BAR_ASSIGNED_TO_FOO = """\
class Bar:
    def bar(self) -> int:
        return 1


Foo = Bar
"""


def subprocess_env() -> dict[str, str]:
    # inside a git hook, GIT_DIR would send these commits to the real repository;
    # FORCE_COLOR and TTY_COMPATIBLE would add color codes to the script's output
    return {
        name: value
        for name, value in os.environ.items()
        if not name.startswith("GIT_") and name not in ("FORCE_COLOR", "TTY_COMPATIBLE")
    }


def git(repo: Path, *args: str) -> None:
    identity = ["-c", "user.name=test", "-c", "user.email=test@example.com", "-c", "commit.gpgsign=false"]
    subprocess.run(["git", *identity, *args], cwd=repo, env=subprocess_env(), check=True, capture_output=True)


def write_package(repo: Path, files: dict[str, str]) -> None:
    shutil.rmtree(repo / PACKAGE_DIR, ignore_errors=True)
    for name, text in {"__init__.py": "", **files}.items():
        path = repo / PACKAGE_DIR / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)


def reported_names(repo: Path, *, baseline: dict[str, str], tip: dict[str, str]) -> list[str]:
    (repo / "scripts").mkdir()
    shutil.copy(SCRIPT, repo / "scripts")
    write_package(repo, baseline)
    git(repo, "init")
    git(repo, "add", ".")
    git(repo, "commit", "-m", "baseline")
    write_package(repo, tip)

    result = subprocess.run(
        [sys.executable, "scripts/detect-breaking-changes.py", "HEAD"],
        cwd=repo,
        env=subprocess_env(),
        capture_output=True,
        text=True,
    )

    lines = [line for line in result.stdout.splitlines() if line.startswith("(")]
    assert result.returncode == (1 if lines else 0), result.stdout + result.stderr
    return sorted(line.split()[-1].removeprefix(f"{PACKAGE}.") for line in lines)


@pytest.mark.parametrize(
    "baseline, tip, reported",
    [
        pytest.param(
            {"foo.py": FOO},
            {"foo.py": "from ._foo import Foo\n", "_foo.py": FOO},
            [],
            id="class moved and imported",
        ),
        pytest.param(
            {"types/__init__.py": "", "types/foo.py": FOO},
            {"types/__init__.py": "", "types/foo.py": "from .._foo import Foo\n", "_foo.py": FOO},
            [],
            id="class moved and imported in a nested module",
        ),
        pytest.param(
            {"foo.py": FOO},
            {"foo.py": "from ._a import Foo\n", "_a.py": "from ._foo import Foo\n", "_foo.py": FOO},
            [],
            id="class moved behind two imports",
        ),
        pytest.param(
            {"foo.py": FOO},
            {"foo/__init__.py": "from ._foo import Foo\n", "foo/_foo.py": FOO},
            [],
            id="module turned into a package",
        ),
        pytest.param(
            {"foo.py": BAR_ASSIGNED_TO_FOO},
            {"foo.py": "from ._foo import Bar, Foo\n", "_foo.py": BAR_ASSIGNED_TO_FOO},
            [],
            id="assigned name moved and imported",
        ),
        pytest.param(
            {"foo.py": "from ._foo import Foo\n", "_foo.py": FOO},
            {"foo.py": "from ._foo import Foo\n", "_foo.py": FOO_WITHOUT_BAZ},
            [],
            id="method removed from a class imported at the baseline is not checked",
        ),
        pytest.param(
            {"_foo.py": FOO, "types/__init__.py": "", "types/foo.py": "from .._foo import Foo\n"},
            {"_foo.py": FOO, "types/__init__.py": "", "types/foo.py": ""},
            [],
            id="import dropped from a nested module is not checked",
        ),
        pytest.param(
            {"foo.py": FOO},
            {"foo.py": FOO_WITHOUT_BAZ},
            ["foo.Foo.baz"],
            id="method removed",
        ),
        pytest.param(
            {"foo.py": FOO},
            {"foo.py": BAR_ASSIGNED_TO_FOO},
            ["foo.Foo.baz"],
            id="method removed from a class assigned to the name",
        ),
        pytest.param(
            {"foo.py": FOO},
            {"foo.py": ""},
            ["foo.Foo"],
            id="class removed",
        ),
        pytest.param(
            {"foo.py": FOO},
            {"foo.py": "from ._foo import Foo\n", "_foo.py": FOO.replace("baz", "qux")},
            ["foo.Foo.baz"],
            id="method renamed in a moved class",
        ),
        pytest.param(
            {"_foo.py": FOO, "foo.py": "from ._foo import Foo\n"},
            {"_foo.py": FOO, "foo.py": ""},
            ["foo.Foo"],
            id="import dropped",
        ),
        pytest.param(
            {"foo.py": FOO},
            {"foo.py": "from other_package import Foo\n"},
            ["foo.Foo.bar", "foo.Foo.baz"],
            id="class replaced by an import from another package",
        ),
        pytest.param(
            {"foo.py": FOO},
            {"foo.py": "from ._a import Foo\n", "_a.py": "from .foo import Foo\n"},
            ["foo.Foo.bar", "foo.Foo.baz"],
            id="class replaced by an import cycle",
        ),
        pytest.param(
            {"foo.py": FOO},
            {
                "foo.py": "from typing import TYPE_CHECKING\n\nif TYPE_CHECKING:\n    from ._foo import Foo\n",
                "_foo.py": FOO,
            },
            ["foo.Foo.bar", "foo.Foo.baz"],
            id="class moved and imported only for type checking",
        ),
        pytest.param(
            {"foo.py": FOO},
            {"__init__.py": "from . import _foo as foo\n", "_foo.py": FOO},
            ["foo.Foo"],
            id="module replaced by an import of another module",
        ),
    ],
)
def test_reported_names(tmp_path: Path, baseline: dict[str, str], tip: dict[str, str], reported: list[str]) -> None:
    assert reported_names(tmp_path, baseline=baseline, tip=tip) == reported
