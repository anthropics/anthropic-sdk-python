"""Tests for :mod:`anthropic.lib._executable` — safe helper-executable resolution.

The vector IDs (V1–V12, W1–W3, P1) and guarantee IDs (G1–G5) are shared with the
sibling Anthropic SDKs (claude-agent-sdk-python, anthropic-sdk-typescript,
anthropic-sdk-go); keep them in sync when changing behaviour.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path
from dataclasses import dataclass

import pytest

from anthropic.lib._executable import (
    WINDOWS_NATIVE_EXTENSIONS,
    ExecutableNotFoundError,
    run,
    resolve_argv,
    find_executable,
    _candidate_names,
    _find_executable,
    require_executable,
    _is_searchable_path_entry,
)

posix_only = pytest.mark.skipif(sys.platform == "win32", reason="exercises the POSIX flavour on the real filesystem")

SEP = os.pathsep


def _make_executable(path: Path, body: str = "#!/bin/sh\nexit 0\n") -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body)
    path.chmod(0o755)
    return path


@dataclass
class Layout:
    """``bin/`` holds the real tools; ``plant/`` is the CWD an attacker controls."""

    bin: Path
    plant: Path
    dirs: Path


@pytest.fixture
def layout(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Layout:
    bin_dir = tmp_path / "bin"
    _make_executable(bin_dir / "tool")
    _make_executable(bin_dir / "tool.exe")
    plant = tmp_path / "plant"
    _make_executable(plant / "tool")
    _make_executable(plant / "tool.exe")
    _make_executable(plant / "rel" / "sub" / "tool")
    # V7: a *directory* named like the tool inside a searchable entry.
    dirs = tmp_path / "dirs"
    (dirs / "tool").mkdir(parents=True)
    monkeypatch.chdir(plant)
    # Nothing may leak in from the host PATH.
    monkeypatch.setenv("PATH", "")
    return Layout(bin=bin_dir, plant=plant, dirs=dirs)


# --------------------------------------------------------------------------- #
# V1–V12: shared vectors, host flavour against the real filesystem             #
# --------------------------------------------------------------------------- #


@posix_only
def test_v1_absolute_entry_is_searched(layout: Layout) -> None:
    assert find_executable("tool", path=str(layout.bin)) == str(layout.bin / "tool")


@posix_only
def test_v2_leading_empty_entry_is_not_the_cwd(layout: Layout) -> None:
    found = find_executable("tool", path="" + SEP + str(layout.bin))
    assert found == str(layout.bin / "tool")
    assert found != str(layout.plant / "tool")


@posix_only
def test_v3_dot_entry_is_not_the_cwd(layout: Layout) -> None:
    assert find_executable("tool", path="." + SEP + str(layout.bin)) == str(layout.bin / "tool")


@posix_only
def test_v4_relative_entry_is_skipped(layout: Layout) -> None:
    assert (layout.plant / "rel" / "sub" / "tool").is_file()
    assert find_executable("tool", path="rel/sub" + SEP + str(layout.bin)) == str(layout.bin / "tool")


@posix_only
def test_v5_only_cwdish_entries_find_nothing(layout: Layout) -> None:
    # Every entry below points (directly or relatively) at a real ``tool`` — via the CWD.
    assert (layout.plant / "tool").is_file() and (layout.plant / "rel" / "sub" / "tool").is_file()
    assert find_executable("tool", path=SEP.join([".", "", "rel/sub", "./rel/sub", "..", "../plant"])) is None


@posix_only
def test_v6_non_executable_file_is_not_a_match(layout: Layout) -> None:
    (layout.bin / "tool").chmod(0o644)
    assert find_executable("tool", path=str(layout.bin)) is None


@posix_only
def test_v7_directory_named_like_the_tool_is_skipped(layout: Layout) -> None:
    assert (layout.dirs / "tool").is_dir()
    assert find_executable("tool", path=str(layout.dirs) + SEP + str(layout.bin)) == str(layout.bin / "tool")


@posix_only
def test_v8_explicit_relative_path_is_honoured(layout: Layout) -> None:
    """G4: ``./tool`` is the caller's explicit decision and resolves against the CWD."""
    found = find_executable("./tool", path=str(layout.bin))
    assert found is not None and os.path.isabs(found)
    assert found == str(layout.plant / "tool")


@posix_only
def test_v9_absolute_name_is_returned_as_is_or_not_found(layout: Layout) -> None:
    assert find_executable(str(layout.bin / "tool"), path="") == str(layout.bin / "tool")
    assert find_executable(str(layout.bin / "missing"), path=str(layout.bin)) is None
    # An absolute path to something that is not a regular executable file is not found either.
    assert find_executable(str(layout.dirs / "tool"), path=str(layout.bin)) is None


@posix_only
def test_v10_result_is_absolute_and_normalised(layout: Layout) -> None:
    found = find_executable("tool", path=str(layout.bin) + "/./")
    assert found is not None
    assert os.path.isabs(found)
    assert found == os.path.normpath(found) == str(layout.bin / "tool")


@pytest.mark.parametrize("name", ["", ".", ".."])
def test_v11_degenerate_names_are_not_found(layout: Layout, name: str) -> None:
    assert find_executable(name, path=str(layout.bin)) is None


@posix_only
def test_v12_unset_or_empty_path_finds_nothing(layout: Layout, monkeypatch: pytest.MonkeyPatch) -> None:
    """No ``os.defpath`` fallback and never the CWD (which holds a ``tool``)."""
    monkeypatch.setenv("PATH", "")
    assert find_executable("tool") is None
    monkeypatch.delenv("PATH", raising=False)
    assert find_executable("tool") is None
    assert find_executable("tool", path="") is None
    # Sanity: the environment PATH is what is consulted by default.
    monkeypatch.setenv("PATH", str(layout.bin))
    assert find_executable("tool") == str(layout.bin / "tool")


# --------------------------------------------------------------------------- #
# W1–W3: Windows flavour, exercised on any host via the pure helpers           #
# --------------------------------------------------------------------------- #


@pytest.mark.parametrize(
    ("entry", "searchable"),
    [
        ("C:\\bin", True),
        ("c:/bin", True),
        ("\\\\srv\\share\\bin", True),
        ("//srv/share/bin", True),
        ('"C:\\Program Files\\X"', True),
        ("\\bin", False),
        ("/bin", False),
        ("C:bin", False),
        ("C:", False),
        (".", False),
        ("", False),
        ('""', False),
        ("bin", False),
        ("..\\x", False),
        ("%SystemRoot%\\system32", False),
        ("~\\bin", False),
    ],
)
def test_w1_windows_entry_check(entry: str, searchable: bool) -> None:
    assert _is_searchable_path_entry(entry, windows=True) is searchable


@pytest.mark.parametrize(
    ("entry", "searchable"),
    [
        ("/usr/bin", True),
        ("/", True),
        ("bin", False),
        (".", False),
        ("", False),
        ("~/bin", False),
        ("$HOME/bin", False),
        # A Windows-style absolute entry is *relative* on POSIX.
        ("C:\\bin", False),
    ],
)
def test_w1_posix_entry_check(entry: str, searchable: bool) -> None:
    assert _is_searchable_path_entry(entry, windows=False) is searchable


@pytest.mark.parametrize(
    ("name", "expected"),
    [
        ("rg", ["rg.exe", "rg.com"]),
        ("rg.exe", ["rg.exe"]),
        ("RG.EXE", ["RG.EXE"]),
        ("claude.cmd", []),
        ("tool.js", []),
    ],
)
def test_w2_windows_candidate_names_default_allow_list(name: str, expected: list[str]) -> None:
    assert _candidate_names(name, windows=True) == expected


def test_w2_windows_candidate_names_wider_allow_list_detects_shims() -> None:
    assert _candidate_names("claude.cmd", windows=True, windows_extensions=(".exe", ".com", ".cmd", ".bat")) == [
        "claude.cmd"
    ]
    assert _candidate_names("claude", windows=True, windows_extensions=(".cmd", ".bat")) == ["claude.cmd", "claude.bat"]
    assert _candidate_names("tool.js", windows=True, windows_extensions=(".exe", ".com", ".cmd", ".bat")) == []


def test_w2_posix_candidate_is_the_name_itself() -> None:
    assert _candidate_names("rg", windows=False) == ["rg"]
    assert _candidate_names("tool.js", windows=False) == ["tool.js"]


def _unc_spelling(p: Path) -> str:
    """Spell an absolute POSIX path so it passes the *Windows* entry check.

    ``//tmp/x/bin`` matches the UNC rule, and a POSIX kernel treats the leading
    ``//`` as ``/`` — so the Windows flavour can be run end-to-end against real
    files on a POSIX host.
    """
    return "/" + str(p)


def _find_windows_flavour(name: str, path: str) -> str | None:
    return _find_executable(name, path=path, windows=True, windows_extensions=WINDOWS_NATIVE_EXTENSIONS)


@posix_only
def test_w3_windows_flavour_end_to_end_never_uses_cwd(layout: Layout) -> None:
    unc_bin = _unc_spelling(layout.bin)
    assert _is_searchable_path_entry(unc_bin, windows=True)

    # ``.`` first and the CWD (= plant) holds ``tool.exe``: the PATH one wins.
    found = _find_windows_flavour("tool", ".;" + unc_bin)
    assert found is not None
    assert Path(found).resolve() == (layout.bin / "tool.exe").resolve()
    assert Path(found).resolve() != (layout.plant / "tool.exe").resolve()
    # Native images only: the extensionless ``bin/tool`` is never a candidate.
    assert found.endswith("tool.exe")
    # An explicit allowed extension is tried as-is.
    found_exe = _find_windows_flavour("tool.exe", unc_bin)
    assert found_exe is not None and Path(found_exe).resolve() == (layout.bin / "tool.exe").resolve()
    # Only CWD-ish / non-absolute entries — including a POSIX-absolute one, which
    # is rooted-but-driveless under the Windows rules: nothing.
    assert _find_windows_flavour("tool", ".;;rel\\sub;" + str(layout.bin)) is None
    # ``.cmd`` shims are never run, but can be *detected* with a wider allow-list.
    _make_executable(layout.bin / "shim.cmd")
    assert _find_windows_flavour("shim", unc_bin) is None
    detected = _find_executable("shim", path=unc_bin, windows=True, windows_extensions=(".cmd", ".bat"))
    assert detected is not None and Path(detected).resolve() == (layout.bin / "shim.cmd").resolve()


# --------------------------------------------------------------------------- #
# P1: POSIX flavour — backslash is not a separator                             #
# --------------------------------------------------------------------------- #


@posix_only
def test_p1_backslash_is_a_plain_character_on_posix(layout: Layout) -> None:
    weird = _make_executable(layout.bin / "a\\b")
    # Searched for as a bare name (not treated as the explicit path ``a/b``)…
    assert _find_executable("a\\b", path=str(layout.bin), windows=False, windows_extensions=()) == str(weird)
    # …whereas the Windows flavour treats it as an explicit, CWD-relative path.
    assert _find_executable("a\\b", path=str(layout.bin), windows=True, windows_extensions=("",)) is None


# --------------------------------------------------------------------------- #
# require_executable / resolve_argv / run                                      #
# --------------------------------------------------------------------------- #


@posix_only
def test_require_executable_raises_a_file_not_found_error(layout: Layout) -> None:
    with pytest.raises(ExecutableNotFoundError) as exc_info:
        require_executable("tool", path="." + SEP + "")
    assert exc_info.value.name == "tool"
    assert isinstance(exc_info.value, FileNotFoundError)
    assert require_executable("tool", path=str(layout.bin)) == str(layout.bin / "tool")


def test_executable_not_found_error_survives_pickling() -> None:
    """Raised inside a ``ProcessPoolExecutor`` worker it must cross the process
    boundary intact (``OSError.__reduce__`` alone would replay three arguments
    into the one-argument constructor)."""
    import copy
    import pickle

    err = ExecutableNotFoundError("rg")
    # Round-trips an object created right here — no untrusted pickle data involved.
    for clone in (pickle.loads(pickle.dumps(err)), copy.copy(err)):
        assert isinstance(clone, ExecutableNotFoundError)
        assert clone.name == "rg" and clone.filename == "rg" and clone.errno == err.errno
        assert str(clone) == str(err)


@posix_only
def test_resolve_argv_replaces_only_argv0(layout: Layout) -> None:
    argv = resolve_argv([Path("tool"), "--flag", Path("rel/ative")], path=str(layout.bin))
    assert argv == [str(layout.bin / "tool"), "--flag", "rel/ative"]
    with pytest.raises(ValueError):
        resolve_argv([], path=str(layout.bin))
    with pytest.raises(ExecutableNotFoundError):
        resolve_argv(["tool"], path=".")
    # A shell-style string is a ``Sequence[str]`` to the type checker, but never an argv.
    with pytest.raises(TypeError):
        resolve_argv("tool --flag", path=str(layout.bin))


@posix_only
def test_run_spawns_the_resolved_absolute_path(layout: Layout, monkeypatch: pytest.MonkeyPatch) -> None:
    _make_executable(layout.bin / "hello", '#!/bin/sh\necho "from-bin $0"\n')
    _make_executable(layout.plant / "hello", "#!/bin/sh\necho from-plant\n")
    monkeypatch.setenv("PATH", "." + SEP + "" + SEP + str(layout.bin))
    result = run(["hello"], capture_output=True, text=True, check=True)
    # ``$0`` is the path the OS was handed: the absolute PATH hit, not ``./hello``.
    assert result.stdout == f"from-bin {layout.bin / 'hello'}\n"
    monkeypatch.setenv("PATH", ".")
    with pytest.raises(ExecutableNotFoundError):
        run(["hello"], capture_output=True)


@posix_only
def test_run_resolves_against_the_path_the_child_will_see(layout: Layout, monkeypatch: pytest.MonkeyPatch) -> None:
    """Like ``subprocess.run`` on POSIX, an explicit ``env`` carrying a ``PATH``
    is the search path — still subject to the absolute-entries-only rule."""
    _make_executable(layout.bin / "hello", '#!/bin/sh\necho "from-bin $0"\n')
    monkeypatch.setenv("PATH", "")
    child_env = {"PATH": "." + SEP + str(layout.bin)}
    assert run(["hello"], env=child_env, capture_output=True, text=True).stdout == f"from-bin {layout.bin / 'hello'}\n"
    with pytest.raises(ExecutableNotFoundError):
        run(["hello"], env={"PATH": "."}, capture_output=True)
    # No PATH in the child env: fall back to this process's (empty here) — never os.defpath.
    with pytest.raises(ExecutableNotFoundError):
        run(["hello"], env={"UNRELATED": "1"}, capture_output=True)
    monkeypatch.setenv("PATH", str(layout.bin))
    assert run(["hello"], env={"UNRELATED": "1"}, capture_output=True, text=True).returncode == 0
