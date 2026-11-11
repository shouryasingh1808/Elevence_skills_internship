from datetime import datetime
from pathlib import Path

from Task_1 import config as clock
import Task_3.scanner as s
import Task_3.scheduler as sch

s.MANIFEST_FILE = Path("Data/test_scheduler_manifest.json")
tz = clock.TIMEZONE
calls = []


def at(day, hour, minute=0):
    return datetime(2026, 10, day, hour, minute, tzinfo=tz)


def always_fails():
    return {"success": False, "error": "service down"}


def fails_once():
    calls.append(1)
    return {"success": len(calls) >= 2, "error": "service down"}


def crashes():
    raise ConnectionError("outage")


def describe(r):
    if not r["ran"]:
        return f"ran=False status={r['status']}"
    if r["success"]:
        return "ran=True success=True"
    if r.get("gave_up"):
        return f"ran=True success=False GAVE UP | {r['error']}"
    return f"ran=True success=False retry in {r['retry_in']} (attempt {r['attempt']}) | {r['error']}"


def timeline(label, job, times):
    s.save_manifest({"active_version": 1, "files": {}})
    print(label)
    for t in times:
        clock.set_time(t)
        print(f"  {t:%a %H:%M}", describe(sch.tick(job)))


timeline("A: always fails", always_fails,
         [at(6, 1, 59), at(6, 2), at(6, 2, 14), at(6, 2, 15), at(6, 2, 45), at(6, 3, 45), at(6, 3, 46), at(7, 2)])
timeline("B: fails once, then works", fails_once, [at(6, 2), at(6, 2, 15), at(6, 2, 16)])
timeline("C: job crashes (outage)", crashes, [at(6, 2)])

clock.clear_time()
s.MANIFEST_FILE.unlink()