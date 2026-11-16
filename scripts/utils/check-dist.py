"""Fails unless a wheel and an sdist hold this commit's files, and metadata that follows from pyproject.toml and README.md.

Usage, from the repository's root: check-dist.py WHEEL SDIST

It needs Python 3.11 or later and imports only the standard library, because the publish job installs nothing.
"""

from __future__ import annotations

import io
import re
import sys
import zlib
import base64
import struct
import hashlib
import tarfile
import zipfile
import subprocess
from typing import Any, NamedTuple
from pathlib import Path
from collections import Counter

import tomllib  # pyright: ignore

# hatchling's default `license-files`
LICENSE = r"(AUTHORS|COPYING|LICEN[CS]E|NOTICE)[^/]*"

problems: list[str] = []


class Committed(NamedTuple):
    git_hash: str
    executable: bool


class Member(NamedTuple):
    name: str
    data: bytes
    executable: bool


def load_pyproject() -> dict[str, Any]:
    return tomllib.loads(Path("pyproject.toml").read_text(encoding="utf-8"))  # pyright: ignore


def git_hash(data: bytes) -> str:
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()


def committed_files() -> dict[str, Committed]:
    tree = subprocess.run(["git", "ls-tree", "-rz", "HEAD"], check=True, capture_output=True, text=True).stdout
    files: dict[str, Committed] = {}
    for entry in tree.split("\0"):
        # not a link (120000) or a submodule (160000)
        if match := re.fullmatch(r"(100\d+) blob (\w+)\t(.*)", entry, re.DOTALL):
            files[match[3]] = Committed(match[2], executable=match[1] == "100755")
    return files


def version_bounds(text: str) -> str:
    return ",".join(sorted(text.replace(" ", "").split(",")))


def requirement(text: str, extra: str | None = None) -> str:
    """`text` as hatchling writes it"""
    match = re.fullmatch(r"([\w.-]+) *(\[.*?\])? *([^;]*?) *(?:; *(.*))?", text)
    assert match, text
    name, extras, bounds, marker = match.groups("")
    marker = marker.replace('"', "'")
    if extra:
        marker = (f"({marker}) and " if marker else "") + f"extra == '{extra}'"
    name = re.sub(r"[-_.]+", "-", name).lower()
    return name + extras + version_bounds(bounds) + (f"; {marker}" if marker else "")


def expected_metadata(pyproject: dict[str, Any], version: str) -> tuple[list[str], str]:
    """The header lines, in any order, and the description"""
    project = pyproject["project"]
    headers = [
        "Metadata-Version: 2.3",
        f"Name: {project['name']}",
        f"Version: {version}",
        f"Summary: {project['description']}",
        f"License: {project['license']}",
        "Author-email: " + ", ".join(f"{author['name']} <{author['email']}>" for author in project["authors"]),
        f"Requires-Python: {version_bounds(project['requires-python'])}",
        "Description-Content-Type: text/markdown",
    ]
    headers += [f"Project-URL: {label}, {url}" for label, url in project["urls"].items()]
    headers += [f"Classifier: {classifier}" for classifier in project["classifiers"]]
    headers += [f"Requires-Dist: {requirement(dependency)}" for dependency in project["dependencies"]]
    for key, dependencies in project["optional-dependencies"].items():
        extra = key.replace("_", "-")
        headers.append(f"Provides-Extra: {extra}")
        headers += [f"Requires-Dist: {requirement(dependency, extra)}" for dependency in dependencies]

    readme = Path("README.md").read_text(encoding="utf-8")
    for rule in pyproject["tool"]["hatch"]["metadata"]["hooks"]["fancy-pypi-readme"]["substitutions"]:
        readme = re.sub(rule["pattern"], rule["replacement"], readme)
    return headers, readme


def check_metadata(archive: str, metadata: bytes, expected: tuple[list[str], str]) -> None:
    header, _, description = metadata.decode().partition("\n\n")
    actual_headers, expected_headers = Counter(header.split("\n")), Counter(expected[0])
    for line in (actual_headers - expected_headers).elements():
        problems.append(f"{archive}: its metadata has a line that does not follow from pyproject.toml: {line}")
    for line in (expected_headers - actual_headers).elements():
        problems.append(f"{archive}: its metadata lacks this line: {line}")
    if description != expected[1]:
        problems.append(f"{archive}: its description differs from README.md")


def decompress(data: bytes, wbits: int) -> bytes | None:
    """`None` unless `data` is one whole stream"""
    stream = zlib.decompressobj(wbits)
    try:
        result = stream.decompress(data)
    except zlib.error:
        return None
    return result if stream.eof and not stream.unused_data else None


def read_wheel(path: Path) -> list[Member]:
    """Readers go by the directory at the end, by the header before each file or by both, so all of it has to agree"""
    wheel = path.read_bytes()
    members: list[Member] = []
    position = 0
    directory_size = 0
    with zipfile.ZipFile(path) as archive:
        entries = archive.infolist()
        for entry in entries:
            header = entry.FileHeader()
            start, end = position + len(header), position + len(header) + entry.compress_size
            data = decompress(wheel[start:end], wbits=-15)
            # hatchling sets the regular-file bit on the package's files, not on those it generates
            mode = entry.external_attr >> 16 & ~0o100000
            if (
                not wheel.startswith(header, position)
                or entry.header_offset != position
                or entry.compress_type != zipfile.ZIP_DEFLATED
                or data is None
                or data != archive.read(entry)
                or mode not in (0o644, 0o755)
                or entry.extra
                # all but the flag of a non-ASCII name
                or entry.flag_bits & ~0x800
            ):
                problems.append(f"{path.name}: {entry.filename} is not stored the way hatchling stores a file")
                return members
            members.append(Member(entry.filename, data, executable=mode == 0o755))
            position = end
            directory_size += len(header) + 16

    count = len(entries)
    sizes = (0, 0, count, count, directory_size, position, 0)
    if wheel[position + directory_size :] != struct.pack("<4s4H2LH", b"PK\5\6", *sizes):
        problems.append(f"{path.name} has something besides its files")
    return members


def read_sdist(path: Path) -> list[Member]:
    """Readers differ in how they take odd headers, so every byte has to be what plain files give"""
    tar = decompress(path.read_bytes(), wbits=31)
    if tar is None:
        problems.append(f"{path.name} is not one gzip stream")
        return []

    members: list[Member] = []
    expected: list[bytes] = []
    with tarfile.open(fileobj=io.BytesIO(tar), mode="r:") as archive:
        for entry in archive:
            data = tar[entry.offset_data : entry.offset_data + entry.size]
            executable = bool(entry.mode & 0o111)
            members.append(Member(entry.name, data, executable))

            plain = tarfile.TarInfo(entry.name)
            plain.size, plain.mtime, plain.mode = len(data), entry.mtime, 0o755 if executable else 0o644
            expected += [plain.tobuf(tarfile.PAX_FORMAT), data, bytes(-len(data) % 512)]
    if tar.rstrip(b"\0") != b"".join(expected).rstrip(b"\0"):
        problems.append(f"{path.name} has something besides plain files")
    return members


def check_files(
    archive: str,
    members: list[Member],
    committed: dict[str, Committed],
    allowed: dict[str, str],
    required: set[str],
) -> dict[str, bytes]:
    """`allowed` gives the committed path of each file's name in the archive"""
    for name, count in Counter(member.name for member in members).items():
        if count > 1:
            problems.append(f"{archive}: {name} is there {count} times")

    for member in members:
        if member.name in allowed:
            path = allowed[member.name]
            if committed[path] != (git_hash(member.data), member.executable):
                problems.append(f"{archive}: {member.name} differs from the commit's {path}")
        elif member.name not in required:
            problems.append(f"{archive}: {member.name} is not in the commit")

    contents = {member.name: member.data for member in members}
    problems.extend(f"{archive}: {name} is missing" for name in sorted(required - contents.keys()))
    return contents


def check_wheel(path: Path, package: str, pyproject: dict[str, Any], committed: dict[str, Committed]) -> bytes:
    info = f"{package}.dist-info/"
    metadata, tags, record = info + "METADATA", info + "WHEEL", info + "RECORD"
    folders = tuple(f"{folder}/" for folder in pyproject["tool"]["hatch"]["build"]["targets"]["wheel"]["packages"])
    allowed = {name.removeprefix("src/"): name for name in committed if name.startswith(folders)}
    allowed |= {f"{info}licenses/{name}": name for name in committed if re.fullmatch(LICENSE, name)}
    contents = check_files(path.name, read_wheel(path), committed, allowed, {*allowed, metadata, tags, record})

    (hatchling,) = (dep for dep in pyproject["build-system"]["requires"] if dep.startswith("hatchling=="))
    generator = hatchling.replace("==", " ")
    expected_tags = f"Wheel-Version: 1.0\nGenerator: {generator}\nRoot-Is-Purelib: true\nTag: py3-none-any\n"
    if contents.get(tags) != expected_tags.encode():
        problems.append(f"{path.name}: {tags} is not what {generator} writes")

    lines = [f"{record},,", ""]
    for name, data in contents.items():
        if name != record:
            digest = base64.urlsafe_b64encode(hashlib.sha256(data).digest()).rstrip(b"=").decode()
            lines.append(f"{name},sha256={digest},{len(data)}")
    if sorted(contents.get(record, b"").decode().split("\n")) != sorted(lines):
        problems.append(f"{path.name}: {record} does not describe its files")

    return contents.get(metadata, b"")


def check_sdist(path: Path, package: str, committed: dict[str, Committed]) -> bytes:
    metadata = f"{package}/PKG-INFO"
    allowed = {f"{package}/{name}": name for name in committed}
    installed = {
        name for name, file in allowed.items() if re.fullmatch(rf"src/.*|pyproject\.toml|README\.md|{LICENSE}", file)
    }
    return check_files(path.name, read_sdist(path), committed, allowed, {*installed, metadata}).get(metadata, b"")


def main() -> None:
    wheel, sdist = (Path(argument) for argument in sys.argv[1:])
    package = wheel.name.removesuffix("-py3-none-any.whl")
    pyproject = load_pyproject()
    committed = committed_files()
    expected = expected_metadata(pyproject, version=package.split("-")[1])

    check_metadata(wheel.name, check_wheel(wheel, package, pyproject, committed), expected)
    check_metadata(sdist.name, check_sdist(sdist, package, committed), expected)

    if problems:
        print(*problems[:20], sep="\n")
        sys.exit(
            "::error::The wheel or the sdist differs from the commit, so nothing was published. "
            "The job's log lists the first differences."
        )
    print("The wheel and the sdist match the commit")


if __name__ == "__main__":
    main()
