"""``FileStore`` — one confined folder; a relative path cannot escape it.

Beta scope: symlinks are refused or skipped wherever the store meets them, but
there is no hardening against a process racing the store's own syscalls;
fsync durability, non-POSIX hosts, and read-size caps are out of scope.
"""

from __future__ import annotations

import os
import stat
import time
import errno
import shutil
import hashlib
from typing import IO, Union, NamedTuple
from pathlib import Path, PurePosixPath
from contextlib import suppress

import anyio
from anyio.to_thread import run_sync

__all__ = ["FileStore", "LocalFileStore", "FileStoreError", "Root"]

PutData = Union[str, bytes]

_OWNER_ONLY_DIR_MODE = 0o700
_OWNER_ONLY_FILE_MODE = 0o600
_OWNER_ONLY_EXEC_MODE = 0o700

# 0 where the platform lacks them; ``open`` refuses such platforms.
_O_NOFOLLOW = getattr(os, "O_NOFOLLOW", 0)
_O_NONBLOCK = getattr(os, "O_NONBLOCK", 0)


class FileStoreError(Exception):
    """A refused operation — input the store will not act on. OS errors propagate as ``OSError``."""

    ESCAPES_ROOT = "escapes the store root"
    IS_A_SYMLINK = "is a symlink"
    NOT_A_FILE = "is not a regular file"
    NOT_A_DIRECTORY = "is not a directory"
    NOT_UTF8 = "is not valid utf-8"
    MOVE_DESTINATION_EXISTS = "already exists"

    def __init__(self, reason: str, rel_path: str) -> None:
        super().__init__(f"path {rel_path!r} {reason}")
        self.reason = reason
        self.rel_path = rel_path


class Root(NamedTuple):
    """The store's resolved root, and what :meth:`FileStore.dispose` will do to it."""

    path: Path
    #: True when ``open`` found no root, so ``dispose`` removes it. A root that
    #: was already there is someone else's — a pre-seeded mount, a caller's
    #: workdir — and is kept.
    removed_on_dispose: bool


class _Hashed(NamedTuple):
    mtime_ns: int
    #: userspace cannot set ctime, so writers that preserve mtimes
    #: (``rsync -t``, ``cp -p``) still miss the cache.
    ctime_ns: int
    size: int
    sha: str


class FileStore:
    """One confined folder of regular files.

    Every ``rel_path`` is relative to the root (a leading ``/`` also means the
    root) and refused with :class:`FileStoreError` when it escapes. The store
    holds regular files only: symlinks are refused on read and skipped by
    listings — :meth:`find_symlinks` reports them. A ``rel_path`` resolving to
    the root itself is banned by this interface: ``put`` and ``get`` refuse it,
    ``move`` and ``remove`` do nothing. A store opened with ``utf8_only=True``
    refuses binary content the same way — on ``put`` of such bytes and on
    ``get`` of such a file. Only :meth:`create_root` makes the root: writes
    create directories below it, never the root itself, so a root removed
    while the store is open stays removed and the write raises
    :class:`FileNotFoundError`.
    """

    def __init__(self, root: Path, removed_on_dispose: bool, utf8_only: bool = False) -> None:
        self._root = root
        self._removed_on_dispose = removed_on_dispose
        self._utf8_only = utf8_only
        self._hashes: dict[str, _Hashed] = {}

    @staticmethod
    def is_path_legal(path: str) -> bool:
        """True for a path usable verbatim as a store location: absolute, no ``..``."""
        p = PurePosixPath(path)
        return p.is_absolute() and ".." not in p.parts

    @classmethod
    async def open(cls, root: str | os.PathLike[str], *, utf8_only: bool = False) -> FileStore:
        """Resolve ``root``; creates nothing — only :meth:`create_root` makes the folder."""
        if not _platform_supported():
            raise RuntimeError("FileStore requires O_NOFOLLOW support on this platform")
        adir = anyio.Path(root)
        # lstat, not exists(): exists() follows symlinks and swallows permission
        # errors — either would mark a real directory ours to delete on dispose.
        try:
            await adir.lstat()
        except FileNotFoundError:
            removed_on_dispose = True
        else:
            removed_on_dispose = False
        return cls(root=Path(await adir.resolve()), removed_on_dispose=removed_on_dispose, utf8_only=utf8_only)

    async def create_root(self) -> None:
        """Create the root directory and any missing ancestors; already existing is fine."""
        await run_sync(_make_dir_and_ancestors, self._root)

    def root(self) -> Root:
        return Root(path=self._root, removed_on_dispose=self._removed_on_dispose)

    async def dispose(self) -> None:
        """Remove the root iff ``open`` created it; pre-existing roots are kept."""
        if not self._removed_on_dispose:
            return
        with suppress(FileNotFoundError):
            await run_sync(shutil.rmtree, self._root)

    async def __aenter__(self) -> FileStore:
        return self

    async def __aexit__(self, *exc: object) -> None:
        await self.dispose()

    async def put(self, rel_path: str, data: PutData, *, is_executable: bool = False) -> None:
        """Write ``str`` (UTF-8) or ``bytes`` atomically to the file at ``rel_path``.

        Missing directories below the root are created; a missing root is not —
        the write raises :class:`FileNotFoundError`.
        """
        # "dir/." names a directory just like a trailing "/".
        tail = rel_path.replace("\\", "/")
        if tail.endswith(("/", "/.")) or tail in ("", "."):
            raise FileStoreError(FileStoreError.NOT_A_FILE, rel_path)
        dest = self._resolve_under_root(rel_path)
        payload = data.encode("utf-8") if isinstance(data, str) else bytes(data)
        self._require_utf8(rel_path, payload)
        await run_sync(_make_dirs_below_root, self._root, dest.parent)
        await run_sync(_replace_via_temp, dest, payload, is_executable)

    async def get(self, rel_path: str) -> bytes | None:
        """The file's bytes; ``None`` when absent."""
        dest = self._resolve_under_root(rel_path)

        def read() -> bytes | None:
            try:
                f = _open_regular_file(rel_path, dest)
            except FileNotFoundError:
                return None
            with f:
                return f.read()

        data = await run_sync(read)
        if data is None:
            return None
        self._require_utf8(rel_path, data)
        return data

    async def ls(self, under: str = "/") -> set[str]:
        """The relative path of every file under the directory ``under``."""
        base = self._resolve_under_root(under)

        def walk() -> set[str]:
            return {rel for rel, _ in _filenames_in_dir(self._root, under, base)}

        return await run_sync(walk)

    async def find_symlinks(self, under: str = "/") -> set[str]:
        """Every symlink under ``under`` — listings skip them and reads refuse
        them, so a caller that must know they exist asks here."""
        base = self._resolve_under_root(under)
        return await run_sync(_symlinks_in_dir, self._root, under, base)

    async def hashtree(self, under: str = "/") -> dict[str, str]:
        """``{rel_path: sha256_hex}`` of every file under the directory ``under``.

        Unchanged files — same size, mtime, and ctime since the last call —
        reuse their recorded hash instead of being re-read.
        """
        base = self._resolve_under_root(under)

        def hash_all() -> dict[str, str]:
            walk_start_ns = _now_ns()
            out: dict[str, str] = {}
            for rel, full in _filenames_in_dir(self._root, under, base):
                sha = self._hash_via_cache(rel, full, walk_start_ns)
                if sha is not None:
                    out[rel] = sha
            return out

        return await run_sync(hash_all)

    async def hash_file(self, rel_path: str) -> str | None:
        """One file's sha256; ``None`` when absent. Shares :meth:`hashtree`'s cache."""
        dest = self._resolve_under_root(rel_path)

        def one() -> str | None:
            try:
                st = dest.lstat()
            except FileNotFoundError:
                return None
            if stat.S_ISLNK(st.st_mode):
                raise FileStoreError(FileStoreError.IS_A_SYMLINK, rel_path)
            if not stat.S_ISREG(st.st_mode):
                raise FileStoreError(FileStoreError.NOT_A_FILE, rel_path)
            return self._hash_via_cache(dest.relative_to(self._root).as_posix(), dest, _now_ns())

        return await run_sync(one)

    async def move(self, src: str, dst: str) -> None:
        """Rename ``src`` to ``dst``; an existing ``dst`` is refused. The banned
        store root as either end does nothing."""
        s = self._resolve_under_root(src)
        d = self._resolve_under_root(dst)
        if s == self._root or d == self._root:
            return
        if await anyio.Path(d).exists():
            raise FileStoreError(FileStoreError.MOVE_DESTINATION_EXISTS, dst)
        await run_sync(_make_dirs_below_root, self._root, d.parent)
        await run_sync(os.rename, s, d)

    async def remove(self, rel_path: str) -> None:
        """Delete a file or subtree; absent — and the banned store root — do nothing."""
        dest = self._resolve_under_root(rel_path)
        if dest == self._root:
            return

        def delete() -> None:
            try:
                # lstat: a dangling symlink must still be unlinked.
                st = dest.lstat()
            except FileNotFoundError:
                return
            if stat.S_ISDIR(st.st_mode):
                shutil.rmtree(dest, ignore_errors=True)
            else:
                with suppress(FileNotFoundError):
                    os.unlink(dest)

        await run_sync(delete)

    def _resolve_under_root(self, rel_path: str) -> Path:
        norm = PurePosixPath(rel_path.replace("\\", "/").lstrip("/"))
        if norm.is_absolute() or ".." in norm.parts:
            raise FileStoreError(FileStoreError.ESCAPES_ROOT, rel_path)
        return self._root.joinpath(*norm.parts)

    def _require_utf8(self, rel_path: str, data: bytes) -> None:
        if not self._utf8_only:
            return
        try:
            data.decode("utf-8")
        except UnicodeDecodeError:
            raise FileStoreError(FileStoreError.NOT_UTF8, rel_path) from None

    def _hash_via_cache(self, rel: str, full: Path, walk_start_ns: int) -> str | None:
        try:
            st = full.lstat()
        except FileNotFoundError:
            return None  # vanished since the walk: not in this snapshot
        if not stat.S_ISREG(st.st_mode):
            return None
        cached = self._hashes.get(rel)
        if cached is not None and _unchanged_since_hashed(cached, st):
            sha = cached.sha
        else:
            try:
                sha = _hash_file(full)
            except (FileNotFoundError, FileStoreError):
                return None
            except OSError as e:
                if e.errno in (errno.ELOOP, errno.EMLINK):
                    return None
                raise
        if _old_enough_to_cache(st, walk_start_ns):
            self._hashes[rel] = _Hashed(st.st_mtime_ns, st.st_ctime_ns, st.st_size, sha)
        return sha


# The helpers below block; they are always called via run_sync.


def _platform_supported() -> bool:
    return _O_NOFOLLOW != 0


def _make_dir_and_ancestors(path: Path) -> None:
    missing: list[Path] = []
    current = path
    while not current.exists() and current != current.parent:
        missing.append(current)
        current = current.parent
    for directory in reversed(missing):
        with suppress(FileExistsError):
            os.mkdir(directory, _OWNER_ONLY_DIR_MODE)


def _make_dirs_below_root(root: Path, directory: Path) -> None:
    # Never the root itself: only create_root() makes it, so a write racing an
    # rm -rf of the folder fails with ENOENT instead of re-creating it.
    current = root
    for part in directory.relative_to(root).parts:
        current = current / part
        with suppress(FileExistsError):
            os.mkdir(current, _OWNER_ONLY_DIR_MODE)


def _replace_via_temp(dest: Path, data: bytes, is_executable: bool) -> None:
    mode = _OWNER_ONLY_EXEC_MODE if is_executable else _OWNER_ONLY_FILE_MODE
    tmp = dest.parent / f".fs-{os.urandom(8).hex()}.tmp"
    fd = os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_EXCL | _O_NOFOLLOW, mode)
    try:
        with os.fdopen(fd, "wb") as f:
            f.write(data)
        os.replace(tmp, dest)
    except BaseException:
        # Best-effort temp cleanup; never mask the original error.
        with suppress(OSError):
            os.unlink(tmp)
        raise


def _open_regular_file(rel_path: str, dest: Path) -> IO[bytes]:
    # O_NONBLOCK: a FIFO fails the fstat check below instead of blocking the open.
    try:
        fd = os.open(dest, os.O_RDONLY | _O_NOFOLLOW | _O_NONBLOCK)
    except OSError as e:
        # FreeBSD reports EMLINK rather than ELOOP for O_NOFOLLOW.
        if e.errno in (errno.ELOOP, errno.EMLINK):
            raise FileStoreError(FileStoreError.IS_A_SYMLINK, rel_path) from None
        raise
    try:
        if not stat.S_ISREG(os.fstat(fd).st_mode):
            raise FileStoreError(FileStoreError.NOT_A_FILE, rel_path)
    except BaseException:
        os.close(fd)
        raise
    return os.fdopen(fd, "rb")


def _hash_file(path: Path) -> str:
    digest = hashlib.sha256()
    with _open_regular_file(path.name, path) as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _raise_unless_vanished(error: OSError) -> None:
    # For os.walk, which otherwise skips an unreadable directory as if it were empty.
    if not isinstance(error, FileNotFoundError):
        raise error


def _filenames_in_dir(root: Path, under: str, base: Path) -> list[tuple[str, Path]]:
    """Every regular file under ``base`` as ``(rel_path, path)``; an absent
    ``base`` is empty, a present non-directory is refused."""
    try:
        st = base.lstat()
    except (FileNotFoundError, NotADirectoryError):
        return []
    if not stat.S_ISDIR(st.st_mode):
        raise FileStoreError(FileStoreError.NOT_A_DIRECTORY, under)
    out: list[tuple[str, Path]] = []
    # os.walk never descends symlinked directories (unlike rglob before 3.13).
    for dirpath, _dirnames, filenames in os.walk(base, onerror=_raise_unless_vanished):
        for name in filenames:
            full = Path(dirpath) / name
            try:
                fst = full.lstat()
            except FileNotFoundError:
                continue  # a listing is a snapshot, not a lock
            if stat.S_ISREG(fst.st_mode):
                out.append((full.relative_to(root).as_posix(), full))
    return out


def _symlinks_in_dir(root: Path, under: str, base: Path) -> set[str]:
    try:
        st = base.lstat()
    except (FileNotFoundError, NotADirectoryError):
        return set()
    if stat.S_ISLNK(st.st_mode):
        return {base.relative_to(root).as_posix()}
    if not stat.S_ISDIR(st.st_mode):
        raise FileStoreError(FileStoreError.NOT_A_DIRECTORY, under)
    out: set[str] = set()
    for dirpath, dirnames, filenames in os.walk(base, onerror=_raise_unless_vanished):
        for name in (*dirnames, *filenames):
            full = Path(dirpath) / name
            try:
                fst = full.lstat()
            except FileNotFoundError:
                continue
            if stat.S_ISLNK(fst.st_mode):
                out.add(full.relative_to(root).as_posix())
    return out


def _unchanged_since_hashed(cached: _Hashed, st: os.stat_result) -> bool:
    return (st.st_mtime_ns, st.st_ctime_ns, st.st_size) == (cached.mtime_ns, cached.ctime_ns, cached.size)


# Filesystems stamp times with coarse clocks, so a rewrite shortly after a
# hashed write can reuse the exact stamps. Files younger than the margin are
# simply re-hashed next walk.
_TIMESTAMP_TRUST_MARGIN_NS = 2_000_000_000

# Tests freeze this clock.
_now_ns = time.time_ns


def _old_enough_to_cache(st: os.stat_result, walk_start_ns: int) -> bool:
    return max(st.st_mtime_ns, st.st_ctime_ns) < walk_start_ns - _TIMESTAMP_TRUST_MARGIN_NS


LocalFileStore = FileStore
