import shutil
from datetime import datetime
from pathlib import Path

from Task_1 import config as clock
import Task_3.activation as a
import Task_3.scanner as s
import Task_3.versions as v

root = Path("Data/test_activation")
shutil.rmtree(root, ignore_errors=True)
kb = root / "kb"
v.ACTIVE_KB = a.ACTIVE_KB = kb
v.VERSIONS = root / "versions"
s.MANIFEST_FILE = root / "manifest.json"

kb.mkdir(parents=True)
(kb / "a.txt").write_text("old a", encoding="utf-8")
v.copy_texts(kb, v.version_path(1))
v.copy_texts(kb, v.version_path(2))
(v.version_path(2) / "a.txt").write_text("new a", encoding="utf-8")
s.save_manifest({"active_version": 1, "files": {}})


def at(day, hour, minute=0):
    return datetime(2026, 10, day, hour, minute, tzinfo=clock.TIMEZONE)


for label, when in [("11:00", at(6, 11)), ("01:59", at(7, 1, 59)), ("02:00", at(7, 2)), ("03:59", at(7, 3, 59)), ("04:00", at(7, 4))]:
    print(label, a.in_maintenance_window(when))

clock.set_time(at(6, 11))
r = a.activate_version(2)
print(r["activated"], r["reason"], "| live a:", (kb / "a.txt").read_text(encoding="utf-8"), "| manifest:", s.load_manifest()["active_version"])

clock.set_time(at(7, 2, 30))
r = a.activate_version(2)
m = s.load_manifest()
print(r["activated"], "| live a:", (kb / "a.txt").read_text(encoding="utf-8"), "| manifest:", m["active_version"], "previous:", m["previous_version"])

clock.clear_time()
shutil.rmtree(root)