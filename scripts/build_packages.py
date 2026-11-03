#!/usr/bin/env python3
"""Build the release packages from the skill files at the repo root.

  novel-ai-scripting.zip    the skill's files with no top folder (SKILL.md at the root)
  novel-ai-scripting.skill  the same files inside a novel-ai-scripting/ folder

Builds are reproducible: files are added in sorted order with a fixed timestamp,
and text files are normalized to LF, so the same sources always give the same
bytes on Windows, macOS, Linux, and CI.

Usage:
  python scripts/build_packages.py           build both packages
  python scripts/build_packages.py --check   exit 1 if the committed packages are out of date
"""
from __future__ import annotations

import io
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILL_FOLDER = "novel-ai-scripting"
# What goes into the packages: these root files plus everything under references/.
ROOT_FILES = ["SKILL.md", "CHANGELOG.md"]
INCLUDE_DIRS = ["references"]
TEXT_SUFFIXES = {".md", ".ts", ".txt", ".json", ".yml", ".yaml"}
FIXED_TIME = (1980, 1, 1, 0, 0, 0)

PACKAGES = {
    f"{SKILL_FOLDER}.zip": "",
    f"{SKILL_FOLDER}.skill": f"{SKILL_FOLDER}/",
}


def source_files() -> list[str]:
    files = []
    for name in ROOT_FILES:
        if not (ROOT / name).is_file():
            sys.exit(f"missing {name}")
        files.append(name)
    for folder in INCLUDE_DIRS:
        files += sorted(p.relative_to(ROOT).as_posix() for p in (ROOT / folder).rglob("*") if p.is_file())
    return files


def read(rel: str) -> bytes:
    data = (ROOT / rel).read_bytes()
    if Path(rel).suffix.lower() in TEXT_SUFFIXES:
        data = data.replace(b"\r\n", b"\n")
    return data


def add(zf: zipfile.ZipFile, name: str, data: bytes | None) -> None:
    info = zipfile.ZipInfo(name, FIXED_TIME)
    if data is None:  # directory entry
        info.external_attr = (0o40755 << 16) | 0x10
        zf.writestr(info, b"")
    else:
        info.external_attr = 0o100644 << 16
        info.compress_type = zipfile.ZIP_DEFLATED
        zf.writestr(info, data, compresslevel=9)


def build(prefix: str, files: list[str]) -> bytes:
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as zf:
        dirs = sorted({str(Path(f).parent.as_posix()) for f in files if "/" in f})
        if prefix:
            add(zf, prefix, None)
        for d in dirs:
            add(zf, f"{prefix}{d}/", None)
        for f in files:
            add(zf, prefix + f, read(f))
    return buf.getvalue()


def main() -> int:
    check = "--check" in sys.argv[1:]
    files = source_files()
    stale = []
    for package, prefix in PACKAGES.items():
        data = build(prefix, files)
        target = ROOT / package
        if check:
            if not target.is_file() or target.read_bytes() != data:
                stale.append(package)
        else:
            target.write_bytes(data)
            print(f"built {package} ({len(files)} files, {len(data):,} bytes)")
    if stale:
        print("out of date: " + ", ".join(stale) + " (run python scripts/build_packages.py)")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
