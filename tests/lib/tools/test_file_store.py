"""Tests for :class:`FileStore` — the confined-folder filesystem layer.

The verbs (``put`` / ``get`` / ``ls`` / ``find_symlinks`` / ``hashtree`` /
``hash_file`` / ``move`` / ``remove``) plus the open and ``async with``
lifecycle. These tests exercise the filesystem directly; consumers (memory
sync, the skills downloader, the builtin memory tool) get their own suites.
"""

from __future__ import annotations

import io
import os
import stat
import shutil
import hashlib
import zipfile
from pathlib import Path

import pytest
import pytest_asyncio

from anthropic.lib.tools._file_store import Root, FileStore, FileStoreError, LocalFileStore

pytestmark = pytest.mark.skipif(os.name != "posix", reason="FileStore refuses non-POSIX platforms")


def _sha(content: str | bytes) -> str:
    return hashlib.sha256(content.encode("utf-8") if isinstance(content, str) else content).hexdigest()


async def _created_store(root: Path, *, utf8_only: bool = False) -> FileStore:
    fs = await FileStore.open(root, utf8_only=utf8_only)
    await fs.create_root()
    return fs


@pytest_asyncio.fixture()
async def store(tmp_path: Path) -> FileStore:
    return await _created_store(tmp_path / "store")


def test_localfilestore_is_an_alias_for_the_combined_class() -> None:
    assert LocalFileStore is FileStore


@pytest.mark.asyncio()
async def test_filestore_put_writes_text_and_creates_owner_only_parents(store: FileStore) -> None:
    """``put`` creates nested parents 0o700 and stores text as UTF-8 (file 0o600)."""
    await store.put("projects/foo/notes.md", "héllo")

    dest = store.root().path / "projects" / "foo" / "notes.md"
    assert dest.read_text(encoding="utf-8") == "héllo"
    assert stat.S_IMODE(dest.parent.stat().st_mode) == 0o700
    assert stat.S_IMODE(dest.stat().st_mode) == 0o600


@pytest.mark.asyncio()
async def test_filestore_put_executable_sets_owner_exec(store: FileStore) -> None:
    await store.put("run.sh", b"#!/bin/sh\necho hi\n", is_executable=True)
    assert stat.S_IMODE((store.root().path / "run.sh").stat().st_mode) == 0o700


@pytest.mark.asyncio()
async def test_filestore_put_is_atomic_and_leaves_no_temp_on_success(store: FileStore) -> None:
    await store.put("a.md", "first")
    await store.put("a.md", "second")  # overwrite
    assert (store.root().path / "a.md").read_text() == "second"
    assert sorted(p.name for p in store.root().path.iterdir()) == ["a.md"]


@pytest.mark.asyncio()
async def test_filestore_creates_every_parent_owner_only_under_permissive_umask(tmp_path: Path) -> None:
    """Every directory the store creates — including intermediate parents, which
    ``mkdir(parents=True, mode=...)`` would leave at the umask default — is 0o700."""
    old_umask = os.umask(0)
    try:
        root = tmp_path / "nested" / "store"
        fs = await _created_store(root)
        await fs.put("projects/foo/notes.md", "hi")
        for directory in (tmp_path / "nested", root, root / "projects", root / "projects" / "foo"):
            assert stat.S_IMODE(directory.stat().st_mode) == 0o700, directory
    finally:
        os.umask(old_umask)


@pytest.mark.asyncio()
@pytest.mark.parametrize("bad", ["../secret.md", "a/../../secret.md"])
async def test_filestore_every_verb_refuses_an_escaping_path(tmp_path: Path, store: FileStore, bad: str) -> None:
    """``..`` (and absolute) paths raise FileStoreError on every verb; nothing
    is read or written outside the root."""
    (tmp_path / "secret.md").write_text("top secret")
    await store.put("ok.md", "ok")

    with pytest.raises(FileStoreError):
        await store.put(bad, "nope")
    with pytest.raises(FileStoreError):
        await store.get(bad)
    with pytest.raises(FileStoreError):
        await store.ls(bad)
    with pytest.raises(FileStoreError):
        await store.hashtree(bad)
    with pytest.raises(FileStoreError):
        await store.hash_file(bad)
    with pytest.raises(FileStoreError):
        await store.find_symlinks(bad)
    with pytest.raises(FileStoreError):
        await store.move("ok.md", bad)
    with pytest.raises(FileStoreError):
        await store.move(bad, "landed.md")
    with pytest.raises(FileStoreError):
        await store.remove(bad)

    assert (tmp_path / "secret.md").read_text() == "top secret"


@pytest.mark.asyncio()
async def test_filestore_get_does_not_follow_a_symlink_leaf(store: FileStore) -> None:
    """A symlink at the target is refused on read and replaced — not written
    through — on put."""
    await store.put("real.md", "original")
    os.symlink(store.root().path / "real.md", store.root().path / "link.md")

    with pytest.raises(FileStoreError):
        await store.get("link.md")
    await store.put("link.md", "new")
    assert (store.root().path / "real.md").read_text() == "original"
    assert not (store.root().path / "link.md").is_symlink()
    assert (store.root().path / "link.md").read_text() == "new"


@pytest.mark.asyncio()
async def test_filestore_get_refuses_a_non_regular_file(store: FileStore) -> None:
    """A present-but-non-regular leaf (fifo, symlink, ...) raises FileStoreError
    instead of hanging or being read."""
    os.mkfifo(store.root().path / "pipe.md")
    os.symlink(store.root().path / "pipe.md", store.root().path / "link.md")

    with pytest.raises(FileStoreError, match="not a regular file"):
        await store.get("pipe.md")
    with pytest.raises(FileStoreError, match="is a symlink"):
        await store.get("link.md")

    # The open itself must refuse the fifo (O_NONBLOCK + fstat) — it must not
    # block the read forever.
    from anthropic.lib.tools import _file_store as mod

    with pytest.raises(FileStoreError, match="not a regular file"):
        mod._open_regular_file("pipe.md", store.root().path / "pipe.md")


@pytest.mark.asyncio()
async def test_filestore_get_returns_none_when_absent(store: FileStore) -> None:
    assert await store.get("absent.md") is None
    await store.put("present.md", "here")
    assert await store.get("present.md") == b"here"


@pytest.mark.asyncio()
async def test_filestore_ls_lists_recursively_and_never_descends_symlinks(tmp_path: Path, store: FileStore) -> None:
    await store.put("a.md", "alpha")
    await store.put("sub/b.md", "bravo")
    outside = tmp_path / "outside"
    outside.mkdir()
    (outside / "s.md").write_text("secret")
    os.symlink(outside, store.root().path / "lnkdir")
    os.symlink(outside / "s.md", store.root().path / "lnk.md")

    assert await store.ls() == {"a.md", "sub/b.md"}
    assert await store.ls("sub") == {"sub/b.md"}
    assert await store.ls("absent") == set()
    assert await store.ls("a.md/under") == set()
    with pytest.raises(FileStoreError, match="not a directory"):
        await store.ls("a.md")


@pytest.mark.asyncio()
async def test_filestore_find_symlinks_reports_every_symlink(tmp_path: Path, store: FileStore) -> None:
    """Listings skip symlinks silently; ``find_symlinks`` is how a caller sees them."""
    await store.put("a.md", "alpha")
    await store.put("sub/b.md", "bravo")
    assert await store.find_symlinks() == set()

    outside = tmp_path / "outside"
    outside.mkdir()
    (outside / "s.md").write_text("secret")
    os.symlink(outside, store.root().path / "lnkdir")
    os.symlink(outside / "s.md", store.root().path / "sub" / "lnk.md")
    os.symlink(store.root().path / "gone.md", store.root().path / "dangling.md")

    assert await store.find_symlinks() == {"lnkdir", "sub/lnk.md", "dangling.md"}
    assert await store.find_symlinks("sub") == {"sub/lnk.md"}
    assert await store.find_symlinks("absent") == set()


@pytest.mark.asyncio()
async def test_filestore_hashtree_hashes_regular_files_and_skips_symlinks(tmp_path: Path, store: FileStore) -> None:
    await store.put("a.md", "alpha")
    await store.put("sub/b.md", "bravo")
    outside = tmp_path / "secret.txt"
    outside.write_text("secret")
    os.symlink(outside, store.root().path / "link.md")

    assert await store.hashtree() == {"a.md": _sha("alpha"), "sub/b.md": _sha("bravo")}
    assert await store.hashtree("sub/") == {"sub/b.md": _sha("bravo")}


@pytest.mark.skipif(os.geteuid() == 0, reason="permission checks do not bind root")
@pytest.mark.asyncio()
async def test_filestore_listings_raise_on_an_unreadable_subdirectory(store: FileStore) -> None:
    """An unreadable subdirectory fails the listing rather than dropping out of it."""
    await store.put("a.md", "alpha")
    await store.put("locked/b.md", "bravo")
    locked = store.root().path / "locked"
    locked.chmod(0o000)
    try:
        with pytest.raises(PermissionError):
            await store.hashtree()
        with pytest.raises(PermissionError):
            await store.ls()
        with pytest.raises(PermissionError):
            await store.find_symlinks()
    finally:
        locked.chmod(0o700)
    assert await store.hashtree() == {"a.md": _sha("alpha"), "locked/b.md": _sha("bravo")}


@pytest.mark.asyncio()
async def test_filestore_hashtree_refuses_a_symlinked_prefix(tmp_path: Path, store: FileStore) -> None:
    """A prefix that is a symlink (here to a directory outside the root) is
    refused, not silently listed as empty."""
    outside = tmp_path / "outside"
    outside.mkdir()
    (outside / "secret.md").write_text("secret")
    os.symlink(outside, store.root().path / "sub")

    with pytest.raises(FileStoreError):
        await store.hashtree("sub")


@pytest.mark.asyncio()
async def test_filestore_hash_file_hashes_one_file_and_shares_the_cache(
    store: FileStore, monkeypatch: pytest.MonkeyPatch
) -> None:
    from anthropic.lib.tools import _file_store as mod

    monkeypatch.setattr(mod, "_TIMESTAMP_TRUST_MARGIN_NS", -(10**15))
    hashed: list[str] = []
    real_hash = mod._hash_file

    def counting_hash(path: Path) -> str:
        hashed.append(path.name)
        return real_hash(path)

    monkeypatch.setattr(mod, "_hash_file", counting_hash)

    await store.put("a.md", "alpha")
    assert await store.hash_file("a.md") == _sha("alpha")
    assert await store.hash_file("absent.md") is None
    # hashtree reuses the entry hash_file just cached.
    assert await store.hashtree() == {"a.md": _sha("alpha")}
    assert hashed == ["a.md"]

    os.symlink(store.root().path / "a.md", store.root().path / "lnk.md")
    with pytest.raises(FileStoreError, match="is a symlink"):
        await store.hash_file("lnk.md")


@pytest.mark.asyncio()
async def test_filestore_move_renames_within_root_and_refuses_existing_dest(store: FileStore) -> None:
    await store.put("a.md", "alpha")
    await store.move("a.md", "nested/b.md")
    assert await store.get("nested/b.md") == b"alpha"
    assert await store.get("a.md") is None

    await store.put("c.md", "charlie")
    with pytest.raises(FileStoreError, match="exists"):
        await store.move("nested/b.md", "c.md")


@pytest.mark.asyncio()
async def test_filestore_root_path_is_banned_from_the_interface(store: FileStore) -> None:
    """A rel_path resolving to the root: put/get refuse, move/remove do nothing."""
    await store.put("x.md", "x")

    await store.remove("/")  # no-op
    assert await store.get("x.md") == b"x"
    await store.move("/", "elsewhere")  # no-op
    await store.move("x.md", "/")  # no-op
    assert await store.ls() == {"x.md"}

    with pytest.raises(FileStoreError):
        await store.put("/", "data")
    with pytest.raises(FileStoreError, match="not a regular file"):
        await store.get("/")


@pytest.mark.asyncio()
async def test_filestore_remove_deletes_file_and_subtree(store: FileStore) -> None:
    await store.put("a.md", "a")
    await store.put("sub/b.md", "b")

    await store.remove("a.md")
    assert not (store.root().path / "a.md").exists()
    await store.remove("sub")
    assert not (store.root().path / "sub").exists()
    await store.remove("absent.md")  # no-op


@pytest.mark.asyncio()
async def test_filestore_remove_unlinks_a_dangling_symlink(store: FileStore) -> None:
    os.symlink(store.root().path / "gone.md", store.root().path / "dangling.md")

    await store.remove("dangling.md")
    assert not (store.root().path / "dangling.md").is_symlink()


@pytest.mark.skipif(os.geteuid() == 0, reason="permission checks do not bind root")
@pytest.mark.asyncio()
async def test_filestore_open_raises_on_an_unreadable_mount_path(tmp_path: Path) -> None:
    """A mount path the process cannot stat raises at open — it is never read
    as absent, which would mark a real directory ours to remove on dispose."""
    locked = tmp_path / "locked"
    (locked / "store").mkdir(parents=True)
    locked.chmod(0o000)
    try:
        with pytest.raises(PermissionError):
            await FileStore.open(locked / "store")
    finally:
        locked.chmod(0o700)


@pytest.mark.asyncio()
async def test_filestore_async_with_removes_root_only_if_created(tmp_path: Path) -> None:
    async with await _created_store(tmp_path / "fresh") as fs:
        await fs.put("x.md", "x")
        assert fs.root() == Root(path=(tmp_path / "fresh").resolve(), removed_on_dispose=True)
    assert not (tmp_path / "fresh").exists()

    (tmp_path / "old").mkdir()
    async with await FileStore.open(tmp_path / "old") as fs:
        await fs.put("y.md", "y")
        assert not fs.root().removed_on_dispose
    assert (tmp_path / "old" / "y.md").read_text() == "y"


@pytest.mark.asyncio()
async def test_filestore_dispose_removes_the_root_it_created_and_keeps_preexisting(tmp_path: Path) -> None:
    fresh = await _created_store(tmp_path / "fresh")
    await fresh.put("x.md", "x")
    await fresh.dispose()
    assert not (tmp_path / "fresh").exists()

    (tmp_path / "old").mkdir()
    old = await FileStore.open(tmp_path / "old")
    await old.put("y.md", "y")
    await old.dispose()
    assert (tmp_path / "old" / "y.md").read_text() == "y"


@pytest.mark.asyncio()
async def test_filestore_put_writes_archive_bytes_verbatim(store: FileStore) -> None:
    """Archive-shaped bytes land as a single byte-identical file — extraction
    is never inferred from the content."""
    bio = io.BytesIO()
    with zipfile.ZipFile(bio, "w") as zf:
        zf.writestr(zipfile.ZipInfo("pdf/SKILL.md"), b"# pdf")
    blob = bio.getvalue()

    await store.put("bundle.zip", blob)
    assert await store.get("bundle.zip") == blob
    assert await store.hashtree() == {"bundle.zip": _sha(blob)}


@pytest.mark.asyncio()
@pytest.mark.parametrize("bad", ["bundles/v1/", "dir/.", ".", "/", ""])
async def test_filestore_put_refuses_a_directory_rel(store: FileStore, bad: str) -> None:
    with pytest.raises(FileStoreError):
        await store.put(bad, b"data")
    assert await store.hashtree() == {}


@pytest.mark.asyncio()
async def test_filestore_utf8_restriction_refuses_binary_content(tmp_path: Path) -> None:
    """A store opened with ``utf8_only=True`` refuses binary content on both
    verbs that touch it: a put of invalid bytes writes nothing, and a get of a
    file that bypassed the store (written directly to disk) is refused rather
    than returned — so callers that decode get's result can never throw."""
    store = await _created_store(tmp_path / "store", utf8_only=True)
    binary = b"\xff\xfe\x00 not utf-8"

    with pytest.raises(FileStoreError, match="not valid utf-8"):
        await store.put("blob.bin", binary)
    assert not (tmp_path / "store" / "blob.bin").exists()

    # str puts and conforming bytes are unaffected.
    await store.put("note.md", "hello")
    await store.put("bytes.md", "hello".encode())
    assert await store.get("note.md") == b"hello"

    # A file smuggled in behind the store's back is refused at get.
    (tmp_path / "store" / "smuggled.bin").write_bytes(binary)
    with pytest.raises(FileStoreError, match="not valid utf-8"):
        await store.get("smuggled.bin")

    # An unrestricted store keeps returning raw bytes.
    loose = await _created_store(tmp_path / "store2")
    await loose.put("blob.bin", binary)
    assert await loose.get("blob.bin") == binary


def test_filestore_is_path_legal() -> None:
    assert FileStore.is_path_legal("/mnt/memory/notes")
    assert not FileStore.is_path_legal("mnt/relative")
    assert not FileStore.is_path_legal("/mnt/../../etc/cron.d")
    assert not FileStore.is_path_legal("")


@pytest.mark.asyncio()
async def test_filestore_hashtree_rehashes_only_what_changed(store: FileStore, monkeypatch: pytest.MonkeyPatch) -> None:
    """A file whose stat identity (mtime, ctime, size) is unchanged since the
    last walk is served from the cache; a changed file is re-read. The trust
    margin is disabled here so fresh files cache immediately; a writer that
    restores mtime and size (``rsync -t`` style) is still re-hashed, because
    userspace cannot restore ctime."""
    from anthropic.lib.tools import _file_store as mod

    monkeypatch.setattr(mod, "_TIMESTAMP_TRUST_MARGIN_NS", -(10**15))
    hashed: list[str] = []
    real_hash = mod._hash_file

    def counting_hash(path: Path) -> str:
        hashed.append(path.name)
        return real_hash(path)

    monkeypatch.setattr(mod, "_hash_file", counting_hash)

    await store.put("a.md", "alpha")
    await store.put("b.md", "bravo")
    assert await store.hashtree() == {"a.md": _sha("alpha"), "b.md": _sha("bravo")}
    assert sorted(hashed) == ["a.md", "b.md"]

    hashed.clear()
    assert await store.hashtree() == {"a.md": _sha("alpha"), "b.md": _sha("bravo")}
    assert hashed == []

    # An mtime-and-size-preserving rewrite: same length, mtime restored. The
    # sleep guarantees the rewrite's ctime lands on a later coarse-clock tick
    # than the original's — ctime is the one stamp the rewrite cannot restore.
    import time as time_mod

    time_mod.sleep(0.05)
    b = store.root().path / "b.md"
    st = b.stat()
    b.write_text("BRAVO")
    os.utime(b, ns=(st.st_atime_ns, st.st_mtime_ns))
    assert (await store.hashtree())["b.md"] == _sha("BRAVO")
    assert hashed == ["b.md"]


@pytest.mark.asyncio()
async def test_filestore_hashtree_distrusts_fresh_stamps(store: FileStore, monkeypatch: pytest.MonkeyPatch) -> None:
    """Filesystems stamp times with coarse clocks, so a same-tick rewrite can
    reuse the exact stat identity of the version just hashed. A file whose
    stamps are within the trust margin of the walk is never cached — pinned
    by freezing the walk clock at the file's own stamp time."""
    from anthropic.lib.tools import _file_store as mod

    hashed: list[str] = []
    real_hash = mod._hash_file

    def counting_hash(path: Path) -> str:
        hashed.append(path.name)
        return real_hash(path)

    monkeypatch.setattr(mod, "_hash_file", counting_hash)

    await store.put("racy.md", "AAAAAA")
    stamp = (store.root().path / "racy.md").stat().st_ctime_ns
    monkeypatch.setattr(mod, "_now_ns", lambda: stamp)

    assert (await store.hashtree())["racy.md"] == _sha("AAAAAA")
    assert (await store.hashtree())["racy.md"] == _sha("AAAAAA")
    # Both walks hashed: nothing this fresh is ever cached.
    assert hashed == ["racy.md", "racy.md"]

    # What the margin defends: a same-tick rewrite that preserves the whole
    # stat identity must be seen by the next walk.
    (store.root().path / "racy.md").write_text("BBBBBB")
    assert (await store.hashtree())["racy.md"] == _sha("BBBBBB")

    # The margin's width is part of the contract: stamps 1.5s old are still
    # distrusted (coarse filesystems stamp in whole seconds); 10s-old stamps
    # are safely past it.
    hashed.clear()
    now = (store.root().path / "racy.md").stat().st_ctime_ns
    monkeypatch.setattr(mod, "_now_ns", lambda: now + 1_500_000_000)
    await store.hashtree()
    await store.hashtree()
    assert hashed == ["racy.md", "racy.md"]
    monkeypatch.setattr(mod, "_now_ns", lambda: now + 10_000_000_000)
    await store.hashtree()
    await store.hashtree()
    assert hashed == ["racy.md"] * 3


@pytest.mark.asyncio()
async def test_filestore_create_root_makes_the_folder_owner_only(tmp_path: Path) -> None:
    store = await FileStore.open(tmp_path / "store")
    await store.create_root()
    assert stat.S_IMODE((tmp_path / "store").stat().st_mode) == 0o700
    await store.create_root()  # already existing is fine
    assert store.root().removed_on_dispose


@pytest.mark.asyncio()
async def test_filestore_put_never_creates_a_missing_root(tmp_path: Path) -> None:
    """Only create_root() makes the folder: a put into a store that was never
    created, or whose folder was removed, raises and re-creates nothing — not
    the root and nothing above it."""
    root = tmp_path / "mnt" / "store"
    fs = await FileStore.open(root)

    with pytest.raises(FileNotFoundError):
        await fs.put("a.md", "a")
    with pytest.raises(FileNotFoundError):
        await fs.put("sub/a.md", "a")
    assert not (tmp_path / "mnt").exists()

    await fs.create_root()
    await fs.put("a.md", "a")
    shutil.rmtree(root)
    with pytest.raises(FileNotFoundError):
        await fs.put("b.md", "b")
    with pytest.raises(FileNotFoundError):
        await fs.put("sub/b.md", "b")
    assert not root.exists()

    shutil.rmtree(tmp_path / "mnt")
    with pytest.raises(FileNotFoundError):
        await fs.put("z.md", "z")
    assert not (tmp_path / "mnt").exists()

    await fs.create_root()
    await fs.put("z.md", "z")
    assert await fs.get("z.md") == b"z"


@pytest.mark.asyncio()
async def test_filestore_move_never_creates_a_missing_root(store: FileStore) -> None:
    await store.put("a.md", "a")
    shutil.rmtree(store.root().path)

    with pytest.raises(FileNotFoundError):
        await store.move("a.md", "sub/b.md")
    assert not store.root().path.exists()
