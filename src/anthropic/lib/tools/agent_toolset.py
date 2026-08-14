"""Reference implementations of the ``agent_toolset_20260401`` tools — ``bash``,
``read``, ``write``, ``edit``, ``glob``, ``grep`` — plus the workdir/skills
:class:`AgentToolContext`.

This sits next to the other ``lib/tools`` helpers (the Messages tool runner, the
memory tool, …). Importing it pulls in ``subprocess`` etc., so it is kept out of
``anthropic.lib.tools.__init__`` — depend on it explicitly
(``from anthropic.lib.tools.agent_toolset import beta_agent_toolset_20260401``).

The result of :func:`beta_agent_toolset_20260401` is a plain
``list[BetaAsyncFunctionTool]`` — *async* function tools, so it is for the
**async** runners only: ``client.beta.sessions.events.tool_runner(...)`` (the
``SessionToolRunner``, always async) for a managed-agents session, or — via the
:class:`~anthropic.lib.environments.EnvironmentWorker` — the self-hosted
environment worker. The sync ``Anthropic`` ``messages.tool_runner`` accepts
``BetaRunnableTool``, which excludes the async function tools this returns, so
it cannot consume this toolset.

.. warning::
   ``bash`` is **stateful**: it owns a persistent ``/bin/bash`` subprocess that
   is only torn down by its ``close`` cleanup hook. Only ``SessionToolRunner``
   (and the ``EnvironmentWorker`` built on it) invoke that hook. The Messages
   ``client.beta.messages.tool_runner(...)`` does **not** call ``close``, so
   handing this toolset to the Messages tool runner leaks the bash subprocess
   (one orphaned shell per run). Run stateful tools under
   ``client.beta.sessions.events.tool_runner(...)`` / the environment worker,
   or drop ``bash`` from the toolset before using the Messages tool runner.

Trust model: the file tools confine to ``workdir`` (symlink-aware) and are safe
without a sandbox; ``bash`` is unrestricted and should run inside one. See
:class:`AgentToolContext`.
"""

from __future__ import annotations

import os
import re
import uuid
import base64
import shutil
import logging
import subprocess
from stat import S_ISREG
from typing import TYPE_CHECKING, Any, List, Optional, NamedTuple, cast
from pathlib import Path, PurePosixPath
from functools import partial
from itertools import islice
from contextlib import asynccontextmanager
from dataclasses import field, dataclass
from collections.abc import Mapping, Callable, Awaitable, AsyncIterator

import anyio
import anyio.abc
from anyio.to_thread import run_sync

from ._skills import _within, download_session_skills
from ..._types import NotGiven, not_given
from ..._utils import is_given
from ...types.beta import (
    BetaManagedAgentsAgentToolset20260401BashInput,
    BetaManagedAgentsAgentToolset20260401EditInput,
    BetaManagedAgentsAgentToolset20260401GlobInput,
    BetaManagedAgentsAgentToolset20260401GrepInput,
    BetaManagedAgentsAgentToolset20260401ReadInput,
    BetaManagedAgentsAgentToolset20260401WriteInput,
)
from ._beta_functions import (
    ToolError,
    BetaContent,
    BetaAsyncFunctionTool,
    BetaFunctionToolResultType,
    beta_async_tool,
)

if TYPE_CHECKING:
    from ..._client import AsyncAnthropic

__all__ = [
    "AgentToolContext",
    "BashSession",
    "BashResult",
    "resolve_path",
    "beta_agent_toolset_20260401",
    "beta_bash_tool",
    "beta_read_tool",
    "beta_write_tool",
    "beta_edit_tool",
    "beta_glob_tool",
    "beta_grep_tool",
]

BASH_OUTPUT_LIMIT = 100 * 1024
BASH_DEFAULT_TIMEOUT = 120.0
DEFAULT_MAX_FILE_BYTES = 256 * 1024
READ_MAX_BYTES = DEFAULT_MAX_FILE_BYTES  # For backwards compat only.
# Default image/PDF caps for the binary ``read`` path (overridable on
# :class:`AgentToolContext`, same shape as ``max_file_bytes``). The API
# enforces a per-image limit on the *encoded* (base64) form and a total
# request-size limit that the raw-PDF cap stays under after the ~4/3 base64
# inflation; an oversized block would be rejected at request time, so reject
# it here with a clear error instead. The spec doesn't publish these limits, so
# they can't be codegen'd; if the API raises them, the only cost of these going
# stale is rejecting a file early that the API would now accept — bump them
# here (or override them on the context) when that happens.
DEFAULT_MAX_IMAGE_BASE64_BYTES = 5 * 1024 * 1024
DEFAULT_MAX_PDF_BYTES = 20 * 1024 * 1024
READ_IMAGE_MAX_BASE64_BYTES = DEFAULT_MAX_IMAGE_BASE64_BYTES  # For backwards compat only.
READ_PDF_MAX_BYTES = DEFAULT_MAX_PDF_BYTES  # For backwards compat only.
# Extension → media type for files ``read`` returns as base64 content blocks
# rather than text. The supported media types ARE codegen'd
# (``BetaBase64ImageSourceParam`` / ``BetaBase64PDFSourceParam``); a test pins
# this map's values to those literals, so a spec change that adds or removes a
# media type fails CI until the map is updated. Not user-configurable (yet).
_BINARY_MEDIA_TYPES = {
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".gif": "image/gif",
    ".webp": "image/webp",
    ".pdf": "application/pdf",
}
GREP_OUTPUT_LIMIT = 100 * 1024
GREP_MAX_LINE_LENGTH = 2000
GLOB_RESULT_LIMIT = 200
WALK_MAX_ENTRIES = 50_000
_ANSI = re.compile(r"\x1b\[[0-9;?]*[ -/]*[@-~]")


def _resolve_max_bytes(configured: int | None | NotGiven, default: int = DEFAULT_MAX_FILE_BYTES) -> int | None:
    """Resolve a configured cap to an effective size limit.

    ``not_given`` selects ``default``; ``None`` disables the size check
    (uncapped); a positive int is the cap. Governs only the size guard — callers
    still reject non-regular files.
    """
    return configured if is_given(configured) else default


log = logging.getLogger("anthropic.lib.tools.agent_toolset")


def _default_bash_env() -> dict[str, str]:
    """The environment for the bash subprocess, with the runner's own
    credentials scrubbed.

    The bash tool runs model-issued commands, so it must never inherit the
    runner's ``ANTHROPIC_*`` variables (API key, environment key, per-work
    session tokens): a prompt-injected ``echo $ANTHROPIC_API_KEY`` would
    otherwise land the credential straight in the session transcript. Passing
    an explicit ``env`` to :class:`AgentToolContext` does NOT add to this
    default — it FULLY REPLACES it. The provided mapping becomes the entire
    bash environment verbatim; nothing here is merged in, so callers who want
    the scrubbed process environment plus extras must build that mapping
    themselves.
    """
    return {k: v for k, v in os.environ.items() if not k.startswith("ANTHROPIC_")}


def _fs_error(op: str, file_path: str, e: OSError) -> ToolError:
    """Map a filesystem ``OSError`` to a consistent, runtime-independent message.

    The raw ``OSError`` string is platform-specific (``[Errno 2] ENOENT: ...``);
    normalise the common cases so the model sees the same wording everywhere.
    """
    if isinstance(e, FileNotFoundError):
        reason = "no such file or directory"
    elif isinstance(e, NotADirectoryError):
        reason = "not a directory"
    elif isinstance(e, IsADirectoryError):
        reason = "is a directory"
    elif isinstance(e, PermissionError):
        reason = "permission denied"
    elif isinstance(e, FileExistsError):
        reason = "file already exists"
    else:
        reason = (e.strerror or "i/o error").lower()
    return ToolError(f"{op}: {file_path}: {reason}")


def _empty_skill_dirs() -> list[Path]:
    return []


@dataclass
class AgentToolContext:
    """Workdir + path-policy for the agent toolset.

    Trust model — two tiers:

    - The file tools (:func:`beta_read_tool`, :func:`beta_write_tool`,
      :func:`beta_edit_tool`, :func:`beta_glob_tool`, :func:`beta_grep_tool`)
      resolve paths against ``workdir`` and reject escapes unless
      ``unrestricted_paths`` is set. :func:`resolve_path` follows every symlink
      (including the leaf, even a dangling one) before the check and returns
      that canonical path for the operation, so a symlink inside the workdir
      that points outside it can neither pass the check nor be followed
      afterwards — a real boundary, consistent with the memory tool, so the
      file tools are safe to use without a sandbox.
    - :func:`beta_bash_tool` runs an unrestricted ``/bin/bash`` regardless of
      ``unrestricted_paths``. Confinement for it must come from the OS layer
      (e.g. a self-hosted environment runner).

    Attributes:
        workdir: Base directory for resolving relative tool paths. Defaults to
            :func:`os.getcwd` captured when the context is constructed (TS
            parity: ``process.cwd()`` at construction), so a ``chdir`` between
            constructing this context and the first tool call does not move
            where paths resolve. Pass an explicit path to override.
        unrestricted_paths: When ``False`` (default), the file tools reject
            paths that resolve outside ``workdir``. Does **not**
            constrain :func:`beta_bash_tool`.
        env: Optional environment for the bash subprocess. When unset, the bash
            tool inherits the process environment with the runner's
            ``ANTHROPIC_*`` credentials scrubbed. When provided, it FULLY
            REPLACES that default environment — the mapping is used verbatim
            and is NOT merged with or added to the scrubbed process
            environment. To keep the defaults plus extra vars, build the
            combined mapping yourself before passing it.
        max_file_bytes: Size cap for the ``read`` and ``edit`` tools, which both
            load the whole file into memory. ``not_given`` (default) uses the
            built-in 256 KiB cap; a positive int sets a custom cap; ``None``
            disables the cap entirely. Disabling it reintroduces the OOM risk on
            a model-controlled path, so pass ``None`` only when the sandbox can
            absorb arbitrarily large files. The non-regular-file (FIFO/device)
            guard always applies regardless of this value. Image/PDF files,
            which ``read`` returns as base64 content blocks, are not subject to
            the 256 KiB default (``max_image_base64_bytes`` /
            ``max_pdf_bytes`` govern instead), but an explicit positive cap
            binds them too.
        max_image_base64_bytes: Cap on the *base64-encoded* size of an image
            ``read`` returns as a content block. ``not_given`` (default)
            uses the built-in 5 MiB cap — a memory bound plus the API's
            per-image limit; a positive int overrides it; ``None`` disables it
            (only ``max_file_bytes`` / the API's own limit then apply).
        max_pdf_bytes: Cap on the raw size of a PDF ``read`` returns as a
            document block. ``not_given`` (default) uses the built-in 20 MiB
            cap; a positive int overrides it; ``None`` disables it.
    """

    # ``default_factory`` (not a literal "." ) so the cwd is snapshotted at
    # *construction* time, not resolved lazily at first use — a chdir in
    # between must not change where tools resolve paths (TS parity).
    workdir: str | os.PathLike[str] = field(default_factory=os.getcwd)
    unrestricted_paths: bool = False
    # When ``client`` and ``session_id`` are both set, entering the context
    # manager fetches the session's resolved agent and downloads each of its
    # skills into ``{workdir}/skills/<name>/`` before any tool runs.
    client: AsyncAnthropic | None = None
    session_id: str | None = None
    env: Optional[Mapping[str, str]] = None
    max_file_bytes: int | None | NotGiven = not_given
    max_image_base64_bytes: int | None | NotGiven = not_given
    max_pdf_bytes: int | None | NotGiven = not_given
    _bash: BashSession | None = field(default=None, init=False, repr=False)
    # Skill directories downloaded by ``setup_skills``; removed again on
    # ``__aexit__`` so a context doesn't leave downloaded skills behind.
    _skill_dirs: list[Path] = field(default_factory=_empty_skill_dirs, init=False, repr=False)

    async def bash(self) -> BashSession:
        if self._bash is None:
            self._bash = await BashSession.start(self.workdir, env=self.env)
        return self._bash

    async def close(self) -> None:
        if self._bash is not None:
            await self._bash.close()
            self._bash = None

    async def setup_skills(self) -> None:
        """Download the session agent's skills into ``{workdir}/skills/<name>/``.

        No-op unless both :attr:`client` and :attr:`session_id` are set. The
        download + safe archive extraction lives in
        :mod:`anthropic.lib.tools._skills`.
        """
        if self.client is None or self.session_id is None:
            return
        self._skill_dirs = await download_session_skills(self.client, session_id=self.session_id, workdir=self.workdir)

    async def _cleanup_skills(self) -> None:
        """Remove the skill directories :meth:`setup_skills` downloaded.

        Only the directories this context created are removed — a pre-existing
        ``{workdir}/skills`` tree is left untouched.
        """
        for skill_dir in self._skill_dirs:
            try:
                # ``shutil.rmtree`` is blocking; keep it off the event loop.
                await run_sync(partial(shutil.rmtree, skill_dir, ignore_errors=True))
            except Exception as e:
                log.warning("failed to remove downloaded skill dir %s: %s", skill_dir, e)
        self._skill_dirs = []

    async def __aenter__(self) -> AgentToolContext:
        await self.setup_skills()
        return self

    async def __aexit__(self, *exc: object) -> None:
        try:
            await self.close()
        finally:
            await self._cleanup_skills()


def resolve_path(ctx: AgentToolContext, p: str) -> Path:
    """Resolve ``p`` against the workdir; reject results that escape it.

    Absolute and relative inputs go through the same canonicalise-then-contain
    check — an absolute path that lands inside the workdir is permitted, only
    paths that resolve *outside* are rejected. ``Path.resolve()`` follows every
    symlink (including the leaf, even a dangling one) before the containment
    check, so a symlink under the workdir that targets ``/etc`` is rejected —
    and the resolved path is what the tool then operates on, so it can't be
    followed afterwards either. See the trust model on :class:`AgentToolContext`.
    """
    candidate = Path(p)
    if ctx.unrestricted_paths and candidate.is_absolute():
        return candidate.resolve()
    root = Path(ctx.workdir).resolve()
    full = (candidate if candidate.is_absolute() else root / candidate).resolve()
    if not ctx.unrestricted_paths and not _within(full, root):
        raise ValueError(f"path {p!r} escapes workdir")
    return full


class BashResult(NamedTuple):
    """Result of :meth:`BashSession.exec` — the captured output and exit code.

    A ``NamedTuple`` so it unpacks positionally (``out, code = await s.exec(...)``)
    and reads by name (``result.output`` / ``result.exit_code``) interchangeably.
    """

    output: str
    """The command's combined stdout + stderr (ANSI escapes stripped, possibly
    truncated to the last :data:`BASH_OUTPUT_LIMIT` bytes)."""

    exit_code: int
    """The command's exit status. ``-1`` when the exit code could not be parsed
    from the shell sentinel (e.g. truncated output)."""


class BashSession:
    """A persistent ``/bin/bash`` process; cwd, env and jobs survive across calls.

    .. warning::
        :class:`BashSession` is **stateful and not safe to share concurrently**.
        Interleaved :meth:`exec` calls would race for the same stdin/stdout
        pipes (mixed input, output read by the wrong caller, and corrupted
        sentinel detection). Each :class:`AgentToolContext` creates its own
        session, so the safe pattern is *one context per session* — never a
        single ``AgentToolContext`` (or hand-constructed ``BashSession``) shared
        across multiple sessions running on different self-hosted environments.
        Holding the shared instance behind a per-call lock would serialize all
        bash work and is almost certainly not what you want.
    """

    def __init__(self, proc: anyio.abc.Process) -> None:
        """Use :meth:`BashSession.start` to construct — ``__init__`` takes an
        already-spawned process and is intended for internal use."""
        self._proc = proc

    @classmethod
    async def start(cls, workdir: str | os.PathLike[str], *, env: Optional[Mapping[str, str]] = None) -> BashSession:
        base = dict(env) if env is not None else _default_bash_env()
        proc = await anyio.open_process(
            ["/bin/bash", "--noprofile", "--norc"],
            cwd=workdir,
            env={**base, "PS1": "", "PS2": "", "TERM": "dumb"},
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        return cls(proc)

    @property
    def closed(self) -> bool:
        """Whether the underlying bash process has exited / been torn down.

        Inverse of "alive". Named ``closed`` (not ``alive``) to match the TS
        ``BashSession.closed`` boolean — porting code between the two SDKs
        should not have to flip the sense of this check.
        """
        return self._proc.returncode is not None

    async def exec(self, cmd: str, timeout: float = BASH_DEFAULT_TIMEOUT) -> BashResult:
        if self.closed:
            raise RuntimeError("bash session terminated; restart required")
        assert self._proc.stdin is not None and self._proc.stdout is not None
        stdin = self._proc.stdin
        stdout = self._proc.stdout
        # Per-call nonce so a command that prints a fixed marker can't spoof the
        # exit-code framing. The `''` split keeps the literal out of what we
        # write to stdin — only the shell's printf reassembles it.
        sentinel = f"__ANT_CMD_{uuid.uuid4().hex}_DONE__"
        sentinel_split = f"{sentinel[:8]}''{sentinel[8:]}"
        # </dev/null: a stdin-reading command (`cat`, `read`) gets EOF instead
        # of blocking on the shared pipe until the timeout.
        wrapped = f"{{ {cmd}\n}} </dev/null 2>&1; printf '\\n{sentinel_split}%d\\n' $?\n"
        await stdin.send(wrapped.encode())

        buf = bytearray()
        truncated = False
        marker = sentinel.encode()

        async def read_until_sentinel() -> None:
            nonlocal truncated
            while True:
                try:
                    chunk = await stdout.receive(4096)
                except anyio.EndOfStream:
                    return
                if not chunk:
                    return
                buf.extend(chunk)
                if len(buf) > BASH_OUTPUT_LIMIT:
                    # Keep only the tail so the sentinel remains detectable and
                    # the buffer cannot grow without bound.
                    del buf[: len(buf) - BASH_OUTPUT_LIMIT]
                    truncated = True
                if marker in buf:
                    return

        try:
            with anyio.fail_after(timeout):
                await read_until_sentinel()
        except TimeoutError as e:
            # This call's own deadline fired. Tear down the subprocess so the
            # timed-out command can't bleed into the next call. Shielded so the
            # teardown still completes if an outer scope is also cancelling.
            with anyio.CancelScope(shield=True):
                await self.close()
            raise TimeoutError(f"bash command timed out after {timeout}s") from e
        except anyio.get_cancelled_exc_class():
            # A cancellation from *any outer scope* (e.g. the session runner's
            # ``TOOL_TIMEOUT`` fail_after winning a race, or a worker-wide
            # shutdown) unwinds this call without ever raising ``TimeoutError``,
            # so the branch above never runs. Without closing here the
            # subprocess would be left alive with the in-flight command still
            # queued, and the NEXT exec() would read this command's stale
            # output + old sentinel — silent cross-call corruption. Close it
            # (shielded, since we're already cancelled) and re-raise the
            # cancellation; never swallow it.
            with anyio.CancelScope(shield=True):
                await self.close()
            raise

        text = _ANSI.sub("", buf.decode(errors="replace"))
        idx = text.rfind(sentinel)
        if idx < 0:
            return BashResult(text.strip(), -1)
        out = text[:idx].rstrip("\n")
        tail = text[idx + len(sentinel) :].strip()
        try:
            code = int(tail.splitlines()[0]) if tail else -1
        except ValueError:
            code = -1
        if truncated:
            out = "[output truncated]\n" + out
        return BashResult(out, code)

    async def close(self) -> None:
        if self._proc.stdin is not None:
            with anyio.CancelScope(shield=True):
                try:
                    await self._proc.stdin.aclose()
                except Exception:
                    pass
        if self._proc.returncode is None:
            self._proc.kill()
            with anyio.move_on_after(2):
                await self._proc.wait()
        with anyio.CancelScope(shield=True):
            try:
                await self._proc.aclose()
            except Exception:
                pass


def beta_bash_tool(ctx: AgentToolContext) -> BetaAsyncFunctionTool[Any]:
    @asynccontextmanager
    async def bash_tool() -> AsyncIterator[Callable[..., Awaitable[str]]]:
        """Run a command in a persistent bash shell."""
        # The bash tool owns its own persistent shell for the lifetime of the
        # tool run. Defining it as an async context manager lets the tool runner
        # drive this cleanup on exit, so the bash tool no longer needs
        # AgentToolContext purely for that lifecycle — it only reads the workdir
        # and subprocess env off ``ctx``.
        session: BashSession | None = None

        async def _session() -> BashSession:
            nonlocal session
            if session is None:
                session = await BashSession.start(ctx.workdir, env=ctx.env)
            return session

        # ``Optional[...]`` (not ``| None``) because ``@beta_async_tool``
        # evaluates these annotations at runtime via pydantic, and PEP 604 union
        # syntax can't be ``eval``'d under Python 3.9 — our minimum version.
        async def bash(
            command: Optional[str] = None, restart: Optional[bool] = None, timeout_ms: Optional[int] = None
        ) -> str:
            nonlocal session
            if restart:
                if session is not None:
                    await session.close()
                    session = None
                await _session()
                return "bash session restarted"
            if not command:
                raise ToolError("bash: command is required")
            timeout = timeout_ms / 1000.0 if timeout_ms else BASH_DEFAULT_TIMEOUT
            try:
                s = await _session()
                out, code = await s.exec(command, timeout=timeout)
            except (RuntimeError, TimeoutError) as e:
                raise ToolError(f"bash: {e}") from e
            if code != 0:
                raise ToolError(out)
            return out

        try:
            yield bash
        finally:
            if session is not None:
                await session.close()

    # ``@beta_async_tool`` detects the async context manager, enters it lazily
    # on first call to obtain the ``bash`` callable, and drives its ``__aexit__``
    # on the tool-runner cleanup path. The ``cast`` is only to satisfy the
    # decorator's "async function" overload — the runtime object is the
    # context-manager factory the decorator expects.
    return beta_async_tool(
        name="bash",
        input_schema=BetaManagedAgentsAgentToolset20260401BashInput,
    )(cast(Any, bash_tool))


def _read_binary_block(target: Path, file_path: str, size: int, media_type: str, ctx: AgentToolContext) -> BetaContent:
    """Read an image/PDF as a base64 ``image``/``document`` content block.

    The text cap does not apply here — its 256 KiB default would reject most
    real images. Instead the media caps (``max_image_base64_bytes`` /
    ``max_pdf_bytes``, defaulting to the API's own limits) govern, checked
    against the stat size before opening (same OOM rationale as the text path)
    and tightened by an *explicitly* configured ``max_file_bytes`` — an
    explicit cap is a memory bound and binds every read.
    """
    # The image cap is on the encoded form: n raw bytes -> 4*ceil(n/3) base64.
    if media_type == "application/pdf":
        limit = _resolve_max_bytes(ctx.max_pdf_bytes, DEFAULT_MAX_PDF_BYTES)
    else:
        b64_cap = _resolve_max_bytes(ctx.max_image_base64_bytes, DEFAULT_MAX_IMAGE_BASE64_BYTES)
        limit = (b64_cap // 4) * 3 if b64_cap is not None else None
    if is_given(ctx.max_file_bytes) and ctx.max_file_bytes is not None:
        limit = ctx.max_file_bytes if limit is None else min(limit, ctx.max_file_bytes)
    if limit is not None and size > limit:
        raise ToolError(f"read: {file_path} is {size} bytes, exceeds {limit}-byte limit for image/PDF files.")
    data = base64.standard_b64encode(target.read_bytes()).decode("ascii")
    if media_type == "application/pdf":
        return {"type": "document", "source": {"type": "base64", "media_type": "application/pdf", "data": data}}
    return {
        "type": "image",
        "source": {"type": "base64", "media_type": cast(Any, media_type), "data": data},
    }


def beta_read_tool(ctx: AgentToolContext) -> BetaAsyncFunctionTool[Any]:
    @beta_async_tool(name="read", input_schema=BetaManagedAgentsAgentToolset20260401ReadInput)
    async def read(file_path: str, view_range: Optional[List[int]] = None) -> BetaFunctionToolResultType:
        """Read a file rooted at the working directory."""
        try:
            target = resolve_path(ctx, file_path)
        except ValueError as e:
            raise ToolError(f"read: {e}") from e
        try:
            # stat() before any open(): the size cap stops a multi-GB file from
            # OOM'ing the runner, and is_file() rejects FIFOs/devices/dirs
            # without opening them (open() on an unconnected FIFO blocks).
            st = target.stat()
            if not S_ISREG(st.st_mode):
                raise ToolError(f"read: {file_path}: not a regular file")
            media_type = _BINARY_MEDIA_TYPES.get(target.suffix.lower())
            if media_type is not None:
                # Images/PDFs come back as content blocks (hosted-toolset
                # parity) — read_text() on them raises UnicodeDecodeError.
                if view_range:
                    raise ToolError("read: view_range is not supported for image/PDF files")
                return [_read_binary_block(target, file_path, st.st_size, media_type, ctx)]
            limit = _resolve_max_bytes(ctx.max_file_bytes)
            if limit is not None and st.st_size > limit:
                raise ToolError(
                    f"read: {file_path} is {st.st_size} bytes, exceeds {limit}-byte limit. "
                    "Use bash (head/tail/sed) to read a slice."
                )
            # Explicit UTF-8: the locale default varies by host (ASCII under
            # LANG=C), which would mislabel valid UTF-8 as binary below.
            text = target.read_text(encoding="utf-8")
        except ToolError:
            raise
        except UnicodeDecodeError as e:
            raise ToolError(
                f"read: {file_path}: not valid UTF-8 text (binary files are only supported for image/PDF extensions)"
            ) from e
        except OSError as e:
            raise _fs_error("read", file_path, e) from e
        if not view_range:
            return text
        if len(view_range) != 2:
            raise ToolError("read: view_range must be [start_line, end_line]")
        start_line, end_line = view_range
        lines = text.split("\n")
        start = max(0, start_line - 1)
        end = end_line if end_line > 0 else len(lines)
        return "\n".join(lines[start:end])

    return read


def beta_write_tool(ctx: AgentToolContext) -> BetaAsyncFunctionTool[Any]:
    @beta_async_tool(name="write", input_schema=BetaManagedAgentsAgentToolset20260401WriteInput)
    async def write(file_path: str, content: str) -> str:
        """Write a file, creating parent directories as needed."""
        try:
            target = resolve_path(ctx, file_path)
        except ValueError as e:
            raise ToolError(f"write: {e}") from e
        try:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content, encoding="utf-8")
        except OSError as e:
            raise _fs_error("write", file_path, e) from e
        return f"wrote {len(content)} bytes to {file_path}"

    return write


def beta_edit_tool(ctx: AgentToolContext) -> BetaAsyncFunctionTool[Any]:
    @beta_async_tool(name="edit", input_schema=BetaManagedAgentsAgentToolset20260401EditInput)
    async def edit(file_path: str, old_string: str, new_string: str, replace_all: Optional[bool] = None) -> str:
        """Replace text in a file by exact string match."""
        try:
            target = resolve_path(ctx, file_path)
        except ValueError as e:
            raise ToolError(f"edit: {e}") from e
        try:
            # stat() before any open(): the size cap stops a multi-GB file from
            # OOM'ing the runner, and is_file() rejects FIFOs/devices/dirs
            # without opening them (open() on an unconnected FIFO blocks). Same
            # guard as the read tool — edit reads the whole file too.
            st = target.stat()
            if not S_ISREG(st.st_mode):
                raise ToolError(f"edit: {file_path}: not a regular file")
            limit = _resolve_max_bytes(ctx.max_file_bytes)
            if limit is not None and st.st_size > limit:
                raise ToolError(
                    f"edit: {file_path} is {st.st_size} bytes, exceeds {limit}-byte limit. "
                    "Use bash (sed/awk) to edit a large file."
                )
            text = target.read_text(encoding="utf-8")
        except ToolError:
            raise
        except UnicodeDecodeError as e:
            raise ToolError(f"edit: {file_path}: not valid UTF-8 text (cannot edit binary files)") from e
        except OSError as e:
            raise _fs_error("edit", file_path, e) from e
        count = text.count(old_string)
        if count == 0:
            raise ToolError(f"edit: old_string not found in {file_path}")
        if not replace_all and count > 1:
            raise ToolError(f"edit: old_string appears {count} times in {file_path} (must be unique)")
        updated = text.replace(old_string, new_string) if replace_all else text.replace(old_string, new_string, 1)
        try:
            target.write_text(updated, encoding="utf-8")
        except OSError as e:
            raise _fs_error("edit", file_path, e) from e
        return f"edited {file_path} ({count if replace_all else 1} replacement(s))"

    return edit


def _mtime_or_zero(p: Path) -> float:
    try:
        return p.stat().st_mtime
    except OSError:
        return 0.0


def beta_glob_tool(ctx: AgentToolContext) -> BetaAsyncFunctionTool[Any]:
    @beta_async_tool(name="glob", input_schema=BetaManagedAgentsAgentToolset20260401GlobInput)
    async def glob(pattern: str, path: Optional[str] = None) -> str:
        """List files matching a glob pattern, newest first."""
        confine: Optional[Path] = None
        if Path(pattern).is_absolute():
            if not ctx.unrestricted_paths:
                raise ToolError("glob: absolute pattern not permitted")
            root = Path("/")
            pat = pattern.lstrip("/")
        else:
            # ``Path.glob`` honours literal ``..`` segments, so a pattern like
            # ``../../etc/*`` would escape the workdir before resolve_path() is
            # ever consulted — reject it up front.
            if not ctx.unrestricted_paths and ".." in PurePosixPath(pattern).parts:
                raise ToolError("glob: '..' is not permitted in the pattern")
            if path:
                try:
                    root = resolve_path(ctx, path)
                except ValueError as e:
                    raise ToolError(f"glob: {e}") from e
            else:
                root = Path(ctx.workdir).resolve()
            pat = pattern
            if not ctx.unrestricted_paths:
                confine = root
        try:
            # islice caps the materialised match list so a pattern that matches
            # an enormous tree can't OOM the runner.
            matches = list(islice(root.glob(pat), WALK_MAX_ENTRIES))
        except (ValueError, OSError) as e:
            raise ToolError(f"glob: {e}") from e
        if confine is not None:
            # Post-filter: a symlink traversed mid-pattern (glob follows
            # symlinks for non-``**`` segments) must not let a result escape the
            # confinement root. ``resolve()`` canonicalises symlinks.
            matches = [m for m in matches if _within(m.resolve(), confine)]
        if not matches:
            return "no matches"
        matches.sort(key=_mtime_or_zero, reverse=True)
        return "\n".join(str(m) for m in matches[:GLOB_RESULT_LIMIT])

    return glob


def beta_grep_tool(ctx: AgentToolContext) -> BetaAsyncFunctionTool[Any]:
    @beta_async_tool(name="grep", input_schema=BetaManagedAgentsAgentToolset20260401GrepInput)
    async def grep(pattern: str, path: Optional[str] = None) -> str:
        """Search file contents for a regular expression."""
        try:
            search = resolve_path(ctx, path) if path else Path(ctx.workdir).resolve()
        except ValueError as e:
            raise ToolError(f"grep: {e}") from e

        if rg := shutil.which("rg"):
            # ``check=False`` because ripgrep exits 1 on "no matches", which
            # isn't an error for us — we surface it as a friendly string.
            result = await anyio.run_process(
                [rg, "-n", "--no-heading", "-e", pattern, "--", str(search)],
                check=False,
            )
            if result.returncode == 1:
                return "no matches"
            if result.returncode != 0:
                raise ToolError(f"grep: rg failed: {result.stderr.decode(errors='replace')}")
            out = result.stdout.decode(errors="replace")
            if len(out) > GREP_OUTPUT_LIMIT:
                out = out[:GREP_OUTPUT_LIMIT] + f"\n[output truncated at {GREP_OUTPUT_LIMIT} bytes]"
            return out

        try:
            rx = re.compile(pattern)
        except re.error as e:
            raise ToolError(f"grep: invalid regex: {e}") from e
        return _walk_grep(rx, search)

    return grep


def _walk_grep(rx: re.Pattern[str], search: Path) -> str:
    hits: list[str] = []
    budget = GREP_OUTPUT_LIMIT

    def push(line: str) -> bool:
        nonlocal budget
        budget -= len(line) + 1
        if budget < 0:
            hits.append(f"[output truncated at {GREP_OUTPUT_LIMIT} bytes]")
            return False
        hits.append(line)
        return True

    def scan(full: Path) -> bool:
        try:
            with full.open("rb") as f:
                if b"\x00" in f.read(512):
                    return True
                f.seek(0)
                for i, raw in enumerate(f, 1):
                    # Cap line length: ``pattern`` is model-supplied and Python's
                    # ``re`` backtracks, so a pathological pattern against a very
                    # long line is a ReDoS.
                    if len(raw) > GREP_MAX_LINE_LENGTH:
                        continue
                    line = raw.decode(errors="replace").rstrip("\r\n")
                    if rx.search(line) and not push(f"{full}:{i}:{line}"):
                        return False
        except OSError:
            pass
        return True

    if search.is_file():
        scan(search)
    else:
        seen = 0
        for dirpath, dirnames, filenames in os.walk(search):
            # Never descend into a symlinked directory: a symlink in the workdir
            # pointing at ``/`` would otherwise let grep walk straight out of it.
            dirnames[:] = [
                d for d in dirnames if d not in (".git", "node_modules") and not (Path(dirpath) / d).is_symlink()
            ]
            for name in filenames:
                full = Path(dirpath) / name
                # Likewise skip symlinked files — a symlink to /etc/shadow must
                # not be read through just because it lives inside the workdir.
                if full.is_symlink():
                    continue
                seen += 1
                if seen > WALK_MAX_ENTRIES or not scan(full):
                    return "\n".join(hits) if hits else "no matches"
    return "\n".join(hits) if hits else "no matches"


def beta_agent_toolset_20260401(ctx: AgentToolContext) -> list[BetaAsyncFunctionTool[Any]]:
    """Return the ``agent_toolset_20260401`` implementations bound to ``ctx``.

    The result is a plain list of :class:`~anthropic.lib.tools.BetaAsyncFunctionTool`
    instances — *async* function tools, so it is for the **async** runners only:
    the ``AsyncAnthropic`` ``client.beta.messages.tool_runner`` and
    ``client.beta.sessions.events.tool_runner`` (always async). The sync
    ``Anthropic`` ``messages.tool_runner`` takes ``BetaRunnableTool``, which
    excludes the async function tools this returns. Filter or extend it before
    passing it on::

        tools = [*beta_agent_toolset_20260401(ctx), my_custom_tool]
        tools = [t for t in beta_agent_toolset_20260401(ctx) if t.name != "grep"]
    """
    return [
        beta_bash_tool(ctx),
        beta_read_tool(ctx),
        beta_write_tool(ctx),
        beta_edit_tool(ctx),
        beta_glob_tool(ctx),
        beta_grep_tool(ctx),
    ]
