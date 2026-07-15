"""Tests for skill-archive extraction (:mod:`anthropic.lib.tools._skills`).

Skill bundles are packaged wrapped in a single directory named after the skill
(e.g. ``pdf/SKILL.md``). The extractor must strip that wrapper so files land at
``<dest>/SKILL.md``, not the doubled ``<dest>/pdf/SKILL.md``. It must also still
refuse zip-slip / tar-slip members.
"""

from __future__ import annotations

import io
import os
import stat
import tarfile
import zipfile
from pathlib import Path
from collections.abc import Callable

ArchiveMaker = Callable[[Path, dict[str, bytes]], None]
# Maps an entry name to ``(data, unix_mode)`` so a test can pin the mode the
# archive records for that member.
ArchiveModeMaker = Callable[[Path, "dict[str, tuple[bytes, int]]"], None]

import pytest

from anthropic.lib.tools._skills import _strip_top, _archive_top_dir, _extract_skill_archive


def _make_zip(path: Path, entries: dict[str, bytes]) -> None:
    with zipfile.ZipFile(path, "w") as zf:
        for name, data in entries.items():
            zf.writestr(name, data)


def _make_targz(path: Path, entries: dict[str, bytes]) -> None:
    with tarfile.open(path, "w:gz") as tf:
        for name, data in entries.items():
            info = tarfile.TarInfo(name)
            info.size = len(data)
            tf.addfile(info, io.BytesIO(data))


def _make_zip_modes(path: Path, entries: dict[str, tuple[bytes, int]]) -> None:
    with zipfile.ZipFile(path, "w") as zf:
        for name, (data, mode) in entries.items():
            info = zipfile.ZipInfo(name)
            # The Unix mode lives in the high 16 bits of ``external_attr``.
            info.external_attr = mode << 16
            zf.writestr(info, data)


def _make_targz_modes(path: Path, entries: dict[str, tuple[bytes, int]]) -> None:
    with tarfile.open(path, "w:gz") as tf:
        for name, (data, mode) in entries.items():
            info = tarfile.TarInfo(name)
            info.size = len(data)
            info.mode = mode
            tf.addfile(info, io.BytesIO(data))


def test_archive_top_dir_detection() -> None:
    assert _archive_top_dir(["pdf/SKILL.md", "pdf/scripts/x.py"]) == "pdf"
    assert _archive_top_dir(["pdf/SKILL.md"]) == "pdf"
    # No common single root -> no strip.
    assert _archive_top_dir(["SKILL.md", "scripts/x.py"]) == ""
    assert _archive_top_dir(["a/x", "b/y"]) == ""
    # Only the bare top dir, nothing nested -> nothing to unwrap.
    assert _archive_top_dir(["pdf/"]) == ""
    assert _archive_top_dir([]) == ""


def test_strip_top() -> None:
    assert _strip_top("pdf/SKILL.md", "pdf") == "SKILL.md"
    assert _strip_top("pdf/scripts/x.py", "pdf") == "scripts/x.py"
    assert _strip_top("pdf", "pdf") == ""  # bare top-dir entry
    assert _strip_top("SKILL.md", "") == "SKILL.md"  # no wrapper -> unchanged
    assert _strip_top("other/x", "pdf") == "other/x"  # not under the wrapper


@pytest.mark.parametrize("make", [_make_zip, _make_targz])
def test_extract_strips_skill_wrapper_dir(make: ArchiveMaker, tmp_path: Path) -> None:
    archive = tmp_path / "skill.archive"
    make(
        archive,
        {
            "pdf/SKILL.md": b"# PDF",
            "pdf/scripts/run.py": b"print(1)",
        },
    )
    dest = tmp_path / "skills" / "pdf"
    _extract_skill_archive(archive, dest)

    # Stripped: files land directly under dest, not dest/pdf/.
    assert (dest / "SKILL.md").read_bytes() == b"# PDF"
    assert (dest / "scripts" / "run.py").read_bytes() == b"print(1)"
    assert not (dest / "pdf").exists(), "wrapper dir was not stripped (doubling)"


@pytest.mark.parametrize("make", [_make_zip, _make_targz])
def test_extract_flat_archive_unchanged(make: ArchiveMaker, tmp_path: Path) -> None:
    archive = tmp_path / "skill.archive"
    make(archive, {"SKILL.md": b"# flat", "scripts/run.py": b"x"})
    dest = tmp_path / "skills" / "flat"
    _extract_skill_archive(archive, dest)
    assert (dest / "SKILL.md").read_bytes() == b"# flat"
    assert (dest / "scripts" / "run.py").read_bytes() == b"x"


def test_extract_refuses_zip_slip(tmp_path: Path) -> None:
    archive = tmp_path / "evil.zip"
    _make_zip(archive, {"../escape.txt": b"pwned"})
    dest = tmp_path / "skills" / "x"
    with pytest.raises(ValueError):
        _extract_skill_archive(archive, dest)
    assert not (tmp_path / "skills" / "escape.txt").exists()
    assert not (tmp_path / "escape.txt").exists()


def _mode(p: Path) -> int:
    return stat.S_IMODE(os.stat(p).st_mode)


def test_zip_preserves_executable_bit(tmp_path: Path) -> None:
    archive = tmp_path / "skill.zip"
    _make_zip_modes(
        archive,
        {
            "scripts/run.sh": (b"#!/bin/sh\necho hi\n", 0o755),
            "SKILL.md": (b"# doc", 0o644),
        },
    )
    dest = tmp_path / "skills" / "x"
    _extract_skill_archive(archive, dest)

    exe = _mode(dest / "scripts" / "run.sh")
    doc = _mode(dest / "SKILL.md")
    assert exe & 0o111, "executable bit was dropped on zip extraction"
    assert exe == 0o755
    assert doc & 0o111 == 0
    assert doc == 0o644


def test_zip_without_unix_attrs_is_not_executable(tmp_path: Path) -> None:
    # ``writestr`` with a plain name records no Unix mode (external_attr == 0);
    # the member must extract non-executable rather than inherit a random mode.
    archive = tmp_path / "skill.zip"
    _make_zip(archive, {"SKILL.md": b"# doc", "scripts/run.sh": b"echo hi"})
    dest = tmp_path / "skills" / "x"
    _extract_skill_archive(archive, dest)

    assert _mode(dest / "SKILL.md") == 0o644
    assert _mode(dest / "scripts" / "run.sh") == 0o644


def test_tar_preserves_executable_bit(tmp_path: Path) -> None:
    archive = tmp_path / "skill.tar.gz"
    _make_targz_modes(
        archive,
        {
            "scripts/run.sh": (b"#!/bin/sh\necho hi\n", 0o755),
            "SKILL.md": (b"# doc", 0o644),
        },
    )
    dest = tmp_path / "skills" / "x"
    _extract_skill_archive(archive, dest)

    exe = _mode(dest / "scripts" / "run.sh")
    doc = _mode(dest / "SKILL.md")
    assert exe & 0o111, "executable bit was dropped on tar extraction"
    assert exe == 0o755
    assert doc & 0o111 == 0
    assert doc == 0o644


@pytest.mark.parametrize("make", [_make_zip_modes, _make_targz_modes])
def test_extract_drops_setuid_setgid_sticky(make: ArchiveModeMaker, tmp_path: Path) -> None:
    # setuid (0o4000) + setgid (0o2000) + sticky (0o1000) on an executable
    # member must never survive extraction; the mode collapses to plain 0o755.
    archive = tmp_path / "skill.archive"
    make(
        archive,
        {
            "scripts/run.sh": (b"#!/bin/sh\n", 0o7755),
            "SKILL.md": (b"# doc", 0o4644),
        },
    )
    dest = tmp_path / "skills" / "x"
    _extract_skill_archive(archive, dest)

    exe = _mode(dest / "scripts" / "run.sh")
    doc = _mode(dest / "SKILL.md")
    assert exe & 0o7000 == 0, "setuid/setgid/sticky leaked onto executable member"
    assert exe == 0o755
    # A non-executable member with setuid set must also drop the bit.
    assert doc & 0o7000 == 0
    assert doc == 0o644
