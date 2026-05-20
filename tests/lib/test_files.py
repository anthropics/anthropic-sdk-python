from __future__ import annotations

from pathlib import Path
from collections.abc import Iterable

import pytest

from anthropic.lib import files_from_dir, async_files_from_dir


def _write_skill_tree(root: Path) -> Path:
    skill_dir = root / "greeting"
    (skill_dir / "scripts").mkdir(parents=True)
    (skill_dir / "SKILL.md").write_text("---\nname: greeting\n---\n", encoding="utf-8")
    (skill_dir / "scripts" / "hello.py").write_text("print('ahoy')\n", encoding="utf-8")
    return skill_dir


def _bytes_by_name(files: Iterable[object]) -> dict[str, bytes]:
    result: dict[str, bytes] = {}
    for file in files:
        assert isinstance(file, tuple)
        assert isinstance(file[0], str)
        assert isinstance(file[1], bytes)
        result[file[0]] = file[1]
    return result


def test_files_from_dir_preserves_skill_top_level(tmp_path: Path) -> None:
    skill_dir = _write_skill_tree(tmp_path)

    files = _bytes_by_name(files_from_dir(skill_dir))

    assert files == {
        "greeting/SKILL.md": b"---\nname: greeting\n---\n",
        "greeting/scripts/hello.py": b"print('ahoy')\n",
    }


@pytest.mark.asyncio
async def test_async_files_from_dir_preserves_skill_top_level(tmp_path: Path) -> None:
    skill_dir = _write_skill_tree(tmp_path)

    files = _bytes_by_name(await async_files_from_dir(skill_dir))

    assert files == {
        "greeting/SKILL.md": b"---\nname: greeting\n---\n",
        "greeting/scripts/hello.py": b"print('ahoy')\n",
    }
