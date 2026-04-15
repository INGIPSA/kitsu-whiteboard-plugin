"""Cross-platform release packer for the Kitsu Whiteboard plugin.

Produces a ZIP with forward-slash paths and Unix (rw-r--r-- / rwxr-xr-x) perms
that extracts cleanly on Linux. Run from the repo root:

    python scripts/pack_release.py
"""

from __future__ import annotations

import os
import sys
import zipfile
from pathlib import Path


OUTPUT_BASENAME = "kitsu-whiteboard-plugin"

INCLUDE_FILES = [
    "manifest.toml",
    "__init__.py",
    "models.py",
    "resources.py",
    "services.py",
    "LICENSE",
    "README.md",
]

INCLUDE_DIRS = [
    "migrations",
    "frontend/dist",
]

EXCLUDE_PARTS = {
    ".git",
    ".github",
    "node_modules",
    "__pycache__",
    ".pytest_cache",
    "tests",
    "scripts",
}
EXCLUDE_SUFFIXES = {".pyc", ".pyo"}


def iter_files(repo: Path):
    for rel in INCLUDE_FILES:
        p = repo / rel
        if p.is_file():
            yield p, rel
    for rel_dir in INCLUDE_DIRS:
        base = repo / rel_dir
        if not base.exists():
            continue
        for root, dirs, files in os.walk(base):
            dirs[:] = [d for d in dirs if d not in EXCLUDE_PARTS]
            for name in files:
                if Path(name).suffix in EXCLUDE_SUFFIXES:
                    continue
                full = Path(root) / name
                rel = full.relative_to(repo).as_posix()
                yield full, rel


def build_zip(repo: Path, out_path: Path) -> None:
    # Files land at the ZIP root because Zou reads manifest.toml from the
    # archive root and extracts into <PLUGIN_FOLDER>/<plugin_id>/ directly.
    with zipfile.ZipFile(
        out_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9
    ) as zf:
        for abs_path, rel in iter_files(repo):
            info = zipfile.ZipInfo.from_file(abs_path, arcname=rel)
            info.external_attr = (0o644 & 0xFFFF) << 16
            info.create_system = 3  # 3 = Unix
            with open(abs_path, "rb") as f:
                zf.writestr(info, f.read(), compress_type=zipfile.ZIP_DEFLATED)


def main() -> int:
    repo = Path(__file__).resolve().parent.parent
    out = repo.parent / f"{OUTPUT_BASENAME}.zip"
    if out.exists():
        out.unlink()
    build_zip(repo, out)

    size_kb = out.stat().st_size / 1024
    with zipfile.ZipFile(out) as zf:
        count = len(zf.namelist())
    print(f"Wrote {out} ({size_kb:.1f} KB, {count} entries)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
