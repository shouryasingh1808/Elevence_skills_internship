from pathlib import Path

import Task_3.scanner as s

s.MANIFEST_FILE = Path("Data/test_manifest.json")
report = s.scan_incoming()
print("files scanned:", len(report))
for r in report:
    print(r["file"], "->", r["status"])
s.MANIFEST_FILE.unlink()