from __future__ import annotations

import os
import sys
from pathlib import Path

import anyio
import pytest

from anthropic._compat import PYDANTIC_V1
from anthropic.lib.tools import ToolError
from anthropic.lib.tools.agent_toolset import (
    BashSession,
    AgentToolContext,
    resolve_path,
    beta_edit_tool,
    beta_glob_tool,
    beta_grep_tool,
    beta_read_tool,
    beta_write_tool,
    beta_agent_toolset_20260401,
)

needs_pydantic_v2 = pytest.mark.skipif(PYDANTIC_V1, reason="tool functions are only supported with pydantic v2")


@pytest.mark.parametrize(
    ("description", "p", "unrestricted", "expect_error"),
    [
        ("relative path inside workdir resolves", "a/b.txt", False, False),
        ("dot-dot that stays inside workdir resolves", "a/../b.txt", False, False),
        ("dot-dot that escapes workdir is rejected", "../etc/passwd", False, True),
        ("absolute path is rejected by default", "/etc/passwd", False, True),
        ("absolute path is allowed when unrestricted_paths is set", "/etc/passwd", True, False),
    ],
)
def test_resolve_path(tmp_path: Path, description: str, p: str, unrestricted: bool, expect_error: bool) -> None:
    env = AgentToolContext(workdir=str(tmp_path), unrestricted_paths=unrestricted)
    if expect_error:
        with pytest.raises(ValueError):
            resolve_path(env, p)
    else:
        assert resolve_path(env, p), description


def test_resolve_path_segment_aware_sibling(tmp_path: Path) -> None:
    """A sibling directory sharing a prefix (workdir vs workdir2) must not satisfy the jail."""
    root = tmp_path / "work"
    root.mkdir()
    env = AgentToolContext(workdir=str(root))
    with pytest.raises(ValueError):
        resolve_path(env, "../work2/file")


@needs_pydantic_v2
def test_agent_toolset_names_and_type(tmp_path: Path) -> None:
    env = AgentToolContext(workdir=str(tmp_path))
    names = [t.name for t in beta_agent_toolset_20260401(env)]
    assert names == ["bash", "read", "write", "edit", "glob", "grep"]


@needs_pydantic_v2
async def test_agent_toolset_filter_and_extend(tmp_path: Path) -> None:
    """The list returned by beta_agent_toolset_20260401 is a plain list that callers can filter or extend."""
    env = AgentToolContext(workdir=str(tmp_path))
    subset = [t for t in beta_agent_toolset_20260401(env) if t.name not in ("bash", "grep")]
    assert [t.name for t in subset] == ["read", "write", "edit", "glob"]
    extended = [*subset, beta_read_tool(env)]
    assert extended[-1].name == "read"


@needs_pydantic_v2
async def test_read_write_edit_roundtrip(tmp_path: Path) -> None:
    env = AgentToolContext(workdir=str(tmp_path))

    msg = await beta_write_tool(env).call({"file_path": "f.txt", "content": "hello world"})
    assert isinstance(msg, str)
    assert "wrote" in msg

    text = await beta_read_tool(env).call({"file_path": "f.txt"})
    assert text == "hello world"

    await beta_edit_tool(env).call({"file_path": "f.txt", "old_string": "world", "new_string": "there"})
    assert (tmp_path / "f.txt").read_text() == "hello there"


@needs_pydantic_v2
async def test_read_view_range(tmp_path: Path) -> None:
    (tmp_path / "f.txt").write_text("a\nb\nc\nd\n")
    env = AgentToolContext(workdir=str(tmp_path))
    out = await beta_read_tool(env).call({"file_path": "f.txt", "view_range": [2, 3]})
    assert out == "b\nc"


@needs_pydantic_v2
async def test_read_rejects_oversized_file(tmp_path: Path) -> None:
    (tmp_path / "big.txt").write_bytes(b"a" * (257 * 1024))
    env = AgentToolContext(workdir=str(tmp_path))
    with pytest.raises(ToolError, match="exceeds"):
        await beta_read_tool(env).call({"file_path": "big.txt"})


@needs_pydantic_v2
async def test_read_rejects_directory(tmp_path: Path) -> None:
    (tmp_path / "sub").mkdir()
    env = AgentToolContext(workdir=str(tmp_path))
    with pytest.raises(ToolError, match="not a regular file"):
        await beta_read_tool(env).call({"file_path": "sub"})


@needs_pydantic_v2
async def test_edit_rejects_oversized_file(tmp_path: Path) -> None:
    (tmp_path / "big.txt").write_bytes(b"a" * (257 * 1024))
    env = AgentToolContext(workdir=str(tmp_path))
    with pytest.raises(ToolError, match="exceeds"):
        await beta_edit_tool(env).call({"file_path": "big.txt", "old_string": "a", "new_string": "b"})


@needs_pydantic_v2
async def test_edit_rejects_directory(tmp_path: Path) -> None:
    (tmp_path / "sub").mkdir()
    env = AgentToolContext(workdir=str(tmp_path))
    with pytest.raises(ToolError, match="not a regular file"):
        await beta_edit_tool(env).call({"file_path": "sub", "old_string": "a", "new_string": "b"})


@needs_pydantic_v2
async def test_edit_normal_within_limit(tmp_path: Path) -> None:
    (tmp_path / "f.txt").write_text("hello world")
    env = AgentToolContext(workdir=str(tmp_path))
    await beta_edit_tool(env).call({"file_path": "f.txt", "old_string": "world", "new_string": "there"})
    assert (tmp_path / "f.txt").read_text() == "hello there"


@needs_pydantic_v2
async def test_edit_custom_max_bytes_rejects_below_cap(tmp_path: Path) -> None:
    (tmp_path / "f.txt").write_bytes(b"OLD" + b"\x00" * 2000)
    env = AgentToolContext(workdir=str(tmp_path), max_file_bytes=1024)
    with pytest.raises(ToolError, match="exceeds"):
        await beta_edit_tool(env).call({"file_path": "f.txt", "old_string": "OLD", "new_string": "NEW"})


@needs_pydantic_v2
async def test_edit_custom_max_bytes_allows_above_default(tmp_path: Path) -> None:
    (tmp_path / "f.txt").write_bytes(b"OLD" + b"\x00" * (257 * 1024))
    env = AgentToolContext(workdir=str(tmp_path), max_file_bytes=512 * 1024)
    await beta_edit_tool(env).call({"file_path": "f.txt", "old_string": "OLD", "new_string": "NEW"})
    assert (tmp_path / "f.txt").read_bytes()[:3] == b"NEW"


@needs_pydantic_v2
async def test_edit_uncapped_allows_oversized(tmp_path: Path) -> None:
    (tmp_path / "f.txt").write_bytes(b"OLD" + b"\x00" * (257 * 1024))
    env = AgentToolContext(workdir=str(tmp_path), max_file_bytes=None)
    await beta_edit_tool(env).call({"file_path": "f.txt", "old_string": "OLD", "new_string": "NEW"})


@needs_pydantic_v2
async def test_edit_rejects_directory_even_when_uncapped(tmp_path: Path) -> None:
    (tmp_path / "sub").mkdir()
    env = AgentToolContext(workdir=str(tmp_path), max_file_bytes=None)
    with pytest.raises(ToolError, match="not a regular file"):
        await beta_edit_tool(env).call({"file_path": "sub", "old_string": "a", "new_string": "b"})


@needs_pydantic_v2
async def test_read_custom_max_bytes_rejects_below_cap(tmp_path: Path) -> None:
    (tmp_path / "f.txt").write_bytes(b"a" * 2000)
    env = AgentToolContext(workdir=str(tmp_path), max_file_bytes=1024)
    with pytest.raises(ToolError, match="exceeds"):
        await beta_read_tool(env).call({"file_path": "f.txt"})


@needs_pydantic_v2
async def test_read_uncapped_allows_oversized(tmp_path: Path) -> None:
    (tmp_path / "big.txt").write_bytes(b"a" * (257 * 1024))
    env = AgentToolContext(workdir=str(tmp_path), max_file_bytes=None)
    await beta_read_tool(env).call({"file_path": "big.txt"})


@needs_pydantic_v2
async def test_read_rejects_directory_even_when_uncapped(tmp_path: Path) -> None:
    (tmp_path / "sub").mkdir()
    env = AgentToolContext(workdir=str(tmp_path), max_file_bytes=None)
    with pytest.raises(ToolError, match="not a regular file"):
        await beta_read_tool(env).call({"file_path": "sub"})


@pytest.mark.parametrize(
    ("description", "args", "want_error"),
    [
        (
            "edit fails when old_string is absent from the file",
            {"file_path": "f.txt", "old_string": "nope", "new_string": "x"},
            True,
        ),
        (
            "edit fails when old_string is non-unique and replace_all is false",
            {"file_path": "f.txt", "old_string": "ab", "new_string": "x"},
            True,
        ),
        (
            "edit succeeds on non-unique old_string when replace_all is true",
            {"file_path": "f.txt", "old_string": "ab", "new_string": "x", "replace_all": True},
            False,
        ),
    ],
)
@needs_pydantic_v2
async def test_edit_uniqueness(tmp_path: Path, description: str, args: dict[str, object], want_error: bool) -> None:
    (tmp_path / "f.txt").write_text("ab ab")
    env = AgentToolContext(workdir=str(tmp_path))
    tool = beta_edit_tool(env)
    if want_error:
        with pytest.raises(ToolError):
            await tool.call(args)
    else:
        assert await tool.call(args), description


@needs_pydantic_v2
async def test_glob_mtime_order(tmp_path: Path) -> None:
    a = tmp_path / "a.txt"
    b = tmp_path / "b.txt"
    a.write_text("a")
    b.write_text("b")
    os.utime(a, (1, 1))
    os.utime(b, (2, 2))
    env = AgentToolContext(workdir=str(tmp_path))
    res = await beta_glob_tool(env).call({"pattern": "*.txt"})
    assert isinstance(res, str)
    lines = res.splitlines()
    assert lines[0].endswith("b.txt") and lines[1].endswith("a.txt")


@needs_pydantic_v2
async def test_glob_with_path(tmp_path: Path) -> None:
    (tmp_path / "sub").mkdir()
    (tmp_path / "sub" / "a.txt").write_text("a")
    (tmp_path / "b.txt").write_text("b")
    env = AgentToolContext(workdir=str(tmp_path))
    res = await beta_glob_tool(env).call({"pattern": "*.txt", "path": "sub"})
    assert isinstance(res, str)
    assert res.endswith("a.txt")
    assert "b.txt" not in res


@needs_pydantic_v2
async def test_grep_finds_match(tmp_path: Path) -> None:
    (tmp_path / "x.txt").write_text("foo\nbar\nbaz\n")
    env = AgentToolContext(workdir=str(tmp_path))
    res = await beta_grep_tool(env).call({"pattern": "ba.", "path": "."})
    assert isinstance(res, str)
    assert "bar" in res and "baz" in res


@needs_pydantic_v2
async def test_grep_single_file_path(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Fallback walker must handle a file path, not just directories."""
    (tmp_path / "x.txt").write_text("alpha\nbeta\n")
    env = AgentToolContext(workdir=str(tmp_path))
    monkeypatch.setattr("shutil.which", lambda _name: None)  # type: ignore[arg-type]
    res = await beta_grep_tool(env).call({"pattern": "beta", "path": "x.txt"})
    assert isinstance(res, str)
    assert "beta" in res
    assert res != "no matches"


@pytest.mark.skipif(sys.platform == "win32", reason="bash session requires /bin/bash")
async def test_bash_session_persistence(tmp_path: Path) -> None:
    s = await BashSession.start(str(tmp_path))
    try:
        out, code = await s.exec("export FOO=bar; echo set")
        assert (out, code) == ("set", 0)
        out, code = await s.exec("echo $FOO")
        assert (out, code) == ("bar", 0)
    finally:
        await s.close()


@pytest.mark.skipif(sys.platform == "win32", reason="bash session requires /bin/bash")
async def test_bash_timeout(tmp_path: Path) -> None:
    s = await BashSession.start(str(tmp_path))
    with pytest.raises(TimeoutError):
        await s.exec("sleep 5", timeout=0.2)


@pytest.mark.skipif(sys.platform == "win32", reason="bash session requires /bin/bash")
async def test_bash_sentinel_not_spoofable(tmp_path: Path) -> None:
    """A command that prints a hardcoded marker can't truncate output or spoof the exit code."""
    s = await BashSession.start(str(tmp_path))
    try:
        out, code = await s.exec("printf '__ANT_CMD_DONE__7\\nafter\\n'; (exit 3)")
        assert "__ANT_CMD_DONE__7" in out
        assert "after" in out
        assert code == 3
    finally:
        await s.close()


@pytest.mark.skipif(sys.platform == "win32", reason="bash session requires /bin/bash")
async def test_bash_stdin_redirect(tmp_path: Path) -> None:
    """A stdin-reading command gets immediate EOF instead of hanging until timeout."""
    s = await BashSession.start(str(tmp_path))
    try:
        out, code = await s.exec("cat; echo done", timeout=2.0)
        assert out == "done"
        assert code == 0
    finally:
        await s.close()


@pytest.mark.skipif(sys.platform == "win32", reason="bash session requires /bin/bash")
async def test_bash_session_closed_property(tmp_path: Path) -> None:
    """``closed`` is the inverse of the old ``alive`` (TS parity) and there is
    no ``alive`` attribute any more."""
    s = await BashSession.start(str(tmp_path))
    assert s.closed is False
    assert not hasattr(s, "alive")
    await s.close()
    assert s.closed is True
    # A closed session refuses further commands rather than silently hanging.
    with pytest.raises(RuntimeError, match="terminated"):
        await s.exec("echo nope")


@pytest.mark.skipif(sys.platform == "win32", reason="bash session requires /bin/bash")
async def test_bash_outer_cancel_closes_subprocess_no_stale_state(tmp_path: Path) -> None:
    """Regression: a cancellation from an *outer* scope (e.g. the session
    runner's ``TOOL_TIMEOUT``) during a bash exec must tear the subprocess down,
    so the next call can't read the cancelled command's stale output/sentinel.

    anyio raises an outer-scope cancel as a plain ``Cancelled`` (not
    ``TimeoutError``), so the ``except TimeoutError`` cleanup never runs — only
    the new ``except get_cancelled_exc_class()`` path saves us here.
    """
    s = await BashSession.start(str(tmp_path))
    try:
        # The inner per-call timeout is huge; an OUTER scope cancels first,
        # mid-command, while `sleep` is producing no output.
        with anyio.move_on_after(0.3):
            await s.exec("sleep 5; echo STALE_MARKER", timeout=120.0)

        # The outer cancel fired mid-exec. The subprocess must have been closed
        # (not left alive with `sleep 5; echo STALE_MARKER` still queued).
        assert s.closed is True
        # And because it's closed, the next exec refuses outright — it can NOT
        # hand back the previous command's STALE_MARKER output + old sentinel.
        with pytest.raises(RuntimeError, match="terminated"):
            await s.exec("echo NEXT")
    finally:
        await s.close()


@needs_pydantic_v2
async def test_read_through_symlink_escape_is_rejected(tmp_path: Path) -> None:
    """resolve_path realpaths, so a symlink that escapes the workdir is caught."""
    outside = tmp_path / "outside"
    outside.mkdir()
    (outside / "secret.txt").write_text("secret")
    work = tmp_path / "work"
    work.mkdir()
    (work / "escape").symlink_to(outside)
    env = AgentToolContext(workdir=str(work))
    with pytest.raises(ToolError, match="escapes workdir"):
        await beta_read_tool(env).call({"file_path": "escape/secret.txt"})


@needs_pydantic_v2
async def test_glob_rejects_dotdot_pattern(tmp_path: Path) -> None:
    """``Path.glob`` honours literal ``..`` segments — the tool must reject a
    pattern that would walk out of the workdir before it ever runs."""
    outside = tmp_path / "outside"
    outside.mkdir()
    (outside / "secret.txt").write_text("secret")
    work = tmp_path / "work"
    work.mkdir()
    env = AgentToolContext(workdir=str(work))
    with pytest.raises(ToolError, match=r"\.\."):
        await beta_glob_tool(env).call({"pattern": "../outside/*.txt"})


@needs_pydantic_v2
async def test_glob_post_filters_symlink_escape(tmp_path: Path) -> None:
    """A symlink traversed mid-pattern must not let a glob result escape the workdir."""
    outside = tmp_path / "outside"
    outside.mkdir()
    (outside / "secret.txt").write_text("secret")
    work = tmp_path / "work"
    work.mkdir()
    (work / "escape").symlink_to(outside)
    env = AgentToolContext(workdir=str(work))
    res = await beta_glob_tool(env).call({"pattern": "escape/*.txt"})
    assert res == "no matches"


@needs_pydantic_v2
async def test_grep_skips_symlinked_files(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """The fallback walker must not read through a symlink that escapes the workdir."""
    secret = tmp_path / "secret.txt"
    secret.write_text("TOPSECRET")
    work = tmp_path / "work"
    work.mkdir()
    (work / "leak").symlink_to(secret)
    (work / "real.txt").write_text("ordinary\n")
    env = AgentToolContext(workdir=str(work))
    monkeypatch.setattr("shutil.which", lambda _name: None)  # type: ignore[arg-type]
    res = await beta_grep_tool(env).call({"pattern": "TOPSECRET"})
    assert res == "no matches"
