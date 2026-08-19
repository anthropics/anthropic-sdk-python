"""Session-level memory-store download and sync.

A session may have several memory stores attached. This module resolves
where each store's folder goes on disk, opens a :class:`LocalFileStore`
there, and reconciles each folder with its remote store — the merge rules
live on :class:`SessionMemoryStores`.
"""

from __future__ import annotations

import os
import hashlib
import logging
from time import monotonic
from typing import TYPE_CHECKING, Literal, NamedTuple, cast
from pathlib import Path
from dataclasses import field, dataclass

import anyio

from ._file_store import FileStore, FileStoreError, LocalFileStore
from ..._exceptions import APIStatusError

if TYPE_CHECKING:
    from collections.abc import AsyncIterator

    from ..._client import AsyncAnthropic
    from ...types.beta import BetaManagedAgentsSession
    from ...types.beta.sessions import BetaManagedAgentsMemoryStoreResource
    from ...types.beta.memory_stores import BetaManagedAgentsMemory, BetaManagedAgentsMemoryView

__all__ = [
    "SessionMemoryStores",
    "SessionMemoryError",
    "MemoryDeleteMode",
    "DEFAULT_MEMORY_SYNC_INTERVAL",
    "MIN_MEMORY_SYNC_INTERVAL",
    "MEMORY_FLUSH_TIMEOUT",
    "MARKER_PATH",
]

#: Whether a locally deleted file may delete its server memory — ``"log_only"`` is the dry run.
MemoryDeleteMode = Literal["enabled", "log_only", "disabled"]

#: How often (seconds) the worker syncs the session's memory stores back
#: while the session runs. Checked after each dispatched tool call.
DEFAULT_MEMORY_SYNC_INTERVAL = 15.0

#: Smallest sync interval (seconds). Anything below it is rejected —
#: each sync lists every attached store, so sub-second cadences would
#: hammer the memory endpoints.
MIN_MEMORY_SYNC_INTERVAL = 5.0


def _check_sync_interval(interval: float) -> None:
    # Phrased so NaN fails: ``NaN < floor`` is False, so the inverse test
    # ``interval < floor`` would wave NaN through — and a NaN interval makes
    # every cadence check due, the exact hammering the floor exists to stop.
    if not interval >= MIN_MEMORY_SYNC_INTERVAL:
        raise ValueError(f"sync interval must be at least {MIN_MEMORY_SYNC_INTERVAL} seconds, got {interval}")


#: Bound (seconds) the worker puts on each shielded teardown pass — the final
#: sync, then the flush — so a slow server cannot stall teardown.
MEMORY_FLUSH_TIMEOUT = 30.0

#: Reserved marker at every store root — two lines: ``version <n>`` and the
#: store's ``memory_store_id``; a sync trusts the folder only when both match.
#: Never itself synced.
MARKER_PATH = ".anthropic-memory-store"

_MARKER_VERSION = 1


def _marker_sha(memory_store_id: str) -> str:
    return hashlib.sha256(f"version {_MARKER_VERSION}\n{memory_store_id}".encode("utf-8")).hexdigest()


#: How long (seconds) a file must stay missing before its server delete goes out.
DELETE_CORROBORATION_SECONDS = 30.0

#: Page sizes for memory listings — the API's maximum per view: ``basic``
#: pages carry up to 100 items, ``full`` pages are capped by the server.
_LIST_PAGE_SIZE = 100
_FULL_LIST_PAGE_SIZE = 20

#: How many single-memory content fetches may be in flight at once during
#: one store's pull pass. Well inside the client's keepalive pool (100),
#: so every fetch reuses a warm connection; a sync rarely pulls more than
#: a handful of memories, so a higher cap buys nothing in the common case.
_FETCH_CONCURRENCY = 16

#: How many uploads one store's flush keeps in flight. At ~0.3s per upload,
#: 32 clears the server's 2000-memories-per-store cap inside
#: :data:`MEMORY_FLUSH_TIMEOUT`; eight stores at once stay far below the
#: client's connection limit.
_UPLOAD_CONCURRENCY = 32

#: Bounds of the per-sync delete cap — the floor keeps small stores'
#: legitimate deletions from crawling.
_DELETE_CAP_FLOOR = 8
_DELETE_CAP_CEILING = 50

log = logging.getLogger("anthropic.lib.tools.agent_toolset")


class _MarkerScan(NamedTuple):
    """One directory scan — the marker checked and removed in the same read as the file listing."""

    files: dict[str, str]
    #: The scan found a marker naming this store — the only state that may drive uploads or deletes.
    marker_ok: bool
    #: Why the marker check failed; ``None`` when it passed.
    distrust_reason: str | None


class SessionMemoryError(Exception):
    """A memory store could not be materialised on disk.

    Raised by :meth:`SessionMemoryStores.download`; the worker lets it fail
    the work item.
    """


@dataclass
class _AttachedStore:
    """One attached store: its :class:`FileStore` on disk plus the sync baseline."""

    memory_store_id: str
    files: FileStore
    read_only: bool
    #: ``{rel_path → content sha}`` as of the last download or successful sync.
    baseline: dict[str, str] = field(default_factory=dict[str, str])
    #: ``{rel_path → sha}`` the server refused; retried only after the file changes.
    refused_shas: dict[str, str] = field(default_factory=dict[str, str])
    #: ``{rel_path → monotonic time first seen missing}``; the server delete waits for a later sync.
    pending_deletes: dict[str, float] = field(default_factory=dict[str, float])


@dataclass
class _DeletePass:
    """One sync's server-delete discipline: the mode, the cap, and what was held back."""

    mode: MemoryDeleteMode
    cap: int
    #: Skip the waiting window — no later sync is coming to confirm.
    waive_window: bool = False
    attempted: int = 0
    capped: int = 0
    suppressed: int = 0

    def take_slot(self) -> bool:
        if self.attempted >= self.cap:
            self.capped += 1
            return False
        self.attempted += 1
        return True


class SessionMemoryStores:
    """The memory stores attached to one session, materialised on disk.

    :meth:`download` opens a :class:`~._file_store.LocalFileStore` at each
    attached store's directory (its ``mount_path``, or a workdir fallback
    — see :meth:`download`), pulls its memories,
    and records each one's ``content_sha256`` as the sync baseline. Each
    sync (:meth:`sync_if_due` on the worker's cadence, :meth:`finish` once
    at the end) reconciles disk against server, per store and per path:

    - a memory changed only remotely is written to disk;
    - a file changed only locally is uploaded — an update with a
      ``content_sha256`` precondition, or a create for a new file;
    - a file changed on both sides logs a warning and takes the server
      version;
    - a file the server refuses (too large, invalid content) is skipped —
      warned once and retried only after the file changes; other files keep
      syncing;
    - a file deleted locally is deleted on the server, guarded by an
      ``expected_content_sha256`` precondition — a concurrent server-side
      edit wins and the file is restored instead. The delete never goes
      out on the first sync that sees the file missing: it waits
      :data:`DELETE_CORROBORATION_SECONDS`, re-checks the file and the
      marker, and each sync sends a bounded number — the rest wait.
      ``sync_deletions="log_only"`` runs the same checks and only logs;
      ``"disabled"`` turns server deletes off;
    - a memory deleted on the server is deleted on disk — unless the file
      holds an un-pushed edit, making it the only copy: a writable store
      re-creates the memory, a read-only store keeps the file unsynced;
    - a store attached read-only pulls but never pushes.

    A download pulls the whole store, so it lists with content included.
    The recurring syncs instead run two phases: a content-free listing
    (paths and shas) drives the merge decisions, then only the memories
    actually being written to disk are fetched, a bounded number at a
    time. A sync that finds nothing changed moves no content at all.

    A file whose write to disk failed is never in the baseline, so its
    absence reads as a failed download — it is pulled again, never deleted.
    A write never re-creates a store folder that vanished mid-sync: it fails,
    and the next sync's scan finds whatever is at the path by then — nothing
    (re-downloaded) or someone else's files (left alone) — under the rules below.

    :meth:`download` stamps :data:`MARKER_PATH` into the folder, and every
    sync checks it in the same directory scan it syncs from:

    - the folder or marker gone with no files left, or the marker intact
      but every one of two-or-more files gone at once: the store is
      re-downloaded — a full local wipe never propagates;
    - the marker gone or naming another store while files remain: the sync
      does nothing — those files never upload and never drive deletes.

    :meth:`download` raises :class:`SessionMemoryError` on the first store it
    cannot materialise. The syncs never raise: mid-session, one bad store
    or one bad file is logged and the rest continue. Instances are not safe for
    concurrent use. The worker builds one on its token-scoped sub-client (the
    memory endpoints reject the environment key): ``sync_if_due`` after each
    tool call, ``finish`` once at a clean end, a bounded
    :meth:`flush_writes` in every teardown, ``dispose`` last.
    """

    def __init__(
        self,
        client: AsyncAnthropic,
        *,
        workdir: str | os.PathLike[str],
        sync_interval: float = DEFAULT_MEMORY_SYNC_INTERVAL,
        sync_deletions: MemoryDeleteMode = "enabled",
    ) -> None:
        _check_sync_interval(sync_interval)
        self._client = client
        self._workdir = workdir
        self._sync_interval = sync_interval
        self._sync_deletions: MemoryDeleteMode = sync_deletions
        self._last_sync = monotonic()
        self._finished = False
        self._stores: list[_AttachedStore] = []

    @property
    def roots(self) -> list[Path]:
        """Every attached store's folder on disk.

        The worker adds these to the file tools' allowed roots, so a store
        mounted outside the working directory stays reachable.
        """
        return [s.files.root().path for s in self._stores]

    @property
    def read_only_roots(self) -> list[Path]:
        """Root directories of stores attached read-only.

        The file tools consult this to refuse writes into read-only stores.
        """
        return [s.files.root().path for s in self._stores if s.read_only]

    def _store_root(self, resource: BetaManagedAgentsMemoryStoreResource) -> Path:
        """Where one store's files land on disk.

        The store's files land at its ``mount_path`` — the very location the
        agent's system prompt tells it to read. A ``mount_path`` we cannot use
        verbatim is refused rather than quietly relocated: the agent would read
        an empty folder at the path it was told about, and write notes somewhere
        the next session looks for nothing.
        """
        if resource.mount_path:
            if not FileStore.is_path_legal(resource.mount_path):
                raise SessionMemoryError(
                    f"memory store mount_path is not a clean absolute path: {resource.mount_path!r} "
                    f"(memory_store_id={resource.memory_store_id})"
                )
            return Path(resource.mount_path)
        # No mount_path at all: nothing points the agent anywhere, so the
        # workdir is as good a home as any.
        return Path(self._workdir) / "memory" / (resource.name or resource.memory_store_id)

    async def download(self, session: BetaManagedAgentsSession) -> None:
        """Download every attached store's memories to disk.

        ``session`` arrives already fetched — one snapshot shared with the
        skills download.
        """
        plan = [(r, self._store_root(r)) for r in session.resources if r.type == "memory_store"]
        for resource, root in plan:
            store: _AttachedStore | None = None
            try:
                store = _AttachedStore(
                    memory_store_id=resource.memory_store_id,
                    # utf8_only: a binary file is refused at put/get, not mid-sync.
                    files=await LocalFileStore.open(root, utf8_only=True),
                    read_only=resource.access == "read_only",
                )
                # A root ``open`` did not create is a dead run's leftovers;
                # the first sync would upload them into the customer's store.
                if not store.files.root().removed_on_dispose:
                    # The configured path, not root().path — that one is
                    # resolved and would name a symlinked mount's target.
                    raise SessionMemoryError(
                        f"something already exists at the memory store's path: {root} "
                        f"(memory_store_id={resource.memory_store_id}); "
                        "it must not exist when the session starts"
                    )
                try:
                    await store.files.create_root()
                except OSError as e:
                    # An unmountable root fails the item, not just one file.
                    raise SessionMemoryError(
                        f"cannot create the memory store's folder: {root} "
                        f"(memory_store_id={resource.memory_store_id}): {e}; "
                        "the worker host must make this mount path writable"
                    ) from e
                await self._stamp_and_pull(store)
                log.info(
                    "downloaded %d memories memory_store_id=%s -> %s",
                    len(store.baseline),
                    store.memory_store_id,
                    store.files.root().path,
                )
                self._stores.append(store)
            except Exception as e:
                # A half-downloaded folder self-destructs; ``dispose`` leaves
                # a refused pre-existing directory exactly as found.
                if store is not None:
                    try:
                        await store.files.dispose()
                    except OSError:
                        pass
                # Every store must land: a session missing a folder its system
                # prompt names runs with amnesia and syncs nothing back.
                if isinstance(e, SessionMemoryError):
                    raise
                raise SessionMemoryError(
                    f"failed to download memory store memory_store_id={resource.memory_store_id}: {e}"
                ) from e
        self._last_sync = monotonic()

    async def finish(self) -> None:
        """The session's last sync — once, at a clean end.

        Same reconciliation as the cadence syncs, but server deletes skip
        the waiting window (the cap still applies). Raises on a second
        call — a repeat would keep skipping the window.
        """
        if self._finished:
            raise RuntimeError("finish() was already called: it is the session's last sync and runs once")
        self._finished = True
        await self._sync_all(final=True)

    async def _sync_all(self, *, final: bool) -> None:
        async with anyio.create_task_group() as tg:
            for store in self._stores:
                tg.start_soon(self._sync_store, store, final)
        self._last_sync = monotonic()

    async def _scan_marker(self, store: _AttachedStore) -> _MarkerScan:
        local = await store.files.hashtree()
        marker = local.pop(MARKER_PATH, None)
        if marker == _marker_sha(store.memory_store_id):
            return _MarkerScan(files=local, marker_ok=True, distrust_reason=None)
        return _MarkerScan(
            files=local,
            marker_ok=False,
            distrust_reason=(
                "the marker file does not match this store" if marker is not None else "the marker file is gone"
            ),
        )

    async def _sync_store(self, store: _AttachedStore, final: bool = False) -> None:
        try:
            scan = await self._scan_marker(store)
            local = scan.files
            if not scan.marker_ok:
                if local:
                    log.warning(
                        "%s; leaving the memory store folder as found and not syncing root=%s memory_store_id=%s",
                        scan.distrust_reason,
                        store.files.root().path,
                        store.memory_store_id,
                    )
                    return
                await self._recover(store, "the folder or its marker is gone")
                return
            # One file gone is a delete; every file gone at once is a wipe.
            if not local and len(store.baseline) > 1:
                await self._recover(store, "every memory file is gone at once")
                return

            remote = {item.path.lstrip("/"): item async for item in self._list_memories(store.memory_store_id)}

            deletes = _DeletePass(
                mode=self._sync_deletions,
                cap=max(_DELETE_CAP_FLOOR, min(_DELETE_CAP_CEILING, len(store.baseline) // 4)),
                waive_window=final,
            )
            pulls: list[tuple[str, BetaManagedAgentsMemory]] = []
            baseline: dict[str, str] = {}
            for rel in sorted({*remote, *local, *store.baseline}):
                remote_item = remote.get(rel)
                local_sha = local.get(rel)
                base_sha = store.baseline.get(rel)
                # Branch server-delete candidates off so the delete discipline
                # stays out of the merge rules.
                if (
                    local_sha is None
                    and base_sha is not None
                    and remote_item is not None
                    and remote_item.content_sha256 == base_sha
                    and not store.read_only
                ):
                    sha = await self._corroborated_delete(store, rel, remote_item, base_sha, deletes=deletes)
                else:
                    sha = await self._sync_path(store, rel, remote_item, local_sha, pulls=pulls)
                if sha is not None:
                    baseline[rel] = sha
            store.baseline = baseline
            # The content pass: everything above moved only shas.
            await self._pull_all(store, pulls)
            if deletes.suppressed:
                log.debug(
                    "server deletes are disabled; %d locally deleted memories stay on the server memory_store_id=%s",
                    deletes.suppressed,
                    store.memory_store_id,
                )
            if deletes.capped:
                log.warning(
                    "delete cap reached: %s %d deletes, held %d for later syncs memory_store_id=%s",
                    "would send" if deletes.mode == "log_only" else "sent",
                    deletes.attempted,
                    deletes.capped,
                    store.memory_store_id,
                )
        except Exception as e:
            log.warning("memory sync failed memory_store_id=%s: %s", store.memory_store_id, e)

    async def sync_if_due(self) -> None:
        """Run one sync when ``sync_interval`` has elapsed since the last.

        Stores sync in parallel; a store's own paths reconcile in a
        deterministic order. Never raises — a failure on one store is
        logged and the others continue.
        """
        if monotonic() - self._last_sync < self._sync_interval:
            return
        await self._sync_all(final=False)

    async def flush_writes(self) -> None:
        """Upload new and changed files; send no deletes and pull nothing.

        The push-only rescue pass for a session ending on an error or cancel —
        best-effort, bounded by the caller. Each store uploads a bounded number
        of files at a time; a store cut off part-way logs how many changed
        files it had not uploaded. Skips read-only stores, refused files, files
        the server already holds, and folders that fail the marker check.
        Never raises.
        """
        async with anyio.create_task_group() as tg:
            for store in self._stores:
                tg.start_soon(self._flush_store, store)

    async def _flush_store(self, store: _AttachedStore) -> None:
        dirty: dict[str, str] = {}
        unsent: set[str] = set()
        try:
            if store.read_only:
                return
            scan = await self._scan_marker(store)
            if not scan.marker_ok:
                log.warning(
                    "%s; not uploading anything from the memory store folder root=%s memory_store_id=%s",
                    scan.distrust_reason,
                    store.files.root().path,
                    store.memory_store_id,
                )
                return
            dirty = {
                rel: sha
                for rel, sha in scan.files.items()
                if sha != store.baseline.get(rel) and store.refused_shas.get(rel) != sha
            }
            if not dirty:
                return
            unsent.update(dirty)
            remote = {item.path.lstrip("/"): item async for item in self._list_memories(store.memory_store_id)}
            limiter = anyio.CapacityLimiter(_UPLOAD_CONCURRENCY)

            async def upload_one(rel: str, local_sha: str, existing: BetaManagedAgentsMemory | None) -> None:
                async with limiter:
                    sha = await self._upload(store, rel, local_sha, existing=existing)
                    unsent.discard(rel)
                    if sha is not None:
                        store.baseline[rel] = sha

            async with anyio.create_task_group() as tg:
                for rel in sorted(dirty):
                    local_sha = dirty[rel]
                    base_sha = store.baseline.get(rel)
                    existing = remote.get(rel)
                    if existing is not None and existing.content_sha256 == local_sha:
                        store.baseline[rel] = local_sha
                        unsent.discard(rel)
                        continue
                    if existing is not None and existing.content_sha256 != base_sha:
                        # A push-only pass cannot pull the winner over the file.
                        log.warning(
                            "memory changed both locally and remotely; the flush leaves the "
                            "remote version path=%s memory_store_id=%s",
                            rel,
                            store.memory_store_id,
                        )
                        unsent.discard(rel)
                        continue
                    tg.start_soon(upload_one, rel, local_sha, existing)
        except Exception as e:
            log.warning("memory flush failed memory_store_id=%s: %s", store.memory_store_id, e)
        except anyio.get_cancelled_exc_class():
            if unsent:
                log.warning(
                    "memory flush cut off part-way; %d of %d changed files had not finished uploading "
                    "memory_store_id=%s",
                    len(unsent),
                    len(dirty),
                    store.memory_store_id,
                )
            raise

    async def dispose(self) -> None:
        """Remove every store directory that :meth:`download` created.

        Pre-existing directories are left alone — that is
        :meth:`FileStore.dispose`'s own rule. A folder that holds files
        but fails the marker check is also kept — sync promised to leave
        it as found, and the next download refuses it visibly.
        """
        for store in self._stores:
            # The caller is tearing down and will not retry.
            try:
                root = store.files.root()
                scan = await self._scan_marker(store)
                if not scan.marker_ok and scan.files:
                    log.warning(
                        "%s; leaving the memory store folder on disk root=%s memory_store_id=%s",
                        scan.distrust_reason,
                        root.path,
                        store.memory_store_id,
                    )
                    continue
                await store.files.dispose()
            except (FileStoreError, OSError) as e:
                log.warning(
                    "failed to remove the memory store folder root=%s memory_store_id=%s: %s",
                    store.files.root().path,
                    store.memory_store_id,
                    e,
                )
                continue
            if root.removed_on_dispose:
                log.info("removed memory store dir %s memory_store_id=%s", root.path, store.memory_store_id)

    async def _recover(self, store: _AttachedStore, reason: str) -> None:
        """Rebuild a destroyed folder from the server; sends no deletes, no uploads."""
        log.warning(
            "%s; re-downloading the memory store folder instead of syncing root=%s memory_store_id=%s",
            reason,
            store.files.root().path,
            store.memory_store_id,
        )
        await store.files.create_root()
        await self._stamp_and_pull(store)

    async def _stamp_and_pull(self, store: _AttachedStore) -> None:
        """Write the trust marker, then pull every remote memory; pushes nothing.

        The baseline is cleared and rebuilt from successful writes only, so a
        failure mid-pull leaves no entry a later pass could read as a delete.
        Every memory is needed here, so the listing carries the content —
        pages cost far fewer round-trips than a request per memory.
        """
        store.baseline = {}
        # The disk was just rebuilt, so earlier absence observations mean nothing.
        store.pending_deletes.clear()
        await store.files.put(MARKER_PATH, f"version {_MARKER_VERSION}\n{store.memory_store_id}")
        async for item in self._list_memories(store.memory_store_id, view="full"):
            rel = item.path.lstrip("/")
            if await self._write(store, rel, item.content or ""):
                store.baseline[rel] = item.content_sha256

    async def _sync_path(
        self,
        store: _AttachedStore,
        rel: str,
        remote: BetaManagedAgentsMemory | None,
        local_sha: str | None,
        *,
        pulls: list[tuple[str, BetaManagedAgentsMemory]],
    ) -> str | None:
        base_sha = store.baseline.get(rel)
        if local_sha is not None:
            store.pending_deletes.pop(rel, None)

        if remote is None:
            if local_sha is None:
                store.pending_deletes.pop(rel, None)
                return None
            if base_sha is not None:
                if local_sha == base_sha:
                    fresh = await self._remove_local(store, rel, base_sha)
                    if fresh is None:
                        return None
                    if fresh == base_sha:
                        return base_sha
                    local_sha = fresh
                # An un-pushed edit exists only in this file, so the remote
                # delete loses: fall through and re-create it (writable) or
                # keep it on disk unsynced (read-only).
                if store.read_only:
                    log.warning(
                        "memory deleted remotely but edited locally; keeping the file, "
                        "which a read-only store cannot push path=%s memory_store_id=%s",
                        rel,
                        store.memory_store_id,
                    )
                elif store.refused_shas.get(rel) != local_sha:
                    log.info(
                        "memory deleted remotely but edited locally; re-creating it from the file "
                        "path=%s memory_store_id=%s",
                        rel,
                        store.memory_store_id,
                    )
            if store.read_only:
                return None
            if store.refused_shas.get(rel) == local_sha:
                return None
            return await self._upload(store, rel, local_sha, existing=None)

        remote_sha = remote.content_sha256
        remote_changed = remote_sha != base_sha
        locally_edited = local_sha is not None and local_sha not in (base_sha, remote_sha)
        # Read-only stores never push, so their local edits don't count.
        local_changed = not store.read_only and locally_edited

        if local_sha is None and base_sha is not None:
            # Only successful writes enter the baseline, so this file was
            # verifiably on disk and is now gone: a real local deletion.
            if remote_changed:
                log.warning(
                    "memory deleted locally but changed remotely; restoring the remote version "
                    "path=%s memory_store_id=%s",
                    rel,
                    store.memory_store_id,
                )
                store.pending_deletes.pop(rel, None)
                pulls.append((rel, remote))
            return base_sha

        if remote_changed:
            if local_sha == remote_sha:
                # The file already holds the remote bytes — adopt without a fetch.
                return remote_sha
            # Read-only edits never push, but overwriting one still logs.
            if locally_edited:
                log.warning(
                    "memory changed both locally and remotely; keeping the remote version path=%s memory_store_id=%s",
                    rel,
                    store.memory_store_id,
                )
            pulls.append((rel, remote))
            return base_sha
        if local_changed:
            if store.refused_shas.get(rel) == local_sha:
                return remote_sha
            # local_changed implies local_sha is present.
            return await self._upload(store, rel, cast(str, local_sha), existing=remote) or remote_sha
        return remote_sha

    async def _remove_local(self, store: _AttachedStore, rel: str, expect_sha: str) -> str | None:
        """Remove the file for a memory the server no longer has, if it still holds ``expect_sha``.

        Returns ``None`` when the file is gone from disk, ``expect_sha`` when it must
        stay in the baseline (I/O error, remove failed), or the file's fresh sha when
        it was edited since the scan.
        """
        try:
            fresh_sha = await store.files.hash_file(rel)
        except (FileStoreError, OSError):
            return expect_sha
        if fresh_sha is None:
            return None
        if fresh_sha != expect_sha:
            return fresh_sha
        try:
            await store.files.remove(rel)
        except (FileStoreError, OSError) as e:
            log.warning(
                "failed to remove memory deleted remotely path=%s memory_store_id=%s: %s",
                rel,
                store.memory_store_id,
                e,
            )
            return expect_sha
        return None

    async def _write(self, store: _AttachedStore, rel: str, content: str) -> bool:
        """Write a memory's content to disk; ``False`` (and a warning) on failure.

        A ``..`` component in the wire path reaches here as
        :class:`FileStoreError` — that is the escape guard.
        """
        try:
            await store.files.put(rel, content)
        except (FileStoreError, OSError) as e:
            log.warning("failed to write memory path=%s memory_store_id=%s: %s", rel, store.memory_store_id, e)
            return False
        return True

    async def _pull_all(self, store: _AttachedStore, pulls: list[tuple[str, BetaManagedAgentsMemory]]) -> None:
        """Fetch and write the given memories, :data:`_FETCH_CONCURRENCY` at a time.

        The sync's content pass: the listing carried no content, so each
        memory is fetched individually and written as it arrives. On
        success the path's baseline advances; on a failed fetch or write
        the old entry stays and the next sync retries. A 404 means the
        memory was deleted after the listing — the next sync reconciles it.
        """
        if not pulls:
            return
        limiter = anyio.CapacityLimiter(_FETCH_CONCURRENCY)

        async def pull_one(rel: str, listed: BetaManagedAgentsMemory) -> None:
            # The write stays inside the limiter so a slow disk cannot let
            # fetched bodies pile up beyond the concurrency bound.
            async with limiter:
                try:
                    item = await self._client.beta.memory_stores.memories.retrieve(
                        listed.id, memory_store_id=store.memory_store_id, view="full"
                    )
                except Exception as e:
                    if isinstance(e, APIStatusError) and e.status_code == 404:
                        return
                    log.warning(
                        "failed to fetch memory content path=%s memory_store_id=%s: %s", rel, store.memory_store_id, e
                    )
                    return
                if await self._write(store, rel, item.content or ""):
                    store.baseline[rel] = item.content_sha256

        async with anyio.create_task_group() as tg:
            for rel, listed in pulls:
                tg.start_soon(pull_one, rel, listed)

    async def _list_memories(
        self, memory_store_id: str, *, view: BetaManagedAgentsMemoryView = "basic"
    ) -> AsyncIterator[BetaManagedAgentsMemory]:
        """The store's memories — ``basic`` view (shas, no content) at
        :data:`_LIST_PAGE_SIZE` per page unless the caller needs ``full``
        pages. ``memory_prefix`` rollups and the reserved marker path are
        skipped."""
        limit = _LIST_PAGE_SIZE if view == "basic" else _FULL_LIST_PAGE_SIZE
        async for item in self._client.beta.memory_stores.memories.list(memory_store_id, view=view, limit=limit):
            if item.type != "memory":
                continue
            if item.path.lstrip("/") == MARKER_PATH:
                log.warning(
                    "the server listed the reserved marker path; skipping path=%s memory_store_id=%s",
                    item.path,
                    memory_store_id,
                )
                continue
            yield item

    async def _upload(
        self, store: _AttachedStore, rel: str, local_sha: str | None, *, existing: BetaManagedAgentsMemory | None
    ) -> str | None:
        """Push one local file; ``None`` keeps the old baseline so the next pass retries.

        A refusal the server would repeat (400/413, the utf-8 gate) enters
        ``refused_shas``: warned once, retried only after the file changes.
        """
        try:
            data = await store.files.get(rel)
            if data is None:
                return None
            if existing is None:
                item = await self._client.beta.memory_stores.memories.create(
                    store.memory_store_id, path="/" + rel, content=data.decode("utf-8")
                )
            else:
                item = await self._client.beta.memory_stores.memories.update(
                    existing.id,
                    memory_store_id=store.memory_store_id,
                    content=data.decode("utf-8"),
                    precondition={"type": "content_sha256", "content_sha256": existing.content_sha256},
                )
        except Exception as e:
            status = e.status_code if isinstance(e, APIStatusError) else None
            if existing is not None and status == 404:
                # Deleted remotely since the listing, so this file is now the only copy.
                return await self._upload(store, rel, local_sha, existing=None)
            permanent = isinstance(e, FileStoreError) or status in (400, 413)
            if existing is not None and status == 409:
                # The precondition lost a race: the remote moved under us, so
                # the push is dropped. The next sync pulls the winner over the
                # file; from the shutdown flush there is no next sync.
                log.warning(
                    "memory changed both locally and remotely; the upload was refused and the "
                    "local edit loses path=%s memory_store_id=%s",
                    rel,
                    store.memory_store_id,
                )
            elif permanent and local_sha is not None:
                store.refused_shas[rel] = local_sha
                log.warning(
                    "the server rejected this memory file, so it stays un-synced until its content "
                    "changes path=%s memory_store_id=%s rejection=%s",
                    rel,
                    store.memory_store_id,
                    e,
                )
            else:
                log.warning("failed to upload memory path=%s memory_store_id=%s: %s", rel, store.memory_store_id, e)
            return None
        store.refused_shas.pop(rel, None)
        return item.content_sha256

    async def _corroborated_delete(
        self,
        store: _AttachedStore,
        rel: str,
        remote: BetaManagedAgentsMemory,
        base_sha: str,
        *,
        deletes: _DeletePass,
    ) -> str | None:
        """Send the server delete only after the file's absence is confirmed.

        Records the miss on the first sync; deletes on a later one after
        the window, a fresh re-check, and the per-pass cap.
        """
        if deletes.mode == "disabled":
            deletes.suppressed += 1
            return base_sha
        first_absent = store.pending_deletes.setdefault(rel, monotonic())
        if not deletes.waive_window and monotonic() - first_absent < DELETE_CORROBORATION_SECONDS:
            return base_sha
        try:
            # Re-check now — the folder may have been destroyed mid-sync.
            marker_ok = await store.files.hash_file(MARKER_PATH) == _marker_sha(store.memory_store_id)
            still_absent = await store.files.hash_file(rel) is None
        except (FileStoreError, OSError):
            marker_ok = still_absent = False
        if not marker_ok:
            return base_sha
        if not still_absent:
            store.pending_deletes.pop(rel, None)
            return base_sha
        if not deletes.take_slot():
            return base_sha
        if deletes.mode == "log_only":
            # Repeats every sync — the dry run mirrors what "enabled" would keep trying.
            log.info(
                "log-only: sync would delete this memory on the server path=%s memory_store_id=%s",
                rel,
                store.memory_store_id,
            )
            return base_sha
        sha = await self._delete_remote(store, rel, remote, base_sha)
        if sha is None:
            store.pending_deletes.pop(rel, None)
        return sha

    async def _delete_remote(
        self, store: _AttachedStore, rel: str, remote: BetaManagedAgentsMemory, base_sha: str
    ) -> str | None:
        try:
            await self._client.beta.memory_stores.memories.delete(
                remote.id,
                memory_store_id=store.memory_store_id,
                expected_content_sha256=base_sha,
            )
        except Exception as e:
            status = e.status_code if isinstance(e, APIStatusError) else None
            if status == 404:
                return None  # already gone remotely too
            if status in (409, 412):
                log.warning(
                    "memory deleted locally but changed remotely; keeping the remote version "
                    "path=%s memory_store_id=%s",
                    rel,
                    store.memory_store_id,
                )
            else:
                log.warning("failed to delete memory path=%s memory_store_id=%s: %s", rel, store.memory_store_id, e)
            return base_sha
        log.info("propagated local deletion path=%s memory_store_id=%s", rel, store.memory_store_id)
        return None
