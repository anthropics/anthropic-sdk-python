"""G5 enforcement: no process-spawning call under ``src/anthropic`` may pass a
program *name* — only an absolute path literal, or a value computed at runtime
(which must come from :mod:`anthropic.lib._executable`; ``shutil.which`` and
``distutils.spawn.find_executable`` are banned separately by ruff's
``flake8-tidy-imports.banned-api`` table in ``pyproject.toml``).

A bare name handed to ``subprocess``/``anyio``/``os.exec*`` is resolved by the
OS or the C runtime, which on Windows searches the current working directory
first — the bug class behind HackerOne #3901184. See ``anthropic.lib._executable``.
"""

from __future__ import annotations

import re
import ast
from typing import NamedTuple
from pathlib import Path
from collections.abc import Iterator
from typing_extensions import override

import anthropic

# (module, function) → index of the positional argument that names the program.
_SPAWN_APIS: dict[tuple[str, str], int] = {
    ("subprocess", "run"): 0,
    ("subprocess", "Popen"): 0,
    ("subprocess", "call"): 0,
    ("subprocess", "check_call"): 0,
    ("subprocess", "check_output"): 0,
    ("subprocess", "getoutput"): 0,
    ("subprocess", "getstatusoutput"): 0,
    ("anyio", "open_process"): 0,
    ("anyio", "run_process"): 0,
    ("asyncio", "create_subprocess_exec"): 0,
    ("asyncio", "create_subprocess_shell"): 0,
    ("os", "system"): 0,
    ("os", "popen"): 0,
    ("os", "startfile"): 0,
    ("os", "posix_spawn"): 0,
    ("os", "posix_spawnp"): 0,
    **{("os", name): 0 for name in ("execl", "execle", "execlp", "execlpe", "execv", "execve", "execvp", "execvpe")},
    # os.spawn*(mode, file, ...): the program is the *second* argument.
    **{
        ("os", name): 1
        for name in ("spawnl", "spawnle", "spawnlp", "spawnlpe", "spawnv", "spawnve", "spawnvp", "spawnvpe")
    },
}
# Keyword spellings of the program argument across those APIs.
_PROGRAM_KEYWORDS = ("args", "command", "cmd", "program", "file", "path", "executable")

_WINDOWS_ABSOLUTE_RE = re.compile(r"^(?:[A-Za-z]:[\\/]|[\\/]{2}[^\\/]+[\\/]+[^\\/]+)")

SRC_ROOT = Path(anthropic.__file__).resolve().parent


class Violation(NamedTuple):
    path: str
    line: int
    call: str
    program: str

    @override
    def __str__(self) -> str:
        return f"{self.path}:{self.line}: {self.call}(...) launches non-absolute program {self.program!r}"


def _is_absolute_program(program: str) -> bool:
    return program.startswith("/") or bool(_WINDOWS_ABSOLUTE_RE.match(program))


def _import_aliases(tree: ast.AST) -> tuple[dict[str, str], dict[str, tuple[str, str]]]:
    """Map local names to what they import: ``import subprocess as sp`` →
    ``{"sp": "subprocess"}``; ``from anyio import run_process as rp`` →
    ``{"rp": ("anyio", "run_process")}``."""
    modules: dict[str, str] = {}
    names: dict[str, tuple[str, str]] = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                modules[alias.asname or alias.name.partition(".")[0]] = (
                    alias.name if alias.asname else alias.name.partition(".")[0]
                )
        elif isinstance(node, ast.ImportFrom) and node.module and node.level == 0:
            for alias in node.names:
                names[alias.asname or alias.name] = (node.module, alias.name)
                # ``from os import path`` style sub-module imports double as modules.
                modules.setdefault(alias.asname or alias.name, f"{node.module}.{alias.name}")
    return modules, names


def _resolve_call(func: ast.expr, modules: dict[str, str], names: dict[str, tuple[str, str]]) -> tuple[str, str] | None:
    if isinstance(func, ast.Name):
        return names.get(func.id)
    if isinstance(func, ast.Attribute):
        parts: list[str] = [func.attr]
        value = func.value
        while isinstance(value, ast.Attribute):
            parts.append(value.attr)
            value = value.value
        if not isinstance(value, ast.Name):
            return None
        module = modules.get(value.id)
        if module is None:
            return None
        dotted = ".".join([module, *reversed(parts[1:])])
        return dotted, parts[0]
    return None


def _program_literal(node: ast.expr) -> str | None:
    """The program named by a spawn argument iff it is spelled as a literal:
    ``"rg -n"`` → ``"rg"``; ``["rg", "-n"]`` → ``"rg"``; ``[rg, "-n"]`` → None."""
    if isinstance(node, (ast.List, ast.Tuple)):
        if not node.elts:
            return None
        node = node.elts[0]
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            return node.value
        return None
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        # Shell-style string: the program is the first word.
        return node.value.split(maxsplit=1)[0] if node.value.strip() else ""
    return None


def scan_source(source: str, path: str = "<string>") -> Iterator[Violation]:
    tree = ast.parse(source, filename=path)
    modules, names = _import_aliases(tree)
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        resolved = _resolve_call(node.func, modules, names)
        if resolved is None or resolved not in _SPAWN_APIS:
            continue
        index = _SPAWN_APIS[resolved]
        arg: ast.expr | None = None
        if len(node.args) > index and not any(isinstance(a, ast.Starred) for a in node.args[: index + 1]):
            arg = node.args[index]
        else:
            arg = next((kw.value for kw in node.keywords if kw.arg in _PROGRAM_KEYWORDS), None)
        if arg is None:
            continue
        program = _program_literal(arg)
        if program is not None and not _is_absolute_program(program):
            yield Violation(path, node.lineno, ".".join(resolved), program)


def test_no_bare_program_names_reach_a_spawn_api() -> None:
    sources = sorted(SRC_ROOT.rglob("*.py"))
    assert len(sources) > 100, f"expected to scan the installed `anthropic` package, found {len(sources)} files"
    violations = [
        str(v)
        for source in sources
        for v in scan_source(source.read_text(encoding="utf-8"), str(source.relative_to(SRC_ROOT.parent)))
    ]
    assert not violations, (
        "Never pass a bare program name to a process API — resolve it with "
        "anthropic.lib._executable (find_executable / resolve_argv / run) and spawn the absolute path:\n"
        + "\n".join(violations)
    )


# The snippets below are only ever *parsed* by the scanner, never executed.
_BAD_SNIPPET = """
import os
import os as operating_system
import anyio
import asyncio
import subprocess
import subprocess as sp
from subprocess import Popen, check_output as co
from anyio import open_process

subprocess.run(["rg", "-n", pattern])
sp.call(("git", "status"))
Popen("tar xzf archive.tgz", shell=True)
co(args=["unzip", "-l"])
anyio.run_process(["rg.exe", "--version"])
open_process(command="bash --noprofile")
asyncio.create_subprocess_exec("security", "find-generic-password")
os.execvp("claude", ["claude", "--version"])
operating_system.spawnv(os.P_WAIT, "node", ["node"])
os.system("where rg")
subprocess.run([r"..\\tools\\rg.exe"])
subprocess.run(["bin/rg"])
subprocess.run(["C:rg.exe"])
"""

_GOOD_SNIPPET = """
import os
import sys
import anyio
import subprocess
from anthropic.lib._executable import find_executable, resolve_argv, run

anyio.open_process(["/bin/bash", "--noprofile", "--norc"], cwd=workdir)
rg = find_executable("rg")
anyio.run_process([rg, "-n", pattern], check=False)
subprocess.run(resolve_argv(["git", "status"]))
subprocess.run([sys.executable, "-c", "print(1)"])
subprocess.run([r"C:\\Windows\\System32\\where.exe", "rg"])
subprocess.run([r"\\\\server\\share\\bin\\tool.exe"])
run(["git", "status"])  # the safe wrapper itself takes bare names by design
os.execv("/usr/bin/security", ["security"])
os.spawnv(os.P_WAIT, "/usr/bin/env", ["env"])
subprocess.run()  # malformed, but not this test's concern
"""


def test_scanner_flags_every_bare_name_form() -> None:
    """The scan above must not be vacuous: prove it catches each spelling."""
    found = [(v.call, v.program) for v in scan_source(_BAD_SNIPPET)]
    assert found == [
        ("subprocess.run", "rg"),
        ("subprocess.call", "git"),
        ("subprocess.Popen", "tar"),
        ("subprocess.check_output", "unzip"),
        ("anyio.run_process", "rg.exe"),
        ("anyio.open_process", "bash"),
        ("asyncio.create_subprocess_exec", "security"),
        ("os.execvp", "claude"),
        ("os.spawnv", "node"),
        ("os.system", "where"),
        ("subprocess.run", "..\\tools\\rg.exe"),
        ("subprocess.run", "bin/rg"),
        ("subprocess.run", "C:rg.exe"),
    ]


def test_scanner_accepts_absolute_paths_and_resolved_values() -> None:
    assert list(scan_source(_GOOD_SNIPPET)) == []
