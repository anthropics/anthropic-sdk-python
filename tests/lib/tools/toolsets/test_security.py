from __future__ import annotations

import os
import re
from pathlib import Path

import pytest

from anthropic.tools import (
    ToolError,
    ToolsetConfigError,
)
from anthropic.tools.browser import (
    BetaURLContext,
    BetaLocalFilePolicy,
    beta_check_upload_path,
)
from anthropic.lib.tools._toolsets import _security

# The refusal texts the model reads for an upload path; pinned because they must never name a root.
UPLOAD_OUTSIDE_ROOTS = "file_upload path is outside the configured upload roots"
UPLOAD_NO_ROOTS = "file_upload has no configured upload roots"
UPLOAD_EMPTY_PATH = "file_upload path is empty or contains a NUL byte"
UPLOAD_DOTDOT = "file_upload path must not contain a '..' component"


def test_upload_path_table(tmp_path: Path) -> None:
    root = tmp_path / "srv" / "upload"
    root.mkdir(parents=True)
    (root / "ok.txt").write_text("x")
    (tmp_path / "srv" / "uploads-old").mkdir()
    (tmp_path / "srv" / "uploads-old" / "x").write_text("x")
    (tmp_path / "secret").write_text("s")
    os.symlink(tmp_path / "secret", root / "link-out")
    os.symlink(root / "link-out", root / "chain")
    roots = [str(root)]

    assert beta_check_upload_path(str(root / "ok.txt"), roots) == str((root / "ok.txt").resolve())
    assert beta_check_upload_path(str(root), roots) == str(root.resolve())
    assert beta_check_upload_path(str(root / "."), roots) == str(root.resolve())
    assert beta_check_upload_path(str(root / "new" / "file.bin"), roots) == str(root.resolve() / "new" / "file.bin")
    assert beta_check_upload_path(str(root / "ok.txt"), [str(tmp_path / "nope"), str(root)]) == str(
        (root / "ok.txt").resolve()
    )

    for bad in [
        str(tmp_path / "srv" / "uploads-old" / "x"),
        str(root / "link-out"),
        str(root / "chain"),
        "relative/path.txt",
    ]:
        with pytest.raises(ToolError) as info:
            beta_check_upload_path(bad, roots)
        assert info.value.content == UPLOAD_OUTSIDE_ROOTS, bad
    for dots in [str(root / ".." / "uploads-old" / "x"), str(root / ".." / ".." / "secret")]:
        with pytest.raises(ToolError) as info:
            beta_check_upload_path(dots, roots)
        assert info.value.content == UPLOAD_DOTDOT, dots

    with pytest.raises(ToolError) as info:
        beta_check_upload_path(str(root / "ok.txt"), [])
    assert info.value.content == UPLOAD_NO_ROOTS
    for invalid in ["", "a\x00b"]:
        with pytest.raises(ToolError) as info:
            beta_check_upload_path(invalid, roots)
        assert info.value.content == UPLOAD_EMPTY_PATH


def test_upload_sibling_prefix_is_not_a_root_match(tmp_path: Path) -> None:
    (tmp_path / "upload").mkdir()
    (tmp_path / "upload-evil").mkdir()
    (tmp_path / "upload-evil" / "x").write_text("x")
    with pytest.raises(ToolError):
        beta_check_upload_path(str(tmp_path / "upload-evil" / "x"), [str(tmp_path / "upload")])


def test_upload_dotdot_component_is_refused(tmp_path: Path) -> None:
    """A `..` component is refused before resolution, so it cannot survive into the
    not-yet-existing tail and let a lexical containment check pass a path that denotes a file
    outside the root."""
    root = tmp_path / "srv" / "upload"
    root.mkdir(parents=True)
    (tmp_path / "secret").write_text("s")
    for bad in [
        str(root / "ghost" / ".." / ".." / ".." / "secret"),
        str(root / "ghost" / ".." / ".." / "secret"),
        str(root / "a" / "b" / ".." / ".." / ".." / "secret"),
        str(root / "ghost" / ".." / "file.bin"),
    ]:
        with pytest.raises(ToolError) as info:
            beta_check_upload_path(bad, [str(root)])
        assert info.value.content == UPLOAD_DOTDOT, bad


def test_a_single_path_string_is_a_config_error() -> None:
    """`Sequence[str]` is structurally satisfied by `str`, so this type-checks clean.

    Iterating one would walk characters: the `"/"` element is a parent of every
    absolute path and approves everything — a fail-open in the default-deny direction.
    """
    with pytest.raises(ToolsetConfigError):
        beta_check_upload_path("/etc/passwd", "/srv/uploads")


def test_a_dangling_symlink_in_a_root_is_judged_by_its_target_and_a_cycle_resolves_as_written(tmp_path: Path) -> None:
    """A symlink under a root that names a missing file elsewhere resolves to that target, so the root check
    refuses it; a symlink cycle has no target and stays as written (opening it fails with ELOOP)."""
    root = tmp_path / "upload"
    root.mkdir()
    outside = tmp_path / "outside"
    outside.mkdir()
    os.symlink(outside / "gone.txt", root / "dangling")
    os.symlink(root / "b", root / "a")
    os.symlink(root / "a", root / "b")

    with pytest.raises(ToolError) as info:
        beta_check_upload_path(str(root / "dangling"), [str(root)])
    assert info.value.content == UPLOAD_OUTSIDE_ROOTS

    for loop in ["a", "b"]:
        assert beta_check_upload_path(str(root / loop), [str(root)]) == str(root.resolve() / loop)

    # a genuinely absent child still resolves
    assert beta_check_upload_path(str(root / "new.bin"), [str(root)]) == str(root.resolve() / "new.bin")


def test_an_upload_path_outside_every_root_is_refused_without_touching_the_filesystem(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    # A path that does not even claim to be under an upload root is refused on its text: the SDK never stats or
    # resolves a path of the model's choosing (an existence probe, an automounted share). A path that does claim to
    # be under a root is still resolved, so a symlink inside the root that points out of it is refused.
    root = tmp_path / "uploads"
    root.mkdir()
    os.symlink(tmp_path, root / "escape")
    resolved: list[str] = []
    real_realpath_lenient = _security.realpath_lenient

    def spy(path: str) -> Path:
        resolved.append(path)
        return real_realpath_lenient(path)

    monkeypatch.setattr(_security, "realpath_lenient", spy)
    with pytest.raises(ToolError, match="outside the configured upload roots"):
        beta_check_upload_path("/net/elsewhere.example/share/f", [str(root)])
    assert not [path for path in resolved if "elsewhere" in path]  # only the deployer's root was looked at

    escape = str(root / "escape" / "secret")
    with pytest.raises(ToolError, match="outside the configured upload roots"):
        beta_check_upload_path(escape, [str(root)])
    assert escape in resolved  # the spy sees a path that is resolved, so the empty result above means something
    assert beta_check_upload_path(str(root / "f.txt"), [str(root)]) == str(root.resolve() / "f.txt")


def test_a_download_path_outside_the_download_dir_is_hidden_without_touching_the_filesystem(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    # As for uploads: a path that does not claim to be under the download directory is judged on its text alone, so a
    # page cannot make the SDK resolve a path of its choosing by getting it into a download event.
    download_dir = tmp_path / "downloads"
    download_dir.mkdir()
    policy = BetaLocalFilePolicy(download_dir=str(download_dir), expose_download_paths=True)
    resolved: list[str] = []
    real_realpath_lenient = _security.realpath_lenient

    def spy(path: str) -> Path:
        resolved.append(path)
        return real_realpath_lenient(path)

    monkeypatch.setattr(_security, "realpath_lenient", spy)
    assert policy.is_path_visible("/net/elsewhere.example/share/f.bin") is False
    # A ".." component is refused on its text alone, since resolving this path would touch the share it names.
    assert policy.is_path_visible(f"/net/elsewhere.example/share/../../..{download_dir}/f.bin") is False
    assert not [path for path in resolved if "elsewhere" in path]

    inside = str(download_dir / "f.bin")
    assert policy.is_path_visible(inside) is True
    assert inside in resolved  # the spy sees a path that is resolved


@pytest.mark.parametrize(
    "candidate",
    [
        r"\\attacker.example\share\f.txt",
        "//attacker.example/share/f.txt",
        "/\\attacker.example\\share\\f.txt",  # mixed separators are UNC to Windows too
        "\\/?\\C:\\x",
        r"\\?\C:\x",
        "CON",
        "com1.tar",
        "NUL.txt",
        r"sub\COM1.txt",  # backslash-separated device: the check splits on '\' too
        r"C:CON",  # drive-relative spelling: split on ':' too
        r"C:NUL.txt",
        "COM1 ",  # Win32 strips a trailing space before resolving the device name
        r"f.txt:CON",  # alternate-data-stream spelling
        "CON .txt",  # Win32 truncates the name at the extension dot after stripping the trailing space
        "NUL   .bin",
        "COM1 .log",
        "CONIN$",  # console device handles
        "CONOUT$",
        "COM0",  # may name a device on some Windows versions
        "lpt0.txt",
    ],
)
def test_windows_network_and_device_paths_are_refused_lexically_on_windows(
    candidate: str, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Refused before the filesystem is touched: resolving a UNC path makes the Windows redirector
    authenticate to the named host, and a DOS device name opens the device, not a file."""

    def _resolved(_path: str) -> str:
        raise AssertionError("the candidate must be refused before it is resolved")

    monkeypatch.setattr(_security, "ON_WINDOWS", True)
    monkeypatch.setattr(_security, "realpath_lenient", _resolved)
    with pytest.raises(ToolError) as info:
        beta_check_upload_path(
            str(tmp_path / candidate) if candidate[:1] not in ("\\", "/") else candidate, [str(tmp_path)]
        )
    assert info.value.content == UPLOAD_OUTSIDE_ROOTS


@pytest.mark.skipif(os.name == "nt", reason="POSIX path semantics")
def test_elsewhere_a_device_named_file_is_an_ordinary_file(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(_security, "ON_WINDOWS", False)
    root = os.path.realpath(tmp_path)
    (tmp_path / "aux").mkdir()

    for name in ("CON", "con.pdf", "aux/notes.txt", "COM1 .log"):
        assert beta_check_upload_path(os.path.join(root, name), [root]) == os.path.join(root, name)

    # two leading slashes name no network location here; such a path is judged by containment like any other
    with pytest.raises(ToolError):
        beta_check_upload_path("//attacker.example/share/f.txt", [root])

    policy = BetaLocalFilePolicy(download_dir=root, expose_download_paths=True)
    assert policy.is_path_visible(os.path.join(root, "nul.bin")) is True

    monkeypatch.setattr(_security, "ON_WINDOWS", True)
    assert policy.is_path_visible(os.path.join(root, "nul.bin")) is False


def test_upload_root_that_does_not_exist_grants_nothing(tmp_path: Path) -> None:
    # A root that does not resolve on disk must grant no containment (default-deny); otherwise a
    # symlink planted in the root's parent chain escapes the gate.
    missing = tmp_path / "nope"
    with pytest.raises(ToolError):
        beta_check_upload_path(str(missing / "file.bin"), [str(missing)])

    # Same when the missing root sits behind a symlink whose target exists but the leaf does not.
    link = tmp_path / "link"
    link.symlink_to(tmp_path)  # link -> an existing dir, but 'uploads' under it does not exist
    with pytest.raises(ToolError):
        beta_check_upload_path(str(link / "uploads" / "file.bin"), [str(link / "uploads")])


def test_all_blank_upload_roots_report_no_configured_roots() -> None:
    # A non-empty list whose entries are all blank configures no usable root, so report that rather
    # than blaming the path.
    for roots in ([""], ["  "], ["", "  "]):
        with pytest.raises(ToolError, match="no configured upload roots"):
            beta_check_upload_path("/x/f", roots)


def test_local_file_policy_resolves_uploads_under_its_roots(tmp_path: Path) -> None:
    root = tmp_path / "uploads"
    root.mkdir()
    (root / "form.pdf").write_text("x")

    ctx = BetaURLContext(member="file_upload")
    policy = BetaLocalFilePolicy(upload_roots=[str(root)])

    assert policy.resolve_upload_paths(ctx, [str(root / "form.pdf")]) == [str(root / "form.pdf")]

    with pytest.raises(ToolError, match="outside the configured upload roots"):
        policy.resolve_upload_paths(ctx, [str(tmp_path / "secret")])
    with pytest.raises(ToolError, match="must not contain a '..' component"):
        policy.resolve_upload_paths(ctx, [str(root / ".." / "secret")])

    # No roots configured: every path-bearing upload is refused.
    with pytest.raises(ToolError, match="no configured upload roots"):
        BetaLocalFilePolicy().resolve_upload_paths(ctx, [str(root / "form.pdf")])


def test_local_file_policy_vets_document_ids_against_its_allowlist() -> None:
    # Document ids (Files API files) are denied unless listed, like paths outside the upload roots; the refusal
    # names no id, and a listed id passes through unchanged.
    ctx = BetaURLContext(member="file_upload")

    with pytest.raises(ToolError, match="not in the upload allowlist"):
        BetaLocalFilePolicy().resolve_upload_documents(ctx, ["file_abc"])

    policy = BetaLocalFilePolicy(upload_document_ids=["file_abc", "file_def"])
    assert policy.resolve_upload_documents(ctx, ["file_def"]) == ["file_def"]

    with pytest.raises(ToolError) as caught:
        policy.resolve_upload_documents(ctx, ["file_def", "file_xyz"])
    assert "file_xyz" not in str(caught.value)
    assert policy.upload_document_ids == frozenset({"file_abc", "file_def"})

    lazy = BetaLocalFilePolicy(upload_document_ids=(d for d in ["file_abc"]))  # any iterable, read once
    assert lazy.resolve_upload_documents(ctx, ["file_abc"]) == ["file_abc"]

    with pytest.raises(ToolsetConfigError):
        BetaLocalFilePolicy(upload_document_ids="file_abc")


def test_local_file_policy_download_visibility(tmp_path: Path) -> None:
    downloads = tmp_path / "downloads"
    downloads.mkdir()

    assert BetaLocalFilePolicy(download_dir=str(downloads)).is_path_visible(str(downloads / "a.bin")) is False

    exposing = BetaLocalFilePolicy(download_dir=str(downloads), expose_download_paths=True)
    assert exposing.is_path_visible(str(downloads / "a.bin")) is True
    assert exposing.is_path_visible(str(downloads / "sub" / "not-yet.bin")) is True

    # A server-suggested name that climbs out, or a path elsewhere, stays hidden.
    assert exposing.is_path_visible(str(downloads / ".." / "a.bin")) is False
    assert exposing.is_path_visible("/etc/passwd") is False


def test_local_file_policy_construction_rules(tmp_path: Path) -> None:
    # with no download_dir there is nothing to expose
    assert BetaLocalFilePolicy(expose_download_paths=True).is_path_visible(str(tmp_path / "f.bin")) is False

    # a string from an environment variable ("false") is truthy: anything but True exposes nothing
    lenient = BetaLocalFilePolicy(download_dir=str(tmp_path), expose_download_paths="true")  # pyright: ignore[reportArgumentType]
    assert lenient.is_path_visible(str(tmp_path / "f.bin")) is False

    with pytest.raises(ToolsetConfigError, match="not a single path"):
        BetaLocalFilePolicy(upload_roots="/srv/uploads")
    with pytest.raises(ToolsetConfigError, match="must not be empty"):
        BetaLocalFilePolicy(upload_roots=[""])
    with pytest.raises(ToolsetConfigError, match="must not be empty"):
        BetaLocalFilePolicy(download_dir=" ")

    # The download-then-upload loop: a download directory inside (or containing) an upload root.
    with pytest.raises(
        ToolsetConfigError, match=f"download_dir {re.escape(repr(str(tmp_path / 'dl')))} must be outside"
    ):
        BetaLocalFilePolicy(upload_roots=[str(tmp_path)], download_dir=str(tmp_path / "dl"))
    with pytest.raises(ToolsetConfigError, match="outside every upload root"):
        BetaLocalFilePolicy(upload_roots=[str(tmp_path / "up")], download_dir=str(tmp_path))
    # On a disk that ignores letter case (macOS by default) a case variant names the same directory, so it is refused
    # everywhere.
    with pytest.raises(ToolsetConfigError, match="outside every upload root"):
        BetaLocalFilePolicy(upload_roots=[str(tmp_path / "Uploads")], download_dir=str(tmp_path / "uploads" / "dl"))
    # The same disk ignores the Unicode form of a name too, so a decomposed spelling of a composed root is refused.
    with pytest.raises(ToolsetConfigError, match="outside every upload root"):
        BetaLocalFilePolicy(
            upload_roots=[str(tmp_path / "t\u00e9l\u00e9")], download_dir=str(tmp_path / "te\u0301le\u0301")
        )

    # A download_dir that is a symlink into an upload root is the same loop by another spelling.
    uploads = tmp_path / "uploads"
    (uploads / "dl").mkdir(parents=True)
    link = tmp_path / "downloads"
    link.symlink_to(uploads / "dl")
    with pytest.raises(ToolsetConfigError, match="outside every upload root"):
        BetaLocalFilePolicy(upload_roots=[str(uploads)], download_dir=str(link))

    # ... and so is an upload root that is a symlink into the download directory.
    real_downloads = tmp_path / "real_downloads"
    real_downloads.mkdir()
    root_link = tmp_path / "root_link"
    root_link.symlink_to(real_downloads)
    with pytest.raises(ToolsetConfigError, match="outside every upload root"):
        BetaLocalFilePolicy(upload_roots=[str(root_link)], download_dir=str(real_downloads / "sub"))

    policy = BetaLocalFilePolicy(upload_roots=[str(tmp_path / "up")], download_dir=str(tmp_path / "dl"))
    assert policy.upload_roots == (str(tmp_path / "up"),) and policy.download_dir == str(tmp_path / "dl")
