import shutil
from pathlib import Path

import Task_3.versions as v

root = Path("Data/test_versions")
v.ACTIVE_KB = root / "kb"
v.INCOMING = root / "incoming"
v.VERSIONS = root / "versions"
v.ACTIVE_KB.mkdir(parents=True)
v.INCOMING.mkdir(parents=True)

(v.ACTIVE_KB / "a.txt").write_text("old a", encoding="utf-8")
(v.ACTIVE_KB / "b.txt").write_text("old b", encoding="utf-8")
(v.INCOMING / "a.txt").write_text("new a", encoding="utf-8")
(v.INCOMING / "c.txt").write_text("new c", encoding="utf-8")

number, folder = v.build_candidate(1, ["a.txt", "c.txt"])
print(number, sorted(p.name for p in folder.glob("*.txt")))
print((folder / "a.txt").read_text(encoding="utf-8"), "|", (v.version_path(1) / "a.txt").read_text(encoding="utf-8"))
print(v.existing_versions(), "active still:", (v.ACTIVE_KB / "a.txt").read_text(encoding="utf-8"))

v.restore_version(2)
print("after restore v2:", sorted(p.name for p in v.ACTIVE_KB.glob("*.txt")), (v.ACTIVE_KB / "a.txt").read_text(encoding="utf-8"))
v.restore_version(1)
print("after restore v1:", sorted(p.name for p in v.ACTIVE_KB.glob("*.txt")), (v.ACTIVE_KB / "a.txt").read_text(encoding="utf-8"))

shutil.rmtree(root)