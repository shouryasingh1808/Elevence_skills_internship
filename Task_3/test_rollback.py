import shutil
from datetime import datetime
from pathlib import Path

from Task_1 import config as clock
import Task_3.activation as a
import Task_3.scanner as s
import Task_3.versions as v

root = Path("Data/test_rollback")
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


def at(minute):
    return datetime(2026, 10, 7, 2, minute, tzinfo=clock.TIMEZONE)


def ok():
    return {"healthy": True, "failures": []}


def bad():
    return {"healthy": False, "failures": ["wrong answer"]}


def outage():
    raise ConnectionError("service down")


def show(label, result):
    m = s.load_manifest()
    live = (kb / "a.txt").read_text(encoding="utf-8")
    print(label, "|", result["state"], "| live:", live, "| active:", m["active_version"], "| health:", m.get("health"))


clock.set_time(at(30)); a.activate_version(2)
clock.set_time(at(32)); show("A ok at +2   ", a.run_health_check(ok))
clock.set_time(at(34)); show("A bad at +4  ", a.run_health_check(bad))

clock.set_time(at(40)); a.activate_version(2)
clock.set_time(at(41)); show("B outage +1  ", a.run_health_check(outage))

clock.set_time(at(50)); a.activate_version(2)
clock.set_time(at(52)); show("C ok at +2   ", a.run_health_check(ok))
clock.set_time(at(56)); show("C bad at +6  ", a.run_health_check(bad))

clock.clear_time()
shutil.rmtree(root)