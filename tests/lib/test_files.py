from __future__ import annotations

import os
from pathlib import Path

import pytest

from anthropic.lib import files_from_dir, async_files_from_dir


@pytest.fixture
def skill(tmp_path: Path) -> Path:
    directory = tmp_path / "greeting"
    (directory / "scripts").mkdir(parents=True)
    (directory / "SKILL.md").write_text("# hi\n")
    (directory / "scripts" / "run.py").write_text("print(1)\n")
    return directory


def _names(files: list[object]) -> list[str]:
    return sorted(name for name, *_ in files)  # type: ignore[misc]


EXPECTED = ["greeting/SKILL.md", "greeting/scripts/run.py"]


def test_names_carry_the_directory(skill: Path) -> None:
    assert _names(files_from_dir(skill)) == EXPECTED


RELATIVE = [("inside", "."), ("inside", "./"), ("inside", "../greeting"), ("parent", "greeting")]


def test_a_relative_root_names_the_same_files(skill: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    # the names go to the API as given, so `.` must not drop the directory and
    # `..` must not reach a name
    for where, spelling in RELATIVE:
        monkeypatch.chdir(skill if where == "inside" else skill.parent)
        assert _names(files_from_dir(spelling)) == EXPECTED, spelling


def test_a_trailing_separator_changes_nothing(skill: Path) -> None:
    assert _names(files_from_dir(f"{skill}{os.sep}")) == EXPECTED


async def test_async_names_carry_the_directory(skill: Path) -> None:
    assert _names(await async_files_from_dir(skill)) == EXPECTED


async def test_async_a_relative_root_names_the_same_files(skill: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    for where, spelling in RELATIVE:
        monkeypatch.chdir(skill if where == "inside" else skill.parent)
        assert _names(await async_files_from_dir(spelling)) == EXPECTED, spelling
