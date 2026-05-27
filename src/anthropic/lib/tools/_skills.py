"""Skill download + archive extraction for the agent toolset.

Split out from ``agent_toolset`` because fetching a session agent's skills and
safely unpacking a (possibly third-party) archive is a distinct concern from the
tool implementations themselves.
"""

from __future__ import annotations

import os
import re
import shutil
import logging
import tarfile
import zipfile
import tempfile
from typing import TYPE_CHECKING, Sequence
from pathlib import Path, PurePosixPath
from functools import partial

import anyio
from anyio.to_thread import run_sync

if TYPE_CHECKING:
    from ..._types import FileTypes
    from ..._client import AsyncAnthropic

__all__ = ["download_session_skills", "normalize_skill_files"]


def _read_file_entry_content(content: object) -> bytes | None:
    """Return the raw bytes of a FileContent value, or None if unreadable."""
    if isinstance(content, bytes):
        return content
    if hasattr(content, "read"):
        data = content.read()
        if hasattr(content, "seek"):
            content.seek(0)
        return data if isinstance(data, bytes) else None
    try:
        return Path(content).read_bytes()  # type: ignore[arg-type]
    except Exception:
        return None


def _parse_skill_name_from_frontmatter(skill_md: bytes) -> str | None:
    """Extract the ``name:`` field from SKILL.md YAML frontmatter, or ``None``."""
    text = skill_md.decode("utf-8", errors="replace")
    fm = re.search(r"^---\s*\n(.*?)\n---", text, re.DOTALL)
    if fm:
        name_match = re.search(r"^name:\s*(\S+)", fm.group(1), re.MULTILINE)
        if name_match:
            return name_match.group(1).strip()
    return None


def normalize_skill_files(
    files: Sequence["FileTypes"],
    *,
    display_title: str | None = None,
) -> list["FileTypes"]:
    """Normalize file paths for :meth:`~anthropic.resources.beta.Skills.create`.

    ``beta.skills.create()`` requires every file path to be prefixed with a
    top-level directory whose name **exactly matches** the ``name:`` field in
    the ``SKILL.md`` frontmatter.  This function is called automatically inside
    ``skills.create()`` — you do not need to call it yourself.

    It can also be called explicitly if you want to inspect or log the
    normalized paths before uploading::

        skill_md = b"---\\nname: my-skill\\n---\\n\\nSkill content."
        files = normalize_skill_files(
            [
                ("SKILL.md", skill_md, "text/markdown"),
                ("scripts/tool.py", script_bytes, "text/plain"),
            ]
        )
        # [
        #   ("my-skill/SKILL.md",        skill_md,     "text/markdown"),
        #   ("my-skill/scripts/tool.py", script_bytes, "text/plain"),
        # ]

    The skill name is resolved in order:

    1. The ``name:`` field in the ``SKILL.md`` YAML frontmatter.
    2. *display_title* normalised to ``lowercase-with-hyphens`` as a fallback
       (useful when ``SKILL.md`` omits the field).

    Paths that are already under the correct top-level directory are left
    unchanged (idempotent).  A wrong top-level prefix is stripped and replaced
    rather than prepended, so re-uploading a skill that was created with the
    wrong prefix is safe.

    Args:
        files: The sequence of file entries to normalize.  Each entry must be a
            tuple whose first element is the file path string.
        display_title: Fallback skill name used when the ``SKILL.md``
            frontmatter does not contain a ``name:`` field.  Special characters
            are replaced with hyphens and the value is lower-cased.

    Returns:
        A new list with every file path prefixed by the skill name.

    Raises:
        ValueError: If no ``SKILL.md`` entry is found, or if neither the
            frontmatter nor *display_title* supplies a skill name.
    """
    # Pass 1: locate SKILL.md, parse the skill name, note the current prefix.
    skill_name: str | None = None
    skill_md_prefix: str = ""  # top-level dir of the SKILL.md entry, or ""
    found_skill_md = False

    for entry in files:
        if not isinstance(entry, tuple) or len(entry) < 2:
            continue
        filename = entry[0]
        if not isinstance(filename, str):
            continue
        if filename.rsplit("/", 1)[-1] != "SKILL.md":
            continue
        found_skill_md = True
        content = _read_file_entry_content(entry[1])
        if content is not None:
            skill_name = _parse_skill_name_from_frontmatter(content)
        parts = filename.split("/", 1)
        skill_md_prefix = parts[0] if len(parts) == 2 else ""
        break

    if not found_skill_md:
        raise ValueError(
            "No SKILL.md entry found in the files list. "
            "Each entry must be a tuple (path, content, ...) where path is a str "
            "and one path must be 'SKILL.md' or '<dir>/SKILL.md'."
        )

    # Fallback: derive name from display_title.
    if skill_name is None and display_title:
        skill_name = re.sub(r"[^a-z0-9]+", "-", display_title.lower().strip()).strip("-")

    if skill_name is None:
        raise ValueError(
            "Could not determine skill name: SKILL.md frontmatter has no 'name:' field "
            "and no display_title was provided as a fallback.\n"
            "Add 'name: <your-skill-name>' to the SKILL.md frontmatter, or pass "
            "display_title='<your-skill-name>' to normalize_skill_files()."
        )

    # Pass 2: rewrite paths so every entry is under ``{skill_name}/``.
    #
    # • Already-correct prefix → unchanged (idempotent).
    # • Wrong top-level prefix → stripped then replaced (not double-prefixed).
    # • No prefix → skill name prepended.
    prefix = f"{skill_name}/"
    result: list[FileTypes] = []
    for entry in files:
        if isinstance(entry, tuple) and entry and isinstance(entry[0], str):
            path = entry[0]
            if path.startswith(prefix):
                result.append(entry)
            elif skill_md_prefix and path.startswith(f"{skill_md_prefix}/"):
                relative = path[len(skill_md_prefix) + 1 :]
                result.append((prefix + relative,) + entry[1:])  # type: ignore[arg-type]
            else:
                result.append((prefix + path,) + entry[1:])  # type: ignore[arg-type]
        else:
            result.append(entry)
    return result


# Skill dirs hold downloaded, possibly third-party content — keep them
# owner-only rather than inheriting whatever the process umask happens to be.
_SKILL_DIR_MODE = 0o700

log = logging.getLogger("anthropic.lib.tools.agent_toolset")


def _within(child: Path, root: Path) -> bool:
    """True if ``child`` is ``root`` or a path inside it (both already resolved)."""
    try:
        child.relative_to(root)
    except ValueError:
        return False
    return True


def _safe_member_name(name: str) -> str:
    """Return ``name`` as a confined relative path, or raise on path-traversal.

    Strips ``.`` components; rejects absolute paths and any ``..`` component
    outright (those only appear in malicious archives). Returns ``""`` for
    entries that resolve to nothing (e.g. ``"./"``) — the caller should skip
    those.
    """
    norm = name.replace("\\", "/")
    if norm.startswith("/") or PurePosixPath(norm).is_absolute():
        raise ValueError(f"refusing archive member with absolute path {name!r}")
    parts = [p for p in PurePosixPath(norm).parts if p != "."]
    if any(p == ".." for p in parts):
        raise ValueError(f"refusing archive member with '..' component: {name!r}")
    return str(PurePosixPath(*parts)) if parts else ""


def _archive_top_dir(names: list[str]) -> str:
    """Return the single top-level directory shared by every archive entry, or
    ``""`` if the entries don't all live under one common directory.

    Skill bundles are packaged wrapped in one directory named after the skill
    (e.g. ``pdf/SKILL.md``, ``pdf/scripts/...``). The extractor strips that
    wrapper so the contents land directly in the skill's destination directory
    instead of a redundant nested ``<skill>/<skill>/`` level.
    """
    tops: set[str] = set()
    has_nested = False
    for n in names:
        parts = PurePosixPath(n).parts
        if not parts:
            continue
        tops.add(parts[0])
        if len(parts) > 1:
            has_nested = True
    return next(iter(tops)) if len(tops) == 1 and has_nested else ""


def _strip_top(safe: str, top: str) -> str:
    """Drop the leading ``top`` component from ``safe`` (an already-confined
    relative path). Returns ``""`` for the bare top-dir entry itself."""
    if not top:
        return safe
    parts = PurePosixPath(safe).parts
    if parts and parts[0] == top:
        rest = parts[1:]
        return str(PurePosixPath(*rest)) if rest else ""
    return safe


def _archive_file_mode(src_mode: int) -> int:
    """Reduce an archive entry's Unix mode to ``0o755`` if it is executable,
    ``0o644`` otherwise.

    Skill bundles can ship executable scripts (e.g. ``scripts/foo.sh``), so the
    execute bit recorded in the archive must survive extraction or invoking the
    script directly fails with permission denied. The mode is deliberately
    collapsed to one of two values: this preserves "is it executable" while
    never propagating setuid/setgid/sticky or group/other-write bits from a
    (possibly third-party) archive.
    """
    return 0o755 if src_mode & 0o111 else 0o644


def _extract_skill_archive(archive_path: Path, dest: Path) -> None:
    """Extract a skill download (a zip or tar.* archive) from disk into ``dest``.

    Skill bundles are wrapped in a single directory named after the skill; that
    wrapper is stripped so files land directly under ``dest`` rather than a
    redundant ``dest/<skill>/`` level. Skills can be third-party, so this
    refuses any member that would escape ``dest`` (zip-slip / tar-slip) and
    skips symlink/hardlink/device members in tar archives.
    """
    dest.mkdir(parents=True, exist_ok=True, mode=_SKILL_DIR_MODE)
    root = dest.resolve()

    if zipfile.is_zipfile(archive_path):
        with zipfile.ZipFile(archive_path) as zf:
            infos = zf.infolist()
            # Compute the wrapper dir from the same confined names the loop
            # uses, so a malicious name still raises before anything is written.
            safe_names = [s for info in infos if (s := _safe_member_name(info.filename))]
            top = _archive_top_dir(safe_names)
            for info in infos:
                safe = _strip_top(_safe_member_name(info.filename), top)
                if not safe:
                    continue
                target = (root / safe).resolve()
                if not _within(target, root):
                    raise ValueError(f"refusing to extract unsafe zip member {info.filename!r}")
                if info.is_dir():
                    target.mkdir(parents=True, exist_ok=True)
                    continue
                target.parent.mkdir(parents=True, exist_ok=True)
                with zf.open(info) as src, open(target, "wb") as out:
                    shutil.copyfileobj(src, out)
                # ``external_attr``'s high 16 bits hold the Unix mode; it is 0
                # for archives created without Unix attrs -> non-executable.
                os.chmod(target, _archive_file_mode(info.external_attr >> 16))
        return

    # tarfile.open with "r:*" transparently handles tar / tar.gz / tar.bz2 / tar.xz.
    with tarfile.open(archive_path, mode="r:*") as tf:
        members = [m for m in tf.getmembers() if not (m.issym() or m.islnk() or m.isdev())]
        safe_names = [s for m in members if (s := _safe_member_name(m.name))]
        top = _archive_top_dir(safe_names)
        for member in members:
            safe = _strip_top(_safe_member_name(member.name), top)
            if not safe:
                continue
            target = (root / safe).resolve()
            if not _within(target, root):
                raise ValueError(f"refusing to extract unsafe tar member {member.name!r}")
            if member.isdir():
                target.mkdir(parents=True, exist_ok=True)
                continue
            target.parent.mkdir(parents=True, exist_ok=True)
            extracted = tf.extractfile(member)
            if extracted is None:
                continue
            with extracted as src, open(target, "wb") as out:
                shutil.copyfileobj(src, out)
            os.chmod(target, _archive_file_mode(member.mode))


async def _resolve_skill_version(client: AsyncAnthropic, skill_id: str, version: str) -> str:
    """Resolve ``version`` to the concrete numeric timestamp the
    ``/v1/skills/{id}/versions/{version}`` endpoints require.

    ``session.agent.skills[].version`` may be an alias such as ``"latest"``,
    which those endpoints reject — so list the skill's versions and pick the
    newest. Numeric versions are returned unchanged.
    """
    if version.isdigit():
        return version
    newest: str | None = None
    async for v in client.beta.skills.versions.list(skill_id):
        if v.version.isdigit() and (newest is None or int(v.version) > int(newest)):
            newest = v.version
    if newest is None:
        raise ValueError(f"skill {skill_id!r} has no concrete version to resolve {version!r} against")
    return newest


async def download_session_skills(
    client: AsyncAnthropic, *, session_id: str, workdir: str | os.PathLike[str]
) -> list[Path]:
    """Download the session agent's skills into ``{workdir}/skills/<name>/``.

    Looks up the session's resolved agent, and for each skill fetches its files
    via ``client.beta.skills.versions.download`` and extracts the archive under a
    directory named after the skill. The archive is streamed to a temp file
    rather than buffered whole in memory. A failure on one skill is logged and
    does not block the others.

    Returns the list of skill directories that were created, so the caller can
    remove them when the workdir is torn down.
    """
    # The sessions/skills resources inject their anthropic-beta headers
    # (managed-agents / skills) themselves — no need to pass `betas=` here.
    session = await client.beta.sessions.retrieve(session_id)
    skills_root = Path(await (anyio.Path(workdir) / "skills").resolve())
    # ``skills_root`` is created lazily by the extraction below — don't create it
    # up front so an agent with no skills leaves no stray directory behind.
    downloaded: list[Path] = []
    for skill in session.agent.skills:
        try:
            version_id = await _resolve_skill_version(client, skill.skill_id, skill.version)
            version = await client.beta.skills.versions.retrieve(version_id, skill_id=skill.skill_id)
            # The directory is the skill's name, but reduce it to a single safe
            # path component so a hostile name can't escape skills_root.
            dirname = os.path.basename(version.name.strip()) or skill.skill_id
            if dirname in ("", ".", ".."):
                dirname = skill.skill_id
            dest = Path(await (anyio.Path(skills_root) / dirname).resolve())
            if not _within(dest, skills_root):
                log.warning("skill name %r escapes the skills dir; skipping", version.name)
                continue
            adest = anyio.Path(dest)
            if await adest.is_symlink():
                await adest.unlink()
            # ``shutil.rmtree`` is blocking; keep it off the event loop.
            await run_sync(partial(shutil.rmtree, dest, ignore_errors=True))
            await _download_and_extract(client, skill.skill_id, version_id, dest)
            downloaded.append(dest)
            log.info("downloaded skill skill_id=%s version=%s -> %s", skill.skill_id, version_id, dest)
        except Exception as e:
            log.warning("failed to download skill skill_id=%s: %s", skill.skill_id, e)
    return downloaded


async def _download_and_extract(client: AsyncAnthropic, skill_id: str, version_id: str, dest: Path) -> None:
    """Stream the skill archive to a temp file, then extract it into ``dest``."""
    await anyio.Path(dest.parent).mkdir(parents=True, exist_ok=True, mode=_SKILL_DIR_MODE)
    fd, tmp_name = await run_sync(partial(tempfile.mkstemp, prefix=".skill-", suffix=".archive", dir=dest.parent))
    os.close(fd)
    tmp = anyio.Path(tmp_name)
    try:
        async with client.beta.skills.versions.with_streaming_response.download(
            version_id, skill_id=skill_id
        ) as archive:
            await archive.stream_to_file(tmp_name)
        # zipfile / tarfile are blocking; keep them off the event loop.
        await run_sync(_extract_skill_archive, Path(tmp_name), dest)
    finally:
        await tmp.unlink(missing_ok=True)
