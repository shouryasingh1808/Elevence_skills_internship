"""Task 3 scanner: finds new, changed and duplicate documents."""

import hashlib
from pathlib import Path
import json
from Task_3.config import MANIFEST_FILE , ACTIVE_KB

def file_hash(path):
    text = Path(path).read_text(encoding="utf-8").replace("\r\n", "\n").strip()  # This is only because i regularly shifts on Mac and PC..
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

def load_manifest():
    if not MANIFEST_FILE.exists():
        return {"active_version" : 0 , "files" : {}}
    return json.loads(MANIFEST_FILE.read_text(encoding="utf-8"))

def save_manifest(manifest):
    MANIFEST_FILE.parent.mkdir(parents = True , exist_ok=True)
    MANIFEST_FILE.write_text(json.dumps(manifest, indent=2) , encoding="utf-8")

def ensure_baseline():
    manifest = load_manifest()
    if manifest["files"]:
        return manifest
    for path in sorted(ACTIVE_KB.glob("*.txt")):
            manifest["files"][path.name] = file_hash(path)
    if manifest["active_version"] == 0:
         manifest["active_version"] == 1
    save_manifest(manifest)
    return manifest