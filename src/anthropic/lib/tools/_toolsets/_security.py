"""Filesystem checks for browser toolsets.

`beta_check_upload_path` is default-deny: no roots means every path is refused. `BetaLocalFilePolicy`
is the file policy the SDK ships: upload roots, a download directory, and whether download paths
reach the model.
"""

from __future__ import annotations

import os
import re
import unicodedata
from pathlib import Path, PurePath
from collections.abc import Iterable, Sequence

from ._hooks import BetaURLContext
from ._errors import ToolsetConfigError, UploadNoRootsError, UploadRefusedError, UploadOutsideRootsError
from .._beta_functions import ToolError

__all__ = ["beta_check_upload_path", "BetaLocalFilePolicy"]

# beta_check_upload_path resolves a not-yet-existing path one component at a time (O(n) per component,
# O(n^2) overall), so a crafted path with tens of thousands of components stalls the tool for seconds.
# No real upload path is anywhere near this, so refuse an over-long one before the walk.
MAX_UPLOAD_PATH_LENGTH = 4096
ON_WINDOWS = os.name == "nt"
# Two leading separators of either kind: Windows reads "/\\host" and "\\/?" as UNC and device paths too.
UNC_OR_DEVICE_PATH_RE = re.compile(r"^[\\/]{2}")
DOS_DEVICE_NAME_RE = re.compile(
    r"^(?:CON|PRN|AUX|NUL|CONIN\$|CONOUT\$|COM[0-9\u00b9\u00b2\u00b3]|LPT[0-9\u00b9\u00b2\u00b3])(?:[.:].*)?$",
    re.IGNORECASE,
)


def realpath_lenient(path: str) -> Path:
    """`path` made absolute with every existing symlink resolved and `..` collapsed. Components that do not exist
    yet (a download directory to be created, a file under it) stay as written after the resolved prefix."""
    return Path(os.path.realpath(path))


def names_network_or_device(candidate: str) -> bool:
    """Whether, on Windows, `candidate` is a UNC / device-namespace path or has a component naming a DOS device.
    Elsewhere these are ordinary names (`aux/notes.txt`, `con.pdf`) and this is `False`: like the rest of this
    module's path checks, the answer is for the host this process runs on."""
    if not ON_WINDOWS:
        return False
    return bool(UNC_OR_DEVICE_PATH_RE.match(candidate)) or any(
        # Win32 resolves a device name from a path component's stem: the text up to the first "." or
        # ":", with trailing spaces and dots dropped. So "CON", "CON.txt", "CON .log" and "COM1 " all
        # name a device. Match that stem, and split components on ":" as well so a drive-relative
        # ("C:CON") or alternate-data-stream ("f.txt:CON") spelling is caught.
        DOS_DEVICE_NAME_RE.match(re.split(r"[.:]", part, maxsplit=1)[0].rstrip(" ."))
        for part in re.split(r"[\\/:]", candidate)
    )


def beta_check_upload_path(
    path: str | os.PathLike[str],
    roots: Sequence[str | os.PathLike[str]],
    *,
    strict_roots: bool = True,
) -> str:
    """Return the resolved path of `path` if it lies under one of `roots` (symlinks
    resolved on both sides, whole-component comparison), else raise `UploadRefusedError` (a `ToolError`).

    The refusal never lists the roots. Empty `roots` refuses everything. With `strict_roots`
    (the default), a root that does not resolve on disk grants nothing. Pass `strict_roots=False`
    for a lenient containment check that tolerates a not-yet-existing root.
    """
    if isinstance(roots, (str, bytes, os.PathLike)):
        # A bare str satisfies `Sequence[str]`, so beta_check_upload_path(p, "/srv/uploads") type-checks
        # and then iterates characters: the first, "/", resolves to a parent of every absolute
        # path and approves everything. Fail closed and loudly on the shape instead.
        raise ToolsetConfigError("roots must be a sequence of paths, not a single path")
    if not roots:
        raise UploadNoRootsError()

    candidate = os.fspath(path)
    if not candidate or "\x00" in candidate:
        raise UploadRefusedError("file_upload path is empty or contains a NUL byte")
    if len(candidate) > MAX_UPLOAD_PATH_LENGTH:
        raise UploadRefusedError("file_upload path is too long")

    if names_network_or_device(candidate):
        # Refused before anything touches the filesystem, on Windows: there, resolving a UNC path makes
        # the redirector connect to the named host with the user's credentials (a forced-auth
        # leak) even though the path is then refused, and a DOS device name (CON, COM1, NUL.txt)
        # is kept by `realpath` as an unresolved tail under the root, and then opens the device
        # rather than a file.
        raise UploadOutsideRootsError()

    usable_roots = [text for text in (os.fspath(r) for r in roots) if text.strip() and "\x00" not in text]
    if not usable_roots:
        # A list whose entries are all blank (an empty or stray-comma upload-roots setting) configures
        # no usable root, so report that rather than reporting the path as outside the roots.
        raise UploadNoRootsError()

    if strict_roots and any(part == ".." for part in re.split(r"[\\/]", candidate)):
        # An upload path is model output (the deployer supplies the roots, the model the path), so a
        # ".." component is never legitimate, and it is where a lexical ".." collapse can disagree
        # with symlink resolution. Refuse it outright. Scoped to strict_roots (uploads): the
        # download-path check refuses a '..' path itself, before it calls this.
        raise UploadRefusedError("file_upload path must not contain a '..' component")

    if strict_roots and not any(lexically_under(os.path.abspath(candidate), root) for root in usable_roots):
        # Decided on the text first: a path that does not even claim to be under an upload root is refused without
        # touching the filesystem, so the model cannot make the SDK stat or resolve a path of its choosing (an
        # existence probe, an automounted share). A path that does claim to be under a root is still resolved and
        # compared below, so a symlink inside the root cannot lead out of it.
        raise UploadOutsideRootsError()

    resolved = realpath_lenient(candidate)
    if names_network_or_device(str(resolved)):
        # On Windows, resolving a link to a share has already connected to its host with the user's credentials.
        # Screening the resolved path refuses the upload, but it cannot undo that connection.
        raise UploadOutsideRootsError()

    for root_text in usable_roots:
        try:
            resolved_root = Path(os.path.realpath(root_text, strict=strict_roots))
        except OSError:
            # strict_roots (upload roots): a root that does not exist grants
            # nothing. Accepting a not-yet-existing root leniently would admit a path under it now and
            # let the root be satisfied later by creating it as a symlink to somewhere outside the
            # deployment. Refusing here closes that. Never raised when strict_roots is False: the
            # download-path check tolerates a download_dir that does not exist yet.
            continue
        if resolved == resolved_root or PurePath(resolved_root) in PurePath(resolved).parents:
            return str(resolved)

    raise UploadOutsideRootsError()


def lexically_under(candidate: str, directory: str) -> bool:
    """Whether `candidate`, normalised as text, is `directory` (as written or as it resolves) or below it."""
    text = os.path.normcase(os.path.normpath(candidate))
    for base in {directory, str(realpath_lenient(directory))}:
        base = os.path.normcase(os.path.normpath(base))
        if text == base or text.startswith(base.rstrip("/\\") + os.sep):
            return True
    return False


def download_dir_conflicts(download_dir: str, upload_roots: Sequence[str]) -> bool:
    """Whether `download_dir` is inside (or contains) an upload root, which opens the download-then-upload
    loop: a page-triggered download written into an upload root is readable back through
    `file_upload`. Compared on the same resolved paths the upload check compares (symlinks
    followed as far as the path exists), so a `download_dir` that is a symlink into an upload
    root, or the other way round, is caught as well as the literal nesting."""
    literal = PurePath(os.path.normcase(download_dir))
    resolved = realpath_lenient(download_dir)
    folded = PurePath(os.path.normcase(str(resolved)))
    for root in upload_roots:
        resolved_root = realpath_lenient(root)
        pairs = ((literal, PurePath(os.path.normcase(root))), (folded, PurePath(os.path.normcase(str(resolved_root)))))
        for d, r in pairs:
            # a macOS disk usually ignores letter case and the Unicode form of a name
            d, r = (PurePath(unicodedata.normalize("NFC", str(p).casefold())) for p in (d, r))
            if d == r or r in d.parents or d in r.parents:
                return True
    return False


class BetaLocalFilePolicy:
    """The file policy the SDK ships: `file_upload` may read paths under `upload_roots` (symlinks
    resolved, whole components compared, a `..` component refused outright) and may name the document
    ids listed in `upload_document_ids` (none by default), and a `download_completed` path reaches
    the model only with `expose_download_paths=True` and only when it lies inside `download_dir`.

    Keep the roots to one dedicated directory holding only the task's files, and put
    `download_dir` outside every upload root and outside anything another tool can reach. The
    driver chooses where downloads are written. This object only controls what the model may see.
    """

    def __init__(
        self,
        *,
        upload_roots: Sequence[str | os.PathLike[str]] = (),
        upload_document_ids: Iterable[str] = (),
        download_dir: str | os.PathLike[str] | None = None,
        expose_download_paths: bool = False,
    ) -> None:
        if isinstance(upload_roots, (str, bytes, os.PathLike)):
            raise ToolsetConfigError("upload_roots must be a sequence of paths, not a single path")
        if isinstance(upload_document_ids, (str, bytes)):
            raise ToolsetConfigError("upload_document_ids must be a sequence of ids, not a single id")

        self._upload_document_ids = frozenset(upload_document_ids)  # read once: a generator is spent after one pass

        roots = [os.fspath(root) for root in upload_roots]
        if any(not root.strip() for root in roots):
            # Anchoring an empty entry would silently make it the working directory.
            raise ToolsetConfigError("upload_roots entries must not be empty")

        directory = None if download_dir is None else os.fspath(download_dir)
        if directory is not None and not directory.strip():
            raise ToolsetConfigError("download_dir must not be empty")

        # Anchored once, here: re-resolving a relative root against the working directory at check
        # time would move the containment boundary.
        self._upload_roots: list[str] = [os.path.abspath(root) for root in roots]
        self._download_dir: str | None = None if directory is None else os.path.abspath(directory)
        self._expose = expose_download_paths is True  # a truthy non-bool that got past the types exposes nothing

        if self._download_dir is not None and download_dir_conflicts(self._download_dir, self._upload_roots):
            raise ToolsetConfigError(
                f"download_dir {self._download_dir!r} must be outside every upload root, otherwise a page-triggered "
                "download landing in an upload root can be read back through file_upload"
            )

    @property
    def upload_roots(self) -> Sequence[str]:
        return tuple(self._upload_roots)

    @property
    def upload_document_ids(self) -> frozenset[str]:
        return self._upload_document_ids

    @property
    def download_dir(self) -> str | None:
        return self._download_dir

    @property
    def expose_download_paths(self) -> bool:
        return self._expose

    def resolve_upload_paths(self, context: BetaURLContext, paths: Sequence[str]) -> list[str]:  # noqa: ARG002
        return [beta_check_upload_path(path, self._upload_roots) for path in paths]

    def resolve_upload_documents(self, context: BetaURLContext, document_ids: Sequence[str]) -> list[str]:  # noqa: ARG002
        for doc in document_ids:
            if doc not in self._upload_document_ids:
                # Named by neither id nor count: the refusal must not tell a steering page which ids exist.
                raise UploadRefusedError("document not in the upload allowlist")
        return list(document_ids)

    def is_path_visible(self, path: str) -> bool:
        if not self._expose or self._download_dir is None:
            return False
        if not lexically_under(path, self._download_dir) or ".." in re.split(r"[\\/]", path):
            # Decided on the text alone: a path that does not even claim to be under the download directory, or
            # that has a ".." component, is never resolved, so a page cannot make the SDK stat a path of its choosing
            # (an automounted share, an existence probe) by getting it into a download event or an error message.
            return False

        try:
            beta_check_upload_path(path, [self._download_dir], strict_roots=False)
        except ToolError:
            # Outside the quarantine directory (a symlink that leads out of it): the event still reaches the
            # model, without the path.
            return False
        return True
