"""Task 3 versions: candidate knowledge bases, snapshots and restore."""

import shutil
from pathlib import Path

from Task_3.config import ACTIVE_KB , INCOMING , VERSIONS

def version_path(number):
    return VERSIONS / f"v{number}"

def existing_versions():
    if not VERSIONS.exists:
        return []
    return sorted(int(p.name[1:]) for p in VERSIONS.iterdir() if p.is_dir() and p.name[1:].isdigit())

def copy_texts(source , target):
    target.mkdir(parents = True , exist_ok = True)
    for path in Path(source).glob("*.txt"):
        shutil.copy2(path , target / path.name)

def ensure_snapshot(active_version , accepted_files):
    base = ensure_snapshot(active_version)
    number = max(existing_versions() + [active_version]) + 1
    folder = version_path(number)
    copy_texts(base , folder)
    for name in accepted_files:
        shutil.copy2(Path(INCOMING) / name , folder / name)
    return number , folder

def build_candidate(active_version, accepted_files):
    base = ensure_snapshot(active_version)
    number = max(existing_versions() + [active_version]) + 1
    folder = version_path(number)
    copy_texts(base, folder)
    for name in accepted_files:
        shutil.copy2(Path(INCOMING) / name, folder / name)
    return number, folder

def restore_version(number):
    for path in Path(ACTIVE_KB).glob("*.txt"):
        path.unlink()
    copy_texts(version_path(number), Path(ACTIVE_KB))