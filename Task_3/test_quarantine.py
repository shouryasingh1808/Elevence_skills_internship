import shutil
from pathlib import Path

import Task_3.quarantine as q

q.QUARANTINE = Path("Data/test_quarantine")
src = Path("Data/test_incoming")
src.mkdir(parents=True, exist_ok=True)

for text in ["first bad file", "second bad file", "third bad file"]:
    bad = src / "broken.txt"
    bad.write_text(text, encoding="utf-8")
    q.quarantine_file(bad, ["problem"])

print(sorted(p.name for p in q.QUARANTINE.iterdir()))
print((q.QUARANTINE / "broken.txt").read_text(encoding="utf-8"))
print((q.QUARANTINE / "broken_3.txt").read_text(encoding="utf-8"))

shutil.rmtree(q.QUARANTINE)
shutil.rmtree(src)