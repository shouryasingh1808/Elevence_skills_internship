import shutil
from datetime import datetime
from pathlib import Path

from Task_1 import config as clock
import Task_3.quarantine as q

q.QUARANTINE = Path("Data/test_quarantine")
src = Path("Data/test_incoming")
src.mkdir(parents=True, exist_ok=True)
bad = src / "broken.txt"
bad.write_text("no header here", encoding="utf-8")

clock.set_time(datetime(2026, 10, 6, 2, 0, tzinfo=clock.TIMEZONE))
target = q.quarantine_file(bad, ["missing or broken header (needs --- lines)"])
clock.clear_time()

print("moved:", target.name, "| still in incoming:", bad.exists())
print(sorted(p.name for p in q.QUARANTINE.iterdir()))
print((q.QUARANTINE / "broken.txt.reason.json").read_text(encoding="utf-8"))

shutil.rmtree(q.QUARANTINE)
shutil.rmtree(src)