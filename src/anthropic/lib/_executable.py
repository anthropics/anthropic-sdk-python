r"""Safe resolution and invocation of helper executables (``rg``, ``git``, …).

**Safe executable resolution.** This SDK never launches a helper program by bare
name. Every program it spawns is either an absolute path it constructed itself, or a
bare name resolved by the SDK's own ``find_executable`` — which searches only the
fully-absolute entries of ``PATH``, never the current working directory (neither
implicitly, as Windows ``CreateProcess``/``shutil.which``/libuv do, nor via ``.``/empty/
relative ``PATH`` entries), and on Windows returns only native executables
(``.exe``/``.com``). The absolute path it returns is what is handed to the OS. This holds
on every platform, so a file planted in a directory the user merely *works in* (a
cloned repository, an extracted archive) is never selected as a helper binary.

Guarantees (the tests and the sibling SDKs cross-reference these IDs):

- **G1 — absolute argv[0].** The program path handed to the OS process-creation
  API is always absolute. Bare names never reach ``subprocess``/``anyio``:
  resolve first (:func:`find_executable`/:func:`require_executable`/
  :func:`resolve_argv`), then spawn the absolute result (:func:`run` does both).
- **G2 — the working directory is never a search location.** Not implicitly
  (as Windows does), not via ``.``, not via an empty ``PATH`` entry (which POSIX
  ``execvp`` treats as the CWD), not via a relative entry (``bin``,
  ``..\tools``), and on Windows not via drive-relative (``C:bin``) or
  rooted-but-driveless (``\bin``) entries either. Only *fully absolute* entries
  are searched: POSIX ``/…``; Windows ``X:\…``/``X:/…`` or UNC
  ``\\server\share\…``. Surrounding double quotes on a Windows entry are
  stripped before the check (``"C:\Program Files\Git\cmd"`` is legal in
  ``PATH``). No ``~`` or ``%VAR%``/``$VAR`` expansion — the OS does not expand
  these at spawn time either. An unset or empty ``PATH`` finds nothing (there is
  deliberately no ``os.defpath`` fallback).
- **G3 — Windows: native images only.** For a bare name the candidates are the
  name with each *allowed* extension appended — default
  :data:`WINDOWS_NATIVE_EXTENSIONS` (``.exe``, ``.com``); never ``.bat``/``.cmd``
  (they run via ``cmd.exe /c`` and re-parse the command line) and never an
  extensionless file. A name that already ends in an allowed extension is tried
  as-is only; a name with any other extension (``tool.js``, or ``claude.cmd``
  under the default allow-list) has no candidates — pass the full file name
  (``python3.12.exe``) when the program name itself contains a dot. The
  allow-list is a parameter so a caller can *detect* (not run) a ``.cmd`` shim
  to print a helpful error. On POSIX the name is tried as-is only.
- **G4 — explicit paths are the caller's decision.** If ``name`` contains a
  path separator (``/``; on Windows also ``\`` or a drive prefix) no search
  happens: the absolute, normalised form is returned iff it is an existing
  regular file (and executable, on POSIX), else "not found". ``./tool``
  deliberately resolves against the CWD — the caller asked for exactly that.
- **G5 — one implementation, enforced.** ``shutil.which`` and
  ``distutils.spawn.find_executable`` are banned repo-wide by ruff
  (``[tool.ruff.lint.flake8-tidy-imports.banned-api]`` in ``pyproject.toml``),
  and ``tests/lib/test_executable_policy.py`` fails if any process-spawning
  call under ``src/anthropic`` passes a program name literal that is not an
  absolute path.

A match is a regular file (symlinks followed, so a *directory* named ``rg`` is
skipped) that is executable (``os.access(X_OK)``) on POSIX; on Windows
existence plus an allowed extension suffices. The result is
``normpath(join(entry, candidate))`` — not ``realpath``, so Homebrew/Scoop
symlink-farm spellings are preserved — and nothing is cached (``PATH`` and the
CWD can change; the walk is cheap).

Why not ``shutil.which(name, path=sanitized)``: on Windows CPython prepends
``os.curdir`` to the search list *even when* ``path=`` is given —
unconditionally before 3.12, and from 3.12 unless
``NoDefaultCurrentDirectoryInExePath`` is set — so the walk is hand-written.

This mirrors Claude Code's ``safeExecutableResolver``; keep it in sync with the
other Anthropic SDKs (claude-agent-sdk-python, anthropic-sdk-python,
anthropic-sdk-typescript, anthropic-sdk-go), which implement the same
guarantees against the same shared test vectors.
"""

from __future__ import annotations

import os
import re
import stat
import errno
import ntpath
import subprocess
from typing import Any, Final, cast
from collections.abc import Sequence

__all__ = [
    "WINDOWS_NATIVE_EXTENSIONS",
    "ExecutableNotFoundError",
    "find_executable",
    "require_executable",
    "resolve_argv",
    "run",
]

WINDOWS_NATIVE_EXTENSIONS: Final = (".exe", ".com")
"""Default Windows candidate extensions (G3): native images only — never
``.bat``/``.cmd`` and never extensionless."""

# The public functions look this up at call time; the pure helpers below take an
# explicit ``windows`` flag instead so the Windows rules are testable on any host.
_IS_WINDOWS = os.name == "nt"

# ``X:\…`` / ``X:/…`` — a drive letter, a colon and a separator. Drive-relative
# ``C:bin`` (resolved against the per-drive CWD) deliberately fails this.
_WINDOWS_DRIVE_ABSOLUTE_RE: Final = re.compile(r"^[A-Za-z]:[\\/]")
# ``\\server\share…`` — two separators, a server name, separator(s), a share.
_WINDOWS_UNC_RE: Final = re.compile(r"^[\\/]{2}[^\\/]+[\\/]+[^\\/]+")

# Not program names on any platform; short-circuit rather than generate
# candidates like ``..exe`` for them.
_NEVER_PROGRAM_NAMES: Final = frozenset({"", ".", ".."})


class ExecutableNotFoundError(FileNotFoundError):
    """Raised by :func:`require_executable` (and so :func:`resolve_argv` /
    :func:`run`) when a program cannot be resolved under G2–G4.

    Subclasses :class:`FileNotFoundError` so existing ``except OSError`` /
    ``except FileNotFoundError`` handlers around spawn sites keep working.
    """

    name: str
    """The program name (or explicit path) that could not be resolved."""

    def __init__(self, name: str) -> None:
        super().__init__(
            errno.ENOENT,
            "executable not found (only absolute PATH entries are searched; the current directory never is)",
            name,
        )
        self.name = name


def _strip_enclosing_quotes(entry: str) -> str:
    """``"C:\\Program Files\\X"`` → ``C:\\Program Files\\X`` (legal in a Windows ``PATH``)."""
    if len(entry) >= 2 and entry[0] == '"' and entry[-1] == '"':
        return entry[1:-1]
    return entry


def _is_searchable_path_entry(entry: str, *, windows: bool) -> bool:
    """G2: is this ``PATH`` entry *fully absolute* under the given flavour's rules?

    Empty, ``.``, relative, and (Windows) drive-relative ``C:bin`` /
    rooted-but-driveless ``\\bin`` entries are not — each of those would make the
    current working directory a search location.
    """
    if windows:
        entry = _strip_enclosing_quotes(entry)
        return bool(_WINDOWS_DRIVE_ABSOLUTE_RE.match(entry) or _WINDOWS_UNC_RE.match(entry))
    return entry.startswith("/")


def _candidate_names(
    name: str, *, windows: bool, windows_extensions: Sequence[str] = WINDOWS_NATIVE_EXTENSIONS
) -> list[str]:
    """G3: the file names to probe inside each searchable ``PATH`` entry for ``name``.

    POSIX: the name as-is. Windows: ``rg`` → ``[rg.exe, rg.com]``; ``rg.exe`` →
    ``[rg.exe]``; ``claude.cmd`` / ``tool.js`` → ``[]`` under the default
    allow-list (a caller may widen ``windows_extensions`` to *detect* a shim).
    """
    if not windows:
        return [name]
    lowered = name.lower()
    if any(lowered.endswith(ext.lower()) for ext in windows_extensions):
        return [name]
    if ntpath.splitext(name)[1]:
        return []
    return [name + ext for ext in windows_extensions]


def _is_explicit_path(name: str, *, windows: bool) -> bool:
    """G4: does ``name`` spell out a location (so no ``PATH`` search must happen)?"""
    if "/" in name:
        return True
    return windows and ("\\" in name or bool(ntpath.splitdrive(name)[0]))


def _is_executable_file(path: str, *, windows: bool) -> bool:
    """Regular file (symlinks followed — a directory named ``rg`` is not a match)
    and, on POSIX, executable by us. On Windows existence + extension suffices."""
    try:
        st = os.stat(path)
    except (OSError, ValueError):  # ValueError: embedded NUL and the like
        return False
    if not stat.S_ISREG(st.st_mode):
        return False
    return windows or os.access(path, os.X_OK)


def _find_executable(name: str, *, path: str, windows: bool, windows_extensions: Sequence[str]) -> str | None:
    """:func:`find_executable` with the platform flavour made explicit.

    ``windows`` selects the *rules* (entry check, candidate names, separator set,
    ``;`` vs ``:``); joining and probing always go through the host ``os.path`` /
    ``os.stat``, which is what lets the Windows rules be exercised on a POSIX host.
    """
    if name in _NEVER_PROGRAM_NAMES:
        return None
    if _is_explicit_path(name, windows=windows):
        explicit = os.path.abspath(name)
        return explicit if _is_executable_file(explicit, windows=windows) else None
    candidates = _candidate_names(name, windows=windows, windows_extensions=windows_extensions)
    if not candidates:
        return None
    for raw_entry in path.split(";" if windows else ":"):
        entry = _strip_enclosing_quotes(raw_entry) if windows else raw_entry
        if not _is_searchable_path_entry(entry, windows=windows):
            continue
        for candidate in candidates:
            full = os.path.normpath(os.path.join(entry, candidate))
            if _is_executable_file(full, windows=windows):
                return full
    return None


def find_executable(
    name: str,
    *,
    path: str | None = None,
    windows_extensions: Sequence[str] = WINDOWS_NATIVE_EXTENSIONS,
) -> str | None:
    """Resolve ``name`` to an absolute executable path, or ``None`` — never via the CWD.

    See the module docstring for the full contract. In short: only fully-absolute
    ``PATH`` entries are searched (G2); on Windows only ``windows_extensions``
    candidates — native ``.exe``/``.com`` images by default — can match (G3); a
    ``name`` containing a path separator is not searched for at all but checked
    as given, relative to the CWD if it is relative (G4); and any hit is returned
    as a normalised absolute path (G1).

    Args:
        name: Bare program name (``"rg"``) or an explicit path (``"./rg"``,
            ``"/usr/bin/rg"``).
        path: Search path to use instead of ``os.environ["PATH"]``. An unset or
            empty search path finds nothing.
        windows_extensions: Windows-only candidate extensions, tried in order.
            Widen it (e.g. add ``".cmd"``) only to *detect* a shim, not to run one.
    """
    return _find_executable(
        name,
        path=os.environ.get("PATH", "") if path is None else path,
        windows=_IS_WINDOWS,
        windows_extensions=windows_extensions,
    )


def require_executable(
    name: str,
    *,
    path: str | None = None,
    windows_extensions: Sequence[str] = WINDOWS_NATIVE_EXTENSIONS,
) -> str:
    """:func:`find_executable`, but raise :class:`ExecutableNotFoundError` instead of returning ``None``."""
    found = find_executable(name, path=path, windows_extensions=windows_extensions)
    if found is None:
        raise ExecutableNotFoundError(name)
    return found


def resolve_argv(
    argv: Sequence[str | os.PathLike[str]],
    *,
    path: str | None = None,
    windows_extensions: Sequence[str] = WINDOWS_NATIVE_EXTENSIONS,
) -> list[str]:
    """Return ``argv`` with ``argv[0]`` replaced by its :func:`require_executable`
    resolution (G1); the remaining arguments are passed through untouched.

    Use this in front of async spawn APIs (``anyio.open_process`` /
    ``anyio.run_process``), which are deliberately not wrapped here.
    """
    args = [os.fspath(arg) for arg in argv]
    if not args:
        raise ValueError("argv must contain at least the program to run")
    args[0] = require_executable(args[0], path=path, windows_extensions=windows_extensions)
    return args


def run(argv: Sequence[str | os.PathLike[str]], /, **kwargs: Any) -> subprocess.CompletedProcess[Any]:
    """``subprocess.run(resolve_argv(argv), **kwargs)`` — the blessed synchronous way
    to run a helper program by name. Raises :class:`ExecutableNotFoundError`
    (a :class:`FileNotFoundError`) when ``argv[0]`` cannot be resolved."""
    # ``cast``: with ``**kwargs`` pyright cannot pick a single ``subprocess.run``
    # overload (they differ only in the ``CompletedProcess`` type parameter).
    return cast("subprocess.CompletedProcess[Any]", subprocess.run(resolve_argv(argv), **kwargs))
