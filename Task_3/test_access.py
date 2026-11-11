from datetime import datetime
from pathlib import Path

from Task_1 import config as clock
from Task_3 import config
from Task_3.access import check_access

config.AUDIT_FILE = Path("Data/test_audit.jsonl")
if config.AUDIT_FILE.exists():
    config.AUDIT_FILE.unlink()
clock.set_time(datetime(2026, 10, 7, 2, 0, tzinfo=clock.TIMEZONE))

tests = [("asha", "admin", "run_update"), ("ravi", "agent", "run_update"), ("sam", "customer", "run_update"),
         ("ravi", "agent", "view_status"), ("sam", "customer", "view_status"),
         ("eve", "guest", "run_update"), ("asha", "admin", "delete_everything")]
for user, level, action in tests:
    r = check_access(user, level, action)
    print(user, level, action, "->", "ALLOWED" if r["allowed"] else "DENIED", "|", r["reason"])

lines = config.AUDIT_FILE.read_text(encoding="utf-8").splitlines()
print(len(lines), "audit lines | last:", lines[-1])

clock.clear_time()
config.AUDIT_FILE.unlink()